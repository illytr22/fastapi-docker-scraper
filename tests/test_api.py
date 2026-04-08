from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_trending():
    response = client.get("/trending")
    assert response.status_code == 200
    assert isinstance(response.json(), list)