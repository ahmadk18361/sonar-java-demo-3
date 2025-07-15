import os
import re

# Root directory to recursively scan
SOURCE_DIR = 'src/main/java/com/example'

# Matches logger lines with concatenated user input or literals
VULNERABLE_LOG_PATTERN = re.compile(
    r'logger\.(info|warn|error|debug)\s*\(\s*("(?:[^"\\]|\\.)*?)"\s*\+\s*(.+?)\s*\)'
)

def remediate_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modified = False
    new_lines = []

    for line in lines:
        match = VULNERABLE_LOG_PATTERN.search(line)
        if match:
            level = match.group(1)                         # info/warn/etc.
            message_prefix = match.group(2).strip()        # "Message text"
            variable = match.group(3).strip()              # Variable name or string literal

            # Wrap string literal variable in (Object) to avoid Throwable overload
            if variable.startswith('"') and variable.endswith('"'):
                variable = f'(Object) {variable}'

            safe_line = f'logger.{level}({message_prefix[:-1]} {{}}", {variable});\n'
            new_lines.append(safe_line)
            modified = True
        else:
            new_lines.append(line)

    if modified:
        with open(file_path, 'w') as file:
            file.writelines(new_lines)
        print(f"[OK] Remediated: {file_path}")
    else:
        print(f"[SKIP] No changes made: {file_path}")

def run_remediation():
    for root, _, files in os.walk(SOURCE_DIR):
        for filename in files:
            if filename.endswith(".java"):
                filepath = os.path.join(root, filename)
                remediate_file(filepath)

if __name__ == "__main__":
    run_remediation()
