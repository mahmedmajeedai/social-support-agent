# src/agent/generate.py
import os
import json
import requests

# Env knobs
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b-instruct")

def _ollama_generate(prompt: str, max_new_tokens: int = 256, temperature: float = 0.1) -> str:
    """
    Calls local Ollama /api/generate (non-stream) and returns the full response text.
    """
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "options": {
            "temperature": temperature,
            "num_predict": max_new_tokens
        },
        "stream": False
    }
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    # /api/generate returns single JSON with "response"
    return data.get("response", "").strip()

def generate(prompt: str, max_new_tokens: int = 256, temperature: float = 0.1) -> str:
    """
    Single entry point used by the agent. Currently routes to Ollama.
    """
    return _ollama_generate(prompt, max_new_tokens=max_new_tokens, temperature=temperature)
