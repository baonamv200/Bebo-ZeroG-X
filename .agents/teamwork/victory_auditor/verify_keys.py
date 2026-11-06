import re
import sys
sys.path.insert(0, '.')
import i18n

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

used_keys = set(re.findall(r"\bt\[['\"]([a-zA-Z0-9_]+)['\"]\]", content))
print('Total unique keys used in app.py:', len(used_keys))

vi_keys = set(i18n.TRANSLATIONS['vi'].keys())
en_keys = set(i18n.TRANSLATIONS['en'].keys())

missing_vi = used_keys - vi_keys
missing_en = used_keys - en_keys

print('Missing in VI:', missing_vi)
print('Missing in EN:', missing_en)
assert not missing_vi, f'Missing keys in VI: {missing_vi}'
assert not missing_en, f'Missing keys in EN: {missing_en}'
print('All used keys exist in both VI and EN!')
