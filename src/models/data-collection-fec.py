import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_squared_error, r2_score

class CongressionalElectionModel:
    def __init__(self):
        self.rf_model = RandomForestRegressor(
            n_estimators=100, 
            min_samples_leaf=1,
            random_state=42
        )
        self.lr_model = LinearRegression()
        self.scaler = StandardScaler()
        
    def prepare_historical_data(self):
        """
        Prepare expanded historical election data
        """
        historical_results = pd.DataFrame({
            'year': [2012, 2014, 2016, 2018, 2020],
            'democratic_vote_share': [57.8, 56.2, 58.1, 56.9, 59.7],
            'turnout_rate': [35.2, 31.8, 38.4, 37.1, 36.8],
            'median_household_income': [68244, 69102, 70156, 71012, 71948],
            'college_education_pct': [29.8, 30.1, 30.5, 30.9, 31.2],
            'unemployment_rate': [8.9, 8.1, 7.8, 7.5, 7.2]
        })
        return historical_results
    
    def evaluate_with_loo(self, X, y):
        """
        Evaluate models using Leave-One-Out cross-validation
        """
        loo = LeaveOneOut()
        rf_predictions = []
        lr_predictions = []
        actuals = []
        
        X_scaled = self.scaler.fit_transform(X)
        
        for train_idx, test_idx in loo.split(X):
            X_train = X_scaled[train_idx]
            X_test = X_scaled[test_idx]
            y_train = y.iloc[train_idx]
            y_test = y.iloc[test_idx]
            
            # Train and predict with Random Forest
            self.rf_model.fit(X_train, y_train)
            rf_pred = self.rf_model.predict(X_test)
            rf_predictions.extend(rf_pred)
            
            # Train and predict with Linear Regression
            self.lr_model.fit(X_train, y_train)
            lr_pred = self.lr_model.predict(X_test)
            lr_predictions.extend(lr_pred)
            
            actuals.extend(y_test)
        
        # Calculate performance metrics
        rf_mse = mean_squared_error(actuals, rf_predictions)
        lr_mse = mean_squared_error(actuals, lr_predictions)
        rf_r2 = r2_score(actuals, rf_predictions)
        lr_r2 = r2_score(actuals, lr_predictions)
        
        return {
            'rf_rmse': np.sqrt(rf_mse),
            'lr_rmse': np.sqrt(lr_mse),
            'rf_r2': rf_r2,
            'lr_r2': lr_r2,
            'predictions': {
                'actual': actuals,
                'rf_pred': rf_predictions,
                'lr_pred': lr_predictions
            }
        }
    
    def analyze_feature_importance(self, X):
        """
        Analyze feature importance using full dataset
        """
        X_scaled = self.scaler.transform(X)
        self.rf_model.fit(X_scaled, y)
        
        importance_df = pd.DataFrame({
            'feature': X.columns,
            'importance': self.rf_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return importance_df

if __name__ == "__main__":
    # Initialize model
    model = CongressionalElectionModel()
    
    # Get historical data
    data = model.prepare_historical_data()
    
    # Prepare features and target
    feature_columns = [
        'median_household_income',
        'college_education_pct',
        'unemployment_rate',
        'turnout_rate'
    ]
    X = data[feature_columns]
    y = data['democratic_vote_share']
    
    # Evaluate models
    results = model.evaluate_with_loo(X, y)
    
    # Analyze feature importance
    importance = model.analyze_feature_importance(X)
    
    # Print comprehensive results
    print("\nModel Performance Metrics:")
    print(f"Random Forest RMSE: {results['rf_rmse']:.2f} percentage points")
    print(f"Random Forest R² Score: {results['rf_r2']:.3f}")
    print(f"Linear Regression RMSE: {results['lr_rmse']:.2f} percentage points")
    print(f"Linear Regression R² Score: {results['lr_r2']:.3f}")
    
    print("\nFeature Importance Rankings:")
    for _, row in importance.iterrows():
        print(f"{row['feature']}: {row['importance']:.3f}")
    
    # Save predictions for analysis
    predictions_df = pd.DataFrame({
        'Year': data['year'],
        'Actual': results['predictions']['actual'],
        'RF_Predicted': results['predictions']['rf_pred'],
        'LR_Predicted': results['predictions']['lr_pred']
    })
    predictions_df.to_csv('model_predictions.csv', index=False)
    print("\nPredictions saved to 'model_predictions.csv'")