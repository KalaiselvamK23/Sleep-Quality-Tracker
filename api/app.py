from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel, Field, model_validator
from pathlib import Path


app = FastAPI(
    title="Sleep Quality Tracker App",
    description="API for predicting sleep efficiency",
    version="1.0.0"
)

# load the trained model and scaler
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "sleep_efficiency_model.pkl"

model = joblib.load(MODEL_PATH)


class SleepData(BaseModel):
    Age: int = Field(..., ge=1, le=100)
    Gender: int
    Sleep_duration: float = Field(..., ge=1, le=16)
    REM_sleep_percentage: int = Field(..., ge=0, le=100)
    Deep_sleep_percentage: int = Field(..., ge=0, le=100)
    Light_sleep_percentage: int = Field(..., ge=0, le=100)
    Awakenings: float = Field(..., ge=0, le=20)
    Caffeine_consumption: float = Field(..., ge=0, le=20)
    Alcohol_consumption: float = Field(..., ge=0, le=20)
    Smoking_status: int
    Exercise_frequency: float = Field(..., ge=0, le=20)
    Bedtime_hour: float
    Wakeup_hour: float
    @model_validator(mode="after")
    def validate_sleep_percentages(self):
        total = (
            self.REM_sleep_percentage
            + self.Deep_sleep_percentage
            + self.Light_sleep_percentage
        )

        if total > 100:
            raise ValueError(
                "REM, Deep, and Light sleep percentages "
                "cannot total more than 100%."
            )

        return self


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