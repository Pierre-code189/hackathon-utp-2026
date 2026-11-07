# Verificación funcional — 2026-11-06 21:50 hora Perú (evidencia propia)
## Tabla de funciones (curl + grep contra URL pública, no auto-aseguración)
- Health / frontend: 200 / 200 ✓
- Listado orden por distancia: ascendente OK, 13 registros ✓
- Filtros: Servicio 6, Producto 2, Favor 2, Emergencia 3 ✓
- Demanda (Solicita): Se necesita gasfitería + Traslado adulto mayor ✓
- Emergencia + vulnerable: 3 grupos/servicios + 1 vulnerable ✓
- WhatsApp: 6 con teléfono ✓
- Zona del aval: misma zona → vistos_zona=1; otra zona → vistos sube, zona NO (vistos 6→7, zona 1→1) ✓
- Asignaciones: crear/listar OK; 404 si no existe ✓
- Errores: 404 servicio, 422 oficio vacío, 404 asignación ✓
- Frontend markers: Modo simple, Modo:Emergencia, Se necesita, Tablero, Tutorial, Visto bueno, WhatsApp ✓
- Tests: 15 passed ✓
## Bug conocido declarado
El botón "Asignar recurso" del frontend toma el primer no-Solicita sin excluir el propio id → puede asignarse taladro→taladro. En esta verificación se observó (id 4). No rompe la demo (sigue listando), pero queda marcado para corregir antes de la sustentación.
## Límite
Sin prueba en teléfono real ni con adultos mayores; capturas 390px sí revisadas.
## Bug filtro UI (reportado por Pierre, confirmado 2026-11-06 21:55)
- Causa: `filtrar()` guarda FILTRO pero `cargar()` hacia fetch sin `&tipo=` (la URL con FILTRO se habia perdido al extraer pintar()). Backend si filtraba (curl tipo=Producto OK), la UI siempre mostraba Todo.
- Fix: URL = `/api/servicios?lat&lng` + (FILTRO?`&tipo=...`:'') en cargar(). Tests 15 passed, frontend 200.
- Correccion del bug conocido de autoasignacion (taladro->taladro): se corrige en la misma pasada (filtrar recurso excluyendo el propio id).
## Fixes 2026-11-06 22:15 (post-auditoria, sin codigo roto)
Backend: 422 geo/tipo/accion, max_length, html.escape al guardar, ?vulnerable+tipo=AND, barrio vacio consistente (default), asignaciones self 422 y duplicada 409.
Frontend: esc() en innerHTML, asignar() con fetch a favores reales + excluye self + solo Solicita, recomendar con barrio explicito, reset telefono/vulnerable, WhatsApp normalizado 51, ficha emergencia con datos reales.
Telefono en listado: se mantiene visible por requisito de WhatsApp en demo (riesgo aceptado en hackathon, sin auth). Auth/rate-limit queda deuda pre-produccion.
Verificacion: curl geo 422 + tipo 422 + XSS escapado, autoasign 422, dup 409. Tests 15 passed.
## Auditoría 5 frentes + cierre (2026-11-06 23:05 hora Perú)
QA encontró: vulnerable=false ignorado, geo GET sin rango, asignacion invertida aceptada, seed Emergencia vacio en BD limpia, etc.
Cierre aplicado:
- DB real restaurada a seed limpio: 13 servicios (vistos originales), 0 recomendaciones, 0 asignaciones. QA ids borrados (27-39), alerta de prueba borrada.
- Seed ampliado en backend/main.py: 13 registros (incluye 3 Emergencia + Demanda) -> BD limpia ya no queda vacia en Emergencia (verificado /tmp/seed_test.db: 3).
- Fix vulnerable: param None (sin param=todos), true=1, false=no-vuln; combinado tipo+vuln = AND. Verificado en vivo: tipo=Favor 2, vuln=true 1, vuln=false 12 (0 vuln dentro), sin param 13.
- Tests 15 passed.
Pendiente post-demo (no bloqueante): geo GET 422, asignacion roles Solicita->Ofrece, auth/rate-limit, OpenAPI docs.
