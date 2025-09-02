import smtplib
from email.message import EmailMessage

email_password = "ngawymjvoyvsyhvz"

def send_email(email, average_height):
    from_email = "goku43210@gmail.com"
    to_email = email
    subject = "Average Height"
    body = f"The average height of all users is {average_height}."

    # Crear mensaje
    email_message = EmailMessage()
    email_message["From"] = from_email
    email_message["To"] = to_email
    email_message["Subject"] = subject
    email_message.set_content(body)

    # Enviar por SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as gmail:
        gmail.starttls()
        gmail.login(from_email, email_password)
        gmail.send_message(email_message)
