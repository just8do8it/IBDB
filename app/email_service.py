import smtplib
from email.message import EmailMessage
import os

EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

def send_book_email(recipient_email, book_title, file_path):
    msg = EmailMessage()
    msg["Subject"] = f"Your requested book: {book_title}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient_email
    msg.set_content(f"Here is the book '{book_title}' that you requested.")

    with open(file_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=f"{book_title}.pdf")

    try:

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.ehlo()  
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  
            smtp.send_message(msg)

        print("Email sent successfully!")
    
    except smtplib.SMTPAuthenticationError as e:
        print("SMTP Authentication Error:", e)

    except Exception as e:
        print("Error:", e)
