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
   - An API endpoint `/predict/` is exposed which takes a list of features as input and returns the predicted area of the forest fire. If the predicted area is greater than 0.26 hectares, it classifies it as "Fire"; otherwise, "No Fire".

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
- In the "Request body" section, you'll see a field named `features`. This is where you'll input the data for prediction.
- Enter the desired input values in the `features` field.

## Sample Inputs

### Sample for a potential fire scenario:
Assume that this is during the month of August (peak of summer), on a Sunday, with relatively high temperature, low humidity, and strong winds:
```
[4, 5, 91.6, 145.4, 608.2, 10.7, 19.5, 70, 6.7, 0.0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
```
### Sample for a less likely fire scenario:
Assume that this is during the month of December (winter), on a Wednesday, with low temperature, high humidity, and light winds:
```
[7, 4, 84.1, 27.8, 290.0, 5.3, 5.2, 95, 2.2, 0.0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
```

These samples are based on logical assumptions and might not reflect real-world scenarios perfectly. However, they should provide a starting point for testing in the Swagger UI.

You can input these values into the Swagger UI for the /predict/ endpoint and check the model's prediction.

