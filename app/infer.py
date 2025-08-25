import joblib, pandas as pd
from functools import lru_cache
from pathlib import Path

ART_DIR = Path(__file__).resolve().parents[1] / "artifacts"
MODEL_PATH = ART_DIR / "model_v1.joblib"
CURVE_PATH = ART_DIR / "curve_by_map_v1.csv"
MODEL_VERSION = "v1"

@lru_cache(maxsize=1)
def load_model():
    return joblib.load(MODEL_PATH)

@lru_cache(maxsize=1)
def load_curve():
    return pd.read_csv(CURVE_PATH)

def get_maps() -> list[str]:
    df = load_curve()
    maps = sorted(df["Map"].dropna().unique().tolist())
    if not maps:
        raise ValueError("No maps found in curve artifact")
    return maps

def predict_prob(map_name: str, score_diff: float) -> float:
    model = load_model()
    X = pd.DataFrame([[score_diff, map_name]], columns=["ScoreDiff_P4", "Map"])
    p = model.predict_proba(X)[:, 1][0]  # Team1 prob
    return float(p)

def curve_for_map(map_name: str) -> pd.DataFrame:
    df = load_curve()
    out = df[df["Map"] == map_name].copy()
    if out.empty:
        raise ValueError(f"Unknown map: {map_name}. Available maps: {df['Map'].unique()}")
    return out