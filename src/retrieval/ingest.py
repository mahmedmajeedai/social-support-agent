import os, json
from pathlib import Path
from pypdf import PdfReader
import pdfplumber
import chromadb
from sentence_transformers import SentenceTransformer

USE_QDRANT = os.getenv("USE_QDRANT", "false").lower() == "true"
DATA_DIR = Path("data/raw/uploads")
CHROMA_DIR = os.getenv("CHROMA_DIR", ".chroma")
embed = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
cclient = chromadb.PersistentClient(path=CHROMA_DIR)

# Qdrant
if USE_QDRANT:
    from src.retrieval.qdrant_store import ensure_collection, add_texts

def _read_pdf(p: Path) -> str:
    try:
        txt = "\n".join([(pg.extract_text() or "") for pg in PdfReader(str(p)).pages])
        if txt.strip(): return txt
    except Exception: pass
    try:
        with pdfplumber.open(str(p)) as pdf:
            return "\n".join([pg.extract_text() or "" for pg in pdf.pages])
    except Exception:
        return ""

def _load(p: Path) -> str:
    s = p.suffix.lower()
    if s == ".pdf": return _read_pdf(p)
    if s in {".txt", ".csv"}: return p.read_text(errors="ignore")
    return ""

def _chunks(text: str, size=900, overlap=150):
    t = " ".join(text.replace("\x00"," ").split()); out=[]; i=0
    while i < len(t):
        out.append(t[i:i+size]); i += size-overlap
    return out


def main():
    files = [p for p in DATA_DIR.rglob("*") if p.is_file() and p.suffix.lower() in {".pdf",".txt",".csv"}]
    total = 0

    if USE_QDRANT:
        ensure_collection(vec_dim=384)  # MiniLM dim
        for idx, f in enumerate(sorted(files)):
            txt = _load(f)
            if not txt.strip():
                continue
            docs = _chunks(txt)
            ids = [f"{idx}-{j}-{f.name}" for j in range(len(docs))]
            metas = [{"source": str(f), "name": f.name, "ext": f.suffix.lower(), "group":"uploads", "text": d} for d in docs]
            add_texts(docs, metas, ids)
            total += len(docs)
    else:
        try:
            cclient.delete_collection("docs")
        except Exception:
            pass
        coll = cclient.get_or_create_collection("docs")
        ids, docs, metas = [], [], []
        for idx, f in enumerate(sorted(files)):
            txt = _load(f)
            if not txt.strip():
                continue
            chunks = _chunks(txt)
            total += len(chunks)
            for j, ch in enumerate(chunks):
                ids.append(f"{idx}-{j}-{f.name}")
                docs.append(ch)
                metas.append({"source": str(f), "name": f.name, "ext": f.suffix.lower(), "group":"uploads"})
            if len(ids) >= 400:
                embs = embed.encode(docs, normalize_embeddings=True).tolist()
                coll.add(ids=ids, documents=docs, metadatas=metas, embeddings=embs)
                ids, docs, metas = [], [], []
        if docs:
            embs = embed.encode(docs, normalize_embeddings=True).tolist()
            coll.add(ids=ids, documents=docs, metadatas=metas, embeddings=embs)

    print(json.dumps({"num_files": len(files), "total_chunks": total, "use_qdrant": USE_QDRANT}, indent=2))


if __name__ == "__main__":
    main()
