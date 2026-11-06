with open('app.py', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if "t['material_id']" in line or 't["material_id"]' in line:
            print(f"Line {idx}: {line.strip()[:100]}")
        if "t['action_1']" in line or 't["action_1"]' in line:
            print(f"Line {idx} (action_1): {line.strip()[:100]}")
