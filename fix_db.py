import re
with open('pos/settings.py', 'r') as f:
    content = f.read()

content = re.sub(r"'NAME':\s*WindowsPath\([^)]+\)", "'NAME': 'db.sqlite3'", content)

with open('pos/settings.py', 'w') as f:
    f.write(content)

print('Updated DATABASES config')
