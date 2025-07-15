import os
import re

# Directory where your Java files are
SOURCE_DIR = "src/main/java/com/example"

# Matches logger.<level>(...) calls with any content
LOG_PATTERN = re.compile(
    r'(logger\.(info|warn|error|debug|trace))\s*\(\s*(.+?)\);',
    re.IGNORECASE | re.DOTALL
)

def extract_message_and_vars(log_content):
    """
    Breaks the logger(...) content into format string and variables.
    """
    tokens = [t.strip() for t in re.split(r'(\+)', log_content) if t.strip() != '+']
    message = ""
    vars = []

    for token in tokens:
        if token.startswith('"') and token.endswith('"'):
            message += token[1:-1]
        else:
            message += "{}"
            vars.append(token)

    return message.strip(), vars

def remediate_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    modified = False

    for line in lines:
        match = LOG_PATTERN.search(line)
        if match:
            logger_call = match.group(1)
            log_content = match.group(3).strip()

            if '+' not in log_content:
                # Already safe or not vulnerable
                new_lines.append(line)
                continue

            # Extract placeholders + variables
            safe_message, variables = extract_message_and_vars(log_content)
            new_line = f'{logger_call}("{safe_message}", {", ".join(variables)});\n'
            new_lines.append(new_line)
            modified = True
            print(f"[FIXED] {file_path} ➜ {new_line.strip()}")
        else:
            new_lines.append(line)

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

def run_remediation():
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(".java"):
                remediate_file(os.path.join(root, file))

if __name__ == "__main__":
    run_remediation()
