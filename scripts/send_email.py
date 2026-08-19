import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr

def send_email():
    # Cargar mensaje generado
    with open("message_data.json", "r", encoding="utf-8") as f:
        msg_data = json.load(f)
    
    # Determinar destinatario
    offer = os.environ.get("OFFER_URL", "")
    
    if "@" in offer:
        # Es un email directo
        to_email = offer
    else:
        # Era una URL, usar email de contacto de secrets
        to_email = os.environ.get("CONTACT_EMAIL", "")
        if not to_email:
            print("⚠️ Era una URL pero no hay CONTACT_EMAIL configurado")
            print("💡 Configura el secret CONTACT_EMAIL en GitHub")
            return
    
    print(f"📧 Enviando email a: {to_email}")
    
    # Credenciales
    from_email = os.environ["GMAIL_USER"]
    from_pass = os.environ["GMAIL_APP_PASS"]
    
    # Construir email
    msg = MIMEMultipart()
    msg["From"] = formataddr(("Candidato", from_email))
    msg["To"] = to_email
    msg["Subject"] = msg_data["subject"]
    
    # Cuerpo del email
    msg.attach(MIMEText(msg_data["body"], "plain", "utf-8"))
    
    # Adjuntar CV
    cv_path = "assets/cv.pdf"
    if os.path.exists(cv_path):
        with open(cv_path, "rb") as f:
            part = MIMEBase("application", "pdf")
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            "attachment",
            filename="CV.pdf"
        )
        msg.attach(part)
        print("✅ CV adjuntado")
    else:
        print("⚠️ No se encontró assets/cv.pdf")
    
    # Enviar email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, from_pass)
            server.send_message(msg)
        
        print(f"✅ Email enviado correctamente a {to_email}")
        
    except Exception as e:
        print(f"❌ Error al enviar email: {e}")
        raise

if __name__ == "__main__":
    send_email()
