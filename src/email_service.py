import os
import smtplib
from email.mime.text import MIMEText

def send_email(to_email: str, subject: str, body: str):
    """
    Sends an email using Gmail SMTP + App Password.
    You must set these environment variables:
    GMAIL_USER, GMAIL_APP_PASSWORD
    """

    gmail_user = os.getenv("GMAIL_USER")
    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_app_password:
        raise ValueError("Missing GMAIL_USER or GMAIL_APP_PASSWORD in environment variables.")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_app_password)
        server.sendmail(gmail_user, [to_email], msg.as_string())