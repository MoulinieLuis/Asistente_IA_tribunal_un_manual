# ia_connector.py
import requests
import json

def preguntar_ia(prompt: str) -> str:
    """
    Envía un prompt a la IA local (Ollama/Mistral) y devuelve la respuesta.
    Maneja errores de formato en las líneas recibidas.
    """
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "mistral",  
            "prompt": prompt
        }
        response = requests.post(url, json=payload, stream=True)

        respuesta = ""
        for line in response.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line.decode("utf-8"))
                print("[DEBUG] Línea recibida:", data)  

                if "response" in data:
                    respuesta += data["response"]

            except Exception as e:
                print(f"[DEBUG] Línea ignorada: {line} -> {e}")
                continue

        if not respuesta:
            return "[ERROR] No se recibió respuesta del modelo. Revisa que el modelo esté cargado y tenga el nombre correcto."

        return respuesta.strip()

    except Exception as e:
        return f"[ERROR] No se pudo conectar con la IA local: {e}"
