from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .schemas import PredictRequest, PredictResponse
from .infer import predict_prob, curve_for_map, MODEL_VERSION, get_maps
from .plots import plot_map_curve_png
from .datawrapper import iframe_html_for_map

app = FastAPI(title="HP Win Probability API", version=MODEL_VERSION)

# allow your UI origin(s); update once you know the Render URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for quick start; tighten later to ["https://hp-ui.onrender.com"]
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    score_diff = float(payload.attack_score) - float(payload.defense_score)
    try:
        p1 = predict_prob(payload.map, score_diff)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return PredictResponse(
        map=payload.map,
        attack_score=payload.attack_score,
        defense_score=payload.defense_score,
        score_diff=score_diff,
        p_team1=p1,
        p_team2=1.0 - p1,
        model_version=MODEL_VERSION,
    )

@app.get("/plot")
def plot(map: str):
    # Validate map and return a PNG image
    try:
        _ = curve_for_map(map)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    png = plot_map_curve_png(map)
    return Response(content=png, media_type="image/png")

@app.get("/plot_embed", response_class=HTMLResponse)
def plot_embed(map: str):
    try:
        html = iframe_html_for_map(map)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return HTMLResponse(content=html)

@app.get("/maps")
def maps():
    try:
        return JSONResponse({"maps": get_maps(), "model_version": MODEL_VERSION})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
def root():
    return {"status": "ok"}
