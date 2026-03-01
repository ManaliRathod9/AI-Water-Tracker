import smtplib
import ssl
import threading
import time
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

stop_flag = False
reminder_thread = None


def send_email(to_email):
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("Email credentials not found")
        return

    try:
        msg = EmailMessage()
        msg["Subject"] = "💧 Hydration Reminder"
        msg["From"] = GMAIL_USER
        msg["To"] = to_email
        msg.set_content("Time to drink water 💦 Stay hydrated!")

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        print("Reminder sent successfully")

    except Exception as e:
        print("Email error:", e)


def start_hourly_reminder(email):
    global stop_flag, reminder_thread
    stop_flag = False

    def reminder_loop():
        while not stop_flag:
            send_email(email)
            time.sleep(3600)

    reminder_thread = threading.Thread(target=reminder_loop)
    reminder_thread.daemon = True
    reminder_thread.start()


def stop_reminder():
    global stop_flag
    stop_flag = True