import os, tempfile
os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "borde.db")
from fastapi.testclient import TestClient
from backend.main import app
c = TestClient(app)

def test_422_oficio_vacio():
    r = c.post("/api/servicios", json={"oficio":"","descripcion":"x","vecino":"y","lat":-11.981,"lng":-77.072})
    assert r.status_code == 422

def test_404_recomendar():
    r = c.post("/api/servicios/99999/recomendar")
    assert r.status_code == 404

def test_cuenta_limpia_solo_seed():
    r = c.get("/api/servicios?lat=-11.981&lng=-77.072")
    assert r.status_code == 200
    assert len(r.json()) >= 5
