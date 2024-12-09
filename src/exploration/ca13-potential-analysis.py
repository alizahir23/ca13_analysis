import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class CA13PotentialAnalyzer:
    def __init__(self):
        self.data_dir = Path('data')
        self.visualization_dir = self.data_dir / 'visualizations'
        self.visualization_dir.mkdir(exist_ok=True)
        
        # Demographics with current and potential data
        self.demographics = {
            'Hispanic': {
                'current_share': 0.454,
                'potential_share': 0.514,
                'untapped': 0.060,
                'cvap': 197495,
                'turnout_rate': 0.54
            },
            'Black': {
                'current_share': 0.043,
                'potential_share': 0.042,
                'untapped': -0.001,
                'cvap': 16130,
                'turnout_rate': 0.63
            },
            'Asian': {
                'current_share': 0.061,
                'potential_share': 0.064,
                'untapped': 0.002,
                'cvap': 24392,
                'turnout_rate': 0.59
            },
            'White': {
                'current_share': 0.441,
                'potential_share': 0.380,
                'untapped': -0.061,
                'cvap': 145957,
                'turnout_rate': 0.71
            }
        }
        
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def analyze_potential_shifts(self):
        """Analyze potential demographic voting power shifts"""
        print("\nAnalyzing potential demographic shifts...")
        
        fig = plt.figure(figsize=(20, 10))
        
        # 1. Current vs Potential Share Comparison
        ax1 = plt.subplot(1, 2, 1)
        groups = list(self.demographics.keys())
        current = [d['current_share'] * 100 for d in self.demographics.values()]
        potential = [d['potential_share'] * 100 for d in self.demographics.values()]
        
        x = np.arange(len(groups))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, current, width, label='Current Share',
                       color='lightblue')
        bars2 = ax1.bar(x + width/2, potential, width, label='Potential Share',
                       color='darkblue')
        
        ax1.set_ylabel('Vote Share (%)')
        ax1.set_title('Current vs Maximum Potential Vote Share')
        ax1.set_xticks(x)
        ax1.set_xticklabels(groups)
        ax1.legend()
        
        # Add value labels
        def autolabel(bars):
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%', ha='center', va='bottom')
        
        autolabel(bars1)
        autolabel(bars2)
        
        # 2. Untapped Potential Analysis
        ax2 = plt.subplot(1, 2, 2)
        untapped = [d['untapped'] * 100 for d in self.demographics.values()]
        colors = ['green' if x > 0 else 'red' for x in untapped]
        
        bars = ax2.bar(groups, untapped, color=colors)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.2)
        ax2.set_title('Untapped Voting Potential by Demographic')
        ax2.set_ylabel('Untapped Potential (%)')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:+.1f}%', ha='center', va='bottom' if height > 0 else 'top')
        
        plt.tight_layout()
        plt.savefig(self.visualization_dir / 'CA13_potential_shifts.png')
        print(f"Saved potential shifts analysis to: {self.visualization_dir / 'CA13_potential_shifts.png'}")
        plt.close()
    
    def analyze_turnout_impact(self):
        """Analyze impact of turnout improvements"""
        print("\nAnalyzing turnout impact scenarios...")
        
        fig = plt.figure(figsize=(20, 10))
        
        # 1. Turnout Improvement Scenarios
        ax1 = plt.subplot(1, 2, 1)
        
        # Calculate vote shares under different turnout improvements
        improvements = [0, 0.05, 0.10, 0.15]  # 0%, 5%, 10%, 15% improvements
        scenarios = {}
        
        for imp in improvements:
            shares = {}
            total_votes = 0
            
            # Calculate total votes under this scenario
            for group, data in self.demographics.items():
                new_turnout = min(1.0, data['turnout_rate'] + imp)
                votes = data['cvap'] * new_turnout
                total_votes += votes
            
            # Calculate shares
            for group, data in self.demographics.items():
                new_turnout = min(1.0, data['turnout_rate'] + imp)
                votes = data['cvap'] * new_turnout
                shares[group] = (votes / total_votes) * 100
            
            scenarios[f'+{int(imp*100)}%'] = shares
        
        # Plot the scenarios
        x = np.arange(len(scenarios))
        width = 0.2
        multiplier = 0
        
        for group in self.demographics.keys():
            offset = width * multiplier
            values = [scenarios[s][group] for s in scenarios.keys()]
            plt.bar(x + offset, values, width, label=group)
            multiplier += 1
        
        plt.xlabel('Turnout Improvement Scenario')
        plt.ylabel('Vote Share (%)')
        plt.title('Vote Share Under Different Turnout Improvements')
        plt.xticks(x + width * 1.5, scenarios.keys())
        plt.legend(title='Demographic Group')
        
        # 2. Power Balance Analysis
        ax2 = plt.subplot(1, 2, 2)
        
        # Calculate current and maximum minority power
        current_minority = sum(d['current_share'] for group, d in self.demographics.items() 
                             if group != 'White')
        potential_minority = sum(d['potential_share'] for group, d in self.demographics.items() 
                               if group != 'White')
        
        data = pd.DataFrame({
            'Status': ['Current', 'Potential'],
            'Minority': [current_minority * 100, potential_minority * 100],
            'White': [(1-current_minority) * 100, (1-potential_minority) * 100]
        })
        
        data.plot(kind='bar', ax=ax2, width=0.8)
        plt.title('Minority vs White Voting Power')
        plt.xlabel('Scenario')
        plt.ylabel('Share of Vote (%)')
        
        # Add value labels
        for i in ax2.containers:
            ax2.bar_label(i, fmt='%.1f%%')
        
        plt.tight_layout()
        plt.savefig(self.visualization_dir / 'CA13_turnout_impact.png')
        print(f"Saved turnout impact analysis to: {self.visualization_dir / 'CA13_turnout_impact.png'}")
        plt.close()
        
        # Print detailed analysis
        print("\nTurnout Impact Analysis:")
        print("-" * 50)
        print("\nVote Share Under Different Turnout Improvements:")
        for scenario, shares in scenarios.items():
            print(f"\n{scenario} Improvement:")
            for group, share in shares.items():
                print(f"  {group}: {share:.1f}%")

if __name__ == "__main__":
    print("CA-13 Potential and Shift Analysis")
    print("=" * 50)
    
    analyzer = CA13PotentialAnalyzer()
    analyzer.analyze_potential_shifts()
    analyzer.analyze_turnout_impact()
