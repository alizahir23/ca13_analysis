import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from pathlib import Path

class CA13GISMapper:
    def __init__(self):
        self.data_dir = Path('data/spatial/raw')
        self.output_dir = Path('data/visualizations/gis_maps')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def map_california_districts(self):
        """Map 1: All Congressional Districts in California"""
        print("\nCreating California Congressional Districts map...")
        
        # Load district data
        districts = gpd.read_file(self.data_dir / 'ca_congressional_districts' / 'US_Congressional_Districts.shp')
        
        # Convert to Web Mercator projection for basemap
        districts = districts.to_crs(epsg=3857)
        
        fig, ax = plt.subplots(figsize=(15, 20))
        
        # Plot districts with different colors and labels
        districts.plot(ax=ax, 
                      column='CongDist_1',
                      categorical=True,
                      legend=True,
                      legend_kwds={'bbox_to_anchor': (1.3, 1)},
                      alpha=0.6)
        
        # Highlight CA-13
        ca13 = districts[districts['CongDist_1'] == 'CD 13']
        ca13.plot(ax=ax, color='red', alpha=0.4, label='CD 13')
        
        # Add OpenStreetMap basemap
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        
        # Add title and legend
        plt.title('California Congressional Districts\nDistrict 13 Highlighted', pad=20)
        
        # Add district labels
        for idx, row in districts.iterrows():
            centroid = row.geometry.centroid
            plt.annotate(row['CongDist_1'], 
                        xy=(centroid.x, centroid.y),
                        ha='center', fontsize=8)
        
        plt.axis('off')
        plt.savefig(self.output_dir / 'california_districts.png', 
                   bbox_inches='tight', dpi=300)
        plt.close()
        
        return districts, ca13  # Return for use in other methods
    
    def map_district_13(self, districts=None, ca13=None):
        """Map 2: Detailed map of CA-13"""
        print("\nCreating detailed CA-13 map...")
        
        if districts is None or ca13 is None:
            # Load district data if not provided
            districts = gpd.read_file(self.data_dir / 'ca_congressional_districts' / 'US_Congressional_Districts.shp')
            districts = districts.to_crs(epsg=3857)
            ca13 = districts[districts['CongDist_1'] == 'CD 13']
        
        # Get CA-13 bounds
        ca13_bounds = ca13.geometry.bounds.iloc[0]
        
        fig, ax = plt.subplots(figsize=(15, 15))
        
        # Plot CA-13 with context
        districts.plot(ax=ax, color='lightgrey', alpha=0.3)
        ca13.plot(ax=ax, color='red', alpha=0.6)
        
        # Add OpenStreetMap basemap
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        
        plt.title('California Congressional District 13', pad=20)
        
        # Zoom to CA-13 with buffer
        ax.set_xlim(ca13_bounds.minx - 50000, ca13_bounds.maxx + 50000)
        ax.set_ylim(ca13_bounds.miny - 50000, ca13_bounds.maxy + 50000)
        
        plt.axis('off')
        plt.savefig(self.output_dir / 'district_13.png', 
                   bbox_inches='tight', dpi=300)
        plt.close()
        
        return ca13  # Return for use in other methods
    
    def map_precincts(self, ca13=None):
        """Map 3: Precincts within CA-13"""
        print("\nCreating precinct map...")
        
        # Load precinct data
        precincts = gpd.read_file(self.data_dir / 'ca_vest_20' / 'ca_vest_20.shp')
        precincts = precincts.to_crs(epsg=3857)
        
        # Filter for CA-13 precincts
        ca13_precincts = precincts[precincts['CDDIST'] == 13]
        
        fig, ax = plt.subplots(figsize=(15, 15))
        
        # Plot precincts with 2020 election results
        ca13_precincts['dem_share'] = (
            ca13_precincts['G20PREDBID'] / 
            (ca13_precincts['G20PREDBID'] + ca13_precincts['G20PRERTRU']) * 100
        )
        
        ca13_precincts.plot(ax=ax,
                           column='dem_share',
                           legend=True,
                           legend_kwds={'label': 'Democratic Vote Share (%)',
                                      'orientation': 'vertical'},
                           cmap='RdBu',
                           vmin=0,
                           vmax=100)
        
        # Add OpenStreetMap basemap
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        
        plt.title('CA-13 Precincts\n2020 Presidential Election Results', pad=20)
        plt.axis('off')
        plt.savefig(self.output_dir / 'ca13_precincts.png', 
                   bbox_inches='tight', dpi=300)
        plt.close()
    
    def map_demographic_feature(self, ca13=None):
        """Map 4: Census tract feature within CA-13"""
        print("\nCreating demographic feature map...")
        
        if ca13 is None:
            # Load district data if not provided
            districts = gpd.read_file(self.data_dir / 'ca_congressional_districts' / 'US_Congressional_Districts.shp')
            districts = districts.to_crs(epsg=3857)
            ca13 = districts[districts['CongDist_1'] == 'CD 13']
        
        # Load census tract data
        tracts = gpd.read_file(self.data_dir / 'tl_2022_06_tract' / 'tl_2022_06_tract.shp')
        tracts = tracts.to_crs(epsg=3857)
        
        # Clip tracts to CA-13 boundary
        ca13_tracts = gpd.overlay(tracts, ca13, how='intersection')
        
        fig, ax = plt.subplots(figsize=(15, 15))
        
        # Plot census tracts with a choropleth based on land area
        ca13_tracts.plot(ax=ax,
                        column='ALAND',
                        legend=True,
                        legend_kwds={'label': 'Land Area (sq meters)'},
                        cmap='YlOrRd')
        
        # Add OpenStreetMap basemap
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        
        plt.title('CA-13 Census Tracts\nLand Area Distribution', pad=20)
        plt.axis('off')
        plt.savefig(self.output_dir / 'ca13_demographic_feature.png', 
                   bbox_inches='tight', dpi=300)
        plt.close()

if __name__ == "__main__":
    print("Creating GIS Maps for CA-13")
    print("=" * 50)
    
    # First, make sure we have all required packages
    try:
        import contextily as ctx
        print("✓ Successfully imported contextily")
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call(["pip", "install", "contextily"])
        import contextily as ctx
    
    mapper = CA13GISMapper()
    
    # Create maps in sequence, passing data between methods
    districts, ca13 = mapper.map_california_districts()
    mapper.map_district_13(districts, ca13)
    mapper.map_precincts()
    mapper.map_demographic_feature(ca13)
    
    print("\nAll maps have been created!")
    print(f"\nMaps are saved in: {mapper.output_dir}")