import os, tempfile
os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "tipos.db")
from fastapi.testclient import TestClient
from backend.main import app
c = TestClient(app)

def test_filtro_producto():
    r = c.get("/api/servicios?tipo=Producto")
    assert r.status_code == 200
    assert all(d["tipo"]=="Producto" for d in r.json())
    assert len(r.json()) >= 1

def test_filtro_favor():
    r = c.get("/api/servicios?tipo=Favor")
    assert r.status_code == 200
    d = r.json()
    assert len(d) >= 1 and all(x["tipo"]=="Favor" for x in d)

def test_publicar_con_tipo():
    r = c.post("/api/servicios", json={"oficio":"TestFavorP1P2","descripcion":"desc","vecino":"Tester","lat":-11.981,"lng":-77.072,"tipo":"Favor"})
    assert r.status_code == 200
    r2 = c.get("/api/servicios?tipo=Favor")
    assert any(x["oficio"]=="TestFavorP1P2" for x in r2.json())
