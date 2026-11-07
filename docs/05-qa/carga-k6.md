# Carga k6 — hackathon.apioai.online (Etapa 6 sdlc-master)

**Dueño:** QA / Pierre · **Fecha:** 2026-11-06 (America/Lima) · **Pregunta:** ¿cuántos usuarios aguanta hoy hackathon.apioai.online?

## Herramienta

- `k6 v1.1.0 (commit/0e3fb953be, go1.24.4, linux/amd64)` en `/usr/local/bin/k6`
- Script: `k6/health.js` → `GET https://hackathon.apioai.online/health`
- Stages: 30s→50 VUs, 30s→200 VUs, 30s→500 VUs, 30s→0 VUs (duración total 2m00s)
- Checks: status 200, body contiene `"ok"`
- Thresholds: `http_req_duration p(95)<500ms`, `http_req_failed rate<1%`
- Solo infraestructura propia (hackathon, puerto 8003). VPA (8000) no tocado.

## Resultado — corrida 2026-11-06 08:00–08:02 (reproducible)

| Métrica | Valor real |
|---|---|
| Exit code | **99** (`thresholds on metrics 'http_req_duration' have been crossed`) |
| VUs máximos alcanzados | **499** (`vus_max=500`, `vus min=2 max=499`) |
| Requests totales | **101,910** (849.24/s) |
| Checks | 203,820 totales · 100.00% OK · 0 fallidos |
| `% fallos` (`http_req_failed`) | **0.00%** (0/101,910) — threshold `<1%` ✓ |
| `http_req_duration` avg | **221.02 ms** |
| `http_req_duration` med (p50) | **190.57 ms** |
| `http_req_duration` p90 | **465.52 ms** |
| `http_req_duration` p95 | **510.03 ms** — threshold `<500ms` ✗ |
| `http_req_duration` max | 725.2 ms · min 903 µs |
| Threshold p95 | **✗ FAIL** |
| Threshold fallos | **✓ PASS** |

Corrida anterior el mismo día (07:52): p95=526.65ms, avg=208.89ms, p90=469.2ms, 107,813 requests, 0% fallos, exit 99. El fallo de p95 es reproducible, no un pico aislado.

Salida completa: `k6/health-run-20261106-080021.log` (+ `k6/health-run.log` de la corrida anterior).
Monitoreo VPS: `k6/vps-monitor-20261106-080021.log`.

## VPS durante la prueba (muestreo cada 2s, 60 muestras)

| Recurso | Máximo observado | Capacidad | ¿Cuello? |
|---|---|---|---|
| Load average (8 cores) | **4.05** | 8.0 | No saturado |
| RAM usada | **1,824 MB** | 24,031 MB | No |

El cuello **no es CPU/RAM del VPS**. Es la aplicación: `hackathon.service` corre
`uvicorn backend.main:app --host 127.0.0.1 --port 8003` **sin `--workers`** = 1 solo worker
(proceso PID 215433). Con 1 worker, a 400–500 VUs el p90/p95 sube por encima de 500ms aunque el VPS tenga load 4/8 y RAM libre.

## Segundo script

`k6/flujo.js` (100 VUs, `/` + `/api/hello`) **no ejecutado**: la tarea y la skill exigen correrlo solo si `/health` pasa thresholds. Como `/health` falló (exit 99), no se corrió.

## Conclusión: ¿cuántos usuarios aguanta?

- **Sin errores hasta 500 VUs:** 0% fallos, 100% checks OK, avg ~220ms. El servicio no se cayó en ningún momento.
- **Con thresholds estrictos (p95<500ms): no pasa a 500 VUs** (p95=510–527ms en dos corridas). p90=465–469ms sí está bajo 500ms, así que el cruce ocurre en la cola alta (p90–p95) durante el stage de 500 VUs.
- **Estimación honesta:** aguanta ~500 VUs sin fallos, pero para cumplir p95<500ms haría falta bajar el pico a ~200–300 VUs o, mejor, subir workers: `uvicorn ... --workers 4` (hay CPU/RAM de sobra: load máx 4.05/8, RAM 1.8/24 GB). Sin ese cambio, declarar "500 usuarios OK" sería falso contra el threshold fijado.
- **Estado post-prueba:** `hackathon` active, `vpa` active (no tocado), `GET /health` → 200 `{"status":"ok"}`. No hizo falta `systemctl restart hackathon`.

## Evidencia / defectos (Etapa 6)

| Defecto | Ubicación | Severidad | Estado |
|---|---|---|---|
| p95>500ms a 500 VUs con 1 worker uvicorn | `hackathon.service` ExecStart, puerto 8003 | medio | abierto (documentado, no bloquea demo liviana) |
| Thresholds no cumplidos → `flujo.js` sin correr | `k6/health.js` exit 99 | medio | abierto |

*Sin reporte en disco la etapa no pasó (sdlc-master § Sistema de documentación). Este archivo es el artefacto de Etapa 6 para carga.*
