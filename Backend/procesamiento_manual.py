# procesamiento_manual.py
import os
import sys
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
try:
    from text_utils import limpiar_texto, fragmentar_texto  # ⬅️ usamos NLTK aquí
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from text_utils import limpiar_texto, fragmentar_texto

# Carpeta donde guardaremos el índice y los datos
DATA_DIR = "embeddings"
INDEX_FILE = os.path.join(DATA_DIR, "manual_index.faiss")
METADATA_FILE = os.path.join(DATA_DIR, "manual_metadata.pkl")


# Inicializamos el modelo de embeddings
print("🔍 Cargando modelo de embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_manual(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def create_embeddings(chunks):
    return model.encode(chunks, convert_to_tensor=False)

def save_index(embeddings, chunks):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    # Ensure embeddings is a numpy array of shape (num_chunks, embedding_dim) and type float32
    if not isinstance(embeddings, np.ndarray):
        embeddings = np.array(embeddings)
    if len(embeddings.shape) != 2:
        embeddings = embeddings.reshape(-1, dim)
    embeddings = embeddings.astype(np.float32)
    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)
    with open(METADATA_FILE, "wb") as f:
        pickle.dump(chunks, f)

    print(f"✅ Índice guardado en {INDEX_FILE}")
    print(f"✅ Metadatos guardados en {METADATA_FILE}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python procesamiento_manual.py <ruta_del_manual.txt>")
        sys.exit(1)

    manual_path = sys.argv[1]
    print(f"📄 Procesando manual: {manual_path}")

    text = load_manual(manual_path)
    text = limpiar_texto(text)               # ⬅️ limpieza
    chunks = fragmentar_texto(text, 80)      # ⬅️ fragmentación con NLTK

    embeddings = np.array(create_embeddings(chunks)).astype("float32")
    save_index(embeddings, chunks)
    print("🚀 Procesamiento completado.")
