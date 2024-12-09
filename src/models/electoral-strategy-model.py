import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

class ElectoralStrategyAnalyzer:
    def __init__(self):
        self.classifier = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )
        self.scaler = StandardScaler()
        
    def prepare_precinct_data(self):
        """
        Prepare precinct-level electoral data with performance shifts
        """
        precinct_data = pd.DataFrame({
            'precinct_id': range(1, 191),  # CA-13 has 190 precincts
            'year': 2020,
            'dem_vote_share': np.random.normal(59.7, 2.5, 190),  # Based on district average
            'prev_dem_vote_share': np.random.normal(56.9, 2.5, 190),
            'turnout_rate': np.random.normal(36.8, 5, 190),
            'prev_turnout': np.random.normal(37.1, 5, 190),
            'median_income': np.random.normal(71948, 15000, 190),
            'college_edu_rate': np.random.normal(31.2, 5, 190),
            'unemployment_rate': np.random.normal(7.2, 1.5, 190)
        })
        
        # Calculate performance shifts
        precinct_data['vote_share_shift'] = (
            precinct_data['dem_vote_share'] - 
            precinct_data['prev_dem_vote_share']
        )
        precinct_data['turnout_shift'] = (
            precinct_data['turnout_rate'] - 
            precinct_data['prev_turnout']
        )
        
        # Create classification target
        precinct_data['performance_improved'] = (
            precinct_data['vote_share_shift'] > 0
        ).astype(int)
        
        return precinct_data
    
    def analyze_performance_patterns(self, data):
        """
        Analyze patterns in electoral performance shifts
        """
        feature_columns = [
            'turnout_shift',
            'turnout_rate',
            'median_income',
            'college_edu_rate',
            'unemployment_rate'
        ]
        
        X = data[feature_columns]
        y = data['performance_improved']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train classifier
        self.classifier.fit(X_scaled, y)
        
        # Generate predictions
        predictions = self.classifier.predict(X_scaled)
        
        # Calculate feature importance
        importance = pd.DataFrame({
            'feature': feature_columns,
            'importance': self.classifier.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Identify high-potential precincts
        data['predicted_improvement'] = predictions
        high_potential = data[
            (data['predicted_improvement'] == 1) & 
            (data['dem_vote_share'] < data['dem_vote_share'].mean())
        ]
        
        return {
            'classification_report': classification_report(y, predictions),
            'feature_importance': importance,
            'high_potential_precincts': high_potential.precinct_id.tolist(),
            'success_rate': (predictions == y).mean()
        }
    
    def generate_strategy_recommendations(self, analysis_results):
        """
        Generate actionable campaign strategy recommendations
        """
        importance_df = analysis_results['feature_importance']
        top_features = importance_df.nlargest(3, 'importance')
        
        recommendations = {
            'priority_areas': {
                'high_potential_precincts': len(analysis_results['high_potential_precincts']),
                'target_precincts': analysis_results['high_potential_precincts'][:5]
            },
            'focus_factors': [
                {
                    'factor': row['feature'],
                    'importance': row['importance'],
                    'strategy_implication': self._get_strategy_implication(row['feature'])
                }
                for _, row in top_features.iterrows()
            ]
        }
        
        return recommendations
    
    def _get_strategy_implication(self, feature):
        """
        Map features to strategic implications
        """
        implications = {
            'turnout_shift': 'Focus on voter mobilization and engagement programs',
            'turnout_rate': 'Implement targeted GOTV efforts in low-turnout areas',
            'median_income': 'Tailor economic messaging to local income levels',
            'college_edu_rate': 'Adjust message complexity and policy detail by area',
            'unemployment_rate': 'Emphasize job creation and economic development'
        }
        return implications.get(feature, 'Consider local demographic factors')

if __name__ == "__main__":
    analyzer = ElectoralStrategyAnalyzer()
    data = analyzer.prepare_precinct_data()
    analysis_results = analyzer.analyze_performance_patterns(data)
    recommendations = analyzer.generate_strategy_recommendations(analysis_results)
    
    print("\nElectoral Performance Analysis:")
    print(f"Model Success Rate: {analysis_results['success_rate']:.1%}")
    
    print("\nKey Predictive Factors:")
    print(analysis_results['feature_importance'])
    
    print("\nStrategic Recommendations:")
    print("\nPriority Areas:")
    print(f"Number of High-Potential Precincts: {recommendations['priority_areas']['high_potential_precincts']}")
    print(f"Top Target Precincts: {recommendations['priority_areas']['target_precincts']}")
    
    print("\nFocus Areas and Implications:")
    for factor in recommendations['focus_factors']:
        print(f"\n{factor['factor']}:")
        print(f"Importance: {factor['importance']:.3f}")
        print(f"Strategy: {factor['strategy_implication']}")
