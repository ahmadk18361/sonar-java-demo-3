import os
import re

# Path to recursively scan
SOURCE_DIR = 'src/main/java/com/example'

# Regex pattern to catch logger statements with string concatenation
# Supports .info, .warn, .error, .debug etc.
LOG_PATTERN = re.compile(r'(logger\.(info|warn|error|debug))\s*\(\s*"([^"]*?)"\s*\+\s*([\w\.]+)\s*\)', re.IGNORECASE)

def remediate_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modified = False
    new_lines = []

    for line in lines:
        match = LOG_PATTERN.search(line)
        if match:
            full_call = match.group(1)
            level = match.group(2)
            message_prefix = match.group(3)
            variable = match.group(4)

            # Construct the safe logger call
            safe_line = f'{full_call}("{message_prefix} {{}}", (Object) {variable});\n'
            new_lines.append(safe_line)
            modified = True
        else:
            new_lines.append(line)

    if modified:
        with open(file_path, 'w') as file:
            file.writelines(new_lines)
        print(f"[OK] Remediated: {file_path}")
    else:
        print(f"[SORRY ] No issues found: {file_path}")

def run_remediation():
    for root, _, files in os.walk(SOURCE_DIR):
        for filename in files:
            if filename.endswith('.java'):
                filepath = os.path.join(root, filename)
                remediate_file(filepath)

if __name__ == '__main__':
    run_remediation()
