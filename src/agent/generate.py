# src/agent/generate.py
import os
import re

PROVIDER = os.getenv("LITELLM_PROVIDER", "local").strip().lower()
MODEL = os.getenv("LITELLM_MODEL", "distilgpt2")

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

def _postprocess(text: str) -> str:
    # Remove duplicate consecutive lines / phrases (e.g., "No code fences." loops)
    # 1) collapse repeated lines
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    deduped = []
    for ln in lines:
        if not deduped or ln != deduped[-1]:
            deduped.append(ln)
    text = " ".join(deduped)

    # 2) collapse repeated short fragments (like "No code fences.")
    text = re.sub(r"(?:\b([A-Z][^.!?]{0,40})[.!?]\s*){3,}", r"\1.", text)

    # 3) strip stray bullets / prefixes
    text = re.sub(r"^\s*[-•]\s*", "", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text

def generate(prompt: str, max_new_tokens: int = 220, temperature: float = 0.2) -> str:
    """
    Uses hosted LLM via LiteLLM if configured; otherwise falls back to tiny local HF model.
    Returns a concise continuation; post-process to remove loops.
    """
    if PROVIDER != "local" and _ensure_litellm():
        from litellm import completion
        resp = completion(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Return a SINGLE short paragraph in plain text. Be concise, factual, grounded."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_new_tokens,
            # stop tokens help avoid trailing formatting
            stop=["```", "---", "#"],
        )
        return _postprocess(resp.choices[0].message.content or "")

    pipe = _ensure_local_pipe()
    out = pipe(
        prompt,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        pad_token_id=50256,
        eos_token_id=50256,
    )[0]["generated_text"]
    return _postprocess(out[len(prompt):])
