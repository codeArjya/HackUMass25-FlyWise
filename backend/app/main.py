from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import flights

app = FastAPI(title="FlyWise API", version="1.0")
app.include_router(flights.router, prefix="/api/flights", tags=["Flights"])

# Allow requests from your frontend
origins = [
    "http://localhost:5173",  # Vite default dev server port
    "http://localhost:3000",  # or other frontend dev ports
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods
    allow_headers=["*"],  # allow all headers
)

@app.get("/")
def root():
    return {"status": "ok", "service": "FlyWise backend"}
