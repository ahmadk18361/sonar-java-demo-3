import re

with open("Log4jCVE2020_9488Example.java", "r") as file:
    code = file.read()

# Comment out or remove the vulnerable setting
fixed_code = re.sub(
    r'(System\.setProperty\("log4j\.configurationFile",\s*".*?"\);)',
    '// REMEDIATED: Avoid setting log4j config dynamically for security reasons',
    code
)

with open("Log4jCVE2020_9488Example.java", "w") as file:
    file.write(fixed_code)
