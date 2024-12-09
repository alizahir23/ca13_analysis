import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class CA13DemographicAnalyzer:
    def __init__(self):
        self.data_dir = Path('data')
        self.processed_dir = self.data_dir / 'processed'
        self.output_dir = self.data_dir / 'analysis'
        self.output_dir.mkdir(exist_ok=True)
        self.district_data = None
        
    def load_data(self):
        """Load the processed CA-13 data"""

        try:
            filepath = self.processed_dir / 'CA13_boundary.geojson'
            self.district_data = gpd.read_file(filepath)
            print("Successfully loaded CA-13 data")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def analyze_demographics(self):
        """Analyze demographic composition of CA-13"""
        if self.district_data is None:
            print("No data loaded")
            return
        
        # Extract demographic data
        demographics = {
            'Total Population': self.district_data['POPULATION'].iloc[0],
            'Citizen Voting Age Population': self.district_data['CVAP_19'].iloc[0],
            'Hispanic CVAP': self.district_data['HSP_CVAP_1'].iloc[0],
            'Black (Non-Hispanic) CVAP': self.district_data['DOJ_NH_BLK'].iloc[0],
            'Asian (Non-Hispanic) CVAP': self.district_data['DOJ_NH_ASN'].iloc[0],
            'White (Non-Hispanic) CVAP': self.district_data['NH_WHT_CVA'].iloc[0]
        }
        
        # Calculate percentages
        cvap_total = demographics['Citizen Voting Age Population']
        demographic_pcts = {
            'Hispanic': (demographics['Hispanic CVAP'] / cvap_total) * 100,
            'Black': (demographics['Black (Non-Hispanic) CVAP'] / cvap_total) * 100,
            'Asian': (demographics['Asian (Non-Hispanic) CVAP'] / cvap_total) * 100,
            'White': (demographics['White (Non-Hispanic) CVAP'] / cvap_total) * 100
        }
        
        # Create summary report
        print("\nCA-13 Demographic Analysis")
        print("=" * 50)
        print(f"Total Population: {demographics['Total Population']:,.0f}")
        print(f"Citizen Voting Age Population: {cvap_total:,.0f}")
        print("\nCVAP Demographic Breakdown:")
        for group, pct in demographic_pcts.items():
            print(f"{group}: {pct:.1f}%")
        
        # Create visualization
        self.create_demographic_plots(demographic_pcts)
        
        # Save analysis to file
        self.save_analysis(demographics, demographic_pcts)
    
    def create_demographic_plots(self, demographic_pcts):
        """Create visualizations of demographic data"""
        # Pie chart
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.pie(demographic_pcts.values(), labels=demographic_pcts.keys(), autopct='%1.1f%%')
        plt.title('CA-13 CVAP Demographic Distribution')
        
        # Bar chart
        plt.subplot(1, 2, 2)
        bars = plt.bar(demographic_pcts.keys(), demographic_pcts.values())
        plt.title('CA-13 CVAP Demographics')
        plt.ylabel('Percentage')
        plt.xticks(rotation=45)
        
        # Add percentage labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Save the plots
        plt.savefig(self.output_dir / 'CA13_demographics.png')
        print(f"\nSaved demographic visualizations to: {self.output_dir / 'CA13_demographics.png'}")
        plt.show()
    
    def save_analysis(self, demographics, demographic_pcts):
        """Save analysis results to file"""
        report_path = self.output_dir / 'CA13_demographic_analysis.txt'
        
        with open(report_path, 'w') as f:
            f.write("CA-13 Congressional District Demographic Analysis\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("Population Statistics:\n")
            f.write("-" * 20 + "\n")
            for key, value in demographics.items():
                f.write(f"{key}: {value:,.0f}\n")
            
            f.write("\nCVAP Demographic Percentages:\n")
            f.write("-" * 20 + "\n")
            for group, pct in demographic_pcts.items():
                f.write(f"{group}: {pct:.1f}%\n")
            
            f.write("\nDistrict Properties:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Ideal Value: {self.district_data['IDEAL_VALU'].iloc[0]:,.0f}\n")
            f.write(f"Deviation: {self.district_data['DEVIATION'].iloc[0]:,.0f}\n")
            f.write(f"Deviation Percentage: {self.district_data['F_DEVIATIO'].iloc[0]:.2f}%\n")
        
        print(f"\nSaved detailed analysis to: {report_path}")

if __name__ == "__main__":
    analyzer = CA13DemographicAnalyzer()
    print("Entry")
    if analyzer.load_data():
        analyzer.analyze_demographics()
    else:
        print("Failed to load data. Please ensure the processed data file exists.")
