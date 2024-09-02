from fastapi.testclient import TestClient

from app.infraestructure.api.main import app


client = TestClient(app)


def test__health_check():
    expected_response = {"name": "AI Feedback", "version": "0.0.1"}

    response = client.get("/health-check")

    assert response.status_code == 200
    assert response.json() == expected_response
