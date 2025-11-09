import xgboost as xgb
import numpy as np
import os
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from app.config import MODEL_DIR

class PriceClassifier:
    def __init__(self, model_path: str = None):
        self.model_path = model_path or os.path.join(MODEL_DIR, "price_classifier.json")
        self.encoder_path = os.path.join(MODEL_DIR, "route_encoder.pkl")
        self.model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        self.encoder = None

        # Load model & encoder if exists
        if os.path.exists(self.model_path) and os.path.exists(self.encoder_path):
            self.model.load_model(self.model_path)
            self.encoder = pd.read_pickle(self.encoder_path)

    def train(self, df: pd.DataFrame):
        """
        df: columns=['origin','destination','days_to_departure','day_of_week','price','next_day_price']
        """
        y = (df['next_day_price'] > df['price']).astype(int)

        # One-hot encode routes
        route_cols = df[['origin','destination']]
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        route_features = self.encoder.fit_transform(route_cols)
        pd.to_pickle(self.encoder, self.encoder_path)

        numeric = df[['days_to_departure','day_of_week','price']].values
        X = np.hstack([numeric, route_features])

        self.model.fit(X, y)
        self.model.save_model(self.model_path)
        print(f"✅ Trained classifier saved to {self.model_path}")

    def classify(self, forecast: dict, origin: str, destination: str, days_to_departure: int = 14, day_of_week: int = None, price: float = None):
        if self.encoder is None:
            raise ValueError("Classifier not trained yet or encoder missing.")

        if day_of_week is None:
            day_of_week = pd.Timestamp.today().weekday()
        if price is None:
            price = forecast["series"][0]["predictedPrice"]

        # Encode route
        route_features = self.encoder.transform([[origin, destination]])
        numeric = np.array([[days_to_departure, day_of_week, price]])
        X = np.hstack([numeric, route_features])
        decision = "Buy" if self.model.predict(X)[0] else "Wait"
        confidence = abs(forecast["trend"]) * 100
        return decision, confidence
