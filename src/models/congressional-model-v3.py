import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_squared_error, r2_score

class EnhancedElectionModel:
    def __init__(self):
        # Use Ridge regression instead of standard Linear Regression
        # to handle multicollinearity
        self.rf_model = RandomForestRegressor(
            n_estimators=100,
            min_samples_leaf=1,
            random_state=42
        )
        self.ridge_model = Ridge(alpha=1.0)
        self.scaler = StandardScaler()
    
    def prepare_enhanced_data(self):
        """
        Prepare enhanced dataset with temporal features and party registration
        """
        historical_results = pd.DataFrame({
            'year': [2012, 2014, 2016, 2018, 2020],
            'democratic_vote_share': [57.8, 56.2, 58.1, 56.9, 59.7],
            'turnout_rate': [35.2, 31.8, 38.4, 37.1, 36.8],
            'median_household_income': [68244, 69102, 70156, 71012, 71948],
            'college_education_pct': [29.8, 30.1, 30.5, 30.9, 31.2],
            'unemployment_rate': [8.9, 8.1, 7.8, 7.5, 7.2],
            'dem_registration': [45.2, 45.8, 46.3, 46.9, 47.2],
            'rep_registration': [28.1, 27.8, 27.2, 26.8, 26.5]
        })
        
        # Add temporal features
        historical_results['year_scaled'] = (historical_results['year'] - 2012) / 8
        historical_results['prev_margin'] = historical_results['democratic_vote_share'].shift(1)
        historical_results['vote_share_trend'] = historical_results['democratic_vote_share'].diff()
        historical_results['turnout_trend'] = historical_results['turnout_rate'].diff()
        
        # Add interaction terms
        historical_results['edu_income_interaction'] = (
            historical_results['college_education_pct'] * 
            historical_results['median_household_income'] / 100000
        )
        
        return historical_results.dropna()
    
    def train_and_evaluate(self, data):
        """
        Train and evaluate models with enhanced features
        """
        feature_columns = [
            'year_scaled',
            'turnout_rate',
            'unemployment_rate',
            'college_education_pct',
            'dem_registration',
            'rep_registration',
            'vote_share_trend',
            'turnout_trend',
            'edu_income_interaction'
        ]
        
        X = data[feature_columns]
        y = data['democratic_vote_share']
        
        # Perform Leave-One-Out cross-validation
        loo = LeaveOneOut()
        rf_predictions = []
        ridge_predictions = []
        actuals = []
        
        X_scaled = self.scaler.fit_transform(X)
        
        for train_idx, test_idx in loo.split(X):
            X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
            
            self.rf_model.fit(X_train, y_train)
            self.ridge_model.fit(X_train, y_train)
            
            rf_pred = self.rf_model.predict(X_test)
            ridge_pred = self.ridge_model.predict(X_test)
            
            rf_predictions.extend(rf_pred)
            ridge_predictions.extend(ridge_pred)
            actuals.extend(y_test)
        
        results = {
            'rf_rmse': np.sqrt(mean_squared_error(actuals, rf_predictions)),
            'ridge_rmse': np.sqrt(mean_squared_error(actuals, ridge_predictions)),
            'rf_r2': r2_score(actuals, rf_predictions),
            'ridge_r2': r2_score(actuals, ridge_predictions),
            'feature_importance': pd.DataFrame({
                'feature': feature_columns,
                'importance': self.rf_model.feature_importances_
            }).sort_values('importance', ascending=False)
        }
        
        return results, actuals, rf_predictions, ridge_predictions

if __name__ == "__main__":
    model = EnhancedElectionModel()
    data = model.prepare_enhanced_data()
    results, actuals, rf_preds, ridge_preds = model.train_and_evaluate(data)
    
    # Save detailed predictions
    predictions_df = pd.DataFrame({
        'Year': data['year'],
        'Actual': actuals,
        'RandomForest_Predicted': rf_preds,
        'Ridge_Predicted': ridge_preds
    })
    predictions_df.to_csv('enhanced_model_predictions.csv', index=False)
    
    # Print comprehensive results
    print("\nEnhanced Model Performance:")
    print(f"Random Forest RMSE: {results['rf_rmse']:.2f} percentage points")
    print(f"Random Forest R² Score: {results['rf_r2']:.3f}")
    print(f"Ridge Regression RMSE: {results['ridge_rmse']:.2f} percentage points")
    print(f"Ridge Regression R² Score: {results['ridge_r2']:.3f}")
    
    print("\nFeature Importance Rankings:")
    print(results['feature_importance'])
