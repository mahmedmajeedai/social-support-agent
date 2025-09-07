# src/ui/app.py
import os
import requests
import streamlit as st
from pathlib import Path
import subprocess

# ---- Config ----
API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")
RAW_DIR = Path("data/raw/uploads")
RAW_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(page_title="Customer Support Agent", layout="centered")
st.title("Customer Support Agent")

# ---- Sidebar: Upload + Reindex + Health ----
with st.sidebar:
    st.header("Documents")
    uploads = st.file_uploader(
        "Upload PDF / TXT / CSV", type=["pdf", "txt", "csv"], accept_multiple_files=True
    )
    if uploads:
        for f in uploads:
            (RAW_DIR / f.name).write_bytes(f.read())
        st.success(f"Saved {len(uploads)} file(s) to {RAW_DIR}")

    st.markdown("---")
    if st.button("Rebuild Index"):
        with st.spinner("Indexing uploaded documents..."):
            ROOT = Path(__file__).resolve().parents[2]
            INGEST = ROOT / "scripts" / "ingest.sh"
            if not INGEST.exists():
                st.error(f"Ingest script not found: {INGEST}")
            else:
                proc = subprocess.run(
                    ["bash", str(INGEST)],
                    cwd=str(ROOT),
                    capture_output=True,
                    text=True,
                )
                if proc.returncode == 0:
                    st.success("✅ Ingestion complete.")
                    if proc.stdout.strip():
                        st.caption(proc.stdout.strip())
                else:
                    st.error("Ingestion failed.")
                    st.code(proc.stderr or proc.stdout or "No output")

    st.markdown("---")
    try:
        ok = requests.get(f"{API_BASE}/health", timeout=5).json().get("ok", False)
        st.info(f"Backend: {'✅ healthy' if ok else '❌ down'}")
    except Exception as e:
        st.error(f"Backend check failed: {e}")

# ---- Chat over uploaded documents (plain answer only) ----
st.subheader("Chat")
q = st.text_input("Your question", "What is the main goal of the solution described in this document?")

def ask_backend(question: str) -> str:
    try:
        r = requests.post(f"{API_BASE}/chat", json={"question": question}, timeout=120)
        data = r.json()
        return str(data.get("answer", "(no answer)"))
    except Exception as e:
        return f"Error: {e}"

if st.button("Send"):
    with st.spinner("Thinking..."):
        answer = ask_backend(q)
    st.write(answer)

st.caption("Flow: upload files → Rebuild Index → ask a question. I answer strictly from your uploads.")
