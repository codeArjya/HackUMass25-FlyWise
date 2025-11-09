import pandas as pd
from prophet import Prophet
import joblib
import os
from app.config import MODEL_DIR

class ForecastModel:
    def __init__(self, model_path: str = None):
        self.model_path = model_path or os.path.join(MODEL_DIR, "prophet_model.pkl")
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            # Train a default model on placeholder future data
            df = pd.DataFrame({
                "ds": pd.date_range("2025-11-01", periods=30),
                "y": 200 + pd.np.random.randint(0, 50, size=30)
            })
            model = Prophet(daily_seasonality=True)
            model.fit(df)
            self.model = model
            joblib.dump(self.model, self.model_path)

    def forecast_prices(self, origin: str = None, destination: str = None, days: int = 14):
        """
        Returns forecast for a given route (currently route-agnostic).
        """
        future = self.model.make_future_dataframe(periods=days)
        forecast = self.model.predict(future)
        series = forecast[['ds','yhat']].tail(days).rename(columns={'ds':'date','yhat':'predictedPrice'})
        trend = (series['predictedPrice'].iloc[-1] - series['predictedPrice'].iloc[0]) / series['predictedPrice'].iloc[0]
        return {"series": series.to_dict(orient="records"), "trend": trend}
