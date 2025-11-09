import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env

AMAD_CLIENT_ID = os.environ.get("AMAD_CLIENT_ID")
AMAD_CLIENT_SECRET = os.environ.get("AMAD_CLIENT_SECRET")
API_KEY = os.environ.get("API_KEY")

import os

MODEL_DIR = os.environ.get("MODEL_DIR", "./trained-models")
os.makedirs(MODEL_DIR, exist_ok=True)
