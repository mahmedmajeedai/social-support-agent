# src/agent/generate.py
import os

PROVIDER = os.getenv("LITELLM_PROVIDER", "local").strip().lower()
MODEL = os.getenv("LITELLM_MODEL", "distilgpt2")

# Lazy singletons
_litellm_ready = False
_local_pipe = None

def _ensure_litellm():
    global _litellm_ready
    if _litellm_ready:
        return True
    try:
        from litellm import completion  # noqa: F401
        _litellm_ready = True
        return True
    except Exception:
        return False

def _ensure_local_pipe():
    global _local_pipe
    if _local_pipe is None:
        from transformers import pipeline
        _local_pipe = pipeline("text-generation", model="distilgpt2")
    return _local_pipe

def generate(prompt: str, max_new_tokens: int = 250, temperature: float = 0.2) -> str:
    """
    Returns a concise, single-passage completion.
    Prefers hosted LLM via LiteLLM if configured, else falls back to tiny local HF.
    """
    if PROVIDER != "local" and _ensure_litellm():
        from litellm import completion
        resp = completion(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Be concise, factual, and grounded. Do not invent numbers."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_new_tokens,
        )
        return resp.choices[0].message.content.strip()

    # Local fallback (tiny CPU model). Keep it deterministic.
    pipe = _ensure_local_pipe()
    out = pipe(
        prompt,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        pad_token_id=50256,  # avoid warnings for GPT2 vocab
        eos_token_id=50256,
    )[0]["generated_text"]
    # return only continuation
    return out[len(prompt):].strip()
