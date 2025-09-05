import os
import sys
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# Carpeta donde guardaremos el índice y los datos
DATA_DIR = "data"
INDEX_FILE = os.path.join(DATA_DIR, "manual_index.faiss")
METADATA_FILE = os.path.join(DATA_DIR, "manual_metadata.pkl")

# Inicializamos el modelo de embeddings
print("🔍 Cargando modelo de embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_manual(file_path):
    """
    Carga el contenido de un archivo de texto y lo devuelve como string.
    Aquí podrías añadir lógica para leer PDF, DOCX, etc.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text, chunk_size=500):
    """
    Divide el texto en fragmentos para facilitar la búsqueda semántica.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def create_embeddings(chunks):
    """
    Crea embeddings para cada fragmento usando el modelo.
    """
    return model.encode(chunks, convert_to_tensor=False)

def save_index(embeddings, chunks):
    """
    Guarda los embeddings en FAISS y asocia cada vector con su texto original.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)

    with open(METADATA_FILE, "wb") as f:
        pickle.dump(chunks, f)

    print(f"✅ Índice guardado en {INDEX_FILE}")
    print(f"✅ Metadatos guardados en {METADATA_FILE}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python manual_processor.py <ruta_del_manual.txt>")
        sys.exit(1)

    manual_path = sys.argv[1]
    print(f"📄 Procesando manual: {manual_path}")

    text = load_manual(manual_path)
    chunks = chunk_text(text)
    embeddings = create_embeddings(chunks)

    # Convertir embeddings a numpy para FAISS
    import numpy as np
    embeddings = np.array(embeddings).astype("float32")

    save_index(embeddings, chunks)
    print("🚀 Procesamiento completado.")