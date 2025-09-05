# main.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from motor_semantico import buscar_fragmentos_relacionados
from ia_connector import preguntar_ia

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/preguntar")
def preguntar(pregunta: str = Query(..., description="Pregunta del usuario")):
    # Buscar fragmentos relacionados
    contextos = buscar_fragmentos_relacionados(pregunta)
    contexto_completo = "\n\n---\n\n".join(contextos)

    prompt = f"""
Eres un asistente experto cuya única fuente de información son los fragmentos del manual proporcionados más abajo.
IMPORTANTE:
- Si la respuesta no está en los fragmentos, debes responder únicamente: "No tengo la información necesaria en el manual."
- No inventes información ni uses conocimiento externo.
- Responde siempre en español.
- Usa un estilo claro y conciso.

Fragmentos del manual:
{contexto_completo}

Pregunta del usuario:
{pregunta}

Respuesta (basada solo en los fragmentos):
"""


    respuesta = preguntar_ia(prompt)

    if respuesta.startswith("[ERROR]"):
        return {"error": respuesta}

    return {"pregunta": pregunta, "fragmentos_relacionados": contextos, "respuesta": respuesta}
