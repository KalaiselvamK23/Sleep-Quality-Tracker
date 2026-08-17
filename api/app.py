from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel

app = FastAPI(
    title="Sleep Quality Tracker App",
    description="API for predicting sleep efficiency",
    version="1.0.0"
)

# load the trained model and scaler
model = joblib.load("models/sleep_efficiency_model.pkl")

class SleepData(BaseModel):
    Age: int
    Gender: int
    Sleep_duration: float
    REM_sleep_percentage: int
    Deep_sleep_percentage: int
    Light_sleep_percentage: int
    Awakenings: float
    Caffeine_consumption: float
    Alcohol_consumption: float
    Smoking_status: int
    Exercise_frequency: float
    Bedtime_hour: float
    Wakeup_hour: float


@app.post("/predict")
def predict_sleep_efficiency(data: SleepData):

    input_data = pd.DataFrame([[
        data.Age,
        data.Gender,
        data.Sleep_duration,
        data.REM_sleep_percentage,
        data.Deep_sleep_percentage,
        data.Light_sleep_percentage,
        data.Awakenings,
        data.Caffeine_consumption,
        data.Alcohol_consumption,
        data.Smoking_status,
        data.Exercise_frequency,
        data.Bedtime_hour,
        data.Wakeup_hour
    ]], columns=[
        "Age",
        "Gender",
        "Sleep duration",
        "REM sleep percentage",
        "Deep sleep percentage",
        "Light sleep percentage",
        "Awakenings",
        "Caffeine consumption",
        "Alcohol consumption",
        "Smoking status",
        "Exercise frequency",
        "Bedtime_hour",
        "Wakeup_hour"
    ])

    #input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_data)[0]
    prediction_percentage = prediction * 100

    if prediction_percentage >= 85:
        quality = "Excellent"
    elif prediction_percentage >= 75:
        quality = "Good"
    elif prediction_percentage >= 60:
        quality = "Moderate"
    else:
        quality = "Needs Improvement"

    return {
        "Sleep_efficiency": round(float(prediction), 4),
        "Sleep_efficiency_percentage": round(float(prediction * 100), 2),
        "Sleep_quality": quality
    }


@app.get("/")
def home():
    return{
        "message": "Sleep Quality Tracker API is running"
    }