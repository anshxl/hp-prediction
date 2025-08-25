from pydantic import BaseModel, Field, field_validator

class PredictRequest(BaseModel):
    map: str = Field(..., description='Exact map name as in training data')
    attack_score: float = Field(..., ge=0, description='Attack side team score')
    defense_score: float = Field(..., ge=0, description='Defense side team score')

class PredictResponse(BaseModel):
    map: str
    attack_score: float
    defense_score: float
    score_diff: float
    p_team1: float
    p_team2: float
    model_version: str

