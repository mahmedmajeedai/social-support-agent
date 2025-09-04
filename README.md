# Social Support Agent (PoC)

This project is a **Proof of Concept** demonstrating **Generative AI + Agentic AI** for automating
social support application decisions. It is built around the case study requirements of a government
social security department:contentReference[oaicite:0]{index=0}.

---

## 🎯 Objectives

- Automate up to **99%** of applicant assessments within minutes of live interaction.
- Support **multimodal data ingestion** (PDF, TXT, CSV).
- Provide **financial eligibility checks** (income, liabilities, credit score).
- Deliver **recommendations** (approve / soft decline, plus enablement opportunities).
- Demonstrate **Agentic AI orchestration** (retrieval, validation, decision).
- Showcase both **local ML/LLM** and the option to use **hosted LLMs** (Gemini, Groq, DeepSeek).

---

## 🏗️ Tech Stack

- **Python 3.11**
- **FastAPI** → backend API
- **Streamlit** → simple UI
- **Chroma** → local vector store
- **Sentence Transformers** → embeddings
- **Transformers / Ollama** → local models
- **LangGraph** → agent orchestration
- **scikit-learn** → eligibility checks (ML classifier)
- **LiteLLM (optional)** → access hosted LLMs (Gemini, Groq, DeepSeek)

---

## 📂 Project Structure
social-support-agent/  
├─ data/  
│ ├─ raw/  
│ │ ├─ pdfs/ # e.g., bank_statement_sample.pdf  
│ │ ├─ txt/ # resume_sample.txt, credit_report_sample.txt  
│ │ └─ excel/ # assets_liabilities_sample.csv  
│ └─ processed/  
├─ scripts/  
│ └─ ingest.sh # build Chroma index  
├─ src/  
│ ├─ api/ # FastAPI app  
│ ├─ agent/ # agent logic (retrieval + synthesis)  
│ ├─ retrieval/ # ingestion & query  
│ ├─ utils/ # financial parsing helpers  
│ └─ ui/ # optional Streamlit UI  
├─ tests/  
├─ README.md  
└─ requirements.txt  

---

## ⚡ Quickstart

### 1. Clone & setup
```bash
git clone <your-repo-url>
cd social-support-agent
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Add dummy data
Place your files:
- `data/raw/pdfs/bank_statement_sample.pdf`
- `data/raw/txt/resume_sample.txt`
- `data/raw/txt/credit_report_sample.txt`
- `data/raw/excel/assets_liabilities_sample.csv`

### 3. Build index
```bash
bash scripts/ingest.sh
```
