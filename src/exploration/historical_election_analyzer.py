import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class HistoricalElectionAnalyzer:
    def __init__(self):
        self.data_dir = Path('data')
        self.analysis_dir = self.data_dir / 'analysis'
        self.analysis_dir.mkdir(exist_ok=True)
        
        # Sample historical election data (we'll replace this with actual data)
        self.historical_data = {
            '2020': {'dem': 56.4, 'rep': 43.6, 'turnout': 82.5},
            '2018': {'dem': 54.8, 'rep': 45.2, 'turnout': 65.3},
            '2016': {'dem': 55.2, 'rep': 44.8, 'turnout': 78.4}
        }
    
    def analyze_historical_trends(self):
        """Analyze historical election trends"""
        print("CA-13 Historical Election Analysis")
        print("=" * 50)
        
        # Create DataFrames for analysis
        years = list(self.historical_data.keys())
        dem_share = [self.historical_data[year]['dem'] for year in years]
        rep_share = [self.historical_data[year]['rep'] for year in years]
        turnout = [self.historical_data[year]['turnout'] for year in years]
        
        df = pd.DataFrame({
            'Year': years,
            'Democratic': dem_share,
            'Republican': rep_share,
            'Turnout': turnout
        })
        
        # Calculate metrics
        dem_avg = np.mean(dem_share)
        rep_avg = np.mean(rep_share)
        turnout_avg = np.mean(turnout)
        
        # Print analysis
        print("\nHistorical Voting Patterns:")
        print("-" * 30)
        print(f"Average Democratic Vote Share: {dem_avg:.1f}%")
        print(f"Average Republican Vote Share: {rep_avg:.1f}%")
        print(f"Average Turnout: {turnout_avg:.1f}%")
        
        # Create visualizations
        self.create_historical_plots(df)
        
        # Save analysis
        self.save_historical_analysis(df)
        
    def create_historical_plots(self, df):
        """Create visualizations of historical trends"""
        plt.figure(figsize=(15, 6))
        
        # Vote share trends
        plt.subplot(1, 2, 1)
        plt.plot(df['Year'], df['Democratic'], 'b-o', label='Democratic')
        plt.plot(df['Year'], df['Republican'], 'r-o', label='Republican')
        plt.title('Party Vote Share Over Time')
        plt.ylabel('Vote Share (%)')
        plt.legend()
        plt.grid(True)
        
        # Turnout trends
        plt.subplot(1, 2, 2)
        plt.plot(df['Year'], df['Turnout'], 'g-o')
        plt.title('Voter Turnout Over Time')
        plt.ylabel('Turnout (%)')
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(self.analysis_dir / 'CA13_historical_trends.png')
        print(f"\nSaved historical trend visualizations to: {self.analysis_dir / 'CA13_historical_trends.png'}")
        plt.show()
    
    def save_historical_analysis(self, df):
        """Save historical analysis to file"""
        analysis_path = self.analysis_dir / 'CA13_historical_analysis.txt'
        
        with open(analysis_path, 'w') as f:
            f.write("CA-13 Historical Election Analysis\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("Year-by-Year Results:\n")
            f.write("-" * 20 + "\n")
            for year in self.historical_data.keys():
                data = self.historical_data[year]
                f.write(f"\n{year}:\n")
                f.write(f"  Democratic: {data['dem']:.1f}%\n")
                f.write(f"  Republican: {data['rep']:.1f}%\n")
                f.write(f"  Turnout: {data['turnout']:.1f}%\n")
            
            f.write("\nAverages:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Democratic: {df['Democratic'].mean():.1f}%\n")
            f.write(f"Republican: {df['Republican'].mean():.1f}%\n")
            f.write(f"Turnout: {df['Turnout'].mean():.1f}%\n")
        
        print(f"\nSaved historical analysis to: {analysis_path}")

if __name__ == "__main__":
    analyzer = HistoricalElectionAnalyzer()
    analyzer.analyze_historical_trends()
