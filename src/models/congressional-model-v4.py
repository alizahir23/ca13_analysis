import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import HuberRegressor
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_squared_error, r2_score

class DeviationBasedModel:
    def __init__(self):
        # Use more robust algorithms for small variations
        self.gb_model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.01,
            max_depth=2,
            random_state=42
        )
        self.robust_model = HuberRegressor(epsilon=1.35)
        self.scaler = StandardScaler()
    
    def prepare_deviation_data(self):
        """
        Prepare dataset focused on deviations from baseline
        """
        base_data = pd.DataFrame({
            'year': [2012, 2014, 2016, 2018, 2020],
            'democratic_vote_share': [57.8, 56.2, 58.1, 56.9, 59.7],
            'turnout_rate': [35.2, 31.8, 38.4, 37.1, 36.8],
            'unemployment_rate': [8.9, 8.1, 7.8, 7.5, 7.2],
            'college_education_pct': [29.8, 30.1, 30.5, 30.9, 31.2],
            'dem_registration': [45.2, 45.8, 46.3, 46.9, 47.2],
            'rep_registration': [28.1, 27.8, 27.2, 26.8, 26.5]
        })
        
        # Calculate baseline and deviations
        baseline_vote_share = base_data['democratic_vote_share'].mean()
        base_data['vote_share_deviation'] = base_data['democratic_vote_share'] - baseline_vote_share
        
        # Add relative change features
        for col in ['turnout_rate', 'unemployment_rate', 'college_education_pct']:
            base_data[f'{col}_relative_change'] = base_data[col].pct_change()
        
        # Add registration advantage
        base_data['dem_reg_advantage'] = base_data['dem_registration'] - base_data['rep_registration']
        
        return base_data.dropna()
    
    def train_and_evaluate(self, data):
        """
        Train and evaluate models using deviation-based approach
        """
        feature_columns = [
            'turnout_rate_relative_change',
            'unemployment_rate_relative_change',
            'college_education_pct_relative_change',
            'dem_reg_advantage'
        ]
        
        X = data[feature_columns]
        y = data['vote_share_deviation']
        
        loo = LeaveOneOut()
        gb_predictions = []
        robust_predictions = []
        actuals = []
        
        X_scaled = self.scaler.fit_transform(X)
        
        for train_idx, test_idx in loo.split(X):
            X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
            
            self.gb_model.fit(X_train, y_train)
            self.robust_model.fit(X_train, y_train)
            
            gb_pred = self.gb_model.predict(X_test)
            robust_pred = self.robust_model.predict(X_test)
            
            gb_predictions.extend(gb_pred)
            robust_predictions.extend(robust_pred)
            actuals.extend(y_test)
            
        baseline = data['democratic_vote_share'].mean()
        
        # Convert deviations back to vote shares for evaluation
        gb_vote_shares = np.array(gb_predictions) + baseline
        robust_vote_shares = np.array(robust_predictions) + baseline
        actual_vote_shares = np.array(actuals) + baseline
        
        results = {
            'gb_rmse': np.sqrt(mean_squared_error(actual_vote_shares, gb_vote_shares)),
            'robust_rmse': np.sqrt(mean_squared_error(actual_vote_shares, robust_vote_shares)),
            'gb_r2': r2_score(actual_vote_shares, gb_vote_shares),
            'robust_r2': r2_score(actual_vote_shares, robust_vote_shares),
            'feature_importance': pd.DataFrame({
                'feature': feature_columns,
                'importance': self.gb_model.feature_importances_
            }).sort_values('importance', ascending=False)
        }
        
        return results, actual_vote_shares, gb_vote_shares, robust_vote_shares

if __name__ == "__main__":
    model = DeviationBasedModel()
    data = model.prepare_deviation_data()
    results, actuals, gb_preds, robust_preds = model.train_and_evaluate(data)
    
    print("\nDeviation-Based Model Performance:")
    print(f"Gradient Boosting RMSE: {results['gb_rmse']:.2f} percentage points")
    print(f"Gradient Boosting R² Score: {results['gb_r2']:.3f}")
    print(f"Robust Regression RMSE: {results['robust_rmse']:.2f} percentage points")
    print(f"Robust Regression R² Score: {results['robust_r2']:.3f}")
    
    print("\nFeature Importance Rankings:")
    print(results['feature_importance'])
    
    # Calculate predictive accuracy metrics
    predictions_df = pd.DataFrame({
        'Year': data['year'],
        'Actual': actuals,
        'GradientBoosting_Predicted': gb_preds,
        'RobustRegression_Predicted': robust_preds,
        'Prediction_Error_GB': np.abs(actuals - gb_preds),
        'Prediction_Error_Robust': np.abs(actuals - robust_preds)
    })
    predictions_df.to_csv('deviation_model_predictions.csv', index=False)
