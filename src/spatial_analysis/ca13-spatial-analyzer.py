import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import pandas as pd
import numpy as np
from pathlib import Path

class CA13SpatialAnalyzer:
    def __init__(self):
        self.data_dir = Path('data/spatial')
        self.raw_dir = self.data_dir / 'raw'
        self.visualization_dir = Path('data/visualizations/spatial')
        self.visualization_dir.mkdir(parents=True, exist_ok=True)
        
        # File paths
        self.district_file = self.raw_dir / 'ca_congressional_districts' / 'US_Congressional_Districts.shp'
        self.precinct_file = self.raw_dir / 'ca_vest_20' / 'ca_vest_20.shp'
        self.tract_file = self.raw_dir / 'tl_2022_06_tract' / 'tl_2022_06_tract.shp'
    
    def load_all_data(self):
        """Load all spatial datasets"""
        print("Loading spatial datasets...")
        
        try:
            # Load Congressional Districts
            self.districts = gpd.read_file(self.district_file)
            print("✓ Loaded congressional districts")
            
            # Load VEST Precinct Data
            self.precincts = gpd.read_file(self.precinct_file)
            print("✓ Loaded precinct data")
            
            # Load Census Tracts
            self.tracts = gpd.read_file(self.tract_file)
            print("✓ Loaded census tracts")
            
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def create_district_map(self):
        """Create map of CA-13 within California"""
        print("\nCreating district map...")
        
        try:
            fig, ax = plt.subplots(figsize=(15, 15))
            
            # Plot all districts
            self.districts.plot(ax=ax, color='lightgray', edgecolor='black')
            
            # Highlight CA-13
            ca13 = self.districts[self.districts['CongDist_1'] == 'CD 13']
            ca13.plot(ax=ax, color='red', alpha=0.5)
            
            # Add labels for neighboring districts
            for idx, row in self.districts.iterrows():
                centroid = row.geometry.centroid
                ax.annotate(row['CongDist_1'], 
                          xy=(centroid.x, centroid.y),
                          ha='center', va='center',
                          fontsize=8)
            
            plt.title('California Congressional District 13 and Surroundings')
            plt.axis('equal')
            
            plt.savefig(self.visualization_dir / 'ca13_district_map.png')
            print(f"Saved district map to: {self.visualization_dir / 'ca13_district_map.png'}")
            plt.close()
            
        except Exception as e:
            print(f"Error creating district map: {e}")
    
    def create_precinct_map(self):
        """Create detailed precinct map of CA-13"""
        print("\nCreating precinct map...")
        
        try:
            # Filter precincts for CA-13
            ca13_precincts = self.precincts[self.precincts['CDDIST'] == 13]
            
            # Create multi-panel visualization
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 20))
            
            # 1. Democratic Vote Share
            ca13_precincts['dem_share'] = (
                ca13_precincts['G20PREDBID'] / 
                (ca13_precincts['G20PREDBID'] + ca13_precincts['G20PRERTRU']) * 100
            )
            ca13_precincts.plot(column='dem_share',
                              ax=ax1,
                              legend=True,
                              legend_kwds={'label': 'Democratic Vote Share (%)'},
                              cmap='RdBu_r',
                              vmin=0,
                              vmax=100)
            ax1.set_title('Democratic Vote Share')
            
            # 2. Total Votes
            ca13_precincts['total_votes'] = ca13_precincts['G20PREDBID'] + ca13_precincts['G20PRERTRU']
            ca13_precincts.plot(column='total_votes',
                              ax=ax2,
                              legend=True,
                              legend_kwds={'label': 'Total Votes'},
                              cmap='viridis')
            ax2.set_title('Total Votes by Precinct')
            
            # 3. Margin of Victory
            ca13_precincts['margin'] = (
                (ca13_precincts['G20PREDBID'] - ca13_precincts['G20PRERTRU']) /
                ca13_precincts['total_votes'] * 100
            )
            ca13_precincts.plot(column='margin',
                              ax=ax3,
                              legend=True,
                              legend_kwds={'label': 'Margin (%)'},
                              cmap='RdBu')
            ax3.set_title('Margin of Victory (+ Dem, - Rep)')
            
            # 4. Precinct Boundaries
            ca13_precincts.plot(ax=ax4, edgecolor='black', facecolor='none')
            ax4.set_title('Precinct Boundaries')
            
            # Adjust layout
            plt.tight_layout()
            plt.savefig(self.visualization_dir / 'ca13_precinct_analysis.png')
            print(f"Saved precinct analysis to: {self.visualization_dir / 'ca13_precinct_analysis.png'}")
            plt.close()
            
            # Save summary statistics
            self.print_election_statistics(ca13_precincts)
            
        except Exception as e:
            print(f"Error creating precinct map: {e}")
            print(f"Detailed error: {str(e)}")
    
    def print_election_statistics(self, ca13_precincts):
        """Print detailed election statistics"""
        print("\nCA-13 Election Statistics:")
        print("-" * 50)
        
        total_biden = ca13_precincts['G20PREDBID'].sum()
        total_trump = ca13_precincts['G20PRERTRU'].sum()
        total_votes = total_biden + total_trump
        
        print(f"Total Votes Cast: {total_votes:,.0f}")
        print(f"Biden Votes: {total_biden:,.0f} ({total_biden/total_votes*100:.1f}%)")
        print(f"Trump Votes: {total_trump:,.0f} ({total_trump/total_votes*100:.1f}%)")
        
        dem_precincts = len(ca13_precincts[ca13_precincts['G20PREDBID'] > ca13_precincts['G20PRERTRU']])
        rep_precincts = len(ca13_precincts[ca13_precincts['G20PREDBID'] < ca13_precincts['G20PRERTRU']])
        
        print(f"\nPrecincts won by Democrats: {dem_precincts}")
        print(f"Precincts won by Republicans: {rep_precincts}")
        
        # Calculate margin statistics
        margins = ca13_precincts['margin']
        print(f"\nMargin Statistics:")
        print(f"Average Margin: {margins.mean():.1f}%")
        print(f"Median Margin: {margins.median():.1f}%")
        print(f"Maximum Democratic Margin: {margins.max():.1f}%")
        print(f"Maximum Republican Margin: {margins.min():.1f}%")

if __name__ == "__main__":
    print("CA-13 Spatial Analysis")
    print("=" * 50)
    
    analyzer = CA13SpatialAnalyzer()
    
    if analyzer.load_all_data():
        analyzer.create_district_map()
        analyzer.create_precinct_map()
    else:
        print("\nError loading data. Please check file paths and data integrity.")