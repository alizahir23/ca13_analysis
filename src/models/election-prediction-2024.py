import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import HuberRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

class MarginPredictor2024:
    def __init__(self):
        self.gb_regressor = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )
        self.robust_regressor = HuberRegressor(epsilon=1.35)
        self.scaler = StandardScaler()
        
    def prepare_historical_data(self):
        """
        Prepare historical election data focusing on margins
        """
        historical_data = pd.DataFrame({
            'year': [2012, 2014, 2016, 2018, 2020, 2022],
            'democratic_margin': [15.6, 12.4, 16.2, 13.8, 19.4, 13.0],  # Margin over Republican
            'dem_registration': [45.2, 45.8, 46.3, 46.9, 47.2, 47.0],
            'rep_registration': [28.1, 27.8, 27.2, 26.8, 26.5, 26.3],
            'turnout_rate': [35.2, 31.8, 38.4, 37.1, 36.8, 35.5],
            'unemployment_rate': [8.9, 8.1, 7.8, 7.5, 7.2, 6.8],
            'presidential_year': [1, 0, 1, 0, 1, 0]
        })
        
        # Calculate additional features
        historical_data['registration_advantage'] = (
            historical_data['dem_registration'] - historical_data['rep_registration']
        )
        historical_data['prev_margin'] = historical_data['democratic_margin'].shift(1)
        
        return historical_data.dropna()
    
    def prepare_2024_features(self):
        """
        Prepare feature set for 2024 prediction
        """
        features_2024 = pd.DataFrame({
            'dem_registration': [47.3],
            'rep_registration': [26.1],
            'turnout_rate': [37.5],
            'unemployment_rate': [6.5],
            'presidential_year': [1],
            'registration_advantage': [21.2],
            'prev_margin': [13.0]
        })
        
        return features_2024
    
    def train_and_predict(self):
        """
        Train model on historical data and predict 2024 margin
        """
        historical_data = self.prepare_historical_data()
        features_2024 = self.prepare_2024_features()
        
        feature_columns = [
            'registration_advantage',
            'turnout_rate',
            'unemployment_rate',
            'presidential_year',
            'prev_margin'
        ]
        
        X = historical_data[feature_columns]
        y = historical_data['democratic_margin']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        X_2024_scaled = self.scaler.transform(features_2024[feature_columns])
        
        # Train models
        self.gb_regressor.fit(X_scaled, y)
        self.robust_regressor.fit(X_scaled, y)
        
        # Generate predictions
        gb_prediction = self.gb_regressor.predict(X_2024_scaled)[0]
        robust_prediction = self.robust_regressor.predict(X_2024_scaled)[0]
        
        # Calculate ensemble prediction (weighted average)
        final_prediction = 0.6 * gb_prediction + 0.4 * robust_prediction
        
        # Get feature importance
        importance = pd.DataFrame({
            'feature': feature_columns,
            'importance': self.gb_regressor.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Calculate model performance metrics
        gb_mse = mean_squared_error(y, self.gb_regressor.predict(X_scaled))
        gb_r2 = r2_score(y, self.gb_regressor.predict(X_scaled))
        
        return {
            'predicted_margin': final_prediction,
            'gb_prediction': gb_prediction,
            'robust_prediction': robust_prediction,
            'feature_importance': importance,
            'model_rmse': np.sqrt(gb_mse),
            'model_r2': gb_r2
        }

if __name__ == "__main__":
    predictor = MarginPredictor2024()
    results = predictor.train_and_predict()
    
    print("\n2024 Election Prediction for CA-13:")
    print(f"Predicted Democratic Margin: {results['predicted_margin']:.1f}%")
    print(f"Model Predictions:")
    print(f"  - Gradient Boosting: {results['gb_prediction']:.1f}%")
    print(f"  - Robust Regression: {results['robust_prediction']:.1f}%")
    
    print("\nModel Performance:")
    print(f"Root Mean Square Error: {results['model_rmse']:.2f} percentage points")
    print(f"R² Score: {results['model_r2']:.3f}")
    
    print("\nKey Predictive Factors:")
    print(results['feature_importance'])
    
    # Save prediction details
    prediction_df = pd.DataFrame({
        'metric': ['Predicted Democratic Margin', 'Model RMSE', 'Model R²'],
        'value': [
            f"{results['predicted_margin']:.1f}%",
            f"{results['model_rmse']:.2f}",
            f"{results['model_r2']:.3f}"
        ]
    })
    prediction_df.to_csv('2024_margin_prediction.csv', index=False)