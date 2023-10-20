from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle as pickle
import numpy as np

app = FastAPI()

# Load the trained model
with open('model/xgb_model.pkl', 'rb') as f:
    xgb_model = pickle.load(f)

# Define the input model
class FireFeatures(BaseModel):
    features: list[float]

@app.post("/predict/")
def predict_fire(data: FireFeatures):
    try:
        # Predict the burned area
        predicted_log_area = xgb_model.predict(np.array([data.features]))
        predicted_area = float(np.expm1(predicted_log_area)[0])  # Convert to native Python float
        
        # Classify based on the threshold
        if predicted_area > 0.26:  # 0.26 hectares threshold
            return {"prediction": "Fire", "predicted_area": predicted_area}
        else:
            return {"prediction": "No Fire", "predicted_area": predicted_area}
    except:
        raise HTTPException(status_code=400, detail="Model prediction failed.")