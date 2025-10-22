# text_utils.py
import nltk
from nltk.tokenize import sent_tokenize

# Descargar recursos la primera vez
nltk.download("punkt", quiet=True)

def limpiar_texto(texto: str) -> str:
    """
    Limpia el texto eliminando espacios extra y saltos de línea innecesarios.
    """
    return " ".join(texto.split())

def fragmentar_texto(texto: str, max_tokens: int = 100) -> list[str]:
    """
    Divide un texto en fragmentos usando NLTK (por oraciones),
    manteniendo el tamaño aproximado en tokens.
    """
    oraciones = sent_tokenize(texto, language="spanish")
    fragmentos = []
    actual = []

    contador = 0
    for oracion in oraciones:
        tokens = len(oracion.split())
        if contador + tokens > max_tokens and actual:
            fragmentos.append(" ".join(actual))
            actual = []
            contador = 0
        actual.append(oracion)
        contador += tokens

    if actual:
        fragmentos.append(" ".join(actual))

    return fragmentos
