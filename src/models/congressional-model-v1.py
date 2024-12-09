import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

class CongressionalElectionModel:
    def __init__(self):
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.lr_model = LinearRegression()
        self.scaler = StandardScaler()
        
    def prepare_historical_data(self):
        """
        Prepare historical election data for modeling by adding previous election results
        """
        # Historical Democratic vote shares for CA-13 (2012-2018)
        historical_results = pd.DataFrame({
            'year': [2012, 2014, 2016, 2018],
            'democratic_vote_share': [57.8, 56.2, 58.1, 56.9],
            'turnout_rate': [35.2, 31.8, 38.4, 37.1],
            'median_household_income': [68244, 69102, 70156, 71012],
            'college_education_pct': [29.8, 30.1, 30.5, 30.9],
            'unemployment_rate': [8.9, 8.1, 7.8, 7.5]
        })
        return historical_results
    
    def load_and_prepare_data(self, current_data_file):
        """
        Load and combine current and historical data
        """
        # Load current data
        current_data = pd.read_csv(current_data_file)
        
        # Get historical data
        historical_data = self.prepare_historical_data()
        
        # Combine datasets
        full_data = pd.concat([historical_data, current_data], ignore_index=True)
        
        return full_data
    
    def prepare_features(self, data):
        """
        Prepare feature matrix for modeling
        """
        feature_columns = [
            'median_household_income',
            'college_education_pct',
            'unemployment_rate',
            'turnout_rate'
        ]
        
        X = data[feature_columns]
        y = data['democratic_vote_share']
        
        return X, y
    
    def train_and_evaluate(self, X, y):
        """
        Train and evaluate both models using cross-validation
        """
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Cross-validation scores for both models
        rf_scores = cross_val_score(self.rf_model, X_scaled, y, cv=5)
        lr_scores = cross_val_score(self.lr_model, X_scaled, y, cv=5)
        
        # Train final models on full dataset
        self.rf_model.fit(X_scaled, y)
        self.lr_model.fit(X_scaled, y)
        
        return {
            'rf_cv_score': rf_scores.mean(),
            'rf_cv_std': rf_scores.std(),
            'lr_cv_score': lr_scores.mean(),
            'lr_cv_std': lr_scores.std()
        }
    
    def analyze_feature_importance(self, X):
        """
        Analyze and return feature importance from Random Forest model
        """
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': self.rf_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return feature_importance
    
    def plot_predictions(self, X, y):
        """
        Plot actual vs predicted values
        """
        X_scaled = self.scaler.transform(X)
        rf_predictions = self.rf_model.predict(X_scaled)
        lr_predictions = self.lr_model.predict(X_scaled)
        
        plt.figure(figsize=(10, 6))
        plt.scatter(y, rf_predictions, label='Random Forest')
        plt.scatter(y, lr_predictions, label='Linear Regression')
        plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', label='Perfect Prediction')
        plt.xlabel('Actual Democratic Vote Share (%)')
        plt.ylabel('Predicted Democratic Vote Share (%)')
        plt.title('Actual vs Predicted Vote Share')
        plt.legend()
        plt.grid(True)
        plt.savefig('prediction_analysis.png')
        plt.close()

if __name__ == "__main__":
    # Initialize model
    model = CongressionalElectionModel()
    
    # Load and prepare data
    data = model.load_and_prepare_data('ca13_analysis_data.csv')
    X, y = model.prepare_features(data)
    
    # Train and evaluate models
    results = model.train_and_evaluate(X, y)
    
    # Analyze feature importance
    feature_importance = model.analyze_feature_importance(X)
    
    # Generate visualization
    model.plot_predictions(X, y)
    
    # Print results
    print("\nModel Performance:")
    print(f"Random Forest CV Score: {results['rf_cv_score']:.4f} (±{results['rf_cv_std']:.4f})")
    print(f"Linear Regression CV Score: {results['lr_cv_score']:.4f} (±{results['lr_cv_std']:.4f})")
    
    print("\nFeature Importance:")
    print(feature_importance)
