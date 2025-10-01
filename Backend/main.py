from fastapi import FastAPI, Query
from ia_connector import preguntar_ia
from motor_semantico import buscar_fragmentos_relacionados
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # o lista de dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/preguntar")
def preguntar(pregunta: str = Query(...)):
    contextos = buscar_fragmentos_relacionados(pregunta, top_k=3)
    if not contextos:
        return {"pregunta": pregunta, "respuesta": "No encontré información en el manual para responder tu pregunta.", "fragmentos_relacionados": []}

    contexto_completo = "\n\n---\n\n".join([c[:500] for c in contextos])  # truncar a 500c
    prompt = f"""Eres un asistente que SOLO puede usar el siguiente CONTEXTO para responder. Si no está allí, responde "No tengo la información...".
    CONTEXTO:
    {contexto_completo}

    PREGUNTA:
    {pregunta}

    RESPUESTA:
    """
    respuesta = preguntar_ia(prompt)
    return {"pregunta": pregunta, "fragmentos_relacionados": contextos, "respuesta": respuesta}

