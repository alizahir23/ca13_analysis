import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class CA13EnhancedExplorer:
    def __init__(self):
        self.data_dir = Path('data')
        self.visualization_dir = self.data_dir / 'visualizations'
        self.visualization_dir.mkdir(exist_ok=True)
        
        # Demographics data
        self.demographics = {
            'Hispanic': {'cvap': 197495, 'turnout_rate': 0.54},
            'Black': {'cvap': 16130, 'turnout_rate': 0.63},
            'Asian': {'cvap': 24392, 'turnout_rate': 0.59},
            'White': {'cvap': 145957, 'turnout_rate': 0.71}
        }
        
        # Color schemes
        self.colors = {
            'main': ['#2ecc71', '#3498db', '#e74c3c', '#f1c40f'],
            'pastel': ['#a8e6cf', '#dcedc1', '#ffd3b6', '#ffaaa5'],
            'dark': ['#1a535c', '#4ecdc4', '#ff6b6b', '#ffe66d']
        }
    
    def create_turnout_analysis(self):
        """Create detailed turnout analysis visualizations"""
        plt.style.use('seaborn-v0_8-darkgrid')
        print("\nCreating turnout analysis visualizations...")
        
        fig = plt.figure(figsize=(20, 10))
        
        # 1. Turnout Rate vs Population Size
        ax1 = plt.subplot(1, 2, 1)
        x = [d['cvap'] for d in self.demographics.values()]
        y = [d['turnout_rate'] * 100 for d in self.demographics.values()]
        sizes = [d['cvap']/1000 for d in self.demographics.values()]  # Size proportional to population
        
        plt.scatter(x, y, s=sizes, c=self.colors['main'], alpha=0.6)
        
        # Add labels for each point
        for i, (group, data) in enumerate(self.demographics.items()):
            plt.annotate(group, 
                        (data['cvap'], data['turnout_rate'] * 100),
                        xytext=(10, 10), textcoords='offset points')
        
        plt.xlabel('CVAP Population')
        plt.ylabel('Turnout Rate (%)')
        plt.title('Turnout Rate vs Population Size')
        
        # 2. Relative Voting Power Analysis
        ax2 = plt.subplot(1, 2, 2)
        total_cvap = sum(d['cvap'] for d in self.demographics.values())
        total_voters = sum(d['cvap'] * d['turnout_rate'] for d in self.demographics.values())
        
        pop_share = [d['cvap']/total_cvap * 100 for d in self.demographics.values()]
        voter_share = [(d['cvap'] * d['turnout_rate'])/total_voters * 100 for d in self.demographics.values()]
        
        x = np.arange(len(self.demographics))
        width = 0.35
        
        ax2.bar(x - width/2, pop_share, width, label='Population Share', color='lightblue')
        ax2.bar(x + width/2, voter_share, width, label='Voter Share', color='darkblue')
        
        plt.xticks(x, self.demographics.keys(), rotation=45)
        plt.ylabel('Percentage')
        plt.title('Population Share vs Voter Share')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(self.visualization_dir / 'CA13_turnout_analysis.png')
        print(f"Saved turnout analysis to: {self.visualization_dir / 'CA13_turnout_analysis.png'}")
        plt.close()
    
    def create_comparative_analysis(self):
        """Create comparative demographic analysis"""
        plt.style.use('seaborn-v0_8-white')
        print("\nCreating comparative analysis visualizations...")
        
        fig = plt.figure(figsize=(20, 10))
        
        # 1. Normalized Comparison
        ax1 = plt.subplot(1, 2, 1)
        
        # Normalize the data
        max_cvap = max(d['cvap'] for d in self.demographics.values())
        max_turnout = max(d['turnout_rate'] for d in self.demographics.values())
        
        normalized_data = pd.DataFrame({
            'Population': [d['cvap']/max_cvap for d in self.demographics.values()],
            'Turnout Rate': [d['turnout_rate']/max_turnout for d in self.demographics.values()]
        }, index=self.demographics.keys())
        
        normalized_data.plot(kind='bar', ax=ax1, color=self.colors['pastel'])
        plt.title('Normalized Comparison (Relative to Maximum)')
        plt.legend(loc='upper right')
        
        # 2. Demographic Contribution to Total Votes
        ax2 = plt.subplot(1, 2, 2)
        votes = [d['cvap'] * d['turnout_rate'] for d in self.demographics.values()]
        plt.pie(votes, labels=self.demographics.keys(), colors=self.colors['dark'],
                autopct='%1.1f%%', startangle=90)
        plt.title('Contribution to Total Votes')
        
        plt.tight_layout()
        plt.savefig(self.visualization_dir / 'CA13_comparative_analysis.png')
        print(f"Saved comparative analysis to: {self.visualization_dir / 'CA13_comparative_analysis.png'}")
        plt.close()
        
        # Print numerical analysis
        total_votes = sum(votes)
        print("\nNumerical Analysis:")
        print("-" * 50)
        for group, vote_count in zip(self.demographics.keys(), votes):
            print(f"{group}:")
            print(f"  Expected Votes: {vote_count:,.0f}")
            print(f"  Share of Total Votes: {(vote_count/total_votes)*100:.1f}%")
    
    def create_combined_report(self):
        """Create a combined analysis report"""
        report_path = self.visualization_dir / 'CA13_analysis_report.txt'
        
        with open(report_path, 'w') as f:
            f.write("CA-13 Congressional District Analysis Report\n")
            f.write("=" * 50 + "\n\n")
            
            total_cvap = sum(d['cvap'] for d in self.demographics.values())
            total_expected_voters = sum(d['cvap'] * d['turnout_rate'] for d in self.demographics.values())
            
            f.write(f"Total CVAP: {total_cvap:,.0f}\n")
            f.write(f"Expected Voters: {total_expected_voters:,.0f}\n")
            f.write(f"Overall Expected Turnout: {(total_expected_voters/total_cvap)*100:.1f}%\n\n")
            
            f.write("Demographic Analysis:\n")
            f.write("-" * 20 + "\n")
            for group, data in self.demographics.items():
                f.write(f"\n{group}:\n")
                f.write(f"  CVAP: {data['cvap']:,.0f}\n")
                f.write(f"  Expected Turnout: {data['cvap'] * data['turnout_rate']:,.0f}\n")
                f.write(f"  Turnout Rate: {data['turnout_rate']*100:.1f}%\n")
                f.write(f"  Share of Total CVAP: {(data['cvap']/total_cvap)*100:.1f}%\n")
                f.write(f"  Share of Expected Voters: {(data['cvap']*data['turnout_rate']/total_expected_voters)*100:.1f}%\n")
        
        print(f"\nSaved detailed analysis report to: {report_path}")

if __name__ == "__main__":
    print("CA-13 Enhanced Data Exploration")
    print("=" * 50)
    
    explorer = CA13EnhancedExplorer()
    explorer.create_turnout_analysis()
    explorer.create_comparative_analysis()
    explorer.create_combined_report()
