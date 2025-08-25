from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_basic():
    # pick a known map from your artifacts
    payload = {"map":"Skidrow","score_diff":0.0}
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    out = r.json()
    assert 0.0 <= out["p_team1"] <= 1.0
    assert abs(out["p_team1"] + out["p_team2"] - 1.0) < 1e-8

def test_plot_png():
    r = client.get("/plot", params={"map":"Skidrow"})
    assert r.status_code == 200
    assert r.headers["content-type"] == "image/png"
