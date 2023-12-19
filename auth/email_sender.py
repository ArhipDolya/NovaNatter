import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import SMTP_USERNAME, SENDER_EMAIL
import logging


def send_email(receiver_email, subject, body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = SMTP_USERNAME
    smtp_password = 'eqojdclltmobmbzx'
    sender_email = SENDER_EMAIL

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)

            server.sendmail(sender_email, receiver_email, msg.as_string())
            print(f"Email sent successfully to {receiver_email}")
            logging.info(f"Email sent successfully to {receiver_email}")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
        logging.error(f"Error sending email: {e}")