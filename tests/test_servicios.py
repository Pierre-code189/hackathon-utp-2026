import os, tempfile
os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")  # aislado, no toca data/ real
from fastapi.testclient import TestClient
from backend.main import app
c = TestClient(app)

def test_health():
    assert c.get("/health").json()["status"] == "ok"

def test_listado_seed_y_visto_bueno():
    r = c.get("/api/servicios?lat=-11.981&lng=-77.072")
    assert r.status_code == 200
    data = r.json()
    assert len(data) >= 5
    # ordenado por distancia ascendente
    dists = [d["distancia_km"] for d in data]
    assert dists == sorted(dists)
    # al menos un servicio con visto bueno
    assert any(d["visto_bueno"] for d in data)

def test_publicar_y_recomendar():
    r = c.post("/api/servicios", json={"oficio":"TestOficio","descripcion":"Desc test","vecino":"Tester","barrio":"Los Olivos","lat":-11.981,"lng":-77.072})
    assert r.status_code == 200
    sid = r.json()["id"]
    r2 = c.post(f"/api/servicios/{sid}/recomendar")
    assert r2.status_code == 200 and r2.json()["vistos"] >= 1
    r3 = c.post("/api/servicios/99999/recomendar")
    assert r3.status_code == 404  # 404 real, no 422/200 maquillado
