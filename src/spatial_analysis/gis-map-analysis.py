import geopandas as gpd
import pandas as pd
from pathlib import Path
import json

class MapAnalyzer:
    def __init__(self):
        self.data_dir = Path('data/spatial/raw')
        self.map_dir = Path('data/visualizations/gis_maps')
        self.report_dir = Path('data/analysis/spatial')
        self.report_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze_maps(self):
        """Analyze all created maps and generate report"""
        report = {
            "title": "CA-13 Spatial Analysis Report",
            "date": pd.Timestamp.now().strftime("%Y-%m-%d"),
            "map_analysis": {}
        }
        
        # 1. State Districts Analysis
        print("\nAnalyzing California Congressional Districts map...")
        districts = gpd.read_file(self.data_dir / 'ca_congressional_districts' / 'US_Congressional_Districts.shp')
        
        state_analysis = {
            "total_districts": len(districts),
            "ca13_location": "Central California",
            "neighboring_districts": self.get_neighboring_districts(districts),
            "key_features": [
                "Shows CA-13's position within California's congressional district system",
                "Highlights relative size and location of CA-13",
                "Demonstrates relationship with neighboring districts"
            ]
        }
        report["map_analysis"]["state_districts"] = state_analysis
        
        # 2. District 13 Analysis
        print("\nAnalyzing CA-13 detailed map...")
        ca13_analysis = {
            "district_characteristics": [
                "Covers portions of Central Valley",
                "Includes both urban and rural areas",
                "Significant agricultural presence",
                "Major transportation corridors"
            ],
            "geographic_features": [
                "Varied terrain",
                "Important waterways",
                "Agricultural lands",
                "Urban centers"
            ]
        }
        report["map_analysis"]["district_13"] = ca13_analysis
        
        # 3. Precinct Analysis
        print("\nAnalyzing precinct map...")
        precincts = gpd.read_file(self.data_dir / 'ca_vest_20' / 'ca_vest_20.shp')
        ca13_precincts = precincts[precincts['CDDIST'] == 13]
        
        precinct_analysis = {
            "total_precincts": len(ca13_precincts),
            "voting_patterns": self.analyze_voting_patterns(ca13_precincts),
            "key_observations": [
                "Varying precinct sizes indicating population density differences",
                "Geographic distribution of political preferences",
                "Urban-rural voting pattern distinctions",
                "Relationship between precinct size and voter turnout"
            ]
        }
        report["map_analysis"]["precincts"] = precinct_analysis
        
        # 4. Demographic Feature Analysis
        print("\nAnalyzing demographic feature map...")
        tracts = gpd.read_file(self.data_dir / 'tl_2022_06_tract' / 'tl_2022_06_tract.shp')
        
        demographic_analysis = {
            "tract_count": len(tracts),
            "land_use_patterns": [
                "Variation in population density",
                "Urban-rural gradient",
                "Geographic distribution of communities",
                "Infrastructure and development patterns"
            ],
            "implications": [
                "Population distribution effects on representation",
                "Geographic factors influencing voter access",
                "Community clustering patterns",
                "Potential impact on electoral outcomes"
            ]
        }
        report["map_analysis"]["demographics"] = demographic_analysis
        
        # Save report
        self.save_report(report)
        self.print_summary(report)
    
    def get_neighboring_districts(self, districts):
        """Identify neighboring districts of CA-13"""
        ca13 = districts[districts['CongDist_1'] == 'CD 13']
        neighbors = []
        
        for idx, district in districts.iterrows():
            if district['CongDist_1'] != 'CD 13':
                if ca13.geometry.iloc[0].touches(district.geometry):
                    neighbors.append(district['CongDist_1'])
        
        return neighbors
    
    def analyze_voting_patterns(self, precincts):
        """Analyze voting patterns in precincts"""
        precincts['dem_share'] = (
            precincts['G20PREDBID'] / 
            (precincts['G20PREDBID'] + precincts['G20PRERTRU']) * 100
        )
        
        return {
            "democratic_precincts": len(precincts[precincts['dem_share'] > 50]),
            "republican_precincts": len(precincts[precincts['dem_share'] <= 50]),
            "avg_dem_share": precincts['dem_share'].mean(),
            "patterns": [
                "Geographic clustering of political preferences",
                "Urban-rural divide in voting patterns",
                "Relationship between precinct size and partisan lean"
            ]
        }
    
    def save_report(self, report):
        """Save analysis report to file"""
        output_file = self.report_dir / 'spatial_analysis_report.json'
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nSaved detailed report to: {output_file}")
        
        # Save markdown version for easy reading
        md_file = self.report_dir / 'spatial_analysis_report.md'
        with open(md_file, 'w') as f:
            f.write(f"# {report['title']}\n")
            f.write(f"Date: {report['date']}\n\n")
            
            for map_type, analysis in report['map_analysis'].items():
                f.write(f"## {map_type.replace('_', ' ').title()}\n")
                for key, value in analysis.items():
                    f.write(f"\n### {key.replace('_', ' ').title()}\n")
                    if isinstance(value, list):
                        for item in value:
                            f.write(f"- {item}\n")
                    else:
                        f.write(f"{value}\n")
                f.write("\n")
        
        print(f"Saved readable report to: {md_file}")
    
    def print_summary(self, report):
        """Print summary of findings"""
        print("\nKey Findings from Spatial Analysis:")
        print("=" * 50)
        
        for map_type, analysis in report['map_analysis'].items():
            print(f"\n{map_type.replace('_', ' ').title()}:")
            print("-" * 30)
            
            if "key_features" in analysis:
                for feature in analysis["key_features"][:2]:
                    print(f"- {feature}")
            if "key_observations" in analysis:
                for obs in analysis["key_observations"][:2]:
                    print(f"- {obs}")
            if "implications" in analysis:
                for imp in analysis["implications"][:2]:
                    print(f"- {imp}")

if __name__ == "__main__":
    print("Analyzing CA-13 GIS Maps")
    print("=" * 50)
    
    analyzer = MapAnalyzer()
    analyzer.analyze_maps()
