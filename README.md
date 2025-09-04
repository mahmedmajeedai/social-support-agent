# Social Support Agent

This project is demonstrating **Generative AI + Agentic AI** for automating social support application decisions. It is built around the case study requirements of a government social security department.

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
│ │ ├─ pdfs/ 
│ │ ├─ txt/  
│ │ └─ excel/   
│ └─ processed/  
├─ scripts/  
│ └─ ingest.sh   
├─ src/  
│ ├─ api/ 
│ ├─ agent/   
│ ├─ retrieval/   
│ ├─ utils/ 
│ └─ ui/ # 
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
### 4. Run API
```bash
uvicorn src.api.app:app --reload --port 8000
```