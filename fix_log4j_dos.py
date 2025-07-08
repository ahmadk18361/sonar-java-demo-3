import re

def fix_log4j_dos(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    backup_path = file_path + ".bak"
    with open(backup_path, 'w', encoding='utf-8') as backup:
        backup.write(code)

    # Replace patterns like ${ctx:username} and %X{username}
    code = re.sub(r'\$\{ctx:[^}]+\}', 'REDACTED', code)
    code = re.sub(r'%X\{[^}]+\}', 'REDACTED', code)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
