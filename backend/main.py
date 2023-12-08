from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
from datetime import datetime
import requests

import uvicorn

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

# Add this before defining the app
origins = [
    "http://192.168.128.34",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model
with open('model/xgb_model.pkl', 'rb') as f:
    xgb_model = pickle.load(f)

# Define the input model
class FireFeatures(BaseModel):
    rain: float
    wind: float

def calculate_ffmc(temp, rh, rain, wind):
    # Constants
    E = 0.97  # used to calculate m
    m0 = 9.5   # Initial moisture content assumed
    
    # Adjustments for rain
    if rain > 0.5:
        mr = m0 + 42.5 * rain * np.exp(-100 / (251 - m0)) - 42.5 * rain * np.exp(-100 / 251)
    else:
        mr = m0

    # Calculation of FFMC
    mo = (147.2 * (101 - mr)) / (59.5 + mr)  # intermediate value
    ko = 0.424 * (1 - ((100 - rh) / 100) ** 1.7) + 0.0694 * np.sqrt(wind)
    k = ko * 0.581 * np.exp(0.0365 * temp)
    m = mo + 1000 * (1 - np.exp(-k))

    ffmc = 59.5 * (250 - m) / (147.2 + m)
    return ffmc


def calculate_dmc(temp, rh, rain):
    # Constants
    Le = [6.5, 7.5, 9.0, 12.5, 13.0, 13.0, 13.0, 11.0, 10.0, 8.5, 8.0, 7.0]  # month-based coefficients
    month = datetime.now().month - 1  # Assuming current month
    b = 100 / (0.5 + 0.3 * rh)
    if temp < -1.1:
        temp = -1.1
    
    m = 20 

    # Adjustments for rain
    if rain > 1.5:
        re = 0.92 * rain - 1.27
        mo = 20 + np.exp(5.6348 - b)
        rf = re / (0.897 * np.exp(b * (0.00163 * Le[month] * np.exp(0.00176 * temp) - 1.0)))
        m = mo + 100 * rf

    dmc = 244.72 - 43.43 * np.log(m)
    return dmc


def calculate_isi(wind, ffmc):
    mo = 147.2 * (101 - ffmc) / (59.5 + ffmc)
    ff = 19.115 * np.exp(mo * -0.1386) * (1 + (mo ** 5.31) / 49300000)
    isi = ff * np.exp(0.05039 * wind)
    return isi


def calculate_dc(temp, rain):
    # Constants
    Le = [6.5, 7.5, 9.0, 12.5, 13.0, 13.0, 13.0, 11.0, 10.0, 8.5, 8.0, 7.0]  # month-based coefficients
    month = datetime.now().month - 1  # Assuming current month
    if temp < -2.8:
        temp = -2.8
    
    Dr=400

    # Adjustments for rain
    if rain > 2.8:
        re = 0.83 * rain - 1.27
        Qo = 800 * np.exp(-Le[month] / 800)
        Qr = Qo + 3.937 * re
        Dr = 400 * np.log(800 / Qr)

    dc = Dr + 1.5 * temp
    return dc

def get_one_hot_month_features(current_month):
    month_columns = [f'month_{i}' for i in range(1, 13)]
    return [1 if i == current_month else 0 for i in range(1, 13)]

def get_one_hot_day_features(current_day):
    day_columns = [f'day_{i}' for i in range(1, 8)]
    return [1 if i == current_day else 0 for i in range(1, 8)]


def get_arduino_data():
    try:
        # Replace the URL with your Arduino server endpoint for getting data
        response = requests.get("http://192.168.43.214/getData")
        response.raise_for_status()  # Raise an exception for bad responses
        humidity, temperature = map(float, response.text.split(','))
        return humidity, temperature
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to get data from Arduino server: {str(e)}")


@app.post("/predict/")
def predict_fire(data: FireFeatures):
    try:
        RH, temp = get_arduino_data()
        current_month = datetime.now().month
        current_day = datetime.now().weekday() + 1  # Python weekdays start from 0 (Monday)

        # Calculate FWI components
        FFMC = calculate_ffmc(temp, RH, data.rain, data.wind)
        DMC = calculate_dmc(temp, RH, data.rain)
        ISI = calculate_isi(data.wind, FFMC)
        DC = calculate_dc(temp, data.rain)

        # One-hot encoding for month and day
        month_features = get_one_hot_month_features(current_month)
        day_features = get_one_hot_day_features(current_day)

        # Form the complete feature array for prediction
        features = [temp,RH, data.rain, data.wind, FFMC, DMC, ISI, DC] + month_features + day_features

        # Predict the burned area
        predicted_log_area = xgb_model.predict(np.array([features]))
        predicted_area = float(np.expm1(predicted_log_area)[0])

        # Classify based on the threshold
        if predicted_area > 3:
            return {"prediction": "Fire", "predicted_area": predicted_area}
        else:
            return {"prediction": "No Fire", "predicted_area": predicted_area}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Model prediction failed: {str(e)}")


if app == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

