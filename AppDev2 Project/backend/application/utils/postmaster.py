import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


SMTP_SERVER_HOST = 'smtp.something.com'
SMTP_SERVER_PORT = 465
SENDER_ADDRESS = 'your-smtp-address@something.com'
SENDER_PASSWORD = 'your-smtp-provider-pass'


def basic_email(to, subject, body, attachment_file=None):
    """Email the specified address"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment_file:
        with open(attachment_file, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)

        part.add_header('Content-Disposition', f"attachment; filename= {attachment_file}")

        msg.attach(part)

    try:
        server = smtplib.SMTP_SSL(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
        server.login(SENDER_ADDRESS, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(e)
        return False