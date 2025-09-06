# src/retrieval/ingest.py
import os
from pathlib import Path
import json
import pdfplumber
import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = os.getenv("CHROMA_DIR", ".chroma")
DATA_DIR = Path("data/raw")

# model + DB
embed = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_DIR)
coll = client.get_or_create_collection("docs")

def chunk_text(text, size=800, overlap=120):
    text = " ".join(text.split())
    out, i, n = [], 0, len(text)
    while i < n:
        out.append(text[i : i + size])
        i += size - overlap
    return out

def load_file(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        txt = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                txt.append(page.extract_text() or "")
        return "\n".join(txt)
    if path.suffix.lower() in {".txt", ".csv"}:
        return path.read_text(errors="ignore")
    return ""  # unsupported formats are skipped

def main():
    # wipe and rebuild index
    try:
        client.delete_collection("docs")
    except Exception:
        pass
    coll = client.get_or_create_collection("docs")

    files = [p for p in DATA_DIR.rglob("*") if p.is_file() and p.suffix.lower() in {".pdf", ".txt", ".csv"}]
    total_chunks = 0
    ids, docs, metas, embs = [], [], [], []

    for idx, f in enumerate(sorted(files)):
        try:
            txt = load_file(f)
        except Exception:
            txt = ""
        if not txt.strip():
            continue
        chunks = chunk_text(txt)
        for j, ch in enumerate(chunks):
            ids.append(f"{idx}-{j}-{f.name}")
            docs.append(ch)
            metas.append({"source": str(f)})
        total_chunks += len(chunks)

        # batch insert every ~500 chunks to keep memory reasonable
        if len(ids) >= 500:
            embs = embed.encode(docs, normalize_embeddings=True).tolist()
            coll.add(ids=ids, documents=docs, metadatas=metas, embeddings=embs)
            ids, docs, metas, embs = [], [], [], []

    if docs:
        embs = embed.encode(docs, normalize_embeddings=True).tolist()
        coll.add(ids=ids, documents=docs, metadatas=metas, embeddings=embs)

    print(json.dumps({
        "indexed_files": [str(p) for p in files],
        "num_files": len(files),
        "total_chunks": total_chunks,
        "collection": "docs",
        "chroma_dir": CHROMA_DIR
    }, indent=2))

if __name__ == "__main__":
    main()
