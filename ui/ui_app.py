import os
import time
import requests
import streamlit as st
from dotenv import load_dotenv

def post_with_retry(url, json, tries=3, timeout=20):
    last = None
    for i in range(tries):
        try:
            return requests.post(url, json=json, headers={"User-Agent":"hp-ui/1.0"}, timeout=timeout)
        except requests.exceptions.ReadTimeout as e:
            last = e
            time.sleep(1 + i)  # backoff
    raise last

load_dotenv()
API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000") 

# ---- Replace with your real map list or expose a /maps endpoint on the API ----
KNOWN_MAPS = [
    'Apocalypse', 'Combine', 'Hacienda', 'Slums', 'Summit'
]

st.set_page_config(page_title="HP Win Probability", page_icon="📈", layout="wide")

# ---------- Sidebar ----------
st.sidebar.title("HP Win Probability")
st.sidebar.caption("After first 4 hills")

# Map picker
map_choice = st.sidebar.selectbox("Select map", KNOWN_MAPS, index=0)

# Scores input
st.sidebar.subheader("Enter Scores")
attack_score = st.sidebar.number_input("Attacking team score", min_value=0, value=100, step=1)
defense_score = st.sidebar.number_input("Defending team score", min_value=0, value=95, step=1)

# Predict button
predict_btn = st.sidebar.button("Predict Win %", use_container_width=True)

# ---------- Header ----------
st.markdown("# 📈 Hardpoint — Win Probability")
st.write("Model: logistic regression on **ScoreDiff_P4** with **Map** (calibrated).")

# ---------- Layout: two columns ----------
col_left, col_right = st.columns([0.45, 0.55], gap="large")

# ---------- Right: Chart (Datawrapper iframe -> PNG fallback) ----------
with col_right:
    st.subheader(f"Curve — {map_choice}")
    # Prefer Datawrapper: request the iframe HTML from your API (returns HTML)
    try:
        r = requests.get(f"{API_BASE}/plot_embed", params={"map": map_choice}, timeout=20)
        if r.status_code == 200 and r.text.strip():
            st.components.v1.html(r.text, height=520, scrolling=False)
        else:
            # Fallback to PNG endpoint
            img = requests.get(f"{API_BASE}/plot", params={"map": map_choice}, timeout=5)
            if img.status_code == 200:
                st.image(img.content, caption=f"Win Probability — {map_choice}")
            else:
                st.warning("Chart unavailable. Check /plot_embed and /plot endpoints.")
    except Exception as e:
        st.warning(f"Chart request failed: {e}")

# ---------- Left: Prediction card ----------
with col_left:
    st.subheader("Point-in-time Prediction")
    if predict_btn:
        payload = {
            "map": map_choice,
            "attack_score": float(attack_score),
            "defense_score": float(defense_score),
        }
        try:
            url = f"{API_BASE}/predict"
            r = requests.post(f"{API_BASE}/predict", json=payload, timeout=20)
            if r.status_code == 200:
                out = r.json()
                p_att = float(out["p_team1"])
                p_def = float(out["p_team2"])
                diff = float(out["score_diff"])
                # Display
                st.metric("Score Diff (Att - Def)", f"{diff:.1f}")
                st.progress(min(max(p_att, 0.0), 1.0))
                st.write(
                    f"**Attacking:** {p_att*100:.1f}% | **Defending:** {p_def*100:.1f}%"
                )
                # # Simple bar
                # st.caption("Probability split")
                # st.bar_chart(
                #     {"Probability": [p_att*100, p_def*100]},
                #     x=None,
                #     height=180
                # )
            else:
                st.error(f"Predict failed: {r.status_code} — {r.text}")
        except Exception as e:
            st.error(f"Predict request error: {e}")
    else:
        st.info("Enter scores and click **Predict Win %**.")

# ---------- Footer ----------
# st.divider()
# st.caption(
#     "Shaded CI shown in the chart (Datawrapper). Backend: FastAPI. "
#     "Percentages are model outputs; interpret as win likelihood given current score and map."
# )
st.divider()
st.caption(f"API_BASE_URL = {API_BASE}")  # should show https://hp-api-mlff.onrender.com
url = f"{API_BASE}/predict"
st.caption(f"Calling: {url}")
r = requests.post(url, json=payload, headers={"User-Agent":"hp-ui/1.0"}, timeout=10)
st.write({"status": r.status_code, "url": url, "text": r.text[:300]})
