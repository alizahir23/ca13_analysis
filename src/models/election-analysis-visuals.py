import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class ReportVisualizer:
    def __init__(self):
        self.fig_size = (10, 6)
        self.colors = {
            'primary': '#2166AC',
            'secondary': '#B2182B',
            'highlight': '#4DAF4A',
            'background': '#F5F5F5'
        }
        self.font_size = {
            'title': 14,
            'label': 12,
            'tick': 10
        }
        
    def configure_plot_style(self, ax):
        ax.set_facecolor(self.colors['background'])
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
    def create_margin_trend_plot(self):
        data = pd.DataFrame({
            'year': [2012, 2014, 2016, 2018, 2020, 2022, 2024],
            'democratic_margin': [15.6, 12.4, 16.2, 13.8, 19.4, 13.0, 19.5],
            'presidential_year': [1, 0, 1, 0, 1, 0, 1]
        })
        
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        # Historical margins
        ax.plot(data['year'][:-1], data['democratic_margin'][:-1], 
                marker='o', color=self.colors['primary'], 
                linewidth=2, label='Historical Margin')
        
        # 2024 prediction
        ax.plot(data['year'][-2:], data['democratic_margin'][-2:], 
                marker='*', linestyle='--', color=self.colors['highlight'],
                linewidth=2, markersize=15, label='2024 Prediction')
        
        # Presidential years
        presidential_years = data[data['presidential_year'] == 1]
        ax.scatter(presidential_years['year'], presidential_years['democratic_margin'],
                   s=100, color='gold', edgecolor='black', zorder=5,
                   label='Presidential Election Years')
        
        self.configure_plot_style(ax)
        ax.set_title('Democratic Margin Trend in CA-13 (2012-2024)', 
                    fontsize=self.font_size['title'], pad=20)
        ax.set_xlabel('Election Year', fontsize=self.font_size['label'])
        ax.set_ylabel('Democratic Margin (%)', fontsize=self.font_size['label'])
        ax.tick_params(labelsize=self.font_size['tick'])
        ax.legend(fontsize=self.font_size['tick'])
        
        plt.tight_layout()
        plt.savefig('margin_trend_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_feature_importance_plot(self):
        importance_data = pd.DataFrame({
            'Feature': ['Presidential Year', 'Previous Margin', 'Registration Advantage',
                       'Turnout Rate', 'Unemployment Rate'],
            'Importance': [0.483, 0.358, 0.088, 0.044, 0.028]
        })
        
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        bars = ax.barh(importance_data['Feature'], importance_data['Importance'],
                      color=self.colors['primary'])
        
        self.configure_plot_style(ax)
        ax.set_title('Feature Importance in 2024 Election Prediction',
                    fontsize=self.font_size['title'], pad=20)
        ax.set_xlabel('Relative Importance', fontsize=self.font_size['label'])
        ax.set_ylabel('Features', fontsize=self.font_size['label'])
        ax.tick_params(labelsize=self.font_size['tick'])
        
        # Value labels
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.01, bar.get_y() + bar.get_height()/2,
                   f'{width:.3f}', ha='left', va='center',
                   fontsize=self.font_size['tick'])
        
        plt.tight_layout()
        plt.savefig('feature_importance_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_model_metrics_plot(self):
        metrics = pd.DataFrame({
            'Metric': ['Model Accuracy (R²)', 'RMSE', 'Prediction Interval',
                      'Training Period', 'Key Features'],
            'Value': ['1.000', '0.00 percentage points', '±2.5%',
                     '2012-2022', '5 predictive factors']
        })
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.axis('off')
        
        # Create table without cellWidth parameter
        table = ax.table(cellText=metrics.values,
                        colLabels=metrics.columns,
                        cellLoc='center',
                        loc='center')
        
        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1.2, 1.8)
        
        # Color header row
        for key, cell in table._cells.items():
            if key[0] == 0:
                cell.set_facecolor(self.colors['primary'])
                cell.set_text_props(color='white')
        
        plt.title('Model Performance Summary', 
                 fontsize=self.font_size['title'], pad=20)
        plt.savefig('model_metrics_summary.png', dpi=300, bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    visualizer = ReportVisualizer()
    
    print("Generating visualizations for your report...")
    
    visualizer.create_margin_trend_plot()
    print("1. Created Democratic margin trend analysis (margin_trend_analysis.png)")
    
    visualizer.create_feature_importance_plot()
    print("2. Created feature importance analysis (feature_importance_analysis.png)")
    
    visualizer.create_model_metrics_plot()
    print("3. Created model performance summary (model_metrics_summary.png)")
    
    print("\nAll visualizations have been generated successfully.")
    print("\nThese visualizations provide a comprehensive view of your model's:")
    print("- Historical performance and future predictions")
    print("- Key predictive factors and their relative importance")
    print("- Overall model performance metrics")