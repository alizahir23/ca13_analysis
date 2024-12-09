import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class TurnoutAnalysisVisualizer:
    def __init__(self):
        self.fig_size = (10, 6)
        self.colors = {
            'presidential': '#2E86C1',
            'midterm': '#AED6F1',
            'prediction': '#27AE60',
            'background': '#F8F9FA',
            'grid': '#EAECEE'
        }
        
    def configure_plot_style(self, ax):
        """Apply consistent styling to plots"""
        ax.set_facecolor(self.colors['background'])
        ax.grid(True, linestyle='--', alpha=0.7, color=self.colors['grid'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
    def create_historical_trend_plot(self):
        """Create visualization of historical turnout trends"""
        data = pd.DataFrame({
            'year': [2012, 2014, 2016, 2018, 2020, 2022, 2024],
            'turnout_rate': [61.8, 35.2, 63.5, 37.1, 65.2, 35.5, 65.2],
            'election_type': ['Presidential', 'Midterm', 'Presidential', 
                            'Midterm', 'Presidential', 'Midterm', 'Presidential']
        })
        
        fig, ax = plt.subplots(figsize=self.fig_size)
        fig.set_facecolor(self.colors['background'])
        
        # Plot presidential year turnout
        presidential = data[data['election_type'] == 'Presidential']
        ax.plot(presidential['year'][:-1], presidential['turnout_rate'][:-1], 
                color=self.colors['presidential'], marker='o', linewidth=2,
                label='Presidential Election Turnout')
        
        # Plot midterm turnout
        midterm = data[data['election_type'] == 'Midterm']
        ax.plot(midterm['year'], midterm['turnout_rate'], 
                color=self.colors['midterm'], marker='s', linewidth=2,
                label='Midterm Election Turnout')
        
        # Add 2024 prediction point
        ax.scatter(2024, 65.2, color=self.colors['prediction'], 
                  s=150, marker='*', label='2024 Prediction')
        
        self.configure_plot_style(ax)
        ax.set_title('Voter Turnout Trends in CA-13 (2012-2024)', 
                    fontsize=14, pad=20)
        ax.set_xlabel('Election Year', fontsize=12)
        ax.set_ylabel('Voter Turnout (%)', fontsize=12)
        ax.legend(loc='upper left')
        
        plt.tight_layout()
        plt.savefig('turnout_trend_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_feature_importance_plot(self):
        """Create feature importance visualization"""
        features = {
            'Presidential Year': 99.31,
            'Democratic Registration': 0.20,
            'Competitive Race': 0.18,
            'Unemployment': 0.12,
            'Median Income': 0.10,
            'Republican Registration': 0.09
        }
        
        fig, ax = plt.subplots(figsize=self.fig_size)
        fig.set_facecolor(self.colors['background'])
        
        y_pos = np.arange(len(features))
        importance = list(features.values())
        
        bars = ax.barh(y_pos, importance, color=self.colors['presidential'])
        ax.set_yticks(y_pos)
        ax.set_yticklabels(features.keys())
        
        # Add value labels
        for i, v in enumerate(importance):
            ax.text(v + 0.5, i, f'{v:.2f}%', 
                   va='center', fontsize=10)
        
        self.configure_plot_style(ax)
        ax.set_title('Impact of Predictive Factors on 2024 Turnout',
                    fontsize=14, pad=20)
        ax.set_xlabel('Relative Importance (%)', fontsize=12)
        
        plt.tight_layout()
        plt.savefig('turnout_factors_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_prediction_summary(self):
        """Create prediction summary visualization"""
        fig, ax = plt.subplots(figsize=(8, 4))
        fig.set_facecolor(self.colors['background'])
        
        data = [
            ['Metric', 'Value'],
            ['Predicted 2024 Turnout', '65.2%'],
            ['Historical Presidential Average', '63.5%'],
            ['Model Accuracy (R²)', '1.000'],
            ['Prediction Range', '65.2% - 65.2%'],
            ['RMSE', '0.00']
        ]
        
        table = ax.table(cellText=data, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1.2, 1.8)
        
        # Style header row
        for j in range(len(data[0])):
            table[(0, j)].set_facecolor(self.colors['presidential'])
            table[(0, j)].set_text_props(color='white')
        
        ax.axis('off')
        plt.title('2024 Turnout Prediction Summary',
                 fontsize=14, pad=20)
        
        plt.savefig('turnout_prediction_summary.png', dpi=300, bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    visualizer = TurnoutAnalysisVisualizer()
    
    print("Generating visualizations for turnout analysis...")
    
    visualizer.create_historical_trend_plot()
    print("1. Created historical trend visualization (turnout_trend_analysis.png)")
    
    visualizer.create_feature_importance_plot()
    print("2. Created feature importance visualization (turnout_factors_analysis.png)")
    
    visualizer.create_prediction_summary()
    print("3. Created prediction summary visualization (turnout_prediction_summary.png)")
    
    print("\nAll visualizations have been generated successfully.")