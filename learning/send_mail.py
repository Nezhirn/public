import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from config import sender_email, receiver_email, password

def send_email(body: str, subject: str):


    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Date"] = time.strftime("%a, %d %b %Y %H:%M:%S %z")

    # Альтернативный текст и HTML
    plain_text = MIMEText(body, "plain", "utf-8")
    message.attach(plain_text)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Письмо отправлено успешно!")
    except Exception as e:
        print("Ошибка при отправке:", e)

send_email(
    body="Привет! 2 письмо для Mail.ru.",
    subject="Безопасное письмо"
)
