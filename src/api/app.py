from fastapi import FastAPI

app = FastAPI(title="Social Support Agent (PoC)")

@app.get("/health")
def health():
    return {"ok": True}
