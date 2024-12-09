import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

class CA13ElectionAnalyzer:
    def __init__(self):
        self.data_dir = Path('data')
        self.analysis_dir = self.data_dir / 'analysis'
        self.processed_dir = self.data_dir / 'processed'
        self.demographic_data = None
        self.total_cvap = 393416  # From previous analysis
        
    def analyze_voter_potential(self):
        """Analyze potential voter turnout based on demographics"""
        # Load demographic analysis
        with open(self.analysis_dir / 'CA13_demographic_analysis.txt', 'r') as f:
            demographic_text = f.read()
        
        print("CA-13 Voter Analysis")
        print("=" * 50)
        
        # Historical turnout rates by demographic (national averages)
        # Source: U.S. Census Bureau, Current Population Survey
        historical_turnout = {
            'Hispanic': 0.54,  # 54% turnout in 2020
            'Black': 0.63,    # 63% turnout in 2020
            'Asian': 0.59,    # 59% turnout in 2020
            'White': 0.71     # 71% turnout in 2020
        }
        
        # Calculate potential voters by demographic
        demographic_voters = {}
        total_potential_voters = 0
        
        for group, turnout_rate in historical_turnout.items():
            # Extract percentage from previous analysis
            if group == 'Hispanic':
                pct = 0.502  # 50.2%
            elif group == 'Black':
                pct = 0.041  # 4.1%
            elif group == 'Asian':
                pct = 0.062  # 6.2%
            elif group == 'White':
                pct = 0.371  # 37.1%
                
            eligible_voters = self.total_cvap * pct
            potential_voters = eligible_voters * turnout_rate
            demographic_voters[group] = {
                'eligible': eligible_voters,
                'potential_turnout': potential_voters,
                'turnout_rate': turnout_rate
            }
            total_potential_voters += potential_voters
        
        self.create_turnout_analysis(demographic_voters, total_potential_voters)
        self.create_turnout_visualizations(demographic_voters)
        self.save_turnout_analysis(demographic_voters, total_potential_voters)
        
    def create_turnout_analysis(self, demographic_voters, total_potential_voters):
        """Print detailed turnout analysis"""
        print("\nPotential Voter Turnout Analysis:")
        print("-" * 50)
        print(f"Total CVAP: {self.total_cvap:,.0f}")
        print(f"Estimated Total Turnout: {total_potential_voters:,.0f}")
        print(f"Estimated Turnout Rate: {(total_potential_voters/self.total_cvap)*100:.1f}%")
        
        print("\nBreakdown by Demographic:")
        for group, data in demographic_voters.items():
            print(f"\n{group}:")
            print(f"  Eligible Voters: {data['eligible']:,.0f}")
            print(f"  Expected Turnout: {data['potential_turnout']:,.0f}")
            print(f"  Historical Turnout Rate: {data['turnout_rate']*100:.1f}%")
            print(f"  % of Total Expected Turnout: {(data['potential_turnout']/total_potential_voters)*100:.1f}%")
    
    def create_turnout_visualizations(self, demographic_voters):
        """Create visualizations of turnout analysis"""
        plt.figure(figsize=(15, 6))
        
        # Turnout comparison
        plt.subplot(1, 2, 1)
        groups = list(demographic_voters.keys())
        eligible = [data['eligible'] for data in demographic_voters.values()]
        turnout = [data['potential_turnout'] for data in demographic_voters.values()]
        
        x = np.arange(len(groups))
        width = 0.35
        
        plt.bar(x - width/2, eligible, width, label='Eligible Voters')
        plt.bar(x + width/2, turnout, width, label='Expected Turnout')
        
        plt.xlabel('Demographic Group')
        plt.ylabel('Number of Voters')
        plt.title('Eligible vs Expected Turnout by Demographic')
        plt.xticks(x, groups)
        plt.legend()
        
        # Turnout rates
        plt.subplot(1, 2, 2)
        rates = [data['turnout_rate']*100 for data in demographic_voters.values()]
        plt.bar(groups, rates)
        plt.ylabel('Turnout Rate (%)')
        plt.title('Historical Turnout Rates by Demographic')
        plt.xticks(rotation=45)
        
        for i, v in enumerate(rates):
            plt.text(i, v + 1, f'{v:.1f}%', ha='center')
        
        plt.tight_layout()
        plt.savefig(self.analysis_dir / 'CA13_turnout_analysis.png')
        print(f"\nSaved turnout visualizations to: {self.analysis_dir / 'CA13_turnout_analysis.png'}")
        plt.show()
    
    def save_turnout_analysis(self, demographic_voters, total_potential_voters):
        """Save detailed turnout analysis to file"""
        analysis_path = self.analysis_dir / 'CA13_turnout_analysis.txt'
        
        with open(analysis_path, 'w') as f:
            f.write("CA-13 Congressional District Turnout Analysis\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total CVAP: {self.total_cvap:,.0f}\n")
            f.write(f"Estimated Total Turnout: {total_potential_voters:,.0f}\n")
            f.write(f"Estimated Turnout Rate: {(total_potential_voters/self.total_cvap)*100:.1f}%\n\n")
            
            f.write("Demographic Breakdown:\n")
            f.write("-" * 20 + "\n")
            for group, data in demographic_voters.items():
                f.write(f"\n{group}:\n")
                f.write(f"  Eligible Voters: {data['eligible']:,.0f}\n")
                f.write(f"  Expected Turnout: {data['potential_turnout']:,.0f}\n")
                f.write(f"  Historical Turnout Rate: {data['turnout_rate']*100:.1f}%\n")
                f.write(f"  % of Total Expected Turnout: {(data['potential_turnout']/total_potential_voters)*100:.1f}%\n")
        
        print(f"\nSaved detailed turnout analysis to: {analysis_path}")

if __name__ == "__main__":
    analyzer = CA13ElectionAnalyzer()
    analyzer.analyze_voter_potential()
