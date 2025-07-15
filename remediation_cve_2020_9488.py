import os
import re

# Root directory to recursively scan
SOURCE_DIR = 'src/main/java'

# Matches logger lines with concatenated user input
VULNERABLE_LOG_PATTERN = re.compile(r'logger\.(info|warn|error|debug)\s*\(\s*"(.*?)"\s*\+\s*(.*?)\s*\)\s*;')

def remediate_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modified = False
    new_lines = []

    for line in lines:
        match = VULNERABLE_LOG_PATTERN.search(line)
        if match:
            level = match.group(1)               # info, warn, etc.
            message_prefix = match.group(2)      # message string
            variable = match.group(3).strip()    # variable name (e.g., username)

            # Construct safe logging statement
            safe_line = f'logger.{level}("{message_prefix} {{}}", {variable});\n'
            new_lines.append(safe_line)
            modified = True
        else:
            new_lines.append(line)

    if modified:
        with open(file_path, 'w') as file:
            file.writelines(new_lines)
        print(f"[OK] Remediated: {file_path}")
    else:
        print(f"[SORRY] No changes made: {file_path}")

def run_remediation():
    for root, _, files in os.walk(SOURCE_DIR):
        for filename in files:
            if filename.endswith(".java"):
                filepath = os.path.join(root, filename)
                remediate_file(filepath)

if __name__ == "__main__":
    run_remediation()
