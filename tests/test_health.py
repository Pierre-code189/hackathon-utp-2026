from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from backend.main import app
c = TestClient(app)
def test_health():
    assert c.get("/health").status_code == 200
def test_hello():
    assert c.get("/api/hello").status_code == 200
