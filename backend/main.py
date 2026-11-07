from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os, sqlite3, math, time, html

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
  accion TEXT DEFAULT 'Ofrece',
  categoria TEXT,
  stock INTEGER,
  precio REAL,
  estado TEXT DEFAULT 'publicado'
);
CREATE TABLE IF NOT EXISTS recomendaciones (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  servicio_id INTEGER NOT NULL,
  barrio TEXT,
  creado REAL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS reportes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  servicio_id INTEGER NOT NULL,
  motivo TEXT,
  creado REAL DEFAULT 0,
  estado TEXT DEFAULT 'pendiente'
);
CREATE TABLE IF NOT EXISTS asignaciones (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  necesidad_id INTEGER NOT NULL,
  recurso_id INTEGER NOT NULL,
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
    if "categoria" not in cols:
        conn.execute("ALTER TABLE servicios ADD COLUMN categoria TEXT")
    if "stock" not in cols:
        conn.execute("ALTER TABLE servicios ADD COLUMN stock INTEGER")
    if "precio" not in cols:
        conn.execute("ALTER TABLE servicios ADD COLUMN precio REAL")
    if "estado" not in cols:
        conn.execute("ALTER TABLE servicios ADD COLUMN estado TEXT DEFAULT 'publicado'")
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
  ("Grupos de apoyo — primeros auxilios", "Botiquín y traslado, disponible 24h", "Comité barrial", "Los Olivos", -11.982, -77.069, 4),
  ("Red de agua y alimentos", "Distribución solidaria en emergencia", "Vecinos unidos", "Los Olivos", -11.986, -77.071, 2),
  ("Se necesita gasfitería", "Busco gasfitero para fuga en cocina, hoy", "Mariana Ruiz", "Los Olivos", -11.9825, -77.0695, 0),
  ("Atención médica 24h (emergencia)", "Médico de turno para urgencias en el barrio", "Dr. Jorge Salas", "Los Olivos", -11.9815, -77.0715, 2),
]

def seed_if_empty():
    conn = get_db()
    n = conn.execute("SELECT COUNT(*) FROM servicios").fetchone()[0]
    if n == 0:
        conn.executemany("INSERT INTO servicios (oficio,descripcion,vecino,barrio,lat,lng,vistos,creado,tipo) VALUES (?,?,?,?,?,?,?,?,?)",
            [(o,d,v,b,la,ln,vi,time.time(),"Servicio" if i<5 else ("Producto" if i<7 else ("Favor" if i<9 else ("Emergencia" if i<12 else "Servicio")))) for i,(o,d,v,b,la,ln,vi) in enumerate(SEED)])
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
    categoria: str = ""
    stock: int | None = None
    precio: float | None = None

@app.get("/health")
def health():
    return {"status": "ok", "service": "vecino-recomienda"}

@app.get("/api/hello")
def hello():
    return {"message": "Vecino Recomienda — esqueleto listo.", "status": "skeleton"}

@app.get("/api/servicios")
def listar(lat: float = -11.981, lng: float = -77.072, tipo: str = "", vulnerable: bool | None = None):
    conn = get_db()
    if vulnerable is not None and not vulnerable:
        rows = conn.execute("SELECT * FROM servicios WHERE vulnerable=0 ORDER BY creado DESC").fetchall()
        # vulnerable=false tratado como no-vulnerables (no ignorado)
    elif vulnerable and tipo:
        rows = conn.execute("SELECT * FROM servicios WHERE vulnerable=1 AND tipo=? ORDER BY creado DESC", (tipo,)).fetchall()
    elif vulnerable:
        rows = conn.execute("SELECT * FROM servicios WHERE vulnerable=1 ORDER BY creado DESC").fetchall()
    elif tipo:
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
    if not (-90 <= s.lat <= 90 and -180 <= s.lng <= 180):
        raise HTTPException(status_code=422, detail="lat/lng fuera de rango")
    if len(s.oficio) > 120 or len(s.descripcion) > 500 or len(s.vecino) > 80:
        raise HTTPException(status_code=422, detail="texto demasiado largo")
    if s.tipo not in ("Servicio","Producto","Favor","Emergencia"):
        raise HTTPException(status_code=422, detail="tipo invalido")
    if s.accion not in ("Ofrece","Solicita"):
        raise HTTPException(status_code=422, detail="accion invalida")
    conn = get_db()
    tipo = s.tipo if s.tipo in ("Servicio","Producto","Favor","Emergencia") else "Servicio"
    accion = s.accion if s.accion in ("Ofrece","Solicita") else "Ofrece"
    cur = conn.execute("INSERT INTO servicios (oficio,descripcion,vecino,barrio,lat,lng,vistos,creado,tipo,telefono,vulnerable,accion,categoria,stock,precio) VALUES (?,?,?,?,?,?,0,?,?,?,?,?,?,?,?)",
        (html.escape(s.oficio.strip()), html.escape(s.descripcion.strip()), html.escape(s.vecino.strip() or "Vecino"), html.escape(s.barrio.strip()), s.lat, s.lng, time.time(), tipo, s.telefono.strip() or None, 1 if s.vulnerable else 0, accion, html.escape(s.categoria.strip()), s.stock, s.precio))
    conn.commit(); conn.close()
    return {"id": cur.lastrowid, "oficio": s.oficio}

ADMIN_CODE = os.environ.get("ADMIN_CODE", "UTP-ADMIN-2026")

class ReporteBody(BaseModel):
    servicio_id: int
    motivo: str = ""

@app.post("/api/reportes")
def crear_reporte(r: ReporteBody):
    conn = get_db()
    row = conn.execute("SELECT id FROM servicios WHERE id=?", (r.servicio_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="servicio no encontrado")
    conn.execute("INSERT INTO reportes (servicio_id, motivo, creado) VALUES (?,?,?)", (r.servicio_id, html.escape(r.motivo.strip()[:200]), time.time()))
    conn.execute("UPDATE servicios SET estado='reportado' WHERE id=?", (r.servicio_id,))
    conn.commit(); conn.close()
    return {"ok": True}

@app.get("/api/reportes")
def listar_reportes(codigo: str = ""):
    if codigo != ADMIN_CODE:
        raise HTTPException(status_code=403, detail="codigo invalido")
    conn = get_db()
    rows = conn.execute("SELECT r.id, r.servicio_id, r.motivo, r.estado, s.oficio FROM reportes r JOIN servicios s ON s.id=r.servicio_id ORDER BY r.id DESC").fetchall()
    conn.close()
    return [dict(x) for x in rows]

@app.post("/api/servicios/{sid}/bajar")
def bajar(sid: int, codigo: str = ""):
    if codigo != ADMIN_CODE:
        raise HTTPException(status_code=403, detail="codigo invalido")
    conn = get_db()
    conn.execute("UPDATE servicios SET estado='bajado' WHERE id=?", (sid,))
    conn.execute("UPDATE reportes SET estado='resuelto' WHERE servicio_id=?", (sid,))
    conn.commit(); conn.close()
    return {"id": sid, "estado": "bajado"}

class AsignacionBody(BaseModel):
    necesidad_id: int
    recurso_id: int

@app.post("/api/asignaciones")
def crear_asignacion(a: AsignacionBody):
    conn = get_db()
    nec = conn.execute("SELECT id FROM servicios WHERE id=?", (a.necesidad_id,)).fetchone()
    rec = conn.execute("SELECT id FROM servicios WHERE id=?", (a.recurso_id,)).fetchone()
    if not nec or not rec:
        conn.close()
        raise HTTPException(status_code=404, detail="necesidad o recurso no encontrado")
    if a.necesidad_id == a.recurso_id:
        conn.close()
        raise HTTPException(status_code=422, detail="necesidad y recurso no pueden ser el mismo")
    dup = conn.execute("SELECT id FROM asignaciones WHERE necesidad_id=? AND recurso_id=?", (a.necesidad_id, a.recurso_id)).fetchone()
    if dup:
        conn.close()
        raise HTTPException(status_code=409, detail="asignacion duplicada")
    cur = conn.execute("INSERT INTO asignaciones (necesidad_id, recurso_id, creado) VALUES (?,?,?)", (a.necesidad_id, a.recurso_id, time.time()))
    conn.commit(); conn.close()
    return {"id": cur.lastrowid, "necesidad_id": a.necesidad_id, "recurso_id": a.recurso_id}

@app.get("/api/asignaciones")
def listar_asignaciones():
    conn = get_db()
    rows = conn.execute("SELECT a.id, a.necesidad_id, a.recurso_id, a.creado, n.oficio AS necesidad, r.oficio AS recurso FROM asignaciones a JOIN servicios n ON n.id=a.necesidad_id JOIN servicios r ON r.id=a.recurso_id ORDER BY a.id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

class RecomendarBody(BaseModel):
    barrio: str = "Los Olivos"

@app.post("/api/servicios/{sid}/recomendar")
def recomendar(sid: int, body: RecomendarBody = None):
    conn = get_db()
    row = conn.execute("SELECT vistos, barrio FROM servicios WHERE id=?", (sid,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="servicio no encontrado")
    barrio = (body.barrio.strip() if body and body.barrio and body.barrio.strip() else "Los Olivos")
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
