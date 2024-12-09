import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
import json

class ContributionAnalyzer:
    def __init__(self):
        self.data_dir = Path('data/campaign_finance')
        self.visualization_dir = Path('data/visualizations')
        self.visualization_dir.mkdir(parents=True, exist_ok=True)
        
        with open(self.data_dir / 'ca13_comprehensive_data.json', 'r') as f:
            self.data = json.load(f)
            
        self.candidates = {
            'GRAY': {
                'total_raised': 5416262.01,
                'individual_contributions': 4813067.49,
                'total_spent': 4671627.25,
                'party': 'DEM'
            },
            'DUARTE': {
                'total_raised': 4147091.59,
                'individual_contributions': 1579691.68,
                'total_spent': 3213218.23,
                'party': 'REP'
            }
        }
    
    def analyze_funding_efficiency(self):
        """Analyze how effectively candidates are using their funding"""
        print("\nAnalyzing funding efficiency...")
        
        fig = plt.figure(figsize=(15, 10))
        
        # 1. Funding Source Analysis
        ax1 = plt.subplot(2, 1, 1)
        
        # Calculate funding breakdown
        breakdowns = []
        for name, data in self.candidates.items():
            individual_pct = (data['individual_contributions'] / data['total_raised']) * 100
            other_pct = ((data['total_raised'] - data['individual_contributions']) / data['total_raised']) * 100
            breakdowns.append({
                'name': name,
                'Individual': individual_pct,
                'Other Sources': other_pct
            })
        
        df_breakdown = pd.DataFrame(breakdowns)
        df_breakdown.set_index('name')[['Individual', 'Other Sources']].plot(
            kind='bar',
            stacked=True,
            ax=ax1,
            color=['#2ecc71', '#3498db']
        )
        
        plt.title('Funding Source Breakdown')
        plt.ylabel('Percentage of Total Funding')
        plt.legend(title='Source')
        
        # Add percentage labels
        for c in ax1.containers:
            ax1.bar_label(c, fmt='%.1f%%')
        
        # 2. Spending Efficiency Analysis
        ax2 = plt.subplot(2, 1, 2)
        
        metrics = {
            'Dollars Raised per Dollar Spent': [
                data['total_raised'] / data['total_spent'] 
                for data in self.candidates.values()
            ],
            'Individual Contributions per Dollar Spent': [
                data['individual_contributions'] / data['total_spent']
                for data in self.candidates.values()
            ]
        }
        
        x = np.arange(len(self.candidates))
        width = 0.35
        multiplier = 0
        
        for metric, values in metrics.items():
            offset = width * multiplier
            rects = ax2.bar(x + offset, values, width, label=metric)
            ax2.bar_label(rects, fmt='%.2f')
            multiplier += 1
        
        ax2.set_ylabel('Ratio')
        ax2.set_title('Fundraising Efficiency Metrics')
        ax2.set_xticks(x + width/2)
        ax2.set_xticklabels(self.candidates.keys())
        ax2.legend(loc='upper right')
        
        plt.tight_layout()
        plt.savefig(self.visualization_dir / 'ca13_funding_efficiency.png')
        print(f"Saved funding efficiency analysis to: {self.visualization_dir / 'ca13_funding_efficiency.png'}")
        plt.close()
        
        # Print detailed analysis
        print("\nFunding Efficiency Analysis:")
        print("-" * 50)
        
        for name, data in self.candidates.items():
            ind_pct = (data['individual_contributions'] / data['total_raised']) * 100
            spending_ratio = data['total_raised'] / data['total_spent']
            ind_spending_ratio = data['individual_contributions'] / data['total_spent']
            
            print(f"\n{name}:")
            print(f"  Individual Contributions: {ind_pct:.1f}% of total funding")
            print(f"  Dollars Raised per Dollar Spent: ${spending_ratio:.2f}")
            print(f"  Individual Contributions per Dollar Spent: ${ind_spending_ratio:.2f}")
    
    def analyze_spending_impact(self):
        """Analyze the impact of spending on fundraising"""
        print("\nAnalyzing spending impact...")
        
        plt.figure(figsize=(15, 8))
        
        # Calculate spending effectiveness metrics
        metrics = []
        for name, data in self.candidates.items():
            metrics.append({
                'name': name,
                'total_spent': data['total_spent'] / 1_000_000,  # Convert to millions
                'total_raised': data['total_raised'] / 1_000_000,
                'individual_contrib': data['individual_contributions'] / 1_000_000,
                'spending_efficiency': data['total_raised'] / data['total_spent'],
                'individual_efficiency': data['individual_contributions'] / data['total_spent']
            })
        
        df_metrics = pd.DataFrame(metrics)
        
        # Create comparison visualization
        x = np.arange(len(self.candidates))
        width = 0.25
        
        plt.bar(x - width, df_metrics['total_spent'], width, label='Total Spent', color='#e74c3c')
        plt.bar(x, df_metrics['total_raised'], width, label='Total Raised', color='#2ecc71')
        plt.bar(x + width, df_metrics['individual_contrib'], width, label='Individual Contributions', color='#3498db')
        
        plt.ylabel('Millions of Dollars')
        plt.title('Spending vs. Fundraising Comparison')
        plt.xticks(x, df_metrics['name'])
        plt.legend()
        
        # Add value labels
        def add_value_labels(x_pos, values):
            for i, v in enumerate(values):
                plt.text(x_pos[i], v, f'${v:.1f}M', ha='center', va='bottom')
        
        add_value_labels(x - width, df_metrics['total_spent'])
        add_value_labels(x, df_metrics['total_raised'])
        add_value_labels(x + width, df_metrics['individual_contrib'])
        
        plt.tight_layout()
        plt.savefig(self.visualization_dir / 'ca13_spending_impact.png')
        print(f"Saved spending impact analysis to: {self.visualization_dir / 'ca13_spending_impact.png'}")
        plt.close()
        
        # Print detailed impact analysis
        print("\nSpending Impact Analysis:")
        print("-" * 50)
        print("\nKey Differences in Spending Effectiveness:")
        
        for metric in df_metrics.itertuples():
            print(f"\n{metric.name}:")
            print(f"  Spending: ${metric.total_spent:,.1f}M")
            print(f"  Total Raised: ${metric.total_raised:,.1f}M")
            print(f"  Return on Spending: ${metric.spending_efficiency:.2f} raised per dollar spent")
            print(f"  Individual Contribution Efficiency: ${metric.individual_efficiency:.2f} in individual contributions per dollar spent")

if __name__ == "__main__":
    print("CA-13 Contribution Pattern Analysis")
    print("=" * 50)
    
    analyzer = ContributionAnalyzer()
    analyzer.analyze_funding_efficiency()
    analyzer.analyze_spending_impact()
