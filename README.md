# 🧑‍💻 Customer Support Agent (Locally Hosted GenAI + RAG)

This project is a **locally hosted Generative + Agentic AI chatbot** that answers questions **strictly from your uploaded documents** (PDF, TXT, CSV).  
It uses:

- **Ollama** to host a local LLM (e.g., LLaMA, Mistral, Phi-3).  
- **SentenceTransformers** + **Chroma** (or optional Qdrant) for embeddings and retrieval.  
- **FastAPI** as backend API.  
- **Streamlit** as chat UI.  

It fully complies with requirements: locally hosted LLM, multimodal ingestion, RAG, interactive chat, and orchestration:contentReference[oaicite:0]{index=0}.

---

## ✨ Features
- Upload your own docs (PDF / TXT / CSV).
- Rebuild index → documents get chunked, embedded, and stored locally.
- Ask questions → chatbot fetches chunks → feeds into local LLM (via Ollama).
- Answers strictly from uploaded docs; if answer not found → *“Sorry, I couldn’t find that information in the documents you uploaded.”*
- Fully local: no API keys, no cloud dependency.

---

## 📦 Tech Stack
- **Language:** Python 3.11
- **LLM Hosting:** [Ollama](https://ollama.com) (runs locally)
- **Vector DB:** Chroma (default), optional Qdrant/Redis
- **Embeddings:** all-MiniLM-L6-v2 (SentenceTransformers)
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Orchestration:** Lightweight agent pipeline (retrieval → context → LLM)

---

## ⚙️ Prerequisites
- Ubuntu 22.04+ (works on Linux/Mac; Windows via WSL2).
- Python 3.11
- [Ollama](https://ollama.com/download) installed and running as a service.
- Git + Docker (optional, if you want to run Qdrant).

---

## 🚀 Quickstart

### 1. Clone the repo
```bash
git clone https://github.com/mahmedmajeedai/social-support-agent.git
cd social-support-agent
```
### 2. Create a virtual environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

### 3. Install & run Ollama
```bash
# install ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# verify service is active
systemctl status ollama

# pull a small instruct model (good for CPU)
ollama pull phi3:3.8b-mini-instruct

# test it
ollama run phi3:3.8b-mini-instruct "Hello!"
```

### 4. Set environment variables
```bash
export OLLAMA_HOST=http://127.0.0.1:11434
export OLLAMA_MODEL=phi3:3.8b-mini-instruct
# quiet Chroma telemetry
export ANONYMIZED_TELEMETRY=false
export CHROMA_TELEMETRY_IMPLEMENTATION=none
```
### 5. Build the vector index
```bash
rm -rf .chroma/
bash scripts/ingest.sh
```
### 6. Run the API
```bash
uvicorn src.api.app:app --reload --port 8000
```

### 7. Run the Streamlit UI
```bash
streamlit run src/ui/app.py
```