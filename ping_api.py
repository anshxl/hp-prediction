import requests

BASE_URL = "http://127.0.0.1:8000"

def check_docs():
    r = requests.get(f"{BASE_URL}/docs")
    if r.status_code == 200:
        print("✅ Docs available at /docs")
    else:
        print(f"⚠️ Docs check failed: {r.status_code}")

def check_predict():
    payload = {
        "map": "Summit",        # replace with a map from your artifacts
        "attack_score": 100,
        "defense_score": 80
    }
    r = requests.post(f"{BASE_URL}/predict", json=payload)
    if r.status_code == 200:
        print("✅ Predict endpoint works:")
        print(r.json())
    else:
        print(f"⚠️ Predict check failed: {r.status_code}, {r.text}")

def check_plot_embed():
    params = {"map": "Summit"}   # replace with a map from your artifacts
    r = requests.get(f"{BASE_URL}/plot_embed", params=params)
    if r.status_code == 200:
        print("✅ Plot embed endpoint works (iframe HTML returned)")
        # print only first 200 chars so you don't spam console
        print(r.text[:200] + "...")
    else:
        print(f"⚠️ Plot embed check failed: {r.status_code}, {r.text}")

if __name__ == "__main__":
    check_docs()
    check_predict()
    check_plot_embed()