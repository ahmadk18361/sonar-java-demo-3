import os
import re

SOURCE_DIR = 'src/main/java/com/example'

# Match unsafe logger statements like: logger.warn("text" + var);
LOG_PATTERN = re.compile(r'(logger\.(warn|info|error))\("([^"]*?)"\s*\+\s*([a-zA-Z0-9_]+)\);')

# Match InputStreamReader(System.in)
ENCODING_PATTERN = re.compile(r'new InputStreamReader\s*\(\s*System\.in\s*\)')

# Match existing encoding import
IMPORT_PATTERN = re.compile(r'import java\.nio\.charset\.StandardCharsets;')


def remediate_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    modified = False
    import_found = False

    for line in lines:
        # Detect if import already exists
        if IMPORT_PATTERN.search(line):
            import_found = True

        # Fix logger + unsafe concat
        match = LOG_PATTERN.search(line)
        if match:
            full_call = match.group(1)
            message_prefix = match.group(3).strip()
            variable = match.group(4).strip()
            safe_line = f'{full_call}("{message_prefix} " + String.valueOf({variable}));\n'
            new_lines.append(safe_line)
            modified = True
            continue

        # Fix default encoding
        if ENCODING_PATTERN.search(line):
            line = ENCODING_PATTERN.sub('new InputStreamReader(System.in, StandardCharsets.UTF_8)', line)
            modified = True

        new_lines.append(line)

    # Add missing import
    if not import_found:
        for i, line in enumerate(new_lines):
            if line.startswith('import') and 'log4j' in line:
                new_lines.insert(i, 'import java.nio.charset.StandardCharsets;\n')
                modified = True
                break

    # Write file if modified
    if modified:
        with open(file_path, 'w') as file:
            file.writelines(new_lines)
        print(f"[OK] Remediated: {file_path}")
    else:
        print(f"[SKIP] No changes needed: {file_path}")


def run_remediation():
    for root, _, files in os.walk(SOURCE_DIR):
        for filename in files:
            if filename.endswith('.java'):
                filepath = os.path.join(root, filename)
                remediate_file(filepath)


if __name__ == '__main__':
    run_remediation()
