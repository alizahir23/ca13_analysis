import pandas as pd
import numpy as np
from pathlib import Path
import json
import re

class CountyDataProcessor:
    def __init__(self):
        self.data_dir = Path('data/election_data')
        self.county_dir = self.data_dir / 'county_data'
        self.county_dir.mkdir(exist_ok=True)
        
        # 2022 CA-13 County Data Template
        self.county_template = {
            'Fresno': {
                'precincts_in_ca13': [],
                'total_votes': 0,
                'democratic_votes': 0,
                'republican_votes': 0,
                'registered_voters': 0
            },
            'Madera': {
                'precincts_in_ca13': [],
                'total_votes': 0,
                'democratic_votes': 0,
                'republican_votes': 0,
                'registered_voters': 0
            },
            'Merced': {
                'precincts_in_ca13': [],
                'total_votes': 0,
                'democratic_votes': 0,
                'republican_votes': 0,
                'registered_voters': 0
            },
            'San Joaquin': {
                'precincts_in_ca13': [],
                'total_votes': 0,
                'democratic_votes': 0,
                'republican_votes': 0,
                'registered_voters': 0
            },
            'Stanislaus': {
                'precincts_in_ca13': [],
                'total_votes': 0,
                'democratic_votes': 0,
                'republican_votes': 0,
                'registered_voters': 0
            }
        }
    
    def create_county_templates(self):
        """Create data entry templates for each county"""
        for county in self.county_template.keys():
            county_file = self.county_dir / f"{county.lower().replace(' ', '_')}_template.csv"
            
            # Create template DataFrame
            df = pd.DataFrame(columns=[
                'precinct_id',
                'precinct_name',
                'in_ca13',  # Yes/No flag
                'registered_voters',
                'total_votes',
                'democratic_votes',
                'republican_votes',
                'other_votes'
            ])
            
            df.to_csv(county_file, index=False)
            print(f"Created template for {county}: {county_file}")
    
    def process_county_data(self, county_name):
        """Process election data for a specific county"""
        county_file = self.county_dir / f"{county_name.lower().replace(' ', '_')}_data.csv"
        
        if not county_file.exists():
            print(f"No data file found for {county_name}")
            return None
        
        try:
            # Load county data
            df = pd.read_csv(county_file)
            
            # Filter for precincts in CA-13
            ca13_precincts = df[df['in_ca13'] == 'Yes']
            
            # Calculate county totals
            county_summary = {
                'precincts_in_ca13': ca13_precincts['precinct_id'].tolist(),
                'total_votes': ca13_precincts['total_votes'].sum(),
                'democratic_votes': ca13_precincts['democratic_votes'].sum(),
                'republican_votes': ca13_precincts['republican_votes'].sum(),
                'registered_voters': ca13_precincts['registered_voters'].sum()
            }
            
            return county_summary
            
        except Exception as e:
            print(f"Error processing {county_name} data: {e}")
            return None
    
    def summarize_district_results(self):
        """Combine all county data and summarize district results"""
        district_summary = {
            'total_registered': 0,
            'total_votes': 0,
            'democratic_votes': 0,
            'republican_votes': 0,
            'county_breakdown': {}
        }
        
        for county in self.county_template.keys():
            county_data = self.process_county_data(county)
            
            if county_data:
                district_summary['total_registered'] += county_data['registered_voters']
                district_summary['total_votes'] += county_data['total_votes']
                district_summary['democratic_votes'] += county_data['democratic_votes']
                district_summary['republican_votes'] += county_data['republican_votes']
                
                # Calculate county-specific percentages
                total_county_votes = county_data['total_votes']
                if total_county_votes > 0:
                    district_summary['county_breakdown'][county] = {
                        'total_votes': total_county_votes,
                        'democratic_percentage': (county_data['democratic_votes'] / total_county_votes) * 100,
                        'republican_percentage': (county_data['republican_votes'] / total_county_votes) * 100
                    }
        
        # Calculate district-wide percentages
        total_votes = district_summary['total_votes']
        if total_votes > 0:
            district_summary['democratic_percentage'] = (district_summary['democratic_votes'] / total_votes) * 100
            district_summary['republican_percentage'] = (district_summary['republican_votes'] / total_votes) * 100
            district_summary['turnout'] = (total_votes / district_summary['total_registered']) * 100
        
        self.save_district_summary(district_summary)
        return district_summary
    
    def save_district_summary(self, summary):
        """Save district summary to file"""
        summary_file = self.data_dir / 'ca13_2022_summary.json'
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=4)
        
        print(f"\nSaved district summary to: {summary_file}")
        
        # Create a readable report
        report_file = self.data_dir / 'ca13_2022_report.txt'
        
        with open(report_file, 'w') as f:
            f.write("CA-13 2022 Election Results Summary\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("District-Wide Results:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Registered Voters: {summary['total_registered']:,}\n")
            f.write(f"Total Votes Cast: {summary['total_votes']:,}\n")
            f.write(f"Turnout: {summary['turnout']:.1f}%\n\n")
            
            f.write("Vote Distribution:\n")
            f.write(f"Democratic: {summary['democratic_percentage']:.1f}%")
            f.write(f" ({summary['democratic_votes']:,} votes)\n")
            f.write(f"Republican: {summary['republican_percentage']:.1f}%")
            f.write(f" ({summary['republican_votes']:,} votes)\n\n")
            
            f.write("County Breakdown:\n")
            for county, data in summary['county_breakdown'].items():
                f.write(f"\n{county} County:\n")
                f.write(f"  Total Votes: {data['total_votes']:,}\n")
                f.write(f"  Democratic: {data['democratic_percentage']:.1f}%\n")
                f.write(f"  Republican: {data['republican_percentage']:.1f}%\n")
        
        print(f"Created detailed report: {report_file}")

if __name__ == "__main__":
    processor = CountyDataProcessor()
    
    print("CA-13 County Election Data Processor")
    print("=" * 50)
    
    # Create templates for data entry
    processor.create_county_templates()
    
    print("\nNext steps:")
    print("1. Fill in the county templates with 2022 election data")
    print("2. Save each county's data as '[county_name]_data.csv'")
    print("3. Run this script again to process the data")
    
    print("\nData collection tips:")
    print("- Focus on one county at a time")
    print("- Mark precincts as 'Yes' in the 'in_ca13' column if they're part of CA-13")
    print("- Double-check precinct numbers against district maps")
    print("- Document any data sources or notes in a separate text file")
