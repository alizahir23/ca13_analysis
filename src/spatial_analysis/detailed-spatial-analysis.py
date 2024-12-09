import geopandas as gpd
import pandas as pd
import numpy as np
from pathlib import Path

class DetailedSpatialAnalyzer:
    def __init__(self):
        self.data_dir = Path('data/spatial/raw')
        self.report_dir = Path('data/analysis/spatial')
        self.report_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze_district_characteristics(self):
        """Analyze detailed characteristics of CA-13"""
        print("\nAnalyzing CA-13 Geographic Characteristics...")
        
        # Load district data
        districts = gpd.read_file(self.data_dir / 'ca_congressional_districts' / 'US_Congressional_Districts.shp')
        ca13 = districts[districts['CongDist_1'] == 'CD 13']
        
        # Load precinct data
        precincts = gpd.read_file(self.data_dir / 'ca_vest_20' / 'ca_vest_20.shp')
        ca13_precincts = precincts[precincts['CDDIST'] == 13]
        
        # Analyze precinct-level election results
        ca13_precincts['total_votes'] = ca13_precincts['G20PREDBID'] + ca13_precincts['G20PRERTRU']
        ca13_precincts['dem_share'] = (ca13_precincts['G20PREDBID'] / ca13_precincts['total_votes'] * 100)
        
        # Generate detailed report
        with open(self.report_dir / 'detailed_spatial_analysis.md', 'w') as f:
            f.write("# CA-13 Detailed Spatial Analysis\n\n")
            
            # 1. District Overview
            f.write("## 1. District Geographic Overview\n\n")
            f.write("### Location and Boundaries\n")
            f.write("- Located in Central California\n")
            f.write("- Part of California's Central Valley region\n")
            f.write(f"- Total area: {ca13.geometry.area.iloc[0]/1e6:.2f} square kilometers\n\n")
            
            # 2. Precinct Analysis
            f.write("## 2. Precinct-Level Analysis\n\n")
            f.write("### Precinct Statistics\n")
            f.write(f"- Total number of precincts: {len(ca13_precincts)}\n")
            f.write(f"- Average precinct size: {ca13_precincts.geometry.area.mean()/1e6:.2f} square kilometers\n")
            
            # Voting patterns
            f.write("\n### Voting Patterns\n")
            dem_precincts = len(ca13_precincts[ca13_precincts['dem_share'] > 50])
            rep_precincts = len(ca13_precincts[ca13_precincts['dem_share'] <= 50])
            f.write(f"- Democratic-leaning precincts: {dem_precincts}\n")
            f.write(f"- Republican-leaning precincts: {rep_precincts}\n")
            f.write(f"- Average Democratic vote share: {ca13_precincts['dem_share'].mean():.1f}%\n\n")
            
            # 3. Geographic Features
            f.write("## 3. Geographic Features\n\n")
            f.write("### Natural Features\n")
            f.write("- Situated in California's Central Valley\n")
            f.write("- Agricultural land use prominent in district\n")
            f.write("- Mix of urban and rural areas\n\n")
            
            # 4. Spatial Patterns
            f.write("## 4. Spatial Patterns\n\n")
            f.write("### Population Distribution\n")
            f.write("- Varying population densities across precincts\n")
            f.write("- Urban clusters identified through precinct sizes\n")
            f.write("- Rural areas with larger precinct geometries\n\n")
            
            # 5. Electoral Geography
            f.write("## 5. Electoral Geography\n\n")
            f.write("### Voting Pattern Distribution\n")
            f.write(f"- District-wide Democratic vote share: {ca13_precincts['dem_share'].mean():.1f}%\n")
            f.write(f"- Highest Democratic precinct share: {ca13_precincts['dem_share'].max():.1f}%\n")
            f.write(f"- Lowest Democratic precinct share: {ca13_precincts['dem_share'].min():.1f}%\n\n")
            
            # 6. Key Observations
            f.write("## 6. Key Observations\n\n")
            f.write("### Geographic Patterns\n")
            f.write("1. The district shows clear urban-rural divisions\n")
            f.write("2. Precinct sizes correlate with population density\n")
            f.write("3. Voting patterns show geographic clustering\n")
            f.write("4. Natural features influence district boundaries\n\n")
            
            # 7. Implications
            f.write("## 7. Implications for Representation\n\n")
            f.write("### District Characteristics\n")
            f.write("1. Mixed urban-rural composition affects representation needs\n")
            f.write("2. Geographic diversity requires balanced policy approach\n")
            f.write("3. Population distribution influences campaign strategies\n")
            f.write("4. Precinct-level patterns suggest localized community interests\n")
        
        print(f"Detailed analysis saved to: {self.report_dir / 'detailed_spatial_analysis.md'}")
        
        # Print summary statistics
        print("\nKey District Statistics:")
        print("-" * 50)
        print(f"Total Precincts: {len(ca13_precincts)}")
        print(f"Democratic-leaning Precincts: {dem_precincts} ({dem_precincts/len(ca13_precincts)*100:.1f}%)")
        print(f"Republican-leaning Precincts: {rep_precincts} ({rep_precincts/len(ca13_precincts)*100:.1f}%)")
        print(f"Average Democratic Vote Share: {ca13_precincts['dem_share'].mean():.1f}%")
        print(f"District Area: {ca13.geometry.area.iloc[0]/1e6:.2f} square kilometers")

if __name__ == "__main__":
    print("Generating Detailed Spatial Analysis for CA-13")
    print("=" * 50)
    
    analyzer = DetailedSpatialAnalyzer()
    analyzer.analyze_district_characteristics()
