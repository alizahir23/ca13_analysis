import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

class CA13FinanceAnalyzer:
    def __init__(self):
        self.data_dir = Path('data/campaign_finance')
        self.visualization_dir = Path('data/visualizations')
        self.visualization_dir.mkdir(parents=True, exist_ok=True)
        self.load_data()
    
    def load_data(self):
        """Load the comprehensive campaign finance data"""
        try:
            with open(self.data_dir / 'ca13_comprehensive_data.json', 'r') as f:
                self.data = json.load(f)
            print("Successfully loaded campaign finance data")
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False
    
    def prepare_financial_summary(self):
        """Prepare summary of financial data for each candidate"""
        summaries = []
        
        for name, info in self.data['candidates'].items():
            financial_data = info.get('financial_data', [{}])[0]
            candidate_info = info.get('candidate_info', {})
            
            summary = {
                'name': name,
                'party': candidate_info.get('party', 'Unknown'),
                'receipts': financial_data.get('receipts', 0),
                'disbursements': financial_data.get('disbursements', 0),
                'cash_on_hand': financial_data.get('cash_on_hand_end_period', 0),
                'individual_contributions': financial_data.get('individual_contributions', 0),
                'pac_contributions': financial_data.get('pac_contributions', 0),
                'operating_expenditures': financial_data.get('operating_expenditures', 0)
            }
            summaries.append(summary)
        
        return pd.DataFrame(summaries)
    
    def analyze_campaign_finances(self):
        """Create comprehensive financial analysis"""
        print("\nAnalyzing campaign finances...")
        df = self.prepare_financial_summary()
        
        # Sort by total receipts
        df_sorted = df.sort_values('receipts', ascending=False)
        
        # Create visualizations
        plt.figure(figsize=(15, 10))
        
        # 1. Total Receipts by Candidate
        plt.subplot(2, 1, 1)
        colors = ['blue' if party == 'DEM' else 'red' for party in df_sorted['party']]
        bars = plt.bar(df_sorted['name'], df_sorted['receipts'] / 1000, color=colors)
        plt.title('Total Campaign Receipts by Candidate')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Thousands of Dollars')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}K',
                    ha='center', va='bottom')
        
        # 2. Cash on Hand Comparison
        plt.subplot(2, 1, 2)
        metrics = ['cash_on_hand', 'disbursements']
        bar_width = 0.35
        index = np.arange(len(df_sorted))
        
        for i, metric in enumerate(metrics):
            offset = i * bar_width
            plt.bar(index + offset, df_sorted[metric] / 1000, bar_width,
                   label=metric.replace('_', ' ').title(),
                   color=['lightblue', 'lightgreen'][i])
        
        plt.title('Cash on Hand vs Disbursements')
        plt.xticks(index + bar_width/2, df_sorted['name'], rotation=45, ha='right')
        plt.ylabel('Thousands of Dollars')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(self.visualization_dir / 'ca13_campaign_finance_overview.png')
        print(f"Saved finance overview to: {self.visualization_dir / 'ca13_campaign_finance_overview.png'}")
        plt.close()
        
        # Print detailed analysis
        print("\nDetailed Financial Analysis:")
        print("-" * 50)
        
        # By party totals
        party_totals = df.groupby('party').agg({
            'receipts': 'sum',
            'disbursements': 'sum',
            'cash_on_hand': 'sum'
        })
        
        print("\nTotals by Party:")
        for party, totals in party_totals.iterrows():
            print(f"\n{party}:")
            print(f"  Total Raised: ${totals['receipts']:,.2f}")
            print(f"  Total Spent: ${totals['disbursements']:,.2f}")
            print(f"  Cash on Hand: ${totals['cash_on_hand']:,.2f}")
        
        # Top fundraisers
        print("\nTop Fundraisers:")
        for _, row in df_sorted.head(3).iterrows():
            print(f"\n{row['name']} ({row['party']}):")
            print(f"  Total Raised: ${row['receipts']:,.2f}")
            print(f"  Cash on Hand: ${row['cash_on_hand']:,.2f}")
            print(f"  Burn Rate: {(row['disbursements']/row['receipts']*100 if row['receipts'] > 0 else 0):.1f}%")

    def analyze_contribution_patterns(self):
        """Analyze patterns in campaign contributions"""
        df = self.prepare_financial_summary()
        
        plt.figure(figsize=(15, 8))
        
        # Calculate contribution breakdown
        df['individual_pct'] = df['individual_contributions'] / df['receipts'] * 100
        df['pac_pct'] = df['pac_contributions'] / df['receipts'] * 100
        
        # Sort by total receipts
        df_sorted = df.sort_values('receipts', ascending=False)
        
        # Stacked bar chart of contribution sources
        contribution_data = pd.DataFrame({
            'Individual': df_sorted['individual_contributions'],
            'PAC': df_sorted['pac_contributions'],
            'Other': df_sorted['receipts'] - df_sorted['individual_contributions'] - df_sorted['pac_contributions']
        }, index=df_sorted['name'])
        
        ax = contribution_data.plot(kind='bar', stacked=True)
        plt.title('Contribution Sources by Candidate')
        plt.xlabel('Candidate')
        plt.ylabel('Dollars')
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Source')
        
        plt.tight_layout()
        plt.savefig(self.visualization_dir / 'ca13_contribution_patterns.png')
        print(f"\nSaved contribution patterns to: {self.visualization_dir / 'ca13_contribution_patterns.png'}")
        plt.close()

if __name__ == "__main__":
    print("CA-13 Campaign Finance Analysis")
    print("=" * 50)
    
    analyzer = CA13FinanceAnalyzer()
    analyzer.analyze_campaign_finances()
    analyzer.analyze_contribution_patterns()
