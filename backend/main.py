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
  creado REAL DEFAULT 0,
  tipo TEXT DEFAULT 'Servicio',
  telefono TEXT,
  vulnerable INTEGER DEFAULT 0,
  accion TEXT DEFAULT 'Ofrece'
);
CREATE TABLE IF NOT EXISTS recomendaciones (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  servicio_id INTEGER NOT NULL,
  barrio TEXT,
  creado REAL DEFAULT 0
);
""")
    cols=[r[1] for r in conn.execute("PRAGMA table_info(servicios)").fetchall()]
    if "tipo" not in cols:
        conn.execute("ALTER TABLE servicios ADD COLUMN tipo TEXT DEFAULT 'Servicio'")
    if "telefono" not in cols:
        conn.execute("ALTER TABLE servicios ADD COLUMN telefono TEXT")
    if "accion" not in cols:
        conn.execute("ALTER TABLE servicios ADD COLUMN accion TEXT DEFAULT 'Ofrece'")
    if "vulnerable" not in cols:
        conn.execute("ALTER TABLE servicios ADD COLUMN vulnerable INTEGER DEFAULT 0")
    conn.commit()
    return conn

SEED = [
  ("Gasfitería", "Destapo y reparo fugas", "Juan Quispe", "Los Olivos", -11.982, -77.070, 3),
  ("Carpintería", "Muebles a medida, reparaciones", "Rosa Pinedo", "Los Olivos", -11.995, -77.065, 2),
  ("Cerrajería", "Aperturas 24h, cambios de chapa", "Luis Torres", "Los Olivos", -11.980, -77.073, 5),
  ("Electricidad", "Instalaciones y reparaciones", "Pedro Díaz", "Los Olivos", -11.978, -77.068, 1),
  ("Clases de matemática", "Refuerzo escolar 1.° a 5.° secundaria", "Ana López", "Los Olivos", -11.990, -77.075, 4),
  ("Almuerzo casero", "Plato del día + sopa, entrega a domicilio", "Carmen Vega", "Los Olivos", -11.983, -77.071, 2),
  ("Silla de ruedas", "Alquiler por días, trae a domicilio", "Miguel Ríos", "Los Olivos", -11.979, -77.074, 1),
  ("Préstamo de taladro", "Ofrezco taladro 2 h, recoger", "Diego Flores", "Los Olivos", -11.984, -77.066, 3),
  ("Ayuda traslado adulto mayor", "Necesito apoyo para trasladar a mi mamá a la posta", "Sofía Marín", "Los Olivos", -11.987, -77.072, 0),
]

def seed_if_empty():
    conn = get_db()
    n = conn.execute("SELECT COUNT(*) FROM servicios").fetchone()[0]
    if n == 0:
        conn.executemany("INSERT INTO servicios (oficio,descripcion,vecino,barrio,lat,lng,vistos,creado,tipo) VALUES (?,?,?,?,?,?,?,?,?)",
            [(o,d,v,b,la,ln,vi,time.time(),"Servicio" if i<5 else ("Producto" if i<7 else "Favor")) for i,(o,d,v,b,la,ln,vi) in enumerate(SEED)])
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
    tipo: str = "Servicio"
    telefono: str = ""
    vulnerable: bool = False
    accion: str = "Ofrece"

@app.get("/health")
def health():
    return {"status": "ok", "service": "vecino-recomienda"}

@app.get("/api/hello")
def hello():
    return {"message": "Vecino Recomienda — esqueleto listo.", "status": "skeleton"}

@app.get("/api/servicios")
def listar(lat: float = -11.981, lng: float = -77.072, tipo: str = ""):
    conn = get_db()
    if tipo:
        rows = conn.execute("SELECT * FROM servicios WHERE tipo=? ORDER BY creado DESC", (tipo,)).fetchall()
    else:
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
    tipo = s.tipo if s.tipo in ("Servicio","Producto","Favor","Emergencia") else "Servicio"
    accion = s.accion if s.accion in ("Ofrece","Solicita") else "Ofrece"
    cur = conn.execute("INSERT INTO servicios (oficio,descripcion,vecino,barrio,lat,lng,vistos,creado,tipo,telefono,vulnerable,accion) VALUES (?,?,?,?,?,?,0,?,?,?,?,?)",
        (s.oficio.strip(), s.descripcion.strip(), s.vecino.strip() or "Vecino", s.barrio.strip(), s.lat, s.lng, time.time(), tipo, s.telefono.strip() or None, 1 if s.vulnerable else 0, accion))
    conn.commit(); conn.close()
    return {"id": cur.lastrowid, "oficio": s.oficio}

class RecomendarBody(BaseModel):
    barrio: str = "Los Olivos"

@app.post("/api/servicios/{sid}/recomendar")
def recomendar(sid: int, body: RecomendarBody = None):
    conn = get_db()
    row = conn.execute("SELECT vistos, barrio FROM servicios WHERE id=?", (sid,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="servicio no encontrado")
    barrio = (body.barrio.strip() if body and body.barrio else "Los Olivos")
    # zona: el aval solo suma a "tu zona" si el recomendante es del mismo barrio del servicio
    conn.execute("INSERT INTO recomendaciones (servicio_id, barrio, creado) VALUES (?,?,?)", (sid, barrio, time.time()))
    conn.execute("UPDATE servicios SET vistos = vistos + 1 WHERE id=?", (sid,))
    conn.commit()
    n = conn.execute("SELECT vistos FROM servicios WHERE id=?", (sid,)).fetchone()[0]
    zona = conn.execute("SELECT COUNT(*) FROM recomendaciones WHERE servicio_id=? AND barrio=?", (sid, row["barrio"] or "Los Olivos")).fetchone()[0]
    conn.close()
    return {"id": sid, "vistos": n, "vistos_zona": zona}

frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_dir, "static")), name="static")
    @app.get("/")
    def root():
        return FileResponse(os.path.join(frontend_dir, "index.html"))
