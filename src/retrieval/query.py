import os
os.environ.setdefault("ANONYMIZED_TELEMETRY","false")
os.environ.setdefault("CHROMA_TELEMETRY_IMPLEMENTATION","none")

USE_QDRANT = os.getenv("USE_QDRANT","false").lower()=="true"

if USE_QDRANT:
    from src.retrieval.qdrant_store import search as qdrant_search
    def retrieve_uploads(query: str, k: int = 6):
        return qdrant_search(query, k=k)
else:
    import chromadb
    from chromadb.errors import InvalidCollectionException
    from sentence_transformers import SentenceTransformer
    CHROMA_DIR = os.getenv("CHROMA_DIR",".chroma")
    _client = chromadb.PersistentClient(path=CHROMA_DIR)
    _embed = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    def _get_collection():
        try: return _client.get_collection("docs")
        except Exception: return _client.get_or_create_collection("docs")
    def retrieve_uploads(query: str, k: int = 6):
        q = _embed.encode(query, normalize_embeddings=True).tolist()
        coll = _get_collection()
        def _run():
            return coll.query(
                query_embeddings=[q],
                n_results=min(k, 6),
                include=["documents","metadatas"],
                where={"group":"uploads"},
            )
        try: res = _run()
        except InvalidCollectionException:
            coll = _get_collection(); res = _run()
        docs = res.get("documents",[[]])[0]; metas = res.get("metadatas",[[]])[0]
        return [{"text": d, "source": m.get("source","unknown")} for d,m in zip(docs, metas)]
