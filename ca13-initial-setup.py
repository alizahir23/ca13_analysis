from pathlib import Path
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class CA13Analyzer:
    def __init__(self):
        """Initialize the CA-13 District Analyzer"""
        self.project_dir = Path.cwd()
        self.data_dir = self.project_dir / 'data'
        self.ensure_directories()
        
        # Data storage
        self.district_boundary = None
        self.precinct_data = None
        self.census_data = None
        self.election_data = None
        
    def ensure_directories(self):
        """Ensure necessary directories exist"""
        directories = ['data', 'notebooks', 'src']
        for directory in directories:
            dir_path = self.project_dir / directory
            dir_path.mkdir(exist_ok=True)
            
    def download_required_data(self):
        """Provide instructions for downloading required datasets"""
        print("Please download the following datasets:")
        print("\n1. CA-13 District Boundary:")
        print("   - Visit: https://redistrictingdatahub.org")
        print("   - Search for: California Congressional Districts")
        print("   - Download the shapefile for CA-13")
        print("   - Save to: data/district_boundary/")
        
        print("\n2. Census Data:")
        print("   - Visit: https://www.census.gov/data.html")
        print("   - Download ACS data for CA-13")
        print("   - Save to: data/census/")
        
        print("\n3. Election Data:")
        print("   - Visit: https://www.sos.ca.gov/elections/prior-elections")
        print("   - Download precinct-level results")
        print("   - Save to: data/election/")
    
    def load_district_boundary(self, file_path):
        """Load district boundary shapefile"""
        try:
            self.district_boundary = gpd.read_file(file_path)
            print("Successfully loaded district boundary data")
            return True
        except Exception as e:
            print(f"Error loading district boundary: {e}")
            return False
    
    def load_census_data(self, file_path):
        """Load census data"""
        try:
            self.census_data = pd.read_csv(file_path)
            print("Successfully loaded census data")
            return True
        except Exception as e:
            print(f"Error loading census data: {e}")
            return False
    
    def load_election_data(self, file_path):
        """Load election results data"""
        try:
            self.election_data = pd.read_csv(file_path)
            print("Successfully loaded election data")
            return True
        except Exception as e:
            print(f"Error loading election data: {e}")
            return False
    
    def create_district_map(self):
        """Create a basic map of CA-13"""
        if self.district_boundary is None:
            print("No district boundary data loaded")
            return
        
        fig, ax = plt.subplots(figsize=(12, 8))
        self.district_boundary.plot(ax=ax)
        ax.set_title('California Congressional District 13')
        plt.axis('equal')
        plt.show()
    
    def analyze_demographics(self):
        """Analyze demographic data"""
        if self.census_data is None:
            print("No census data loaded")
            return None
        
        # Basic demographic summary
        demographic_summary = self.census_data.describe()
        return demographic_summary
    
    def analyze_election_results(self):
        """Analyze election results"""
        if self.election_data is None:
            print("No election data loaded")
            return None
        
        # Basic election summary
        election_summary = self.election_data.describe()
        return election_summary

# Example usage
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = CA13Analyzer()
    
    # Show data download instructions
    analyzer.download_required_data()
    
    # Once data is downloaded, you can load and analyze it
    # Example paths (update these with your actual file paths):
    # analyzer.load_district_boundary('data/district_boundary/CA13.shp')
    # analyzer.load_census_data('data/census/ca13_census.csv')
    # analyzer.load_election_data('data/election/ca13_election.csv')
    
    print("\nSetup complete. Ready to begin analysis.")
