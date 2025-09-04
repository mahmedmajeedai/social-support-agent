import os
import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = os.getenv("CHROMA_DIR", ".chroma")
_client = chromadb.PersistentClient(path=CHROMA_DIR)
_coll = _client.get_or_create_collection("docs")
_embed = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def retrieve(query: str, k: int = 5):
    q = _embed.encode(query, normalize_embeddings=True).tolist()
    res = _coll.query(query_embeddings=[q], n_results=k)
    docs = res["documents"][0]
    metas = res["metadatas"][0]
    return [{"text": d, "source": m.get("source","unknown")} for d, m in zip(docs, metas)]
