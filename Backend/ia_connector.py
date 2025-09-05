import requests

def preguntar_ia(prompt: str) -> str:
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "mistral",
            "prompt": prompt
        }
        response = requests.post(url, json=payload, stream=True)

        respuesta = ""
        for line in response.iter_lines():
            if line:
                data = line.decode("utf-8")
                import json
                obj = json.loads(data)
                if "response" in obj:
                    respuesta += obj["response"]

        return respuesta.strip()

    except Exception as e:
        return f"[ERROR] No se pudo conectar con la IA local: {e}"
