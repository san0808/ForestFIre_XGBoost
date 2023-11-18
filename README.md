# Forest Fire Prediction using XGBoost

This repository contains a machine learning model that predicts the area of forest fire using the XGBoost algorithm. The model is trained on the `forestfires.csv` dataset and is exposed as an API using FastAPI.

## Repository Structure

- `backend/`: Contains the main codebase for the project.
  - [`data/forestfires.csv`](https://github.com/san0808/ForestFIre_XGBoost/blob/main/backend/data/forestfires.csv): The dataset used for training the model.
  - [`main.py`](https://github.com/san0808/ForestFIre_XGBoost/blob/main/backend/main.py): The FastAPI application that exposes the trained model as an API endpoint.
  - [`train.py`](https://github.com/san0808/ForestFIre_XGBoost/blob/main/backend/train.py): The script used to train the XGBoost model.
  - [`model/xgb_model.pkl`](https://github.com/san0808/ForestFIre_XGBoost/blob/main/backend/model/xgb_model.pkl): The trained XGBoost model saved as a pickle file.
  - [`requirements.txt`](https://github.com/san0808/ForestFIre_XGBoost/blob/main/backend/requirements.txt): Lists the Python packages required to run the project.

## How it Works

1. **Training the Model ([train.py](https://github.com/san0808/ForestFIre_XGBoost/blob/main/backend/train.py)):**
   - The dataset is loaded and preprocessed.
   - One-hot encoding is applied to the 'month' and 'day' columns.
   - The data is split into training and test sets.
   - The target variable (`area`) undergoes a log transformation to handle its skewed distribution.
   - The XGBoost model is trained with specific parameters.
   - The trained model is saved as a pickle file.

2. **API Endpoint ([main.py](https://github.com/san0808/ForestFIre_XGBoost/blob/main/backend/main.py)):**
   - The trained model is loaded.
   - An API endpoint `/predict/` is exposed, which takes `temp`, `RH`, `rain`, and `wind` as input, calculates additional features like FFMC, DMC, ISI, and DC, and returns the predicted area of the forest fire. If the predicted area is greater than 0.26 hectares, it classifies it as "Fire"; otherwise, "No Fire".

## Making Requests using FastAPI's Swagger UI

FastAPI provides an interactive API documentation using Swagger UI. Here's how you can use it:

1. **Run the FastAPI application**:
   ```
   uvicorn backend.main:app --reload
   ```
   
## Access the Swagger UI:
Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). This will open the Swagger UI where you can see all the available API endpoints.

## Using the `/predict/` endpoint:
- In the Swagger UI, locate the `/predict/` POST endpoint.
- Click on the "Try it out" button.
- Provide input values for `temp`, `RH`, `rain`, and `wind`.
- Click "Execute" to see the model's prediction.

## Sample Inputs

### Sample for a Potential Fire Scenario:
- Assume the following conditions: high temperature, low humidity, and strong winds.
- Input: `{"temp": 30, "RH": 20, "rain": 0, "wind": 10}`

### Sample for a Less Likely Fire Scenario:
- Assume conditions typical of a wet and calm day.
- Input: `{"temp": 15, "RH": 80, "rain": 5, "wind": 3}`

These samples are based on logical assumptions and might not reflect real-world scenarios perfectly. However, they should provide a starting point for testing in the Swagger UI.

You can input these values into the Swagger UI for the /predict/ endpoint and check the model's prediction.

