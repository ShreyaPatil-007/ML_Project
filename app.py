
from datetime import date

import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel, Field

# Load saved model
saved = joblib.load("models/adaboost_model.pkl")
model = saved["model"]
features = saved["features"]

app = FastAPI(
    title="SmartStock AI",
    description="Retail demand forecasting API",
    version="1.0.0"
)


class DemandRequest(BaseModel):
    date: date
    demand_lag_1: float = Field(ge=0)
    demand_lag_7: float = Field(ge=0)
    demand_lag_14: float = Field(ge=0)
    rolling_mean_7: float = Field(ge=0)


@app.get("/")
def home():
    return {
        "message": "SmartStock AI API is running!"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict_demand(request: DemandRequest):
    prediction_date = pd.Timestamp(request.date)

    input_data = pd.DataFrame([{
        "day_of_week": prediction_date.dayofweek,
        "month": prediction_date.month,
        "day_of_month": prediction_date.day,
        "demand_lag_1": request.demand_lag_1,
        "demand_lag_7": request.demand_lag_7,
        "demand_lag_14": request.demand_lag_14,
        "rolling_mean_7": request.rolling_mean_7
    }])[features]

    prediction = float(model.predict(input_data)[0])

    return {
        "date": request.date.isoformat(),
        "store_id": "S001",
        "product_id": "P0001",
        "predicted_demand": round(max(0, prediction), 2)
    }
