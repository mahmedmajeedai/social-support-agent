import os
from typing import List, Dict
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from sentence_transformers import SentenceTransformer

QDRANT_URL = os.getenv("QDRANT_URL", "http://127.0.0.1:6333")
COLLECTION = os.getenv("QDRANT_COLLECTION", "uploads")
EMBED = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

_client = QdrantClient(url=QDRANT_URL)

def ensure_collection(vec_dim: int = 384):
    _client.recreate_collection(
        collection_name=COLLECTION,
        vectors_config=qmodels.VectorParams(size=vec_dim, distance=qmodels.Distance.COSINE)
    )

def add_texts(texts: List[str], metadatas: List[Dict], ids: List[str]):
    vecs = EMBED.encode(texts, normalize_embeddings=True).astype(np.float32)
    _client.upsert(
        collection_name=COLLECTION,
        points=[
            qmodels.PointStruct(id=ids[i], vector=vecs[i].tolist(), payload=metadatas[i])
            for i in range(len(ids))
        ],
    )

def search(query: str, k: int = 6) -> List[Dict]:
    qvec = EMBED.encode([query], normalize_embeddings=True)[0].astype(np.float32).tolist()
    res = _client.search(
        collection_name=COLLECTION,
        query_vector=qvec,
        limit=k,
        query_filter=qmodels.Filter(
            must=[qmodels.FieldCondition(key="group", match=qmodels.MatchValue(value="uploads"))]
        ),
        with_payload=True,
    )
    out = []
    for p in res:
        payload = p.payload or {}
        out.append({
            "text": payload.get("text", ""),
            "source": payload.get("source", "unknown"),
            "score": p.score
        })
    return out
