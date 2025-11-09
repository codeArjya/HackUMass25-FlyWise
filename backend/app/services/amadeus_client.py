import pandas as pd
from datetime import date, timedelta
from amadeus import Client, ResponseError
import os

amadeus = Client(
    client_id=os.environ.get("AMAD_CLIENT_ID"),
    client_secret=os.environ.get("AMAD_CLIENT_SECRET")
)

def get_flight_prices(origin: str, destination: str, start_date: date, end_date: date) -> pd.DataFrame:
    """
    Fetch flight prices from Amadeus.
    Returns a DataFrame with columns ['date', 'price'].
    """
    data = []
    current_date = start_date

    while current_date <= end_date:
        try:
            # Call Amadeus Flight Offers Prediction API
            response = amadeus.travel.predictions.flight_price.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=current_date.isoformat(),
                adults=1
            )
            
            # Extract price (USD or default currency)
            price = float(response.data['price']['total'])
            data.append({"date": current_date, "price": price})

        except ResponseError as e:
            print(f"Amadeus API error for {current_date}: {e}")
            # fallback to a default/mock value if API fails
            price = 200  # or some interpolation
            data.append({"date": current_date, "price": price})

        current_date += timedelta(days=1)

    return pd.DataFrame(data)
