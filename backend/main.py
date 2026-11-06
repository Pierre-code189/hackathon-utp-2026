from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="Hackathon UTP - El Comercio 2026", version="0.0.1")

@app.get("/health")
def health():
    return {"status": "ok", "service": "hackathon-utp-2026"}

@app.get("/api/hello")
def hello():
    return {"message": "Hackathon UTP - El Comercio 2026 — esqueleto listo. Falta el tema.", "status": "skeleton"}

# Servir frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_dir, "static")), name="static")

    @app.get("/")
    def root():
        idx = os.path.join(frontend_dir, "index.html")
        return FileResponse(idx)
