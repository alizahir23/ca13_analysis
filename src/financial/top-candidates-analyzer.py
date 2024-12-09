import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

class TopCandidatesAnalyzer:
    def __init__(self):
        self.data_dir = Path('data/campaign_finance')
        self.visualization_dir = Path('data/visualizations')
        self.visualization_dir.mkdir(parents=True, exist_ok=True)
        
        # Load data
        with open(self.data_dir / 'ca13_comprehensive_data.json', 'r') as f:
            self.data = json.load(f)
        
        # Focus candidates
        self.focus_candidates = ['GRAY, ADAM C.', 'DUARTE, JOHN']
    
    def analyze_head_to_head(self):
        """Create head-to-head comparison of top candidates"""
        print("\nAnalyzing head-to-head comparison...")
        
        # Extract data for top candidates
        comparisons = []
        for name in self.focus_candidates:
            candidate_data = self.data['candidates'][name]
            financial_data = candidate_data['financial_data'][0]
            
            comparison = {
                'name': name,
                'party': candidate_data['candidate_info']['party'],
                'total_receipts': financial_data.get('receipts', 0),
                'total_disbursements': financial_data.get('disbursements', 0),
                'individual_contributions': financial_data.get('individual_contributions', 0),
                'pac_contributions': financial_data.get('pac_contributions', 0),
                'operating_expenditures': financial_data.get('operating_expenditures', 0),
                'loan_payments': financial_data.get('loan_payments', 0),
                'refunds': financial_data.get('refunds', 0)
            }
            comparisons.append(comparison)
        
        df = pd.DataFrame(comparisons)
        
        # Create visualization
        plt.figure(figsize=(15, 10))
        
        # 1. Financial Overview
        plt.subplot(2, 1, 1)
        metrics = ['total_receipts', 'total_disbursements', 'individual_contributions', 'pac_contributions']
        x = np.arange(len(metrics))
        width = 0.35
        
        gray_data = df[df['name'] == 'GRAY, ADAM C.'][metrics].values[0] / 1000
        duarte_data = df[df['name'] == 'DUARTE, JOHN'][metrics].values[0] / 1000
        
        plt.bar(x - width/2, gray_data, width, label='Gray (D)', color='blue', alpha=0.6)
        plt.bar(x + width/2, duarte_data, width, label='Duarte (R)', color='red', alpha=0.6)
        
        plt.title('Financial Overview: Gray vs Duarte')
        plt.xticks(x, [m.replace('_', ' ').title() for m in metrics], rotation=45)
        plt.ylabel('Thousands of Dollars')
        plt.legend()
        
        # Add value labels
        for i, v in enumerate(gray_data):
            plt.text(i - width/2, v, f'${v:,.0f}K', ha='center', va='bottom')
        for i, v in enumerate(duarte_data):
            plt.text(i + width/2, v, f'${v:,.0f}K', ha='center', va='bottom')
        
        # 2. Fundraising Efficiency
        plt.subplot(2, 1, 2)
        
        # Calculate efficiency metrics
        efficiency_metrics = pd.DataFrame([
            {
                'name': row['name'],
                'party': row['party'],
                'burn_rate': row['total_disbursements'] / row['total_receipts'] * 100,
                'individual_contribution_rate': row['individual_contributions'] / row['total_receipts'] * 100,
                'pac_contribution_rate': row['pac_contributions'] / row['total_receipts'] * 100
            }
            for _, row in df.iterrows()
        ])
        
        metrics = ['burn_rate', 'individual_contribution_rate', 'pac_contribution_rate']
        x = np.arange(len(metrics))
        
        for i, row in efficiency_metrics.iterrows():
            color = 'blue' if row['party'] == 'DEM' else 'red'
            plt.bar(x + (i-0.5)*width, 
                   [row[m] for m in metrics],
                   width,
                   label=row['name'].split(',')[0],
                   color=color,
                   alpha=0.6)
        
        plt.title('Campaign Efficiency Metrics')
        plt.xticks(x, ['Burn Rate', 'Individual Cont. Rate', 'PAC Cont. Rate'], rotation=45)
        plt.ylabel('Percentage')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(self.visualization_dir / 'ca13_head_to_head.png')
        print(f"Saved head-to-head analysis to: {self.visualization_dir / 'ca13_head_to_head.png'}")
        plt.close()
        
        # Print detailed comparison
        print("\nDetailed Head-to-Head Comparison:")
        print("-" * 50)
        
        for _, row in df.iterrows():
            print(f"\n{row['name']} ({row['party']}):")
            print(f"  Total Raised: ${row['total_receipts']:,.2f}")
            print(f"  Total Spent: ${row['total_disbursements']:,.2f}")
            print(f"  Individual Contributions: ${row['individual_contributions']:,.2f}")
            print(f"  PAC Contributions: ${row['pac_contributions']:,.2f}")
            print(f"  Burn Rate: {row['total_disbursements']/row['total_receipts']*100:.1f}%")
            
        # Calculate and print key differences
        gray_data = df[df['name'] == 'GRAY, ADAM C.'].iloc[0]
        duarte_data = df[df['name'] == 'DUARTE, JOHN'].iloc[0]
        
        fundraising_gap = gray_data['total_receipts'] - duarte_data['total_receipts']
        spending_gap = gray_data['total_disbursements'] - duarte_data['total_disbursements']
        
        print("\nKey Differences:")
        print(f"Fundraising Gap (Gray - Duarte): ${fundraising_gap:,.2f}")
        print(f"Spending Gap (Gray - Duarte): ${spending_gap:,.2f}")

if __name__ == "__main__":
    print("CA-13 Top Candidates Analysis")
    print("=" * 50)
    
    analyzer = TopCandidatesAnalyzer()
    analyzer.analyze_head_to_head()
