<div align="center">

<!-- BANNER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:203a43,100:2c5364&height=200&section=header&text=AskMyDocs%20AI&fontSize=52&fontColor=ffffff&fontAlignY=38&desc=Your%20Documents.%20Your%20AI.%20Your%20Machine.&descSize=18&descAlignY=60&descColor=a8d8ea" width="100%"/>

<!-- BADGES -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Ollama-Local%20LLM-black?style=for-the-badge&logo=ollama&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/ChromaDB-Vector%20DB-7B2FBE?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/100%25%20Local-No%20Cloud-success?style=flat-square"/>
  <img src="https://img.shields.io/badge/No%20API%20Key-Required-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Privacy-First-red?style=flat-square"/>
</p>

<br/>

> **AskMyDocs AI** is a fully local, privacy-first Retrieval-Augmented Generation (RAG) chatbot that answers questions **strictly from your own uploaded documents** — PDFs, TXTs, and CSVs — with no cloud, no API keys, and no data leaving your machine.

<br/>

[🚀 Quickstart](#-quickstart) · [✨ Features](#-features) · [🏗️ Architecture](#️-architecture) · [📦 Tech Stack](#-tech-stack) · [🤝 Contributing](#-contributing)

</div>

---

## 🎯 What is AskMyDocs AI?

Most AI chatbots send your data to the cloud. **AskMyDocs AI doesn't.**

Upload your internal documents — policies, manuals, reports, datasets — and ask questions in plain English. The agent retrieves the most relevant chunks and generates grounded, accurate answers using a local LLM via Ollama. If the answer isn't in your docs, it says so. No hallucinations from outside knowledge.

```
User: "What is our refund policy for digital products?"
Bot:  "Based on the uploaded documents: Digital products are eligible
       for a full refund within 14 days of purchase if..."
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 📂 **Multi-format Ingestion** | Upload PDF, TXT, and CSV documents |
| 🔍 **RAG Pipeline** | Semantic chunking → embedding → vector retrieval |
| 🤖 **Local LLM** | Powered by Ollama (LLaMA 3, Mistral, Phi-3, and more) |
| 🔒 **100% Private** | No cloud, no API keys, no data leaves your machine |
| 💬 **Grounded Answers** | Answers only from uploaded docs — no hallucinations |
| 🔄 **Rebuild Index** | Re-ingest anytime when documents are updated |
| 🖥️ **Clean Chat UI** | Streamlit-powered conversational interface |
| ⚡ **Fast API Backend** | RESTful FastAPI server for the retrieval pipeline |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│                    Streamlit Chat App                         │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP
┌────────────────────────▼────────────────────────────────────┐
│                      FASTAPI BACKEND                         │
│              /chat  /ingest  /rebuild-index                  │
└──────────┬─────────────────────────────┬────────────────────┘
           │                             │
┌──────────▼──────────┐     ┌────────────▼───────────────────┐
│    RETRIEVAL ENGINE  │     │       DOCUMENT INGESTION        │
│                      │     │                                  │
│  1. Embed query      │     │  PDF / TXT / CSV  →  Chunks     │
│  2. Search ChromaDB  │     │  Chunks  →  Embeddings          │
│  3. Return top-k     │     │  Embeddings  →  ChromaDB        │
│     chunks           │     │                                  │
└──────────┬──────────┘     └─────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────────┐
│                    OLLAMA  (Local LLM)                        │
│       LLaMA 3 / Mistral / Phi-3 / Gemma2 / ...              │
│   Context: [retrieved chunks] + User Query → Answer          │
└─────────────────────────────────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────────┐
│                    SENTENCE TRANSFORMERS                      │
│              all-MiniLM-L6-v2  (embedding model)             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.11 |
| **LLM Runtime** | [Ollama](https://ollama.com) — runs LLaMA, Mistral, Phi-3 locally |
| **Embeddings** | `all-MiniLM-L6-v2` via SentenceTransformers |
| **Vector Database** | [ChromaDB](https://www.trychroma.com/) (default) · optional Qdrant / Redis |
| **Backend API** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Frontend UI** | [Streamlit](https://streamlit.io/) |
| **Orchestration** | Custom RAG pipeline: retrieval → context assembly → generation |

---

## ⚙️ Prerequisites

Before you start, make sure you have:

- **OS:** Ubuntu 22.04+ · macOS · Windows (via WSL2)
- **Python:** 3.11
- **[Ollama](https://ollama.com/download):** Installed and running
- **Git** (and optionally Docker for Qdrant)

---

## 🚀 Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/mahmedmajeedai/social-support-agent.git
cd social-support-agent
```

### 2. Set up Python environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install & configure Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify it's running
systemctl status ollama

# Pull a model (Phi-3 is lightweight, great for CPU)
ollama pull phi3:3.8b-mini-instruct

# Quick test
ollama run phi3:3.8b-mini-instruct "Hello!"
```

> 💡 **Tip:** Other good models: `llama3.2:3b`, `mistral:7b`, `gemma2:2b`

### 4. Set environment variables

```bash
export OLLAMA_HOST=http://127.0.0.1:11434
export OLLAMA_MODEL=phi3:3.8b-mini-instruct
export ANONYMIZED_TELEMETRY=false
export CHROMA_TELEMETRY_IMPLEMENTATION=none
```

### 5. Add your documents & build the index

Place your PDF, TXT, or CSV files in the `data/raw/` folder, then:

```bash
rm -rf .chroma/          # Clear any existing index
bash scripts/ingest.sh   # Chunk, embed, and store your docs
```

### 6. Start the backend API

```bash
uvicorn src.api.app:app --reload --port 8000
```

API docs available at: `http://localhost:8000/docs`

### 7. Launch the chat UI

```bash
streamlit run src/ui/app.py
```

Open your browser at `http://localhost:8501` — start chatting! 🎉

---

## 📁 Project Structure

```
social-support-agent/
│
├── data/
│   └── raw/                  # 📂 Drop your documents here (PDF, TXT, CSV)
│
├── scripts/
│   └── ingest.sh             # 🔄 Document ingestion script
│
├── src/
│   ├── api/
│   │   └── app.py            # ⚡ FastAPI backend (chat + ingest endpoints)
│   │
│   ├── rag/
│   │   ├── chunker.py        # ✂️  Document chunking logic
│   │   ├── embedder.py       # 🔢 Embedding with SentenceTransformers
│   │   └── retriever.py      # 🔍 ChromaDB vector search
│   │
│   └── ui/
│       └── app.py            # 💬 Streamlit chat interface
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 💬 Example Use Cases

- 🏢 **Internal HR Chatbot** — Upload your employee handbook; let staff ask HR questions
- 📜 **Legal Doc Assistant** — Query contracts and policies without reading every page
- 📊 **Report Analyst** — Ask questions across multiple quarterly CSV/PDF reports
- 🛒 **Product Support Bot** — Ingest product manuals; answer customer support tickets
- 🎓 **Study Aid** — Upload lecture notes and textbooks; quiz yourself on content

---

## 🔧 Configuration

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_HOST` | `http://127.0.0.1:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `phi3:3.8b-mini-instruct` | LLM model to use |
| `CHROMA_PATH` | `.chroma/` | ChromaDB persistence directory |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | SentenceTransformer model |
| `CHUNK_SIZE` | `512` | Characters per document chunk |
| `TOP_K` | `5` | Number of retrieved chunks per query |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "feat: describe your change"
git push origin feature/your-feature-name
# Open a Pull Request 🎉
```

Please keep PRs focused and include a brief description of what changed and why.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with ❤️ by [mahmedmajeedai](https://github.com/mahmedmajeedai)**

*If this project helped you, consider giving it a ⭐ — it means a lot!*

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:203a43,100:2c5364&height=100&section=footer" width="100%"/>

</div>
