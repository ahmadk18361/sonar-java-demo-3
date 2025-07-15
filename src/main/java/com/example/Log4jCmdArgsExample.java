import org.apache.log4j.Logger;

public class Log4jCmdArgsExample {
    static Logger logger = Logger.getLogger(Log4jCmdArgsExample.class);

    public static void main(String[] args) {
        if (args.length > 0) {
            String username = args[0];  //  Untrusted input
            logger.info("Attempted access by: " +  username);  //  Unsafe if input includes JNDI injection
        }
    }
}
