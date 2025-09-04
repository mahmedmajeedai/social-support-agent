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

