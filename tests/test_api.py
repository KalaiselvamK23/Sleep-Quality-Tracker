from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_predict_endpoint():
    payload = {
        "Age": 30,
        "Gender": 1,
        "Sleep_duration": 8,
        "REM_sleep_percentage": 25,
        "Deep_sleep_percentage": 25,
        "Light_sleep_percentage": 50,
        "Awakenings": 0,
        "Caffeine_consumption": 0,
        "Alcohol_consumption": 0,
        "Smoking_status": 0,
        "Exercise_frequency": 5,
        "Bedtime_hour": 22,
        "Wakeup_hour": 6
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert "Sleep_efficiency" in result
    assert "Sleep_efficiency_percentage" in result
    assert "Sleep_quality" in result


    # verify the prediction is approximately correct
    assert abs(result["Sleep_efficiency"] - 0.6623) < 0.001

    # verify the percentage
    assert abs(result["Sleep_efficiency_percentage"] - 66.23) < 0.1

    # verify the quality classification
    assert result["Sleep_quality"] == "Moderate"


def test_high_sleep_quality_prediction():
    payload = {
        "Age": 30,
        "Gender": 1,
        "Sleep_duration": 8,
        "REM_sleep_percentage": 25,
        "Deep_sleep_percentage": 80,
        "Light_sleep_percentage": 10,
        "Awakenings": 0,
        "Caffeine_consumption": 0,
        "Alcohol_consumption": 0,
        "Smoking_status": 0,
        "Exercise_frequency": 5,
        "Bedtime_hour": 22,
        "Wakeup_hour": 6
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert abs(result["Sleep_efficiency"] - 0.9192) < 0.001
    assert abs(result["Sleep_efficiency_percentage"] - 91.92) < 0.1
    assert result["Sleep_quality"] == "Excellent"

def test_invalid_age():
    payload = {
        "Age": "abc",
        "Gender": 1,
        "Sleep_duration": 8,
        "REM_sleep_percentage": 25,
        "Deep_sleep_percentage": 25,
        "Light_sleep_percentage": 50,
        "Awakenings": 0,
        "Caffeine_consumption": 0,
        "Alcohol_consumption": 0,
        "Smoking_status": 0,
        "Exercise_frequency": 5,
        "Bedtime_hour": 22,
        "Wakeup_hour": 6
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422

def test_missing_required_field():
    payload = {
        "Age": 30,
        "Gender": 1,
        "Sleep_duration": 8,
        "REM_sleep_percentage": 25,
        "Deep_sleep_percentage": 25,
        "Light_sleep_percentage": 50,
        "Awakenings": 0,
        "Caffeine_consumption": 0,
        "Alcohol_consumption": 0,
        "Smoking_status": 0,
        "Exercise_frequency": 5,
        "Bedtime_hour": 22
        # Wakeup_hour is intentionally missing
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422

def test_good_sleep_quality_prediction(monkeypatch):
    def mock_predict(_):
        return [0.80]

    monkeypatch.setattr("api.app.model.predict", mock_predict)

    payload = {
        "Age": 30,
        "Gender": 1,
        "Sleep_duration": 8,
        "REM_sleep_percentage": 25,
        "Deep_sleep_percentage": 25,
        "Light_sleep_percentage": 50,
        "Awakenings": 0,
        "Caffeine_consumption": 0,
        "Alcohol_consumption": 0,
        "Smoking_status": 0,
        "Exercise_frequency": 5,
        "Bedtime_hour": 22,
        "Wakeup_hour": 6
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert response.json()["Sleep_quality"] == "Good"

def test_needs_improvement_sleep_quality(monkeypatch):
    def mock_predict(_):
        return [0.50]

    monkeypatch.setattr("api.app.model.predict", mock_predict)

    payload = {
        "Age": 30,
        "Gender": 1,
        "Sleep_duration": 8,
        "REM_sleep_percentage": 25,
        "Deep_sleep_percentage": 25,
        "Light_sleep_percentage": 50,
        "Awakenings": 0,
        "Caffeine_consumption": 0,
        "Alcohol_consumption": 0,
        "Smoking_status": 0,
        "Exercise_frequency": 5,
        "Bedtime_hour": 22,
        "Wakeup_hour": 6
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert response.json()["Sleep_quality"] == "Needs Improvement"


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Sleep Quality Tracker API is running"