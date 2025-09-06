import os
import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = os.getenv("CHROMA_DIR", ".chroma")
_client = chromadb.PersistentClient(path=CHROMA_DIR)
_coll = _client.get_or_create_collection("docs")
_embed = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def retrieve(query: str, k: int = 5):
    q = _embed.encode(query, normalize_embeddings=True).tolist()
    res = _coll.query(query_embeddings=[q], n_results=k, include=["documents", "metadatas", "distances"])
    docs   = res["documents"][0]
    metas  = res["metadatas"][0]
    dists  = res.get("distances", [[None]*len(docs)])[0]
    # Chroma returns cosine distance (0 = identical). Convert to similarity ~ (1 - dist).
    out = []
    for d, m, dist in zip(docs, metas, dists):
        sim = None if dist is None else (1.0 - float(dist))
        out.append({"text": d, "source": m.get("source", "unknown"), "similarity": sim})
    return out
