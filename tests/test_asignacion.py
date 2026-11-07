import os, tempfile
os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "asig.db")
from fastapi.testclient import TestClient
from backend.main import app
c = TestClient(app)

def test_asignar_y_listar():
    n = c.post("/api/servicios", json={"oficio":"NecAsig","descripcion":"d","vecino":"A","lat":-11.981,"lng":-77.072,"tipo":"Favor","accion":"Solicita"})
    r = c.post("/api/servicios", json={"oficio":"RecAsig","descripcion":"d","vecino":"B","lat":-11.981,"lng":-77.072,"tipo":"Favor","accion":"Ofrece"})
    assert n.status_code==200 and r.status_code==200
    res = c.post("/api/asignaciones", json={"necesidad_id": n.json()["id"], "recurso_id": r.json()["id"]})
    assert res.status_code==200
    a = c.get("/api/asignaciones").json()
    assert any(x["necesidad"]=="NecAsig" and x["recurso"]=="RecAsig" for x in a)
    assert c.post("/api/asignaciones", json={"necesidad_id": 99999, "recurso_id": 99999}).status_code==404
    assert c.get("/api/servicios?vulnerable=1").status_code==200
