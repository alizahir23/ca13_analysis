import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

class PresidentialPredictor2024:
    def __init__(self):
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )
        self.scaler = StandardScaler()
        
    def prepare_historical_data(self):
        """
        Prepare historical presidential election data for CA-13
        """
        return pd.DataFrame({
            'year': [2012, 2016, 2020],
            'democratic_vote_share': [68.5, 71.2, 73.4],
            'turnout_rate': [61.8, 63.5, 65.2],
            'dem_registration': [45.2, 46.3, 47.2],
            'rep_registration': [28.1, 27.2, 26.5],
            'unemployment_rate': [8.9, 7.8, 7.2],
            'national_approval': [49, 45, 43],
            'incumbent_party': [1, 0, 0]  # 1 if Democratic incumbent
        })
    
    def prepare_2024_features(self):
        """
        Prepare features for 2024 prediction
        """
        return pd.DataFrame({
            'turnout_rate': [64.5],  # Projected based on historical patterns
            'dem_registration': [47.3],
            'rep_registration': [26.1],
            'unemployment_rate': [6.5],
            'national_approval': [41],  # Current approval rating
            'incumbent_party': [1]      # Democratic incumbent in 2024
        })
    
    def calculate_prediction_interval(self, prediction, historical_errors):
        """
        Calculate confidence interval for prediction
        """
        std_error = np.std(historical_errors)
        return {
            'lower_bound': prediction - (1.96 * std_error),
            'upper_bound': prediction + (1.96 * std_error)
        }
    
    def train_and_predict(self):
        """
        Train model and generate 2024 prediction
        """
        historical_data = self.prepare_historical_data()
        features_2024 = self.prepare_2024_features()
        
        feature_columns = [
            'turnout_rate',
            'dem_registration',
            'rep_registration',
            'unemployment_rate',
            'national_approval',
            'incumbent_party'
        ]
        
        X = historical_data[feature_columns]
        y = historical_data['democratic_vote_share']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        X_2024_scaled = self.scaler.transform(features_2024[feature_columns])
        
        # Train model
        self.model.fit(X_scaled, y)
        
        # Generate predictions
        prediction = self.model.predict(X_2024_scaled)[0]
        historical_predictions = self.model.predict(X_scaled)
        historical_errors = y - historical_predictions
        
        # Calculate confidence interval
        interval = self.calculate_prediction_interval(prediction, historical_errors)
        
        # Feature importance
        importance = pd.DataFrame({
            'feature': feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return {
            'prediction': prediction,
            'confidence_interval': interval,
            'feature_importance': importance,
            'model_rmse': np.sqrt(mean_squared_error(y, historical_predictions)),
            'model_r2': r2_score(y, historical_predictions)
        }

if __name__ == "__main__":
    predictor = PresidentialPredictor2024()
    results = predictor.train_and_predict()
    
    print("\n2024 Presidential Election Prediction for CA-13:")
    print(f"Predicted Democratic Vote Share: {results['prediction']:.1f}%")
    print(f"Confidence Interval: ({results['confidence_interval']['lower_bound']:.1f}%, "
          f"{results['confidence_interval']['upper_bound']:.1f}%)")
    
    print("\nModel Performance:")
    print(f"RMSE: {results['model_rmse']:.2f} percentage points")
    print(f"R² Score: {results['model_r2']:.3f}")
    
    print("\nKey Predictive Factors:")
    print(results['feature_importance'])
    
    # Calculate Republican vote share
    republican_share = 100 - results['prediction']
    print(f"\nPredicted Republican Vote Share: {republican_share:.1f}%")
    
    # Save detailed results
    prediction_df = pd.DataFrame({
        'Metric': ['Democratic Vote Share', 'Republican Vote Share',
                  'Confidence Interval', 'Model RMSE', 'Model R²'],
        'Value': [f"{results['prediction']:.1f}%",
                 f"{republican_share:.1f}%",
                 f"±{(results['confidence_interval']['upper_bound'] - results['prediction']):.1f}%",
                 f"{results['model_rmse']:.2f}",
                 f"{results['model_r2']:.3f}"]
    })
    prediction_df.to_csv('presidential_prediction_2024.csv', index=False)
