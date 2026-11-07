# Reporte de verificación — Core MVP (verificado 2026-11-06 20:05 hora Perú)
## Evidencia propia
- pytest -q → 5 passed (health, listado seed+orden, publicar+recomendar, 404 real).
- GET /health → 200. GET / → 200. curl grep: "Tutorial rápido", "En emergencia", "Ver mapa (opcional)" presentes.
- GET /api/servicios → 5 seed ordenados (Cerrajería 0.16 km ✓). POST /99999/recomendar → 404 (no 200 maquillado).
## Límite honesto
- Mapa es opcional online (Leaflet CDN); sin internet el fallback es la lista ordenada — verificado por código (typeof L === 'undefined' → mensaje offline), no con DevTools offline.
- Ficha de emergencia es estática/informativa por diseño (Won't firmado).
- Captura 390px pendiente de revisión visual completa en el próximo paso (H28 estabilizar).
