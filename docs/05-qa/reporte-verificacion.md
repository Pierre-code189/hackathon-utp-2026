# Reporte de verificación — esqueleto 2026-11-06
- GET https://hackathon.apioai.online/health → 200 {"status":"ok"} (verificado por curl)
- GET https://hackathon.apioai.online/api/hello → 200 (verificado)
- GET https://hackathon.apioai.online/ → 200 HTML frontend (verificado)
- pytest -q (tests/test_health.py) → 2 passed
- systemctl hackathon.service → active, puerto 127.0.0.1:8003
- TLS Let's Encrypt válido hasta 2027-02-04
