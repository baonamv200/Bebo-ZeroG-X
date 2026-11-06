import ast
import re
import sys

def check_app_integrity():
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()
        
    tree = ast.parse(content, filename="app.py")
    
    # 1. Check dangerous calls
    dangerous = []
    facades = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in ("eval", "exec", "compile"):
                    dangerous.append((node.func.id, getattr(node, 'lineno', 0)))
            elif isinstance(node.func, ast.Attribute):
                if node.func.attr in ("system", "popen") and isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                    dangerous.append(("os." + node.func.attr, getattr(node, 'lineno', 0)))
                elif node.func.attr in ("Popen", "run", "call", "check_output") and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
                    dangerous.append(("subprocess." + node.func.attr, getattr(node, 'lineno', 0)))
                    
        # Check facade functions
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Check if function body is just 'return constant' or 'pass' or 'raise NotImplementedError'
            if len(node.body) == 1:
                stmt = node.body[0]
                if isinstance(stmt, ast.Pass):
                    facades.append((node.name, "pass", node.lineno))
                elif isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Constant):
                    facades.append((node.name, f"return {stmt.value.value}", node.lineno))
                elif isinstance(stmt, ast.Raise):
                    if isinstance(stmt.exc, ast.Call) and isinstance(stmt.exc.func, ast.Name) and stmt.exc.func.id == "NotImplementedError":
                        facades.append((node.name, "raise NotImplementedError", node.lineno))

    print(f"Dangerous calls: {len(dangerous)} -> {dangerous}")
    print(f"Single-statement facade functions: {len(facades)} -> {facades}")

    # 2. Check Tab 2 typography:
    # Find Tab 2 definition: 'with tab_morph:' or tab 2 section
    tab2_start = content.find("with tab_morph:")
    tab3_start = content.find("with tab_rag:")
    
    if tab2_start != -1 and tab3_start != -1:
        tab2_content = content[tab2_start:tab3_start]
        print(f"Tab 2 slice length: {len(tab2_content)} chars")
        
        # Look for fonts in Tab 2
        font_families = re.findall(r'font-family:\s*([^;"]+)', tab2_content, re.IGNORECASE)
        print(f"Total font-family declarations in Tab 2: {len(font_families)}")
        
        # Group them
        from collections import Counter
        font_counts = Counter([f.strip() for f in font_families])
        for font, cnt in font_counts.items():
            print(f"  - {font}: {cnt}")
            
        # Check if any font contains Courier or monospace (except CAD/contour markers)
        for line_no, line in enumerate(tab2_content.splitlines(), start=content[:tab2_start].count('\n') + 1):
            if any(term in line.lower() for term in ["monospace", "courier", "jetbrains mono"]):
                # check context
                print(f"  [Line {line_no}] Mono occurrence: {line.strip()[:100]}")
    else:
        print("WARNING: tab_morph or tab_suppression not found")

if __name__ == "__main__":
    check_app_integrity()
