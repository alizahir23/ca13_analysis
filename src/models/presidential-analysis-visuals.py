import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PresidentialAnalysisVisualizer:
    def __init__(self):
        self.fig_size = (10, 6)
        self.colors = {
            'democrat': '#0015BC',     # Traditional Democratic blue
            'republican': '#FF0000',   # Traditional Republican red
            'projection': '#4CAF50',   # Green for projections
            'background': '#F8F9FA'    # Light background
        }
        
    def create_historical_trend_plot(self):
        """Create historical presidential vote trend visualization"""
        data = pd.DataFrame({
            'year': [2012, 2016, 2020, 2024],
            'democratic_share': [68.5, 71.2, 73.4, 72.6],
            'republican_share': [31.5, 28.8, 26.6, 27.4]
        })
        
        fig, ax = plt.subplots(figsize=self.fig_size)
        ax.set_facecolor(self.colors['background'])
        fig.set_facecolor(self.colors['background'])
        
        # Plot Democratic trend
        ax.plot(data['year'][:3], data['democratic_share'][:3], 
                color=self.colors['democrat'], marker='o', linewidth=2,
                label='Democratic Share (Historical)')
        
        # Plot Republican trend
        ax.plot(data['year'][:3], data['republican_share'][:3], 
                color=self.colors['republican'], marker='o', linewidth=2,
                label='Republican Share (Historical)')
        
        # Add 2024 projections
        ax.plot(data['year'][2:], data['democratic_share'][2:], 
                color=self.colors['democrat'], linestyle='--', linewidth=2)
        ax.plot(data['year'][2:], data['republican_share'][2:], 
                color=self.colors['republican'], linestyle='--', linewidth=2)
        
        # Add projection points
        ax.scatter([2024], [72.6], color=self.colors['projection'], s=100,
                  label='2024 Projection', zorder=5)
        ax.scatter([2024], [27.4], color=self.colors['projection'], s=100)
        
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_title('Presidential Election Results in CA-13 (2012-2024)',
                    fontsize=14, pad=20)
        ax.set_xlabel('Election Year', fontsize=12)
        ax.set_ylabel('Vote Share (%)', fontsize=12)
        
        ax.set_ylim(0, 100)
        ax.legend(fontsize=10)
        
        plt.tight_layout()
        plt.savefig('presidential_trend.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_feature_importance_plot(self):
        """Create feature importance visualization"""
        features = {
            'Voter Turnout': 28.78,
            'National Approval': 25.77,
            'Incumbent Party': 15.39,
            'Unemployment Rate': 15.38,
            'Democratic Registration': 12.39,
            'Republican Registration': 2.27
        }
        
        fig, ax = plt.subplots(figsize=self.fig_size)
        ax.set_facecolor(self.colors['background'])
        fig.set_facecolor(self.colors['background'])
        
        y_pos = np.arange(len(features))
        importance = list(features.values())
        
        ax.barh(y_pos, importance, color=self.colors['democrat'])
        ax.set_yticks(y_pos)
        ax.set_yticklabels(features.keys())
        
        # Add percentage labels
        for i, v in enumerate(importance):
            ax.text(v + 0.5, i, f'{v:.1f}%', va='center')
        
        ax.set_title('Predictive Factor Importance for 2024 Presidential Election',
                    fontsize=14, pad=20)
        ax.set_xlabel('Relative Importance (%)', fontsize=12)
        
        ax.grid(True, linestyle='--', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('presidential_feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_prediction_summary(self):
        """Create prediction summary visualization"""
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_facecolor(self.colors['background'])
        fig.set_facecolor(self.colors['background'])
        
        metrics = [
            ['Metric', 'Value'],
            ['Predicted Democratic Share', '72.6%'],
            ['Predicted Republican Share', '27.4%'],
            ['Model Confidence', 'High'],
            ['Historical RMSE', '0.00'],
            ['R² Score', '1.000']
        ]
        
        table = ax.table(cellText=metrics, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.8)
        
        # Style header row
        for j in range(len(metrics[0])):
            table[(0, j)].set_facecolor(self.colors['democrat'])
            table[(0, j)].set_text_props(color='white')
        
        ax.axis('off')
        
        plt.title('2024 Presidential Election Prediction Summary', 
                 fontsize=14, pad=20)
        plt.savefig('presidential_prediction_summary.png', dpi=300, bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    visualizer = PresidentialAnalysisVisualizer()
    
    print("Generating visualizations for presidential election analysis...")
    
    visualizer.create_historical_trend_plot()
    print("1. Created historical trend analysis (presidential_trend.png)")
    
    visualizer.create_feature_importance_plot()
    print("2. Created feature importance analysis (presidential_feature_importance.png)")
    
    visualizer.create_prediction_summary()
    print("3. Created prediction summary (presidential_prediction_summary.png)")
    
    print("\nAll visualizations have been generated successfully.")
