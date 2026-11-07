# Spikes H0-2 — 2 riesgos técnicos
Fecha: 2026-11-06 (H0, hora Perú) | Método: prueba mínima throwaway en /root/.hermes/cache/scratch/spike*.py, sin tocar backend/

## Spike 1 (30 min) — Publicación en ≤3 clics + Visto Bueno Vecinal
- Prueba: SQLite en memoria con tablas vecinos/servicios/recomendaciones; seed gasfitería con 1 recomendación real; query filtra HAVING COUNT>=1.
- **Resultado: PASA.** `servicios con visto bueno: [('Gasfiteria', ..., 1)]`. El filtro de confianza es una query trivial; el flujo cabe en 1 pantalla y 3 campos (oficio, descripción, ubicación auto).
- Decisión: sin auth en el slice; vecino = nombre + barrio + auto-ubicación. La publicación es INSERT + 1 recomendación = 2 operaciones, compatible con ≤3 clics.

## Spike 2 (30 min) — Geolocalización + offline
- Prueba: Haversine en Python ordena 3 servicios por distancia sin red: Cerrajero 0.16 km, Gasfitería 0.24 km, Carpintería 1.73 km. Correcto.
- **Resultado: PASA con recorte.** Ordenar por distancia es gratis y offline. El mapa con tiles (Leaflet/OSM) NO es offline sin caché pesada: se decide **lista ordenada por distancia como vista por defecto** + mapa opcional online con fallback a la lista. Así cumplimos "online y offline" sin depender de red en la demo.
- Decisión de stack: FastAPI + vanilla JS + SQLite (ya en venv, domina el equipo, 1 deploy). Next+Supabase implicaría segundo deploy/CORS y aprendizaje en 48h: se rechaza en este spike.

## Consecuencia en alcance
- Must = directorio + visto bueno + publicación 3 clics (sin mapa de tiles obligatorio).
- Should = mapa opcional online + tutorial.
- Won't = tiles offline, auth completa, motor de emergencias completo.
