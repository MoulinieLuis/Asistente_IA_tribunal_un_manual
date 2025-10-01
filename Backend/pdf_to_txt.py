from pdfminer.high_level import extract_text
from pathlib import Path

def pdf_to_txt(pdf_path: str, txt_output: str = None):
    """
    Convierte un PDF con texto (aunque tenga imágenes) a un archivo .txt
    """
    if txt_output is None:
        txt_output = Path(pdf_path).with_suffix(".txt")
    text = extract_text(pdf_path)
    Path(txt_output).write_text(text, encoding="utf-8")
    print(f"✅ Texto extraído en: {txt_output}")
    return txt_output

if __name__ == "__main__":
    # Ajusta las rutas a tu archivo real
    pdf_to_txt(
        "data/MANUAL_DE_REPORTES_SALA_ORDINARIA_PONENCIA.pdf",
        "data/MANUAL_DE_REPORTES_SALA_ORDINARIA_PONENCIA.txt"
    )
