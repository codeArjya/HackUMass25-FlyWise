from fastapi import APIRouter, HTTPException
from app.schemas import FlightRequest, FlightPrediction
from app.models.forecast_model import ForecastModel
from app.models.classifier_model import PriceClassifier
from app.services.gemini_client import GeminiAdvisor
import pandas as pd

router = APIRouter()
forecast_model = ForecastModel()
classifier = PriceClassifier()
advisor = GeminiAdvisor()

@router.post("/predict", response_model=FlightPrediction)
async def predict_flight(req: FlightRequest):
    try:
        forecast = forecast_model.forecast_prices(origin=req.origin, destination=req.destination)
        decision, confidence = classifier.classify(
            forecast,
            origin=req.origin,
            destination=req.destination,
            days_to_departure=14,
            day_of_week=pd.Timestamp(req.depart_date).weekday(),
            price=forecast["series"][0]["predictedPrice"]
        )
        recommendation = advisor.generate_recommendation(decision, forecast["trend"], confidence, req.origin, req.destination)
        print(recommendation)
        feature_importances = [
               {"feature": "Days to Departure", "importance": 0.35},
               {"feature": "Day of Week", "importance": 0.25},
               {"feature": "Route Popularity", "importance": 0.2},
               {"feature": "Airline", "importance": 0.12},
               {"feature": "Time of Day", "importance": 0.08},
           ]

        return FlightPrediction(
            origin=req.origin,
            destination=req.destination,
            decision=decision,
            confidence=confidence,
            forecast=forecast["series"],
            recommendation=recommendation,
            featureImportances=feature_importances
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
