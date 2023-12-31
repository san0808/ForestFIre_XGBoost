import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
import pickle

# Load the data
data_path = 'data/forestfires.csv'
data = pd.read_csv(data_path)

# One-Hot Encode the 'month' and 'day' columns
data = pd.get_dummies(data, columns=['month', 'day'])

# Preprocess the data (assuming 'area' is the target variable and the rest are features)
X = data.drop(columns=['area'])
y = data['area']

# Print the data types
print(X.dtypes)

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply log transformation to the target variable to handle its skewed distribution
y_train_log = np.log1p(y_train)

# Best parameters for XGBoost
best_params = {
    'colsample_bytree': 0.6,
    'gamma': 0.2,
    'learning_rate': 0.01,
    'max_depth': 3,
    'min_child_weight': 1,
    'subsample': 0.8,
    'objective': 'reg:squarederror',
    'n_estimators': 150,
    'random_state': 42
}

# Train the model
xgb_model = xgb.XGBRegressor(**best_params)
xgb_model.fit(X_train, y_train_log)

# Save the trained model to a file
model_path = 'model/xgb_model.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(xgb_model, f)

print(f"Model trained and saved at {model_path}")
