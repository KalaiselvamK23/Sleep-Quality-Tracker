import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import os

HISTORY_FILE = "data/sleep_history.csv"

def generate_recommendations(
    sleep_duration,
    rem_sleep,
    deep_sleep,
    light_sleep,
    awakenings,
    caffeine,
    alcohol,
    smoking,
    exercise
):
    recommendations = []

    if sleep_duration < 7:
        recommendations.append(
            "Try to increase your sleep duration toward 7–9 hours."
        )

    if awakenings > 2:
        recommendations.append(
            "Frequent awakenings may affect sleep quality. "
            "Try to maintain a quiet and comfortable sleep environment."
        )

    if caffeine > 5:
        recommendations.append(
            "Consider reducing caffeine consumption, especially later in the day."
        )

    if alcohol > 2:
        recommendations.append(
            "Reducing alcohol consumption may help improve sleep quality."
        )

    if smoking == "Yes":
        recommendations.append(
            "Reducing or avoiding smoking may support healthier sleep."
        )

    if exercise < 2:
        recommendations.append(
            "Regular physical activity may help improve sleep quality."
        )

    if rem_sleep < 20:
        recommendations.append(
            "Your REM sleep percentage is relatively low. "
            "Maintaining a consistent sleep schedule may help."
        )

    if deep_sleep < 20:
        recommendations.append(
            "Your deep sleep percentage is relatively low. "
            "Focus on a consistent bedtime and a comfortable sleep environment."
        )

    if not recommendations:
        recommendations.append(
            "Your sleep and lifestyle inputs look balanced. "
            "Keep maintaining your current healthy habits."
        )

    return recommendations

feature_importance = pd.read_csv(
    "data/feature_importance.csv"
)

st.set_page_config(
    page_title="Sleep Quality Tracker",
    page_icon="🌙",
    layout="wide"
)

if "sleep_history" not in st.session_state:
    if os.path.exists(HISTORY_FILE):
        st.session_state.sleep_history = pd.read_csv(
            HISTORY_FILE
        ).to_dict("records")
    else:
        st.session_state.sleep_history = []

st.title("🌙 Sleep Quality Tracker")

st.markdown(
    "### Understand your sleep. Improve your habits."
)

st.write(
    "Enter your sleep, lifestyle, and daily routine information "
    "to estimate your sleep efficiency and receive personalized insights."
)

st.divider()

with st.container(border=True):
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

with st.container(border=True):
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
            step=1.0
        )

    with col3:
        caffeine = st.number_input(
            "Caffeine Consumption",
            min_value=0.0,
            max_value=20.0,
            value=1.0,
            step=1.0
        )
with st.container(border=True):
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


with st.container(border=True):
    st.subheader("Sleep Schedule")

    col1, col2 = st.columns(2)

    with col1:
        bedtime = st.time_input("Bedtime")

    with col2:
        wakeup = st.time_input("Wakeup Time")

    st.divider()

    if st.button("Predict Sleep Efficiency", type="primary"):
        if rem_sleep + deep_sleep + light_sleep != 100:
            st.error(
                "REM, Deep, and Light sleep percentages "
                "must total exactly 100%."
            )
            st.stop()

        if sleep_duration < 1 or sleep_duration > 16:
            st.error(
                "sleep duration must be between 1 and 16 hours."
            )
            st.stop()
            
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

                st.session_state.sleep_history.append({
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Sleep Efficiency": result["Sleep_efficiency_percentage"],
                    "Sleep Quality": result["Sleep_quality"],
                    "Sleep Duration": sleep_duration,
                    "REM %": rem_sleep,
                    "Deep Sleep %": deep_sleep,
                    "Light Sleep %": light_sleep,
                    "Awakenings": awakenings
                })

                history_df = pd.DataFrame(st.session_state.sleep_history)

                history_df.to_csv(
                    HISTORY_FILE,
                    index=False
                )

                st.success("prediction completed successfully!")
                st.subheader("Your Sleep Analysis")

                recommendations = generate_recommendations(
                    sleep_duration,
                    rem_sleep,
                    deep_sleep,
                    light_sleep,
                    awakenings,
                    caffeine,
                    alcohol,
                    smoking,
                    exercise
                )
                st.subheader("🎯 Your Sleep Result")

                st.subheader("🎯 Your Sleep Result")

                with st.container(border=True):
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.markdown("### Sleep Efficiency")
                        st.markdown(
                            f"### {result['Sleep_efficiency_percentage']:.2f}%"
                        )

                        st.progress(
                            min(
                                int(result["Sleep_efficiency_percentage"]),
                                100
                            )
                        )

                    with col2:
                        st.markdown("### Sleep Quality")
                        st.markdown(
                            f"### {result['Sleep_quality']}"
                        )

                    st.caption(
                        "This score represents the predicted efficiency of your sleep."
                    )

                st.subheader("💡 Personalized Recommendations")

                with st.expander(
                    f"View {len(recommendations)} personalized recommendation(s)"
                ):
                    for recommendation in recommendations:
                        st.info(recommendation)

                st.subheader("🛌 Sleep Composition")

                sleep_composition = pd.DataFrame({
                    "Sleep Stage": ["REM", "Deep", "Light"],
                    "Percentage": [rem_sleep, deep_sleep, light_sleep]
                })

                st.bar_chart(
                    sleep_composition,
                    x="Sleep Stage",
                    y="Percentage"
                )

                st.subheader("📋 Sleep Metrics")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Sleep Duration", f"{sleep_duration:.1f} hrs")

                with col2:
                    st.metric("REM Sleep", f"{rem_sleep}%")

                with col3:
                    st.metric("Deep Sleep", f"{deep_sleep}%")

                with col4:
                    st.metric("Awakenings", f"{awakenings:.0f}")


                if result["Sleep_quality"] == "Excellent":
                    interpretation = "Your predicted sleep efficiency is excellent. Your current sleep pattern appears to be supporting good sleep quality."
                elif result["Sleep_quality"] == "Good":
                    interpretation = "Your predicted sleep efficiency is good. Maintaining consistent sleep and healthy habits can help preserve it."
                elif result["Sleep_quality"] == "Moderate":
                    interpretation = "Your predicted sleep efficiency is moderate. Improving sleep duration, consistency, and lifestyle habits may help."
                else:
                    interpretation = "Your predicted sleep efficiency needs improvement. Focus on consistent sleep, reducing disturbances, and healthier lifestyle habits."

                st.info(
                    f"**Sleep Insight:** {interpretation}"
                )

                st.divider()
                with st.expander("About Your Prediction"):
                    st.write(
                            "The prediction is generated using a tuned Gradient Boosting "
                            "regression model trained on sleep and lifestyle characteristics."
                    )

                    st.write("The most influential features in the trained model were:")

                    st.dataframe(
                        feature_importance.head(5),
                        hide_index=True,
                        use_container_width=True
                    )

                    st.bar_chart(
                        feature_importance.head(5),
                        x="Feature",
                        y="Importance",
                        horizontal=True
                    )
            else:
                st.error(
                    f"API Error: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the Sleep quality Tracker API. "
                "Make sure FasTAPI is running"
            )


# sleep history
st.divider()

st.subheader("📈 Sleep History")

if st.session_state.sleep_history:
    history_df = pd.DataFrame(st.session_state.sleep_history)

    st.dataframe(
        history_df,
        hide_index=True,
        use_container_width=True
    )

    if st.button("🗑️ Clear Sleep History"):
        st.session_state.sleep_history = []

        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)

        st.success("Sleep history cleared successfully.")
        st.rerun()

    st.subheader("Sleep Efficiency Trend")

    if st.session_state.sleep_history:
        history_df = pd.DataFrame(st.session_state.sleep_history)

        st.line_chart(
            history_df,
            x="Date",
            y="Sleep Efficiency"
        )

    else:
        st.info(
            "No sleep history available yet."
            "Make a prediction to start tracking. "
        )

    
else:
    st.info("No sleep history available yet."
            "Make a prediction to start tracking."
            )