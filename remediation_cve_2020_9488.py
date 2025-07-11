import re

with open("src/main/java/com/example/Log4jCVE2020_9488Example.java", "r") as file:
    code = file.read()

# Fix the JNDI assignment (Log4Shell-style pattern)
code = re.sub(
    r'String username = "\$\{jndi:ldap://.*?\}";',
    '// REMEDIATED: Removed vulnerable JNDI string\nString username = "unknown_user";',
    code
)

# Fix the log injection
code = re.sub(
    r'logger\.error\("Login failed for user:\s*"\s*\+\s*username\);',
    '// REMEDIATED: Avoid logging raw user input\nlogger.error("Login failed for user.");',
    code
)

with open("src/main/java/com/example/Log4jCVE2020_9488Example.java", "w") as file:
    file.write(code)
