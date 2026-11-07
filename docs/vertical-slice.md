# Vertical slice E2E (H12) — verificado 2026-11-06 20:00 hora Perú
Flujo: UI (form 3 campos) → POST /api/servicios → SQLite → GET /api/servicios ordenado por distancia (Haversine) → POST /api/servicios/{id}/recomendar incrementa contador en vivo.
Evidencia: pytest 5 passed; GET /api/servicios 200 con 5 seed ordenados (Cerrajería 0.16 km); POST publica id=7; POST /99999 → 404 real; GET / → 200. URL: https://hackathon.apioai.online
Límite honesto: frontend es esqueleto feo pero funcionando (pendiente H12-28 pulir); sin auth (verdadero por diseño); geolocalización usa ubicación del navegador con fallback Los Olivos.
## P1+P2 (2026-11-06 20:25 hora Perú, descongelar autorizado)
Tipo Servicio/Producto/Favor + filtros Todo/Servicios/Productos/Ayuda. Migración automática de columna tipo. Seed: 9 servicios (5 Servicio, 2 Producto, 2 Favor). Tests: 11 passed. Filtros en vivo verificados (Producto: Almuerzo, Silla; Favor: taladro, traslado).
## P3-P5 (2026-11-06 20:35 hora Perú, autorizado "Procede")
Emergencia como tipo con sello y filtro (2 grupos seed), marcador ⚠ Vulnerabilidad, teléfono opcional + enlace WhatsApp (wa.me), accesibilidad (base 16px, botones ≥44px, Modo simple). Backend: columnas telefono/vulnerable con migración. Tests: 13 passed. Vivo: ?tipo=Emergencia → 2 grupos ✓; vulnerable=WARN ✓; WA aparece en grep del frontend ✓.
## Partes 1-2 (2026-11-06 20:50 hora Perú)
Zona del aval: tabla recomendaciones(barrio); POST recomendar acepta barrio (default Los Olivos) y devuelve vistos_zona; el badge ahora es zone-aware en backend. Solicita/Ofrece: columna accion + selector en formulario + etiqueta en tarjeta; traslado adulto mayor = Solicita. Tests: 14 passed. Vivo: Favor → Solicita/Ofrece ✓; recomendar misma zona → vistos_zona=1 ✓.
## Partes 3-4 (2026-11-06 21:00 hora Perú)
Tablero: GET /api/servicios?vulnerable=1 → lista vulnerable (traslado adulto mayor). Coordinar: POST/GET /api/asignaciones (necesidad_id, recurso_id) con 404 si no existen; frontend con sección desplegable y botón Asignar recurso. Tests: 15 passed. Vivo: asignar 12→11 OK y listado OK; limpieza posterior a seed limpio.
## Offline (2026-11-06 21:10 hora Perú)
localStorage vr_cache: si fetch falla, se muestra la última lista guardada con aviso "Sin conexión: mostrando última lista guardada". Sin PWA (sin service worker/manifest): es límite declarado — la app se abre sin red pero no sincroniza favores offline. Verificado por grep + tests 15 passed (backend intacto).
## Parte A (2026-11-06 21:30 hora Perú)
Demanda de oficio: seed "Se necesita gasfitería" (Servicio+Solicita, día a día); tarjeta muestra "Se necesita" cuando accion=Solicita.Separación de modos: etiqueta Modo: Día a día (Servicio/Producto/Favor) vs Modo: Emergencia (Emergencia) + seed "Atención médica 24h (emergencia)" dentro de Emergencia junto a los grupos. Tests 15 passed. Vivo: Solicita incluye demanda ✓, Emergencia = 3 registros ✓. Datos de prueba "Abc" eliminados.
