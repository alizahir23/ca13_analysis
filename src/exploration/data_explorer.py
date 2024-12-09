import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
try:
    import seaborn as sns
    sns.set_theme(style="whitegrid")  # Set seaborn style
except ImportError:
    print("Seaborn not installed, using default matplotlib style")
    plt.style.use('default')

from pathlib import Path

class CA13DataExplorer:
    def __init__(self):
        self.data_dir = Path('data')
        self.analysis_dir = self.data_dir / 'analysis'
        self.visualization_dir = self.data_dir / 'visualizations'
        self.visualization_dir.mkdir(exist_ok=True)
        
        # Demographics data from our previous analysis
        self.demographics = {
            'Hispanic': {'cvap': 197495, 'turnout_rate': 0.54},
            'Black': {'cvap': 16130, 'turnout_rate': 0.63},
            'Asian': {'cvap': 24392, 'turnout_rate': 0.59},
            'White': {'cvap': 145957, 'turnout_rate': 0.71}
        }
        
        # Set colors for consistency
        self.colors = ['#2ecc71', '#3498db', '#e74c3c', '#f1c40f']
        
        # Print available matplotlib styles
        print("\nAvailable matplotlib styles:")
        print(plt.style.available)
    
    def create_demographic_deep_dive(self):
        """Create detailed demographic visualizations"""
        print("\nCreating demographic analysis visualizations...")
        
        # Create figure with multiple subplots
        fig = plt.figure(figsize=(20, 15))
        
        # 1. CVAP Distribution (Pie Chart)
        ax1 = plt.subplot(2, 2, 1)
        cvap_values = [d['cvap'] for d in self.demographics.values()]
        plt.pie(cvap_values, labels=self.demographics.keys(), autopct='%1.1f%%',
                colors=self.colors, startangle=90)
        plt.title('CVAP Distribution in CA-13', pad=20, size=14)
        
        # 2. CVAP vs Turnout (Bar Chart)
        ax2 = plt.subplot(2, 2, 2)
        groups = list(self.demographics.keys())
        cvap = [d['cvap'] for d in self.demographics.values()]
        expected_turnout = [d['cvap'] * d['turnout_rate'] for d in self.demographics.values()]
        
        x = np.arange(len(groups))
        width = 0.35
        
        ax2.bar(x - width/2, cvap, width, label='Total CVAP', color='lightblue')
        ax2.bar(x + width/2, expected_turnout, width, label='Expected Turnout', color='darkblue')
        ax2.set_xticks(x)
        ax2.set_xticklabels(groups)
        ax2.legend()
        plt.title('CVAP vs Expected Turnout by Demographic', pad=20, size=14)
        plt.xticks(rotation=45)
        
        # 3. Turnout Rates (Horizontal Bar Chart)
        ax3 = plt.subplot(2, 2, 3)
        turnout_rates = [d['turnout_rate'] * 100 for d in self.demographics.values()]
        
        bars = ax3.barh(groups, turnout_rates, color=self.colors)
        ax3.set_xlim(0, 100)
        plt.title('Historical Turnout Rates by Demographic (%)', pad=20, size=14)
        
        # Add percentage labels on bars
        for bar in bars:
            width = bar.get_width()
            ax3.text(width + 1, bar.get_y() + bar.get_height()/2,
                    f'{width:.1f}%', ha='left', va='center')
        
        # 4. Demographic Impact (Stacked Bar)
        ax4 = plt.subplot(2, 2, 4)
        impact_data = pd.DataFrame({
            'CVAP': cvap,
            'Non-Voters': [d['cvap'] * (1 - d['turnout_rate']) for d in self.demographics.values()],
            'Likely Voters': expected_turnout
        }, index=groups)
        
        impact_data.plot(kind='bar', stacked=True, ax=ax4)
        plt.title('Voting Impact by Demographic', pad=20, size=14)
        plt.xticks(rotation=45)
        
        plt.tight_layout(pad=3.0)
        plt.savefig(self.visualization_dir / 'CA13_demographic_analysis.png')
        print(f"Saved demographic visualizations to: {self.visualization_dir / 'CA13_demographic_analysis.png'}")
        plt.close()
        
        # Return the data for verification
        return impact_data

if __name__ == "__main__":
    print("CA-13 Data Exploration and Visualization")
    print("=" * 50)
    
    # Create explorer instance
    explorer = CA13DataExplorer()
    
    # Create demographic visualizations
    impact_data = explorer.create_demographic_deep_dive()
    
    # Print the data for verification
    print("\nDemographic Impact Data:")
    print(impact_data)