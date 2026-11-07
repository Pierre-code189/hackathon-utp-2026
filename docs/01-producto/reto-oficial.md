# Reto oficial — Hackathon UTP - El Comercio 2026

Fuente: 3 capturas de videollamada (Mario Cortijo, 19:09-19:12 hora Perú, 6 nov 2026). Los 3 videos enviados (20.1 MB, 59.2 MB, 42.4 MB) fueron rechazados por Telegram (>20 MB), por lo que NO hay audio/transcripción disponible. Este informe se basa solo en frames visibles.

## Transcripción literal

### Reto
- Crear en 48 horas un aplicativo que sirva a los ciudadanos para obtener con costos mínimos, y sin necesidad de transporte mayor, productos y servicios avalados por recomendaciones de vecinos. La aplicación debe integrar mecanismos de intercambios solidarios y evolucionar en situaciones de emergencia para coordinar soporte a los vecinos.

### Características funcionales (2 diapositivas, 10 bullets)
1. Función principal. Obtención de información recomendada sobre productos y servicios que se ofrecen cerca de la zona de residencia
2. Facilidad para promover servicios y compartir recomendaciones vecinales.
3. Facilidad para solicitar y ofrecer ayuda e intercambios solidarios entre vecinos.
4. Identificación de servicios y grupos de apoyo disponibles durante emergencias.
5. Coordinación de necesidades de ayuda y recursos entre vecinos en situaciones de emergencia.
6. Geolocalización de servicios, recursos y necesidades de apoyo.
7. Tutorial para usar la aplicación.
8. Enfoque móvil, con un máximo de tres clics para publicar.
9. Funcionalidad online y offline.
10. Uso intuitivo y accesible para cualquier vecino del barrio.

## Análisis

**Problema:** acceso a productos/servicios de proximidad sin transporte y sin confianza — se resuelve con recomendación vecinal verificable.
**Propuesta de valor:** "lo que necesitas a 3 cuadras, recomendado por tu vecino" + intercambio solidario (ayuda mutua sin dinero) + modo emergencia (coordinación en crisis).
**Usuarios:** vecinos del barrio (oferentes: venden/ofrecen servicios; demandantes: buscan; adultos mayores como usuarios críticos por "accesible para cualquier vecino").
**Flujo demo mínimo:** publicar en ≤3 clics → ver mapa/listado geolocalizado → filtrar por recomendado → contactar/ofertar ayuda → activar emergencia.
**Requisitos duros extraídos:** móvil primero, ≥3 clics para publicar, online+offline, geolocalización, tutorial, accesibilidad.
**Riesgos técnicos (candidatos a spike):** geolocalización/mapas offline, accesibilidad + offline en FastAPI+SQLite, confianza/recomendaciones.
**Riesgo de alcance:** el reto pide DOS productos en uno (mercado local + emergencias). La demo de 15 min solo puede mostrar uno bien.

## Video clip (6s, 19:23)
Archivo: video_b577c828e40e.mp4 — 576x1280, 1.6 MB, 5.96s. Frames extraídos con ffmpeg (fps=1, 6 frames). Audio extraído a 16kHz mono y transcripto con faster-whisper small (es, prob 1.0).

**Frames (f01-f06):** videollamada vertical, sin diapositiva visible. Arriba: Leandro Mairátegui (hombre mayor, calvo, gafas, polo gris, mirando abajo). Abajo: mujer de la UTP (cabello largo oscuro, gafas, blusa negra) con borde verde = hablante activo. Logo parcial HA/UTP en ambos. Banner: "Grabando la llamada. Proteja su privacidad y la de otras personas...". Estado 19:23, 4G. Ningún frame cambia de escena: todo el clip es la misma conversación.

**Audio (único segmento 0.0-5.8s):** "Lo vamos a pasar también por el canal de teams en unos minutos para que..." — frase incompleta, logística de difusión, sin contenido del reto.

**Conclusión del clip:** no aporta requisitos nuevos. Solo confirma la sesión en curso (Leandro + UTP) y que la grabación se difundirá por Teams.
