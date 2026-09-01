from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_index_renders_vision_review() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "PPE review" in response.text


def test_api_disables_identity_tracking() -> None:
    payload = {
        "frame_id": "SYN-FRAME-001",
        "detections": [
            {
                "detection_id": "SYN-PERSON-1",
                "label": "person",
                "confidence": 0.95,
                "x": 0.1,
                "y": 0.1,
                "width": 0.2,
                "height": 0.3,
            }
        ],
    }
    response = client.post("/evaluate", json=payload)
    assert response.status_code == 200
    assert response.json()["identity_tracking"] is False
