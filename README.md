# Vecino Recomienda — Hackathon UTP · El Comercio 2026

## Demo
**URL pública:** https://hackathon.apioai.online
**Estado:** MVP desplegado y verificado (13 tests verdes, 11 servicios seed geolocalizados, /health 200).
**Video respaldo:** prototipo 720p en `docs/demo-video/respaldo-90s-prototipo.mp4` — la versión final 2-3 min con narración real queda pendiente de grabación por el equipo.

## 1. Inspiration
Falta de acceso, sin transporte y sin confianza a productos y servicios de proximidad. En el barrio nadie sabe quién ofrece qué, ni quién ya lo probó. "Lo que necesitas a 3 cuadras, con el visto bueno de quien ya lo probó."

## 2. What it does
- Directorio de proximidad: Servicios, Productos, Favores y grupos de Emergencia, ordenado por distancia (Haversine, offline).
- Publicación en ≤3 clics, sin registro pesado.
- **Visto Bueno Vecinal**: contador de recomendaciones visibles por servicio.
- Muro solidario: solicitar/ofrecer favores sin dinero.
- Emergencia consultable: grupos de apoyo + marcador de vulnerabilidad.
- Contacto por WhatsApp (opcional), tutorial de 1 min y modo simple accesible.

## 3. How we built it
FastAPI + vanilla JS + SQLite en un VPS (Nginx + systemd, puerto 8003). Geolocalización por navegador con fallback a Los Olivos; lista ordenada por distancia como vista por defecto y mapa Leaflet/OSM opcional con fallback a la lista (sin tiles offline). Flujo en 48 h: pre-mortem → spike vinculante (2 riesgos) → alcance con Checkpoints → vertical slice H12 → Core MVP → estabilización → freeze H36 (docs en `docs/`).

## 4. Challenges
- El reto pide dos productos (mercado + emergencias): recortado en el spike — Must = mercado con visto bueno; emergencias = grupo consultable, no motor completo.
- Geolocalización + offline real: resuelto con Haversine sin red; mapa con tiles requiere internet y queda como capa opcional.
- Cumplir ≤3 clics para publicar sin auth: flujo sin login, solo nombre + ubicación.

## 5. Accomplishments
- 11 servicios seed (Servicios, Productos, Favores, Emergencia) geolocalizados.
- Filtros por tipo, visto bueno con contador en vivo, 422/404 reales, estados vacío/error.
- Corrección de bug de conteo de parámetros SQL detectada por tests en esta pasada (13 passed).

## 6. What we learned
- La lista ordenada por distancia sustituye al mapa como vista principal en offline; el mapa es decoración si bloquea la demo.
- Un solo flujo E2E sólido rinde más que diez módulos a medias para un jurado.
- Sin evidencia en disco (tests, curl, capturas), no hay checkpoint superado.

## 7. What's next
- Video final con narración y ensayos en vivo 3x cronometrados.
- Sin reglas de comité: atribución de visto bueno y moderación. Tablero humanitario completo (fase 2, fuera del scope del hackathon).

## Cómo correr
```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8003
```
Test: `.venv/bin/python -m pytest -q`
