import os, tempfile
os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "za.db")
from fastapi.testclient import TestClient
from backend.main import app
c = TestClient(app)

def test_accion_y_zona():
    c.post("/api/servicios", json={"oficio":"TestZona","descripcion":"d","vecino":"T","lat":-11.981,"lng":-77.072,"tipo":"Favor","accion":"Solicita","barrio":"Los Olivos"})
    d = c.get("/api/servicios?tipo=Favor").json()
    row = next(x for x in d if x["oficio"]=="TestZona")
    assert row["accion"]=="Solicita"
    r = c.post(f"/api/servicios/{row['id']}/recomendar", json={"barrio":"Los Olivos"})
    assert r.status_code==200 and r.json()["vistos_zona"]>=1
    r2 = c.post(f"/api/servicios/{row['id']}/recomendar", json={"barrio":"Otra Zona"})
    assert r2.status_code==200  # suma total, no zona
