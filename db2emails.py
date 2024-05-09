import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_confirmation_email(user_email, user_name):
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Registration Confirmation"
    message["From"] = sender_email
    message["To"] = user_email

    text = f"Hi {user_name},\n\nThank you for registering at Collark Creative Hub. We are excited to have you on board!"
    part = MIMEText(text, "plain")
    message.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, user_email, message.as_string())
    server.quit()