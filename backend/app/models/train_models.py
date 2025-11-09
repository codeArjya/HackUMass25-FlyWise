import os
from datetime import date, timedelta
import pandas as pd
import numpy as np
import joblib
from prophet import Prophet
import xgboost as xgb
from sklearn.preprocessing import OneHotEncoder
from app.config import MODEL_DIR

os.makedirs(MODEL_DIR, exist_ok=True)

# -----------------------------
# 1️⃣ Setup Amadeus client
# -----------------------------
try:
    from amadeus import Client
    AMAD_CLIENT_ID = os.environ.get("AMAD_CLIENT_ID")
    AMAD_CLIENT_SECRET = os.environ.get("AMAD_CLIENT_SECRET")
    amadeus = Client(client_id=AMAD_CLIENT_ID, client_secret=AMAD_CLIENT_SECRET)
    USE_AMADEUS = True
except ImportError:
    USE_AMADEUS = False
    print("Amadeus SDK not installed. Using synthetic data.")

# -----------------------------
# 2️⃣ Define routes
# -----------------------------
routes = [
    ("JFK", "LAX"),
    ("ORD", "SFO"),
    ("ATL", "MIA"),
    ("LAX", "SEA"),
    ("BOS", "ORD")
]

# -----------------------------
# 3️⃣ Fetch flight prices
# -----------------------------
def fetch_route_data(origin, destination, days=30):
    today = date.today()
    dates = [today + timedelta(days=i) for i in range(days)]

    if USE_AMADEUS:
        prices = []
        for d in dates:
            try:
                resp = amadeus.shopping.flight_offers_search.get(
                    originLocationCode=origin,
                    destinationLocationCode=destination,
                    departureDate=str(d),
                    adults=1,
                    max=1
                )
                price = float(resp.data[0]['offerItems'][0]['price']['total'])
            except Exception:
                price = 200 + np.random.randint(0, 100)
            prices.append(price)
    else:
        prices = 200 + np.random.randint(0, 100, size=days)

    df = pd.DataFrame({
        "origin": origin,
        "destination": destination,
        "date": dates,
        "price": prices,
        "days_to_departure": list(range(days)),
        "day_of_week": [d.weekday() for d in dates]
    })
    return df

# -----------------------------
# 4️⃣ Collect all route data
# -----------------------------
all_data = pd.concat([fetch_route_data(o,d) for o,d in routes]).reset_index(drop=True)
print(f"✅ Collected {len(all_data)} rows across {len(routes)} routes.")

# -----------------------------
# 5️⃣ Generate labels for classifier
# -----------------------------
all_data['next_day_price'] = all_data.groupby(['origin','destination'])['price'].shift(-1)
all_data = all_data.dropna()

# -----------------------------
# 6️⃣ Train per-route XGBoost classifier
# -----------------------------
route_cols = all_data[['origin','destination']]
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
route_features = encoder.fit_transform(route_cols)
pd.to_pickle(encoder, os.path.join(MODEL_DIR, "route_encoder.pkl"))

numeric = all_data[['days_to_departure','day_of_week','price']].values
X = np.hstack([numeric, route_features])
y = (all_data['next_day_price'] > all_data['price']).astype(int)

clf = xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss")
clf.fit(X, y)
clf_path = os.path.join(MODEL_DIR, "price_classifier.json")
clf.save_model(clf_path)
print(f"✅ XGBoost classifier trained and saved to {clf_path}")

# -----------------------------
# 7️⃣ Train Prophet model (route-agnostic)
# -----------------------------
df_prophet = all_data.groupby('date')['price'].mean().reset_index()
df_prophet = df_prophet.rename(columns={"date": "ds", "price": "y"})
prophet_model = Prophet(daily_seasonality=True)
prophet_model.fit(df_prophet)
prophet_path = os.path.join(MODEL_DIR, "prophet_model.pkl")
joblib.dump(prophet_model, prophet_path)
print(f"✅ Prophet model trained and saved to {prophet_path}")

print("🎉 All models ready for multi-route FlyWise backend!")
