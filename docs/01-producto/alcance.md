# Alcance — Vecino Recomienda (borrador Checkpoint 1)
Dueño: agente | Fecha: 2026-11-06 (H2, hora Perú) | Estado: APROBADO por Pierre 2026-11-06

## Nombre de trabajo
Vecino Recomienda — directorio de proximidad con Visto Bueno Vecinal.

## Must (demostrable en 15 min sin fallar)
- Publicar un servicio en ≤3 clics (oficio + descripción + ubicación auto, sin auth pesada).
- Listado de servicios ordenado por distancia (Haversine, offline) con sello "✓ Visto bueno vecinal (n)".
- Recomendar un servicio (1 clic) y que el contador de visto bueno se incremente en vivo.
- Seed realista (gasfitería, carpintería, cerrajería, electricidad, clases) desde el minuto 1.
- Deploy público 200 antes de H4.

## Should (solo si el Must está verde)
- Mapa opcional online (Leaflet) con fallback automático a la lista.
- Ficha estática "grupo de apoyo en emergencia" demoable (sin motor de emergencias).
- Tutorial de 3 pasos en la landing.

## Won't (firmado)
- Auth completa / roles / moderación.
- Tiles de mapa offline.
- Motor completo de emergencias (tablero humanitario, reportes geolocalizados en vivo).
- Pagos, chat en vivo, notificaciones push.
- Cualquier feature que no se vea en la demo de 15 min.

## Acciones
- Decisiones de stack en spikes.md (FastAPI+SQLite, lista por defecto).
- Nueva idea = 2 votos + quitar otra cosa. Freeze H36.
