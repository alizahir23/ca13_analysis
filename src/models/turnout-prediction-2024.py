import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

class TurnoutPredictor2024:
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
        Prepare historical turnout data combining both presidential and midterm elections
        """
        return pd.DataFrame({
            'year': [2012, 2014, 2016, 2018, 2020, 2022],
            'turnout_rate': [61.8, 35.2, 63.5, 37.1, 65.2, 35.5],
            'presidential_year': [1, 0, 1, 0, 1, 0],
            'competitive_race': [1, 0, 1, 1, 1, 0],
            'dem_registration': [45.2, 45.8, 46.3, 46.9, 47.2, 47.0],
            'rep_registration': [28.1, 27.8, 27.2, 26.8, 26.5, 26.3],
            'median_income': [68244, 69102, 70156, 71012, 71948, 72500],
            'unemployment': [8.9, 8.1, 7.8, 7.5, 7.2, 6.8]
        })
    
    def prepare_2024_features(self):
        """
        Prepare features for 2024 turnout prediction
        """
        return pd.DataFrame({
            'presidential_year': [1],
            'competitive_race': [1],
            'dem_registration': [47.3],
            'rep_registration': [26.1],
            'median_income': [73000],
            'unemployment': [6.5]
        })
    
    def train_and_predict(self):
        """
        Train model and generate 2024 turnout prediction
        """
        historical_data = self.prepare_historical_data()
        features_2024 = self.prepare_2024_features()
        
        feature_columns = [
            'presidential_year',
            'competitive_race',
            'dem_registration',
            'rep_registration',
            'median_income',
            'unemployment'
        ]
        
        X = historical_data[feature_columns]
        y = historical_data['turnout_rate']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        X_2024_scaled = self.scaler.transform(features_2024[feature_columns])
        
        # Train model
        self.model.fit(X_scaled, y)
        
        # Generate prediction
        prediction = self.model.predict(X_2024_scaled)[0]
        historical_predictions = self.model.predict(X_scaled)
        
        # Calculate confidence interval
        rmse = np.sqrt(mean_squared_error(y, historical_predictions))
        confidence_interval = 1.96 * rmse
        
        # Calculate feature importance
        importance = pd.DataFrame({
            'feature': feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return {
            'prediction': prediction,
            'confidence_interval': confidence_interval,
            'model_rmse': rmse,
            'model_r2': r2_score(y, historical_predictions),
            'feature_importance': importance,
            'historical_presidential_avg': historical_data[
                historical_data['presidential_year'] == 1
            ]['turnout_rate'].mean(),
            'historical_range': {
                'min': historical_data['turnout_rate'].min(),
                'max': historical_data['turnout_rate'].max()
            }
        }

if __name__ == "__main__":
    predictor = TurnoutPredictor2024()
    results = predictor.train_and_predict()
    
    print("\n2024 Voter Turnout Prediction for CA-13:")
    print(f"Predicted Turnout Rate: {results['prediction']:.1f}%")
    print(f"Confidence Interval: ±{results['confidence_interval']:.1f} percentage points")
    print(f"(Range: {results['prediction'] - results['confidence_interval']:.1f}% - "
          f"{results['prediction'] + results['confidence_interval']:.1f}%)")
    
    print("\nHistorical Context:")
    print(f"Average Presidential Year Turnout: {results['historical_presidential_avg']:.1f}%")
    print(f"Historical Range: {results['historical_range']['min']:.1f}% - "
          f"{results['historical_range']['max']:.1f}%")
    
    print("\nModel Performance:")
    print(f"RMSE: {results['model_rmse']:.2f} percentage points")
    print(f"R² Score: {results['model_r2']:.3f}")
    
    print("\nKey Predictive Factors:")
    print(results['feature_importance'])
    
    # Save detailed results
    prediction_df = pd.DataFrame({
        'Metric': ['Predicted Turnout', 'Confidence Interval',
                  'Model RMSE', 'Model R²', 'Historical Presidential Average'],
        'Value': [f"{results['prediction']:.1f}%",
                 f"±{results['confidence_interval']:.1f}%",
                 f"{results['model_rmse']:.2f}",
                 f"{results['model_r2']:.3f}",
                 f"{results['historical_presidential_avg']:.1f}%"]
    })
    prediction_df.to_csv('turnout_prediction_2024.csv', index=False)
