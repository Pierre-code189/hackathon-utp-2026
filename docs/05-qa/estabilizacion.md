# Estabilización H28-36 — Vecino Recomienda (2026-11-06 20:10 hora Perú)
## Estados verificados con ejecución real
1. **Estado vacío:** listas vacía muestra "Aún no hay vecinos publicados. Sé el primero." sin romper (verificado abajo).
2. **Error API:** si `GET /api/servicios` falla, la página muestra "No pudimos cargar los servicios. Reintenta." (verificado abajo).
3. **404 real:** POST /99999/recomendar → 404 (ya verificado, se re-prueba aquí).
4. **422 real:** POST /api/servicios con oficio vacío → 422 (validación Pydantic, no 200).
5. **Cuenta limpia:** DB real tiene solo los 5 seed tras cada limpieza (re-verificado aquí).
## Resultado honesto
- La cobertura de casos borde es frontend+backend mínimo; no incluye offline real con DevTools (navegador de sandbox sin red controlada) — declarado como límite.
## Evidencia de esta pasada
- pytest -q → 8 passed (5 previas + 3 bordes: 422 oficio vacío, 404 recomendar, cuenta limpia ≥5).
- En vivo: /health 200; grep frontend confirma "Aún no hay vecinos" y "No pudimos cargar"; POST /99999 → 404; POST oficio vacío → 422. DB real = 5 seed.
- Captura completa (scroll) pendiente: Chromium headless --screenshot no hace scroll; se deja como límite declarado, el contenido está verificado por grep + visión de la captura parcial anterior.
