# Hackathon UTP - El Comercio 2026

Esqueleto listo. Sin tema aún — no codificar el reto hasta spike + alcance (sdlc-master Checkpoint 1).

## Stack
FastAPI + vanilla JS + SQLite + Nginx/systemd en VPS.

## Cómo correr
```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8003
```
## URL
https://hackathon.apioai.online (puerto 8003 local)

## Docs
- docs/01-producto/alcance.md
- docs/02-arquitectura/api.md
- docs/05-qa/reporte-verificacion.md
- docs/06-devops/despliegue.md
