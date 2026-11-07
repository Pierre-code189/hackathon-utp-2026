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
## Parte B (2026-11-06 22:30 hora Perú)
Boton "Emitir alerta con mi ubicacion": POST /api/servicios con tipo=Emergencia, vulnerable=1, accion=Solicita, lat/lng automaticas (geoloc navegador, fallback Los Olivos). Backend sin cambios (endpoint ya soportaba vulnerable+tipo). Verificado en vivo: 1 clic crea alerta y aparece en ?vulnerable=1 junto al traslado. Prueba limpiada despues.
## Parte C (2026-11-06 22:40 hora Perú)
Seccion "Recursos criticos (economia solidaria)": lista tipo=Emergencia (3 recursos: atencion medica, primeros auxilios, red de agua/alimentos) con estado Disponible/Ocupado derivado de GET /api/asignaciones (sin backend nuevo). Verificado en vivo: 3 recursos listados, asignaciones=0 => todo Disponible. Residuo de pruebas limpiado.
## Diseño color (2026-11-06 22:50 hora Perú)
Tokens: confianza #1B8A5A (servicio/sello), solicita #5B8DEF, ofrece #8B5CF6, emergencia #D32F2F, aviso #F9A825. Tarjetas con borde izquierdo por tipo + badges b-Servicio/b-Producto/b-Favor/b-Emergencia y Solicita/Ofrece. Boton alerta btn-alerta rojo. Captura 390px revisada.
## Modulo 1 completado (2026-11-07 01:20 hora Peru)
categoria/stock/precio/estado + reportes/moderacion con codigo admin. Frontend: tarjeta con categoria/stock/precio, detalle con mapa y Reportar/Volver.
## Módulos 2-3 (2026-11-07 01:40 hora Perú)
Mod2 Solidaria: details con Favor (ofrece/solicita) + distancia. Mod3 Emergencias: grupos tipo Emergencia + /api/noticias con 3 fuentes oficiales (INDECI/SENAMHI) (no scraping privado). 15 passed.
