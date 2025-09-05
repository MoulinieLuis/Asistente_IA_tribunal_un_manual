# motor_semantico.py
import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

# Modelo de embeddings
modelo = SentenceTransformer("all-MiniLM-L6-v2")

# Carpetas y archivos
DATA_DIR = "data"
EMBEDDINGS_FILE = "embeddings/manual_embeddings.faiss"
FRAGMENTS_FILE = "embeddings/manual_fragments.txt"

# Configuración de Docling
pipeline_options = PdfPipelineOptions()
pipeline_options.do_code_enrichment = True
pipeline_options.do_formula_enrichment = True
pipeline_options.do_picture_classification = True
pipeline_options.do_picture_description = False  # activar si quieres captions de imágenes

converter = DocumentConverter(
    format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
)

def procesar_manuales_y_generar_embeddings():
    """
    Usa Docling para extraer fragmentos de PDFs en data/,
    genera embeddings y guarda índice FAISS + fragmentos.
    """
    fragmentos = []
    print("Procesando manuales con Docling...")

    os.makedirs("embeddings", exist_ok=True)

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".pdf"):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                result = converter.convert(filepath)
                doc = result.document

                # Extraer fragmentos relevantes (texto, código, fórmulas, imágenes con descripciones)
                for item in doc.items:
                    if item.category == "TEXT":
                        fragmentos.append(item.text)
                    elif item.category == "CODE":
                        fragmentos.append(f"[Código {item.code_language}] {item.text}")
                    elif item.category == "FORMULA":
                        fragmentos.append(f"[Fórmula LaTeX] {item.latex}")
                    elif item.category == "PICTURE":
                        if item.picture_classification:
                            fragmentos.append(f"[Imagen: {item.picture_classification}]")
                        if item.description:
                            fragmentos.append(f"[Descripción imagen] {item.description}")

                print(f"   - Procesado: {filename} ({len(fragmentos)} fragmentos acumulados)")

            except Exception as e:
                print(f"   - Error al procesar {filename}: {e}")

    if not fragmentos:
        print("No se encontraron fragmentos.")
        return None, None

    # Generar embeddings
    print("Generando embeddings...")
    vectores = modelo.encode(fragmentos)

    # Crear índice FAISS
    dimension = vectores.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectores.astype(np.float32))
    faiss.write_index(index, EMBEDDINGS_FILE)

    # Guardar fragmentos
    with open(FRAGMENTS_FILE, "w", encoding="utf-8") as f:
        f.write("\n\n".join(fragmentos))

    print("Embeddings generados y guardados.")
    return index, fragmentos

def cargar_o_generar_embeddings():
    """
    Carga embeddings y fragmentos si existen, o los genera.
    """
    if os.path.exists(EMBEDDINGS_FILE) and os.path.exists(FRAGMENTS_FILE):
        print("Cargando embeddings guardados...")
        index = faiss.read_index(EMBEDDINGS_FILE)
        with open(FRAGMENTS_FILE, "r", encoding="utf-8") as f:
            fragmentos = f.read().split("\n\n")
        return index, fragmentos
    else:
        return procesar_manuales_y_generar_embeddings()

# Cargar al inicio
index, fragmentos = cargar_o_generar_embeddings()

def buscar_fragmentos_relacionados(pregunta: str, k: int = 3) -> list[str]:
    """
    Busca los k fragmentos más relevantes para la pregunta.
    """
    if not index or not fragmentos:
        return []

    vector_pregunta = modelo.encode([pregunta])
    distancias, indices = index.search(vector_pregunta.astype(np.float32), k=k)
    return [fragmentos[i] for i in indices[0]]
