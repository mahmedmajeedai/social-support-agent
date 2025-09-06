import os
import requests
import streamlit as st
from pathlib import Path
import subprocess
import json

# ---- Config ----
API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")
RAW_DIR = Path("data/raw/uploads")
RAW_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(page_title="Social Support Agent", layout="centered")
st.title("Social Support Agent (PoC)")

with st.sidebar:
    st.header("Documents")
    up = st.file_uploader(
        "Upload PDF / TXT / CSV", type=["pdf", "txt", "csv"], accept_multiple_files=True
    )
    if up:
        for f in up:
            dst = RAW_DIR / f.name
            dst.write_bytes(f.read())
        st.success(f"Saved {len(up)} file(s) to {RAW_DIR}")

    st.markdown("---")
    if st.button("Rebuild Index"):
        with st.spinner("Ingesting documents into Chroma..."):
            # Resolve project root and script path from this file
            ROOT = Path(__file__).resolve().parents[2]  # social-support-agent/
            INGEST = ROOT / "scripts" / "ingest.sh"
            if not INGEST.exists():
                st.error(f"Ingest script not found: {INGEST}")
            else:
                proc = subprocess.run(
                    ["bash", str(INGEST)],
                    cwd=str(ROOT),                    # IMPORTANT: run from project root
                    capture_output=True,
                    text=True
                )
                if proc.returncode == 0:
                    st.success("✅ Ingestion complete.")
                    if proc.stdout:
                        st.caption(proc.stdout.strip())
                else:
                    st.error("Ingestion failed.")
                    st.code(proc.stderr or proc.stdout or "No output")


    st.markdown("---")
    # Backend health
    try:
        ok = requests.get(f"{API_BASE}/health", timeout=5).json().get("ok", False)
        st.info(f"Backend: {'✅ healthy' if ok else '❌ down'}")
    except Exception as e:
        st.error(f"Backend check failed: {e}")

st.subheader("Assessment")

mode = st.radio(
    "Mode",
    ("Assessment (financial)", "Document Q&A"),
    horizontal=True,
)

q_default = "Assess eligibility and summarize the applicant’s finances." if mode.startswith("Assessment") else "Ask a question about the uploaded documents."
q = st.text_input(
    "Prompt",
    q_default,
)

if st.button("Run"):
    try:
        endpoint = "/assess" if mode.startswith("Assessment") else "/ask"
        resp = requests.post(f"{API_BASE}{endpoint}", json={"question": q}, timeout=120)
        data = resp.json()

        st.write("### Answer")
        st.write(data.get("answer", "(no answer)"))

        if mode.startswith("Assessment"):
            st.write("### Structured")
            st.json(data.get("structured", {}))

        st.write("### Citations")
        for c in data.get("citation_files", []):
            st.write(f"- {c}")
    except Exception as e:
        st.error(str(e))

st.caption("Tip: Upload files in the sidebar, click Rebuild Index, then run.")