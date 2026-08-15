import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Sleep Quality Tracker",
    page_icon="🌙",
    layout="wide"
)

st.title("🌙 Sleep Quality Tracker")
st.write(
    "Predict your sleep efficiency based on your sleep habits "
    "and lifestyle factors"
)

st.divider()

st.subheader("personal information")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age",
        min_value=1,
        max_value=100,
        value=25
    )

with col2:
    gender = st.selectbox(
        "Gender",
        ["Female", "Male"]
    )

st.subheader("Sleep Information")

col1, col2, col3 = st.columns(3)

with col1:
    sleep_duration = st.number_input(
        "Sleep Duration (hours)",
        min_value=0.0,
        max_value=24.0,
        value=7.5,
        step=0.5
    )

with col2:
    rem_sleep = st.number_input(
        "REM Sleep Percentage",
        min_value=0,
        max_value=100,
        value=20
    )

with col3:
    deep_sleep = st.number_input(
        "Deep Sleep Percentage",
        min_value=0,
        max_value=100,
        value=25
    )

col1, col2, col3 = st.columns(3)

with col1:
    light_sleep = st.number_input(
        "Light Sleep Percentage",
        min_value=0,
        max_value=100,
        value=55
    )

with col2:
    awakenings = st.number_input(
        "Awakenings",
        min_value=0.0,
        max_value=20.0,
        value=1.0,
        #step=1.0
    )

with col3:
    caffeine = st.number_input(
        "Caffeine Consumption",
        min_value=0.0,
        max_value=20.0,
        value=1.0,
        step=1.0
    )

st.subheader("Lifestyle Information")

col1, col2, col3 = st.columns(3)

with col1:
    alcohol = st.number_input(
        "Alcohol Consumption",
        min_value=0.0,
        max_value=20.0,
        value=0.0,
        step=1.0
    )

with col2:
    smoking = st.selectbox(
        "Smoking Status",
        ["No", "Yes"]
    )

with col3:
    exercise = st.number_input(
        "Exercise Frequency",
        min_value=0.0,
        max_value=20.0,
        value=3.0,
        step=1.0
    )

st.subheader("Sleep Schedule")

col1, col2 = st.columns(2)

with col1:
    bedtime = st.time_input("Bedtime")

with col2:
    wakeup = st.time_input("Wakeup Time")

st.divider()

if st.button("Predict Sleep Efficiency", type="primary"):
    gender_value = 1 if gender == "Male" else 0
    smoking_value = 1 if smoking == "Yes" else 0
    bedtime_hour = bedtime.hour + bedtime.minute / 60
    wakeup_hour = wakeup.hour + wakeup.minute / 60

    payload = {
        "Age": age,
        "Gender": gender_value,
        "Sleep_duration": sleep_duration,
        "REM_sleep_percentage": rem_sleep,
        "Deep_sleep_percentage": deep_sleep,
        "Light_sleep_percentage": light_sleep,
        "Awakenings": awakenings,
        "Caffeine_consumption": caffeine,
        "Alcohol_consumption": alcohol,
        "Smoking_status": smoking_value,
        "Exercise_frequency": exercise,
        "Bedtime_hour": bedtime_hour,
        "Wakeup_hour": wakeup_hour
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=payload
        )

        if response.status_code == 200:
            result = response.json()

            quality = result["Sleep_quality"]

            if quality == "Excellent":
                recommendation = "Great job! Your predicted sleep quality is excellent. Keep maintaining your current sleep habits."
            elif quality == "Good":
                recommendation = "Your predicted sleep quality is good. Continue maintaining consistent sleep and healthy lifestyle habits."
            elif quality == "Moderate":
                recommendation = "Your predicted sleep quality is moderate. Consider improving sleep consistency, reducing disturbances, and maintaining healthy sleep habits."
            else:
                recommendation = "Your predicted sleep quality needs improvement. Focus on consistent sleep schedules and healthier lifestyle habits."
            

            st.success("Prediction completed successfully!")
            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Sleep Effficiency",
                    f"{result['Sleep_efficiency_percentage']:.2f}%"
                )

            with col2:
                st.metric(
                    "Sleep Quality",
                    result["Sleep_quality"]
                )

            st.info(recommendation)
        else:
            st.error(
                f"API Error: {response.status_code}"
            )

    except requests.exceptions.ConnectionError:
        st.error(
            "Could not connect to the Sleep quality Tracker API. "
            "Make sure FasTAPI is running"
        )