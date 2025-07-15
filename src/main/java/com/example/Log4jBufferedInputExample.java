import java.io.*;
import java.nio.charset.StandardCharsets;
import org.apache.log4j.Logger;

public class Log4jBufferedInputExample {
    static Logger logger = Logger.getLogger(Log4jBufferedInputExample.class);

    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        System.out.print("Enter username: ");
        String username = reader.readLine();  //  User-controlled input
        logger.warn("User login failed: " + String.valueOf(username));  //  Dangerous logging
    }
}

