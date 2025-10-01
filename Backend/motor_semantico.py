import faiss, pickle
from sentence_transformers import SentenceTransformer

INDEX_FILE = "embeddings/manual_index.faiss"
META_FILE  = "embeddings/manual_metadata.pkl"

MODEL = SentenceTransformer('all-MiniLM-L6-v2')

index = faiss.read_index(INDEX_FILE)
with open(META_FILE, "rb") as f:
    chunks = pickle.load(f)

def buscar_fragmentos_relacionados(query, top_k=3):
    q_emb = MODEL.encode([query]).astype("float32")
    D, I = index.search(q_emb, top_k)
    return [chunks[i] for i in I[0]]
