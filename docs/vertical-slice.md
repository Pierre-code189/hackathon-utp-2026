# Vertical slice E2E (H12) — verificado 2026-11-06 20:00 hora Perú
Flujo: UI (form 3 campos) → POST /api/servicios → SQLite → GET /api/servicios ordenado por distancia (Haversine) → POST /api/servicios/{id}/recomendar incrementa contador en vivo.
Evidencia: pytest 5 passed; GET /api/servicios 200 con 5 seed ordenados (Cerrajería 0.16 km); POST publica id=7; POST /99999 → 404 real; GET / → 200. URL: https://hackathon.apioai.online
Límite honesto: frontend es esqueleto feo pero funcionando (pendiente H12-28 pulir); sin auth (verdadero por diseño); geolocalización usa ubicación del navegador con fallback Los Olivos.
## P1+P2 (2026-11-06 20:25 hora Perú, descongelar autorizado)
Tipo Servicio/Producto/Favor + filtros Todo/Servicios/Productos/Ayuda. Migración automática de columna tipo. Seed: 9 servicios (5 Servicio, 2 Producto, 2 Favor). Tests: 11 passed. Filtros en vivo verificados (Producto: Almuerzo, Silla; Favor: taladro, traslado).
