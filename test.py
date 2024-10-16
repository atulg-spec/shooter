import smtplib
import socks
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email details
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # TLS port
your_email = 'seoworks065@gmail.com'
your_password = 'wnrs qsqf izcw duiv'
to_email = 'atulg0736@gmail.com'
subject = 'Test Email through Paid HTTP Proxy'
body = 'This is a test email sent through a paid HTTP proxy server.'

# Proxy details (HTTP proxy)
proxy_host = '165.154.172.141'
proxy_port = 3660
proxy_username = '36420396-zone-custom-region-us-sessid-4bwx5c6n-sessTime-50'
proxy_password = 'rashidghjff'

# Set up the proxy with authentication for HTTP
socks.setdefaultproxy(socks.HTTP, proxy_host, proxy_port, True, proxy_username, proxy_password)
socks.wrapmodule(smtplib)  # Wrap smtplib to use the proxy

# Create the email message
msg = MIMEMultipart()
msg['From'] = your_email
msg['To'] = to_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

server = None  # Initialize server to avoid NameError

try:
    # Set up the SMTP connection
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.set_debuglevel(1)
    server.set_debuglevel(1)  # Enable debug output
    server.starttls()  # Start TLS for security
    server.login(your_email, your_password)  # Log in to the SMTP server
    text = msg.as_string()
    server.sendmail(your_email, to_email, text)  # Send the email
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    if server:
        server.quit()  # Close the connection if server is defined
