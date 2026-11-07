# Auditoría 3 frentes — 2026-11-06 22:00 hora Perú (backend + frontend + operación, subagentes independientes)
## Backend (QA escéptico, 31 casos)
PASS: health/listado/orden, filtros simples, 404/422/SQLi, asignar/listar, /static sin leak.
Ajustes pendientes (no bloquean demo, sí producción):
- POST tipo/accion inválidos → coerce silencioso (422 esperado).
- Sin validación geo ni max_length; stored-XSS persistido crudo.
- ?vulnerable + ?tipo: tipo ignorado (precedencia silenciosa).
- Recomendar: barrio vacío ("") sin zona pero suma global; aval externo infla vistos.
- Asignaciones: self (1,1) y duplicadas aceptadas 200.
- Servicios expuestos con teléfono sin auth.
## Frontend vs backend
(ver informe del subagente) Bugs de lógica/estado por corregir antes de sustentar.
## Operación
(ver informe del subagente) Limpieza de filas QA en DB prod.
## Síntesis solicitada al lector
Priorizar fix: filtro combinado, validación geo, max_length, sanitize XSS, auth/rate-limit, fuga telefono.
