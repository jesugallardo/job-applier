import os
import json
from groq import Groq

def generate_message():
    # Cargar datos de la oferta
    offer_file = "offer_data.json"
    if os.path.exists(offer_file):
        with open(offer_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        offer_text = data.get("content", "")
        offer_url = data.get("url", "")
    else:
        offer_text = ""
        offer_url = os.environ.get("OFFER_URL", "")
    
    notes = os.environ.get("NOTES", "")
    
    # Si no hay contenido extraído, usar el email como referencia
    if not offer_text:
        if "@" in offer_url:
            offer_text = f"Email de contacto: {offer_url}"
        else:
            offer_text = "Oferta de trabajo (no se pudo extraer contenido)"
    
    print("🤖 Generando mensaje personalizado con IA...")
    
    # Inicializar cliente Groq
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    
    # Prompt para generar el mensaje
    prompt = f"""Eres un redactor profesional de candidaturas laborales en español.

Genera un email breve, profesional y personalizado para aplicar a esta oferta de trabajo.

OFERTA DE TRABAJO:
{offer_text[:2500]}

NOTAS ADICIONALES DEL CANDIDATO: {notes if notes else 'Ninguna'}

INSTRUCCIONES:
- Genera un asunto atractivo y profesional (línea 1)
- Genera el cuerpo del email (resto del texto)
- Tono: profesional pero cercano, no robótico
- Máximo 200 palabras
- Menciona que adjuntas el CV
- Termina con un saludo cordial
- NO incluyas "Asunto:" ni "Cuerpo:" en tu respuesta

FORMATO DE RESPUESTA:
[Línea 1: Solo el asunto]
[Líneas siguientes: Cuerpo del email]"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        
        result = response.choices[0].message.content.strip()
        
        # Separar asunto y cuerpo
        lines = result.split("\n", 1)
        subject = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else result
        
        # Limpiar posibles prefijos
        subject = subject.replace("Asunto:", "").replace("Subject:", "").strip()
        
        # Guardar resultado
        message_data = {
            "subject": subject,
            "body": body
        }
        
        with open("message_data.json", "w", encoding="utf-8") as f:
            json.dump(message_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Mensaje generado: {subject}")
        
    except Exception as e:
        print(f"❌ Error al generar mensaje: {e}")
        # Mensaje por defecto en caso de error
        message_data = {
            "subject": "Candidatura para puesto de trabajo",
            "body": "Estimados,\n\nMe pongo en contacto con ustedes para presentar mi candidatura.\n\nAdjunto mi CV para su revisión.\n\nQuedo a la espera de sus noticias.\n\nUn cordial saludo."
        }
        with open("message_data.json", "w", encoding="utf-8") as f:
            json.dump(message_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generate_message()
