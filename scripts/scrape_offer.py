import os
import json
import requests
from bs4 import BeautifulSoup

def scrape_offer():
    url = os.environ.get("OFFER_URL", "")
    
    if not url:
        print("❌ No se proporcionó URL")
        return
    
    print(f"🔍 Extrayendo datos de: {url}")
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Eliminar elementos no relevantes
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        
        # Extraer texto principal
        text = soup.get_text(separator="\n", strip=True)
        
        # Limitar a 4000 caracteres para no saturar la IA
        text = text[:4000]
        
        # Guardar datos
        data = {
            "url": url,
            "content": text
        }
        
        with open("offer_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Oferta extraída correctamente ({len(text)} caracteres)")
        
    except Exception as e:
        print(f"❌ Error al extraer oferta: {e}")
        # Crear archivo vacío para que el flujo continúe
        with open("offer_data.json", "w") as f:
            json.dump({"url": url, "content": ""}, f)

if __name__ == "__main__":
    scrape_offer()
