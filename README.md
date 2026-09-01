![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-FF4B4B?logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.9.0-F7931E?logo=scikit-learn)
![Tests](https://img.shields.io/badge/Tests-8%20Passed-success)
![License](https://img.shields.io/badge/License-MIT-green)

[🚀 Live Demo](https://sleep-quality-tracker-2smetxsupaxucux95svsk4.streamlit.app/) 
[📡 API](https://sleep-quality-api.onrender.com/)
[📖 API Docs](https://sleep-quality-api.onrender.com/docs)

# Sleep Quality Tracker

A machine learning-based web application that predicts sleep efficiency and classifies overall sleep quality based on sleep patterns and lifestyle factors.

## Overview

Sleep Quality Tracker is an end-to-end machine learning project developed to analyze sleep-related data and predict an individual's sleep efficiency.

The project includes:

- Exploratory Data Analysis (EDA)
- Machine learning model comparison and selection
- Sleep efficiency prediction
- Sleep quality classification
- FastAPI backend for model inference
- Streamlit frontend for user interaction
- Automated API testing using Pytest
- Continuous Integration using GitHub Actions
- Cloud deployment

The trained machine learning model predicts sleep efficiency and categorizes the result into:

- Excellent
- Good
- Moderate
- Needs Improvement

## Features

- Predict sleep efficiency from sleep and lifestyle parameters
- Classify predicted sleep quality
- Interactive Streamlit user interface
- REST API using FastAPI
- Input validation using Pydantic
- Validation for sleep-stage percentages
- Automated API test suite
- GitHub Actions CI pipeline
- Cloud-hosted FastAPI backend
- Cloud-hosted Streamlit frontend

## Technologies Used

### Programming Language

- Python

### Machine Learning

- Pandas
- NumPy
- Scikit-learn
- Joblib

### Visualization and Analysis

- Matplotlib
- Seaborn
- Jupyter Notebook

### Backend

- FastAPI
- Uvicorn
- Pydantic

### Frontend

- Streamlit

### Testing and CI

- Pytest
- Pytest-Cov
- GitHub Actions

### Deployment

- Render
- Streamlit Community Cloud

## Dataset

The project uses a sleep efficiency dataset containing sleep patterns and lifestyle-related attributes.

Important features include:

- Age
- Gender
- Sleep duration
- REM sleep percentage
- Deep sleep percentage
- Light sleep percentage
- Awakenings
- Caffeine consumption
- Alcohol consumption
- Smoking status
- Exercise frequency
- Bedtime
- Wakeup time

The dataset was cleaned and prepared before model training.

## Model Selection

Multiple regression models were evaluated to determine the most suitable model for predicting sleep efficiency.

The evaluated models included:

| Model | R² Score |
|---|---:|
| Linear Regression | 0.7918 |
| Decision Tree | 0.6574 |
| Random Forest | 0.8508 |
| Gradient Boosting | 0.8562 |

Gradient Boosting achieved the best baseline performance.

The model was subsequently tuned using:

```text
learning_rate = 0.03
max_depth = 2
n_estimators = 150
```

The tuned Gradient Boosting model achieved:

* MAE: 0.0397
* MSE: 0.0026
* RMSE: 0.0507
* R²: 0.8620

Therefore, the tuned Gradient Boosting Regressor was selected as the final prediction model.

## Feature Importance

The most influential features in the final model were:

| Feature                | Importance |
| ---------------------- | ---------: |
| Light sleep percentage |     0.4370 |
| Deep sleep percentage  |     0.3582 |
| Awakenings             |     0.1509 |
| Smoking status         |     0.0282 |
| Age                    |     0.0133 |
| Alcohol consumption    |     0.0055 |
| Exercise frequency     |     0.0040 |

Light sleep percentage and deep sleep percentage were the most important features according to the trained model.

## Folder Structure

```text
Sleep-Quality-Tracker/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── api/
│   ├── __init__.py
│   └── app.py
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── Sleep_Efficiency.csv
│   ├── sleep_efficiency_cleaned.csv
│   └── feature_importance.csv
│
├── models/
│   ├── sleep_efficiency_model.pkl
│   └── scaler.pkl
│
├── notebooks/
│   ├── 01_Exploratory_Data_Analysis.ipynb
│   └── Sleep_efficiency,loaded.ipynb
│
├── src/
│   ├── improved_sleep_efficiency_model.py
│   ├── load_sleep_data.py
│   └── sleep_efficiency_predictor.py
│
├── tests/
│   └── test_api.py
│
├── pytest.ini
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/KalaiselvamK23/Sleep-Quality-Tracker.git
cd Sleep-Quality-Tracker
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Run the FastAPI Backend

```bash
uvicorn api.app:app --reload
```

The API will be available locally at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### Run the Streamlit Application

Open another terminal and activate the virtual environment if required.

Then run:

```bash
streamlit run app/streamlit_app.py
```

The Streamlit application will open in your browser.

The Streamlit application communicates with the FastAPI backend using the configured `API_URL`.

## API

### Health Check

```text
GET /
```

Response:

```json
{
  "message": "Sleep Quality Tracker API is running"
}
```

### Prediction

```text
POST /predict
```

The API accepts sleep and lifestyle information and returns the predicted sleep efficiency and sleep quality.

Example response:

```json
{
  "Sleep_efficiency": 0.9192,
  "Sleep_efficiency_percentage": 91.92,
  "Sleep_quality": "Excellent"
}
```

### Sleep Quality Classification

The predicted sleep efficiency is classified as:

| Sleep Efficiency | Quality           |
| ---------------: | ----------------- |
|            ≥ 85% | Excellent         |
|     75% – 84.99% | Good              |
|     60% – 74.99% | Moderate          |
|            < 60% | Needs Improvement |

## Input Validation

The API validates user inputs using Pydantic.

The application also validates the relationship between REM, deep, and light sleep percentages.

For example:

```text
REM sleep       = 20%
Deep sleep      = 25%
Light sleep     = 65%

Total           = 110%
```

This is an invalid sleep-stage composition.

The API returns:

```text
422 Unprocessable Entity
```

The Streamlit interface also prevents invalid sleep-stage combinations before sending the request to the API.

## Testing

The project includes automated API tests using Pytest.

Run the tests with:

```bash
pytest
```

Current test status:

```text
8 passed
```

The test suite covers:

* Valid prediction requests
* High sleep quality prediction
* Good sleep quality classification
* Needs Improvement classification
* Invalid age
* Missing required fields
* Invalid sleep-stage percentages
* Home endpoint

## Continuous Integration

GitHub Actions is configured to automatically run the test suite whenever changes are pushed to the repository.

Workflow:

```text
.github/workflows/tests.yml
```

The CI pipeline currently passes successfully.

## Deployment

### FastAPI Backend

The FastAPI backend is deployed using Render.

Production API:

[https://sleep-quality-api.onrender.com](https://sleep-quality-api.onrender.com)

Interactive API documentation:

[https://sleep-quality-api.onrender.com/docs](https://sleep-quality-api.onrender.com/docs)

### Streamlit Frontend

The Streamlit frontend is deployed using Streamlit Community Cloud.

Production application:

[https://sleep-quality-tracker-2smetxsupaxucux95svsk4.streamlit.app/](https://sleep-quality-tracker-2smetxsupaxucux95svsk4.streamlit.app/)

The Streamlit application communicates with the deployed FastAPI backend through the `API_URL` configuration.

## End-to-End Architecture

```text
                    User
                     │
                     ▼
            ┌─────────────────┐
            │    Streamlit    │
            │   Frontend UI   │
            └────────┬────────┘
                     │
                  API_URL
                     │
                     ▼
            ┌─────────────────┐
            │     FastAPI     │
            │     Backend     │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Gradient Boosting│
            │      Model      │
            └────────┬────────┘
                     │
                     ▼
            Sleep Efficiency
                     │
                     ▼
          Sleep Quality Classification
```

## Model Results

The final tuned Gradient Boosting model achieved:

```text
MAE  : 0.0397
MSE  : 0.0026
RMSE : 0.0507
R²   : 0.8620
```

The model demonstrated strong predictive performance for sleep efficiency on the evaluated dataset.

## Deployment Validation

The deployed application was tested end-to-end.

Validation results:

| Component                         | Status     |
| --------------------------------- | ---------- |
| FastAPI deployment                | Passed     |
| FastAPI health endpoint           | Passed     |
| FastAPI `/predict` endpoint       | Passed     |
| API input validation              | Passed     |
| Streamlit deployment              | Passed     |
| Streamlit → FastAPI communication | Passed     |
| Invalid sleep-stage validation    | Passed     |
| Automated API tests               | 8/8 Passed |
| GitHub Actions CI                 | Passed     |

## Model Selection Reference

The initial model selection and experimentation were performed using Google Colab.

Model Selector:

[https://colab.research.google.com/drive/1yeajPJW3vC4jW5FDX79xeH-_JFnTXNN0?usp=sharing](https://colab.research.google.com/drive/1yeajPJW3vC4jW5FDX79xeH-_JFnTXNN0?usp=sharing)

## Future Improvements

Possible future improvements include:

* Adding personalized sleep recommendations
* Adding sleep-history visualization
* Adding user authentication
* Adding persistent user profiles
* Adding database integration
* Improving model performance with additional data
* Adding model monitoring
* Adding automated model retraining
* Improving UI and data visualization
* Adding Docker-based deployment
* Adding more advanced sleep analytics

## Author

**Kalaiselvam K**

GitHub:

[https://github.com/KalaiselvamK23/Sleep-Quality-Tracker](https://github.com/KalaiselvamK23/Sleep-Quality-Tracker)

## 📄 License

This project is licensed under the MIT License.
