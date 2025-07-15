import os
import re

SOURCE_DIR = 'src/main/java/com/example'

# Match logger.warn/error/info("... " + variable);
LOG_PATTERN = re.compile(r'(logger\.(warn|info|error))\("([^"]*?)"\s*\+\s*([a-zA-Z0-9_]+)\);')

def remediate_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    modified = False

    for line in lines:
        match = LOG_PATTERN.search(line)
        if match:
            full_call = match.group(1)
            message_prefix = match.group(3).strip()
            variable = match.group(4).strip()
            # Safe concatenation
            safe_line = f'{full_call}("{message_prefix} " + String.valueOf({variable}));\n'
            new_lines.append(safe_line)
            modified = True
        else:
            new_lines.append(line)

    if modified:
        with open(file_path, 'w') as file:
            file.writelines(new_lines)
        print(f"[OK] Remediated: {file_path}")
    else:
        print(f"[SKIP] No match in: {file_path}")

def run_remediation():
    for root, _, files in os.walk(SOURCE_DIR):
        for filename in files:
            if filename.endswith('.java'):
                filepath = os.path.join(root, filename)
                remediate_file(filepath)

if __name__ == '__main__':
    run_remediation()
