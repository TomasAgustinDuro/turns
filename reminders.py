import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

# Manejo lógica de recordatiorios
def reserve_reminder_email(recipient, subject, message):
        sender_email = os.getenv('EMAIL_USER')
        sender_password = os.getenv('EMAIL_PASSWORD')
        
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient
        msg.set_content(message)
        
        try: 
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)
            print('Correo enviado exitosamente')
        except Exception as e: 
            print(f'Error al enviar correo: {e}')

# def reserve_reminder_sms():
#     pass

