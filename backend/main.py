from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os, sqlite3, math, time

app = FastAPI(title="Vecino Recomienda — Hackathon UTP 2026", version="0.1.0-slice")

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DB_PATH = os.environ.get("DB_PATH", os.path.join(DATA_DIR, "hackathon.db"))

def get_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript("""
CREATE TABLE IF NOT EXISTS servicios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  oficio TEXT NOT NULL,
  descripcion TEXT NOT NULL,
  vecino TEXT NOT NULL,
  barrio TEXT,
  lat REAL, lng REAL,
  vistos INTEGER DEFAULT 0,
  creado REAL DEFAULT 0
);
""")
    return conn

SEED = [
  ("Gasfitería", "Destapo y reparo fugas", "Juan Quispe", "Los Olivos", -11.982, -77.070, 3),
  ("Carpintería", "Muebles a medida, reparaciones", "Rosa Pinedo", "Los Olivos", -11.995, -77.065, 2),
  ("Cerrajería", "Aperturas 24h, cambios de chapa", "Luis Torres", "Los Olivos", -11.980, -77.073, 5),
  ("Electricidad", "Instalaciones y reparaciones", "Pedro Díaz", "Los Olivos", -11.978, -77.068, 1),
  ("Clases de matemática", "Refuerzo escolar 1.° a 5.° secundaria", "Ana López", "Los Olivos", -11.990, -77.075, 4),
]

def seed_if_empty():
    conn = get_db()
    n = conn.execute("SELECT COUNT(*) FROM servicios").fetchone()[0]
    if n == 0:
        conn.executemany("INSERT INTO servicios (oficio,descripcion,vecino,barrio,lat,lng,vistos,creado) VALUES (?,?,?,?,?,?,?,?)",
            [(o,d,v,b,la,ln,vi,time.time()) for o,d,v,b,la,ln,vi in SEED])
        conn.commit()
    conn.close()

seed_if_empty()

def haversine(lat1, lng1, lat2, lng2):
    R = 6371.0; p = math.pi/180
    a = math.sin((lat2-lat1)*p/2)**2 + math.cos(lat1*p)*math.cos(lat2*p)*math.sin((lng2-lng1)*p/2)**2
    return 2*R*math.asin(math.sqrt(a))

class NuevoServicio(BaseModel):
    oficio: str
    descripcion: str
    vecino: str
    barrio: str = ""
    lat: float = -11.981
    lng: float = -77.072

@app.get("/health")
def health():
    return {"status": "ok", "service": "vecino-recomienda"}

@app.get("/api/hello")
def hello():
    return {"message": "Vecino Recomienda — esqueleto listo.", "status": "skeleton"}

@app.get("/api/servicios")
def listar(lat: float = -11.981, lng: float = -77.072):
    conn = get_db()
    rows = conn.execute("SELECT * FROM servicios ORDER BY creado DESC").fetchall()
    conn.close()
    out = []
    for r in rows:
        d = round(haversine(lat, lng, r["lat"] or lat, r["lng"] or lng), 2)
        out.append({**dict(r), "distancia_km": d, "visto_bueno": r["vistos"] >= 1})
    out.sort(key=lambda x: x["distancia_km"])
    return out

@app.post("/api/servicios")
def crear(s: NuevoServicio):
    if not s.oficio.strip() or not s.descripcion.strip():
        raise HTTPException(status_code=422, detail="oficio y descripcion son obligatorios")
    conn = get_db()
    cur = conn.execute("INSERT INTO servicios (oficio,descripcion,vecino,barrio,lat,lng,vistos,creado) VALUES (?,?,?,?,?,?,0,?)",
        (s.oficio.strip(), s.descripcion.strip(), s.vecino.strip() or "Vecino", s.barrio.strip(), s.lat, s.lng, time.time()))
    conn.commit(); conn.close()
    return {"id": cur.lastrowid, "oficio": s.oficio}

@app.post("/api/servicios/{sid}/recomendar")
def recomendar(sid: int):
    conn = get_db()
    row = conn.execute("SELECT vistos FROM servicios WHERE id=?", (sid,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="servicio no encontrado")
    conn.execute("UPDATE servicios SET vistos = vistos + 1 WHERE id=?", (sid,))
    conn.commit()
    n = conn.execute("SELECT vistos FROM servicios WHERE id=?", (sid,)).fetchone()[0]
    conn.close()
    return {"id": sid, "vistos": n}

frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_dir, "static")), name="static")
    @app.get("/")
    def root():
        return FileResponse(os.path.join(frontend_dir, "index.html"))
