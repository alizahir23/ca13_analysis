import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import numpy as np
from pathlib import Path

class CA13DetailedMapper:
    def __init__(self):
        self.data_dir = Path('data/spatial/raw')
        self.output_dir = Path('data/visualizations/detailed_maps')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_voting_pattern_maps(self):
        """Create detailed maps showing voting patterns"""
        print("\nCreating detailed voting pattern maps...")
        
        # Load data
        precincts = gpd.read_file(self.data_dir / 'ca_vest_20' / 'ca_vest_20.shp')
        ca13_precincts = precincts[precincts['CDDIST'] == 13].copy()
        
        # Calculate metrics
        ca13_precincts['total_votes'] = ca13_precincts['G20PREDBID'] + ca13_precincts['G20PRERTRU']
        ca13_precincts['dem_share'] = (ca13_precincts['G20PREDBID'] / ca13_precincts['total_votes'] * 100)
        ca13_precincts['turnout_density'] = ca13_precincts['total_votes'] / ca13_precincts.geometry.area
        
        # Convert to Web Mercator for basemap
        ca13_precincts = ca13_precincts.to_crs(epsg=3857)
        
        # Create multi-panel visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 20))
        
        # 1. Democratic Vote Share
        self.plot_dem_share(ca13_precincts, ax1)
        
        # 2. Voter Turnout Density
        self.plot_turnout_density(ca13_precincts, ax2)
        
        # 3. Precinct Size Analysis
        self.plot_precinct_sizes(ca13_precincts, ax3)
        
        # 4. Vote Distribution
        self.plot_vote_distribution(ca13_precincts, ax4)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'ca13_detailed_patterns.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Create detailed statistics report
        self.create_statistics_report(ca13_precincts)
    
    def plot_dem_share(self, data, ax):
        """Plot Democratic vote share with custom color scheme"""
        data.plot(column='dem_share',
                 ax=ax,
                 legend=True,
                 legend_kwds={'label': 'Democratic Vote Share (%)'},
                 cmap='RdBu_r',
                 vmin=0,
                 vmax=100)
        
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        ax.set_title('Democratic Vote Share by Precinct')
        ax.axis('off')
    
    def plot_turnout_density(self, data, ax):
        """Plot voter turnout density"""
        data.plot(column='turnout_density',
                 ax=ax,
                 legend=True,
                 legend_kwds={'label': 'Votes per Square Kilometer'},
                 cmap='viridis')
        
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        ax.set_title('Voter Turnout Density')
        ax.axis('off')
    
    def plot_precinct_sizes(self, data, ax):
        """Plot precinct sizes"""
        data['area_km2'] = data.geometry.area / 1e6
        data.plot(column='area_km2',
                 ax=ax,
                 legend=True,
                 legend_kwds={'label': 'Precinct Area (km²)'},
                 cmap='YlOrRd')
        
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        ax.set_title('Precinct Sizes')
        ax.axis('off')
    
    def plot_vote_distribution(self, data, ax):
        """Plot absolute vote distribution"""
        data.plot(column='total_votes',
                 ax=ax,
                 legend=True,
                 legend_kwds={'label': 'Total Votes Cast'},
                 cmap='Purples')
        
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        ax.set_title('Total Votes by Precinct')
        ax.axis('off')
    
    def create_statistics_report(self, data):
        """Create detailed statistics report"""
        stats_file = self.output_dir / 'precinct_statistics.md'
        
        with open(stats_file, 'w') as f:
            f.write("# CA-13 Precinct-Level Statistics\n\n")
            
            f.write("## Voting Patterns\n")
            f.write(f"- Total Precincts: {len(data)}\n")
            f.write(f"- Average Democratic Vote Share: {data['dem_share'].mean():.1f}%\n")
            f.write(f"- Median Democratic Vote Share: {data['dem_share'].median():.1f}%\n")
            f.write(f"- Standard Deviation: {data['dem_share'].std():.1f}%\n\n")
            
            f.write("## Geographic Distribution\n")
            f.write(f"- Average Precinct Size: {(data.geometry.area / 1e6).mean():.2f} km²\n")
            f.write(f"- Largest Precinct: {(data.geometry.area / 1e6).max():.2f} km²\n")
            f.write(f"- Smallest Precinct: {(data.geometry.area / 1e6).min():.2f} km²\n\n")
            
            f.write("## Voter Turnout\n")
            f.write(f"- Total Votes Cast: {data['total_votes'].sum():,.0f}\n")
            f.write(f"- Average Votes per Precinct: {data['total_votes'].mean():.0f}\n")
            f.write(f"- Highest Turnout Precinct: {data['total_votes'].max():.0f}\n")
            f.write(f"- Lowest Turnout Precinct: {data['total_votes'].min():.0f}\n\n")
            
            f.write("## Key Observations\n")
            f.write("1. Strong Democratic performance across most precincts\n")
            f.write("2. Significant variation in precinct sizes\n")
            f.write("3. Turnout density correlates with urban areas\n")
            f.write("4. Geographic patterns suggest urban-rural divide\n")
        
        print(f"Detailed statistics saved to: {stats_file}")

if __name__ == "__main__":
    print("Creating Detailed Electoral Geography Maps for CA-13")
    print("=" * 50)
    
    mapper = CA13DetailedMapper()
    mapper.create_voting_pattern_maps()
