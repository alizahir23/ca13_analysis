import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
from datetime import datetime

class FundraisingStrategyAnalyzer:
    def __init__(self):
        self.data_dir = Path('data/campaign_finance')
        self.visualization_dir = Path('data/visualizations')
        self.visualization_dir.mkdir(parents=True, exist_ok=True)
        
        # Key metrics from our analysis
        self.candidate_data = {
            'GRAY': {
                'total_raised': 5416262.01,
                'individual_contrib': 4813067.49,
                'other_sources': 5416262.01 - 4813067.49,
                'total_spent': 4671627.25,
                'party': 'DEM'
            },
            'DUARTE': {
                'total_raised': 4147091.59,
                'individual_contrib': 1579691.68,
                'other_sources': 4147091.59 - 1579691.68,
                'total_spent': 3213218.23,
                'party': 'REP'
            }
        }

    def analyze_funding_strategies(self):
        """Analyze the different funding strategies employed by candidates"""
        print("\nAnalyzing funding strategies...")
        
        fig = plt.figure(figsize=(20, 10))
        
        # 1. Funding Source Distribution
        ax1 = plt.subplot(1, 2, 1)
        
        # Prepare data for stacked bars
        candidates = list(self.candidate_data.keys())
        individual = [d['individual_contrib'] for d in self.candidate_data.values()]
        other = [d['other_sources'] for d in self.candidate_data.values()]
        
        # Create stacked bars
        plt.bar(candidates, individual, label='Individual Contributions',
                color='#2ecc71', alpha=0.7)
        plt.bar(candidates, other, bottom=individual, label='Other Sources',
                color='#3498db', alpha=0.7)
        
        plt.title('Funding Source Distribution\n(in Millions $)')
        plt.ylabel('Amount Raised ($)')
        plt.legend()
        
        # Add value labels
        for i in range(len(candidates)):
            # Label for individual contributions
            plt.text(i, individual[i]/2, 
                    f'${individual[i]/1e6:.1f}M\n({individual[i]/self.candidate_data[candidates[i]]["total_raised"]*100:.1f}%)',
                    ha='center', va='center')
            # Label for other sources
            plt.text(i, individual[i] + other[i]/2,
                    f'${other[i]/1e6:.1f}M\n({other[i]/self.candidate_data[candidates[i]]["total_raised"]*100:.1f}%)',
                    ha='center', va='center')
        
        # 2. Efficiency Metrics
        ax2 = plt.subplot(1, 2, 2)
        
        metrics = {
            'Return on Spending': [d['total_raised']/d['total_spent'] for d in self.candidate_data.values()],
            'Individual Contribution Efficiency': [d['individual_contrib']/d['total_spent'] for d in self.candidate_data.values()]
        }
        
        x = np.arange(len(candidates))
        width = 0.35
        multiplier = 0
        
        for metric_name, values in metrics.items():
            offset = width * multiplier
            rects = ax2.bar(x + offset, values, width, label=metric_name)
            # Add value labels
            ax2.bar_label(rects, fmt='${:.2f}')
            multiplier += 1
        
        ax2.set_title('Fundraising Efficiency Metrics\n($ Raised per $ Spent)')
        ax2.set_xticks(x + width/2)
        ax2.set_xticklabels(candidates)
        ax2.legend(loc='upper right')
        
        plt.tight_layout()
        plt.savefig(self.visualization_dir / 'ca13_funding_strategies.png')
        print(f"Saved funding strategies analysis to: {self.visualization_dir / 'ca13_funding_strategies.png'}")
        plt.close()
        
        # Create comparative metrics
        self.analyze_comparative_metrics()
    
    def analyze_comparative_metrics(self):
        """Analyze and print comparative fundraising metrics"""
        print("\nComparative Fundraising Analysis:")
        print("-" * 50)
        
        # Calculate key comparative metrics
        for candidate, data in self.candidate_data.items():
            individual_pct = data['individual_contrib'] / data['total_raised'] * 100
            other_pct = data['other_sources'] / data['total_raised'] * 100
            roi = (data['total_raised'] - data['total_spent']) / data['total_spent'] * 100
            
            print(f"\n{candidate}:")
            print(f"  Total Fundraising: ${data['total_raised']:,.2f}")
            print(f"  Individual Contributions: ${data['individual_contrib']:,.2f} ({individual_pct:.1f}%)")
            print(f"  Other Sources: ${data['other_sources']:,.2f} ({other_pct:.1f}%)")
            print(f"  Return on Investment: {roi:+.1f}%")
            print(f"  Cost per Dollar Raised: ${data['total_spent']/data['total_raised']:.2f}")
        
        # Calculate and print key differences
        gray = self.candidate_data['GRAY']
        duarte = self.candidate_data['DUARTE']
        
        print("\nKey Differences (Gray vs Duarte):")
        print("-" * 30)
        total_gap = gray['total_raised'] - duarte['total_raised']
        individual_gap = gray['individual_contrib'] - duarte['individual_contrib']
        efficiency_gap = (gray['individual_contrib']/gray['total_spent']) - (duarte['individual_contrib']/duarte['total_spent'])
        
        print(f"Total Fundraising Gap: ${total_gap:,.2f}")
        print(f"Individual Contribution Gap: ${individual_gap:,.2f}")
        print(f"Individual Contribution Efficiency Gap: ${efficiency_gap:.2f} per dollar spent")
        
        # Strategy implications
        print("\nStrategy Implications:")
        print("-" * 30)
        print("GRAY:")
        print("- Heavy reliance on individual contributions")
        print("- Higher individual contribution efficiency")
        print("- Lower overall return on spending")
        print("\nDUARTE:")
        print("- More diverse funding sources")
        print("- Better overall return on spending")
        print("- Lower individual contribution efficiency")

if __name__ == "__main__":
    print("CA-13 Fundraising Strategy Analysis")
    print("=" * 50)
    
    analyzer = FundraisingStrategyAnalyzer()
    analyzer.analyze_funding_strategies()
