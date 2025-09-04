import os
from pathlib import Path
import pdfplumber
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

CHROMA_DIR = os.getenv("CHROMA_DIR", ".chroma")

def read_text(p: Path) -> str:
    ext = p.suffix.lower()
    if ext == ".pdf":
        parts = []
        with pdfplumber.open(p) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                if t.strip():
                    parts.append(t)
        return "\n".join(parts)
    elif ext in {".txt", ".md"}:
        return p.read_text(errors="ignore")
    elif ext in {".csv"}:
        return p.read_text(errors="ignore")
    else:
        return ""  # keep PoC simple

def chunk(text: str, size: int = 800, overlap: int = 120):
    words = text.split()
    n = len(words)
    i = 0
    while i < n:
        j = min(i + size, n)
        yield " ".join(words[i:j])
        i = j - overlap if j - overlap > i else j

def main():
    client = chromadb.PersistentClient(path=CHROMA_DIR, settings=Settings(allow_reset=True))
    coll = client.get_or_create_collection("docs")
    embed = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    idx = 0
    for p in Path("data/raw").rglob("*"):
        if not p.is_file():
            continue
        text = read_text(p)
        if not text.strip():
            continue
        for ci, ch in enumerate(chunk(text)):
            emb = embed.encode(ch, normalize_embeddings=True).tolist()
            coll.add(
                ids=[f"{idx}-{ci}"],
                embeddings=[emb],
                documents=[ch],
                metadatas=[{"source": str(p)}],
            )
        idx += 1
    print("✅ Ingestion complete.")

if __name__ == "__main__":
    main()