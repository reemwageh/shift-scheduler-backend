import sys
import os

# Add the parent directory to the Python path so it can find main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}  # ✅ fixed here


def test_optimize_schedule():
    sample_request = {
        "period": "2025-07-01/2025-07-14",
        "employees": [
            {
                "id": "E1",
                "name": "John Doe",
                "skills": ["cook", "cashier"],
                "max_hours": 80,
                "availability": {
                    "start": "2025-07-01T08:00:00",
                    "end": "2025-07-14T22:00:00"
                }
            }
        ],
        "shifts": [
            {
                "id": "S1",
                "role": "morning_cook",
                "start_time": "2025-07-01T09:00:00",
                "end_time": "2025-07-01T17:00:00",
                "required_skill": "cook"
            }
        ],
        "current_assignments": []
    }

    response = client.post("/api/schedule/optimize", json=sample_request)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert isinstance(json_data["assignments"], list)
