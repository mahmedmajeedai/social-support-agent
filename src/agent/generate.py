from transformers import pipeline

# tiny, CPU-friendly fallback for PoC
_gen = pipeline("text-generation", model="distilgpt2")

def generate(prompt: str, max_new_tokens: int = 180) -> str:
    out = _gen(prompt, max_new_tokens=max_new_tokens, do_sample=False)[0]["generated_text"]
    # return only the new continuation
    return out[len(prompt):].strip()
