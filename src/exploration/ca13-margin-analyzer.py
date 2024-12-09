import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class CA13MarginAnalyzer:
    def __init__(self):
        self.data_dir = Path('data')
        self.visualization_dir = self.data_dir / 'visualizations'
        self.visualization_dir.mkdir(exist_ok=True)
        
        # Base demographic data
        self.demographics = {
            'Hispanic': {
                'cvap': 197495,
                'turnout_rate': 0.54,
                'base_share': 0.454
            },
            'Black': {
                'cvap': 16130,
                'turnout_rate': 0.63,
                'base_share': 0.043
            },
            'Asian': {
                'cvap': 24392,
                'turnout_rate': 0.59,
                'base_share': 0.061
            },
            'White': {
                'cvap': 145957,
                'turnout_rate': 0.71,
                'base_share': 0.441
            }
        }
        
        # Turnout impact data
        self.turnout_impacts = {
            '0%':  {'Hispanic': 45.4, 'Black': 4.3, 'Asian': 6.1, 'White': 44.1},
            '5%':  {'Hispanic': 45.9, 'Black': 4.3, 'Asian': 6.1, 'White': 43.7},
            '10%': {'Hispanic': 46.3, 'Black': 4.3, 'Asian': 6.2, 'White': 43.3},
            '15%': {'Hispanic': 46.6, 'Black': 4.3, 'Asian': 6.2, 'White': 42.9}
        }
    
    def calculate_margins(self):
        """Calculate Hispanic-White margins across scenarios"""
        margins = []
        scenarios = ['0%', '5%', '10%', '15%']
        for scenario in scenarios:
            margin = self.turnout_impacts[scenario]['Hispanic'] - self.turnout_impacts[scenario]['White']
            margins.append(margin)
        return margins, scenarios
    
    def analyze_turnout_patterns(self):
        """Analyze detailed turnout patterns"""
        print("\nAnalyzing turnout patterns...")
        
        margins, scenarios = self.calculate_margins()
        
        # Plot turnout pattern analysis
        fig = plt.figure(figsize=(20, 10))
        
        # 1. Vote Share Changes
        ax1 = plt.subplot(1, 2, 1)
        for group in ['Hispanic', 'White', 'Asian', 'Black']:
            shares = [self.turnout_impacts[s][group] for s in scenarios]
            plt.plot(scenarios, shares, marker='o', label=group)
        
        plt.title('Vote Share by Demographic\nAcross Turnout Scenarios')
        plt.xlabel('Turnout Improvement Scenario')
        plt.ylabel('Vote Share (%)')
        plt.legend()
        plt.grid(True)
        
        # 2. Hispanic-White Margin
        ax2 = plt.subplot(1, 2, 2)
        plt.bar(scenarios, margins, color=['green' if m > 0 else 'red' for m in margins])
        plt.title('Hispanic-White Vote Share Margin\nBy Turnout Scenario')
        plt.xlabel('Turnout Improvement Scenario')
        plt.ylabel('Margin (Percentage Points)')
        
        # Add value labels
        for i, margin in enumerate(margins):
            plt.annotate(f'{margin:+.1f}',
                        (scenarios[i], margin),
                        textcoords="offset points",
                        xytext=(0,10),
                        ha='center')
        
        plt.tight_layout()
        plt.savefig(self.visualization_dir / 'CA13_turnout_patterns.png')
        print(f"Saved turnout pattern analysis to: {self.visualization_dir / 'CA13_turnout_patterns.png'}")
        plt.close()
        
        # Print detailed analysis
        print("\nDetailed Turnout Analysis:")
        print("-" * 50)
        print(f"Initial Hispanic-White margin: {margins[0]:+.1f} points")
        print(f"Final Hispanic-White margin: {margins[-1]:+.1f} points")
        print(f"Total margin change: {margins[-1] - margins[0]:+.1f} points")
        
        # Analyze demographic shifts
        print("\nDemographic Shifts:")
        print("-" * 50)
        for group in self.demographics:
            initial = self.turnout_impacts['0%'][group]
            final = self.turnout_impacts['15%'][group]
            change = final - initial
            print(f"{group}:")
            print(f"  Initial share: {initial:.1f}%")
            print(f"  Final share: {final:.1f}%")
            print(f"  Net change: {change:+.1f} points")
    
    def analyze_combined_minority_impact(self):
        """Analyze combined minority voting power"""
        print("\nAnalyzing combined minority impact...")
        
        scenarios = ['0%', '5%', '10%', '15%']
        minority_shares = []
        white_shares = []
        
        for scenario in scenarios:
            minority = (self.turnout_impacts[scenario]['Hispanic'] + 
                       self.turnout_impacts[scenario]['Black'] + 
                       self.turnout_impacts[scenario]['Asian'])
            minority_shares.append(minority)
            white_shares.append(self.turnout_impacts[scenario]['White'])
        
        # Plot combined minority analysis
        plt.figure(figsize=(12, 8))
        plt.plot(scenarios, minority_shares, 'g-o', label='Combined Minority', linewidth=2)
        plt.plot(scenarios, white_shares, 'b-o', label='White', linewidth=2)
        
        plt.title('Combined Minority vs White Share\nUnder Turnout Improvements')
        plt.xlabel('Turnout Improvement Scenario')
        plt.ylabel('Vote Share (%)')
        plt.legend()
        plt.grid(True)
        
        # Add value labels
        for i, (min_share, white_share) in enumerate(zip(minority_shares, white_shares)):
            plt.annotate(f'{min_share:.1f}%', 
                        (scenarios[i], min_share),
                        textcoords="offset points",
                        xytext=(0,10),
                        ha='center')
            plt.annotate(f'{white_share:.1f}%', 
                        (scenarios[i], white_share),
                        textcoords="offset points",
                        xytext=(0,-15),
                        ha='center')
        
        plt.tight_layout()
        plt.savefig(self.visualization_dir / 'CA13_minority_impact.png')
        print(f"Saved minority impact analysis to: {self.visualization_dir / 'CA13_minority_impact.png'}")
        plt.close()
        
        # Print analysis
        print("\nCombined Minority vs White Analysis:")
        print("-" * 50)
        for i, scenario in enumerate(scenarios):
            print(f"\n{scenario} Improvement:")
            print(f"  Combined Minority: {minority_shares[i]:.1f}%")
            print(f"  White: {white_shares[i]:.1f}%")
            print(f"  Margin: {minority_shares[i] - white_shares[i]:+.1f} points")

if __name__ == "__main__":
    print("CA-13 Turnout Impact Analysis")
    print("=" * 50)
    
    analyzer = CA13MarginAnalyzer()
    analyzer.analyze_turnout_patterns()
    analyzer.analyze_combined_minority_impact()