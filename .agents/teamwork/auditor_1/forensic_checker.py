import ast
import sys
import os
import re

sys.path.insert(0, "d:/ai/nasa")

print("=== STARTING FORENSIC STATIC ANALYSIS ===")

# 1. AST Analysis for Security & Dangerous Calls
dangerous_calls = []
class SecurityVisitor(ast.NodeVisitor):
    def visit_Call(self, node):
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
            
        if func_name in ["eval", "exec", "system", "popen", "spawn", "fork", "subprocess"]:
            dangerous_calls.append((func_name, getattr(node, 'lineno', 0)))
        self.generic_visit(node)

for fname in ["app.py", "i18n.py"]:
    with open(os.path.join("d:/ai/nasa", fname), "r", encoding="utf-8") as f:
        code = f.read()
    tree = ast.parse(code, filename=fname)
    visitor = SecurityVisitor()
    visitor.visit(tree)
    print(f"[{fname}] AST parsed successfully. Dangerous calls found: {len(dangerous_calls)}")
    for dc in dangerous_calls:
        print(f"  -> Dangerous call: {dc[0]} at line {dc[1]}")
    dangerous_calls.clear()

# 2. Check for Facades / Dummy Implementations in app.py
print("\n=== CHECKING FOR FACADE FUNCTIONS ===")
with open("d:/ai/nasa/app.py", "r", encoding="utf-8") as f:
    app_text = f.read()
    app_tree = ast.parse(app_text, filename="app.py")

facades = []
for node in ast.walk(app_tree):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        if len(node.body) == 1:
            stmt = node.body[0]
            if isinstance(stmt, ast.Pass):
                facades.append((node.name, node.lineno, "pass"))
            elif isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Constant):
                facades.append((node.name, node.lineno, f"return {stmt.value.value}"))
            elif isinstance(stmt, ast.Raise) and isinstance(stmt.exc, ast.Name) and stmt.exc.id == "NotImplementedError":
                facades.append((node.name, node.lineno, "raise NotImplementedError"))

print(f"Total single-statement facade candidates: {len(facades)}")
for f in facades:
    print(f"  -> Function '{f[0]}' at line {f[1]}: {f[2]}")

# 3. Check for Hardcoded Test Returns in Physics Engine
print("\n=== CHECKING SPECIFIC OCCURRENCES OF TEST TERMS ===")
lines = app_text.splitlines()
test_terms = ["MAT-01", "MAT-03", "MAT-08", "test_full_suite", "verify_all_fixes", "mock", "patch"]
for t in test_terms:
    for idx, l in enumerate(lines):
        if t in l:
            print(f"Match '{t}' at line {idx+1}: {l.strip()[:100]}")

# 4. Check i18n Key Parity between 'vi' and 'en'
print("\n=== CHECKING i18n KEY PARITY ===")
import i18n
vi_keys = set(i18n.TRANSLATIONS.get("vi", {}).keys())
en_keys = set(i18n.TRANSLATIONS.get("en", {}).keys())
missing_in_en = vi_keys - en_keys
missing_in_vi = en_keys - vi_keys

print(f"Total keys in 'vi': {len(vi_keys)}")
print(f"Total keys in 'en': {len(en_keys)}")
print(f"Missing in 'en': {len(missing_in_en)}")
print(f"Missing in 'vi': {len(missing_in_vi)}")
if missing_in_en:
    print(f"Keys missing in en: {list(missing_in_en)}")
if missing_in_vi:
    print(f"Keys missing in vi: {list(missing_in_vi)}")

# 5. Check if app.py calls any missing i18n keys
print("\n=== CHECKING app.py i18n LOOKUPS ===")
i18n_calls = re.findall(r"\bt\[['\"]([a-zA-Z0-9_]+)['\"]\]", app_text)
unique_calls = set(i18n_calls)
print(f"Total i18n lookups found in app.py: {len(i18n_calls)} ({len(unique_calls)} unique keys)")
missing_called_vi = [k for k in unique_calls if k not in vi_keys]
missing_called_en = [k for k in unique_calls if k not in en_keys]
print(f"i18n lookups missing in 'vi': {missing_called_vi}")
print(f"i18n lookups missing in 'en': {missing_called_en}")

print("\n=== FORENSIC CHECK COMPLETED ===")
