import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class CA13VotingPatternAnalyzer:
    def __init__(self):
        self.data_dir = Path('data')
        self.visualization_dir = self.data_dir / 'visualizations'
        self.visualization_dir.mkdir(exist_ok=True)
        
        # Demographics data with extended information
        self.demographics = {
            'Hispanic': {
                'cvap': 197495, 
                'turnout_rate': 0.54,
                'expected_votes': 106647,
                'share': 0.454
            },
            'Black': {
                'cvap': 16130, 
                'turnout_rate': 0.63,
                'expected_votes': 10162,
                'share': 0.043
            },
            'Asian': {
                'cvap': 24392, 
                'turnout_rate': 0.59,
                'expected_votes': 14391,
                'share': 0.061
            },
            'White': {
                'cvap': 145957, 
                'turnout_rate': 0.71,
                'expected_votes': 103629,
                'share': 0.441
            }
        }
        
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def analyze_voter_composition(self):
        """Create detailed voter composition analysis"""
        print("\nAnalyzing voter composition...")
        
        fig = plt.figure(figsize=(20, 10))
        
        # 1. Voter Power Index
        ax1 = plt.subplot(1, 2, 1)
        groups = list(self.demographics.keys())
        cvap_share = [d['cvap']/sum(d['cvap'] for d in self.demographics.values()) for d in self.demographics.values()]
        voter_share = [d['share'] for d in self.demographics.values()]
        power_index = [v/c for v, c in zip(voter_share, cvap_share)]
        
        bars = plt.bar(groups, power_index)
        plt.axhline(y=1, color='r', linestyle='--', alpha=0.5)
        plt.title('Voter Power Index\n(Share of Votes / Share of Population)')
        plt.ylabel('Power Index (1.0 = Proportional Representation)')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom')
        
        # 2. Comparative Influence Analysis
        ax2 = plt.subplot(1, 2, 2)
        
        # Create a matrix of relative voting power
        total_votes = sum(d['expected_votes'] for d in self.demographics.values())
        voting_power = {}
        
        for g1 in groups:
            voting_power[g1] = {}
            for g2 in groups:
                if g1 != g2:
                    ratio = self.demographics[g1]['expected_votes'] / self.demographics[g2]['expected_votes']
                    voting_power[g1][g2] = ratio
        
        power_df = pd.DataFrame(voting_power)
        sns.heatmap(power_df, annot=True, fmt='.2f', cmap='RdYlBu')
        plt.title('Relative Voting Power Matrix\n(Row Group / Column Group)')
        
        plt.tight_layout()
        plt.savefig(self.visualization_dir / 'CA13_voter_composition.png')
        print(f"Saved voter composition analysis to: {self.visualization_dir / 'CA13_voter_composition.png'}")
        plt.close()
    
    def analyze_turnout_scenarios(self):
        """Analyze different turnout scenarios"""
        print("\nAnalyzing turnout scenarios...")
        
        fig = plt.figure(figsize=(20, 10))
        
        # 1. Turnout Sensitivity Analysis
        ax1 = plt.subplot(1, 2, 1)
        
        # Create turnout scenarios
        scenarios = {
            'Current': [d['turnout_rate'] for d in self.demographics.values()],
            '+5%': [min(1, d['turnout_rate'] + 0.05) for d in self.demographics.values()],
            '+10%': [min(1, d['turnout_rate'] + 0.10) for d in self.demographics.values()],
            'Maximum': [1.0 for _ in self.demographics.values()]
        }
        
        x = np.arange(len(self.demographics))
        width = 0.2
        multiplier = 0
        
        for scenario, rates in scenarios.items():
            offset = width * multiplier
            plt.bar(x + offset, np.array(rates) * 100, width, label=scenario)
            multiplier += 1
        
        plt.xlabel('Demographic Group')
        plt.ylabel('Turnout Rate (%)')
        plt.title('Turnout Scenarios')
        plt.xticks(x + width * 1.5, self.demographics.keys())
        plt.legend(loc='upper right')
        
        # 2. Voting Power Balance
        ax2 = plt.subplot(1, 2, 2)
        
        # Calculate current voting power balance
        total_votes = sum(d['expected_votes'] for d in self.demographics.values())
        hispanic_white_ratio = self.demographics['Hispanic']['expected_votes'] / self.demographics['White']['expected_votes']
        minority_combined = (self.demographics['Hispanic']['expected_votes'] + 
                           self.demographics['Black']['expected_votes'] + 
                           self.demographics['Asian']['expected_votes'])
        minority_ratio = minority_combined / total_votes
        
        plt.pie([minority_combined, self.demographics['White']['expected_votes']], 
                labels=['Combined Minority', 'White'],
                autopct='%1.1f%%',
                colors=['#2ecc71', '#3498db'])
        plt.title('Combined Minority vs White Voting Power')
        
        plt.tight_layout()
        plt.savefig(self.visualization_dir / 'CA13_turnout_scenarios.png')
        print(f"Saved turnout scenarios analysis to: {self.visualization_dir / 'CA13_turnout_scenarios.png'}")
        plt.close()
        
        # Print detailed analysis
        print("\nDetailed Voting Power Analysis:")
        print("-" * 50)
        print(f"Hispanic/White Voting Power Ratio: {hispanic_white_ratio:.2f}")
        print(f"Combined Minority Share: {minority_ratio*100:.1f}%")
        
        print("\nTurnout Impact Analysis:")
        print("-" * 50)
        for group, data in self.demographics.items():
            current_share = data['expected_votes'] / total_votes
            max_potential = data['cvap'] / sum(d['cvap'] for d in self.demographics.values())
            print(f"\n{group}:")
            print(f"  Current Voting Share: {current_share*100:.1f}%")
            print(f"  Maximum Potential Share: {max_potential*100:.1f}%")
            print(f"  Untapped Potential: {(max_potential - current_share)*100:.1f}%")

if __name__ == "__main__":
    print("CA-13 Voting Pattern Analysis")
    print("=" * 50)
    
    analyzer = CA13VotingPatternAnalyzer()
    analyzer.analyze_voter_composition()
    analyzer.analyze_turnout_scenarios()
