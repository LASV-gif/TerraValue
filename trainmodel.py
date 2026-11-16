import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


def train_terraval_models():
  # 1. Load the synthetic dataset
  print('Loading natural capital dataset...')
  df = pd.read_csv('natural_capital_data.csv')

  # 2. Define Features (X) and Targets (y)
  X = df[
      [
          'ndvi',
          'tree_cover_density',
          'water_stress_index',
          'bii',
          'proximity_to_threat',
      ]
  ]
  y_value = df['asset_value_per_ha']
  y_risk = df['depreciation_risk_pct']

  # 3. Train-Test Split (80% training, 20% testing)
  X_train, X_test, y_val_train, y_val_test = train_test_split(
      X, y_value, test_size=0.2, random_state=42
  )
  _, _, y_risk_train, y_risk_test = train_test_split(
      X, y_risk, test_size=0.2, random_state=42
  )

  # 4. Initialize and Train Random Forest Regressors
  print('Training Asset Value Regressor...')
  rf_value = RandomForestRegressor(n_estimators=100, random_state=42)
  rf_value.fit(X_train, y_val_train)

  print('Training Depreciation Risk Regressor...')
  rf_risk = RandomForestRegressor(n_estimators=100, random_state=42)
  rf_risk.fit(X_train, y_risk_train)

  # 5. Evaluate Model Performance
  val_preds = rf_value.predict(X_test)
  risk_preds = rf_risk.predict(X_test)

  print('\n--- Model Evaluation Metrics ---')
  print(
      'Asset Value MAE: $'
      f'{mean_absolute_error(y_val_test, val_preds):.2f}/ha'
  )
  print(f'Asset Value R² Score: {r2_score(y_val_test, val_preds):.4f}')
  print(
      'Depreciation Risk MAE:'
      f' {mean_absolute_error(y_risk_test, risk_preds):.2f}%'
  )
  print(f'Depreciation Risk R² Score: {r2_score(y_risk_test, risk_preds):.4f}')

  # 6. Save the trained models for web deployment / app usage
  joblib.dump(rf_value, 'asset_value_model.pkl')
  joblib.dump(rf_risk, 'depreciation_risk_model.pkl')
  print(
      '\nModels successfully trained and saved as `asset_value_model.pkl` and'
      ' `depreciation_risk_model.pkl`!'
  )


if __name__ == '__main__':
  train_terraval_models()