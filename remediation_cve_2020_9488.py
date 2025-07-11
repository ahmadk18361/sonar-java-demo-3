import re

with open("src/main/java/com/example/Log4jCVE2020_9488Example.java", "r") as file:
    code = file.read()

# 1. Remediate dynamic config setting
code = re.sub(
    r'System\.setProperty\("log4j2\.configurationFile",\s*".*?"\);',
    '// REMEDIATED: Avoid setting log4j config dynamically for security reasons',
    code
)

# 2. Remediate unsafe logging of user input
code = re.sub(
    r'logger\.error\("Login failed for user:\s*"\s*\+\s*username\);',
    '// REMEDIATED: Avoid logging raw user input\nlogger.error("Login failed for user.");',
    code
)

with open("src/main/java/com/example/Log4jCVE2020_9488Example.java", "w") as file:
    file.write(code)
