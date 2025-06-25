from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json() == {
        "message": "Hello Jenkins, it works!"
    }, f"Expected {'message': 'Hello Jenkins, it works!'}, got {response.json()}"
