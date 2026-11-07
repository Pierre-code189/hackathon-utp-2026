import os, tempfile
os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "ce.db")
from fastapi.testclient import TestClient
from backend.main import app
c = TestClient(app)

def test_emergencia_seed():
    # En DB tmp no hay seed de emergencia (seed de emergencia solo en DB real); se crea uno y se filtra
    c.post("/api/servicios", json={"oficio":"TestEmerg","descripcion":"d","vecino":"T","lat":-11.981,"lng":-77.072,"tipo":"Emergencia"})
    r = c.get("/api/servicios?tipo=Emergencia")
    assert r.status_code == 200 and len(r.json()) >= 1

def test_telefono_y_vulnerable():
    r = c.post("/api/servicios", json={"oficio":"TestContacto","descripcion":"d","vecino":"T","lat":-11.981,"lng":-77.072,"telefono":"51999999999","vulnerable":True,"tipo":"Servicio"})
    assert r.status_code == 200
    d = c.get("/api/servicios").json()
    row = next(x for x in d if x["oficio"]=="TestContacto")
    assert row["telefono"]=="51999999999" and row["vulnerable"]==1
