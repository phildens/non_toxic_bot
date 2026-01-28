import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_predict_endpoint_success():
    """Проверяем, что API возвращает правильную структуру ответа"""
    payload = {"text": "Привет, какой прекрасный день!"}
    response = client.post("/predict", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "toxic_probability" in data
    assert "is_toxic" in data
    assert isinstance(data["toxic_probability"], float)

def test_predict_toxicity_logic():
    """Проверяем, что на явную грубость вероятность выше, чем на вежливость"""
    bad_res = client.post("/predict", json={"text": "Ты ужасный человек и я тебя ненавижу"})
    good_res = client.post("/predict", json={"text": "Большое спасибо за помощь, вы лучший"})
    
    bad_prob = bad_res.json()["toxic_probability"]
    good_prob = good_res.json()["toxic_probability"]
    
    assert bad_prob > good_prob
    assert bad_prob > 0.5  # Грубость должна быть выше порога
    assert good_prob < 0.5 # Вежливость должна быть ниже
