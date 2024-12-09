import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os

class CA13Processor:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.data_dir = self.base_dir / 'data'
        self.district_data = None
        self.ca13_data = None
        
    def process_district_data(self):
        """Process the 2021 Final District data"""
        try:
            # Path to shapefile
            shapefile_path = self.data_dir / 'ca_cong_adopted_2021' / 'CD_Final 2021-12-20.shp'
            
            if not shapefile_path.exists():
                print(f"Error: Shapefile not found at {shapefile_path}")
                return False
            
            print("Loading district data...")
            self.district_data = gpd.read_file(shapefile_path)
            
            # Look for district identifier in the data
            print("\nAvailable columns:", self.district_data.columns.tolist())
            
            # Try to find district column (common names in CA redistricting data)
            district_cols = ['DISTRICT', 'District', 'CD', 'CD_NUM', 'CONG_DIST']
            district_col = None
            
            for col in district_cols:
                if col in self.district_data.columns:
                    district_col = col
                    break
            
            if district_col is None:
                print("\nCould not automatically find district column.")
                print("Please select the column containing district numbers:")
                for i, col in enumerate(self.district_data.columns):
                    print(f"{i}: {col}")
                col_idx = int(input("Enter column number: "))
                district_col = self.district_data.columns[col_idx]
            
            # Extract CA-13
            print(f"\nExtracting District 13 using column: {district_col}")
            self.ca13_data = self.district_data[
                self.district_data[district_col].astype(str).str.strip() == '13'
            ]
            
            if len(self.ca13_data) == 0:
                print("Error: Could not find District 13")
                print("Available districts:", 
                      sorted(self.district_data[district_col].unique()))
                return False
            
            # Save processed data
            output_dir = self.data_dir / 'processed'
            output_dir.mkdir(exist_ok=True)
            
            output_path = output_dir / 'CA13_boundary.geojson'
            self.ca13_data.to_file(output_path, driver='GeoJSON')
            print(f"\nSaved CA-13 boundary to: {output_path}")
            
            # Create visualizations
            self.create_district_maps()
            
            return True
            
        except Exception as e:
            print(f"Error processing district data: {e}")
            return False
    
    def create_district_maps(self):
        """Create maps of CA-13"""
        if self.ca13_data is None:
            print("No data loaded")
            return
        
        try:
            # Create output directory for maps
            maps_dir = self.data_dir / 'maps'
            maps_dir.mkdir(exist_ok=True)
            
            # Create two maps: state context and district detail
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
            
            # State context map
            self.district_data.plot(ax=ax1, color='lightgray', edgecolor='black')
            self.ca13_data.plot(ax=ax1, color='red', edgecolor='black')
            ax1.set_title('CA-13 Location in California')
            ax1.axis('equal')
            
            # District detail map
            self.ca13_data.plot(ax=ax2, color='lightblue', edgecolor='black')
            ax2.set_title('CA-13 District Detail')
            ax2.axis('equal')
            
            # Remove axis ticks for cleaner look
            for ax in [ax1, ax2]:
                ax.set_xticks([])
                ax.set_yticks([])
            
            plt.tight_layout()
            
            # Save maps
            map_path = maps_dir / 'CA13_maps.png'
            plt.savefig(map_path, dpi=300, bbox_inches='tight')
            print(f"\nSaved maps to: {map_path}")
            plt.show()
            
        except Exception as e:
            print(f"Error creating maps: {e}")
    
    def analyze_district_data(self):
        """Analyze district characteristics"""
        if self.ca13_data is None:
            print("No data loaded")
            return
        
        print("\nCA-13 District Analysis:")
        print("-" * 50)
        print(f"Number of geometric features: {len(self.ca13_data)}")
        print(f"Coordinate system: {self.ca13_data.crs}")
        
        # Calculate area (if applicable)
        if self.ca13_data.crs and self.ca13_data.crs.is_projected:
            area_km2 = self.ca13_data.geometry.area.sum() / 1_000_000  # Convert to km²
            print(f"Approximate district area: {area_km2:.2f} km²")
        
        print("\nAvailable attributes:")
        for col in self.ca13_data.columns:
            if col != 'geometry':
                print(f"- {col}: {self.ca13_data[col].iloc[0]}")
        print("-" * 50)

if __name__ == "__main__":
    processor = CA13Processor()
    
    print("CA-13 District Data Processor")
    print("=" * 50)
    
    if processor.process_district_data():
        processor.analyze_district_data()
        print("\nProcessing complete! Check the 'data/processed' and 'data/maps' directories for outputs.")
    else:
        print("\nProcessing failed. Please check the error messages above.")
