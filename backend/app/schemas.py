from pydantic import BaseModel
from typing import List, Dict, Any

class FlightRequest(BaseModel):
    origin: str
    destination: str
    depart_date: str

class FlightPrediction(BaseModel):
    origin: str
    destination: str
    decision: str
    confidence: float
    forecast: List[Dict[str, Any]]
    recommendation: str
    featureImportances: List[Dict[str, Any]]
