# Pre-mortem — H0 (2026-11-06, hora Perú)
Dueño: agente (todos los roles asumidos por ahora) | Estado: propuesto, pendiente equipo

## 8 modos de fallo
1. Demo cae en vivo (red/mapa externo caído, sin fallback).
2. Scope creep: intentamos mercado + emergencias completas y dejamos ambos a medias.
3. "Visto Bueno Vecinal" no se entiende en 30 s; el jurado lo ve como directorio común.
4. Publicación >3 clics o con auth pesada; el jurado no logra publicar en la demo.
5. Offline de juguete (solo caché de página, datos no disponibles sin red).
6. Datos inventados / seed vacío en vivo; el mapa se ve vacío.
7. Estética antes que estructura; se pierde H12 sin slice E2E.
8. Manejo del tiempo: 15 min exactos + 5 Q&A sin ensayo; nos cortan a mitad.

## Top 3 + plan B
1. **Demo cae (modo 1)** — Dueño: agente. Plan B: video respaldo ≥720p antes del freeze H36 + seed local + lista ordenada por distancia sin tiles como vista por defecto; mapa solo como capa opcional con fallback.
2. **Doble producto (modo 2)** — Dueño: agente. Plan B: Must = mercado local + Visto Bueno (demo 15 min). Emergency = solo ficha estática demoable, no motor completo.
3. **Visto Bueno no se entiende (modo 3)** — Dueño: agente. Plan B: el sello "✓ Visto bueno vecinal (n vecinos lo recomiendan)" siempre visible junto al oficio + ejemplo cerrajero en el guión 90s (H6).

## Pregunta de control cada 6h
¿Esto se ve en la demo? Si no, no se hace ahora.
