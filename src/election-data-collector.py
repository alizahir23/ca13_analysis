import pandas as pd
import requests
from pathlib import Path
import json
import time

class ElectionDataCollector:
    def __init__(self):
        self.data_dir = Path('data')
        self.election_dir = self.data_dir / 'election_data'
        self.election_dir.mkdir(exist_ok=True)
        self.results = {}
        
    def create_election_template(self):
        """Create a template for manual data entry"""
        template = {
            'general_elections': {
                '2022': {
                    'date': 'November 8, 2022',
                    'total_votes': None,
                    'candidates': {
                        'democratic': {
                            'name': 'John Duarte',
                            'party': 'Democratic',
                            'votes': None,
                            'percentage': None
                        },
                        'republican': {
                            'name': 'Adam Gray',
                            'party': 'Republican',
                            'votes': None,
                            'percentage': None
                        }
                    },
                    'turnout': None
                },
                '2020': {
                    'date': 'November 3, 2020',
                    'total_votes': None,
                    'candidates': {
                        'democratic': {
                            'name': 'Barbara Lee',  # Previous district
                            'party': 'Democratic',
                            'votes': None,
                            'percentage': None
                        },
                        'republican': {
                            'name': 'Nikka Piterman',
                            'party': 'Republican',
                            'votes': None,
                            'percentage': None
                        }
                    },
                    'turnout': None
                }
            }
        }
        
        # Save template
        template_path = self.election_dir / 'election_data_template.json'
        with open(template_path, 'w') as f:
            json.dump(template, f, indent=4)
            
        # Create CSV template for precinct-level data
        precinct_template = pd.DataFrame(columns=[
            'year', 'precinct_id', 'precinct_name', 'total_votes',
            'democratic_votes', 'republican_votes', 'other_votes',
            'registered_voters', 'turnout'
        ])
        
        precinct_template.to_csv(self.election_dir / 'precinct_data_template.csv', index=False)
        
        print("Created data templates:")
        print(f"1. Election data template: {template_path}")
        print(f"2. Precinct data template: {self.election_dir / 'precinct_data_template.csv'}")
        print("\nPlease fill in the templates with data from:")
        print("- CA Secretary of State: https://www.sos.ca.gov/elections/prior-elections")
        print("- County Election Offices:")
        print("  * Fresno County: https://www.co.fresno.ca.us/departments/county-clerk-registrar-of-voters/election-information/election-results")
        print("  * Madera County: https://votemadera.com/election-results/")
        print("  * Merced County: https://www.co.merced.ca.us/221/Elections")
        print("  * San Joaquin County: https://www.sjgov.org/department/rov/election-information/past-elections")
        print("  * Stanislaus County: https://www.stanvote.com/past-elections.shtm")
        
        self.create_data_collection_guide()
    
    def create_data_collection_guide(self):
        """Create a guide for collecting election data"""
        guide_path = self.election_dir / 'data_collection_guide.txt'
        
        with open(guide_path, 'w') as f:
            f.write("CA-13 Election Data Collection Guide\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("1. District Information:\n")
            f.write("   - Current CA-13 (2022-Present):\n")
            f.write("     * Parts of Fresno, Madera, Merced, San Joaquin, and Stanislaus counties\n")
            f.write("   - Previous CA-13 (Pre-2022):\n")
            f.write("     * Different boundaries (Oakland area)\n\n")
            
            f.write("2. Data Sources:\n")
            f.write("   a) State Level:\n")
            f.write("      - CA Secretary of State website\n")
            f.write("      - Statement of Vote archives\n\n")
            
            f.write("   b) County Level:\n")
            f.write("      - Each county's election office website\n")
            f.write("      - Contact county registrars for detailed precinct data\n\n")
            
            f.write("3. Data to Collect:\n")
            f.write("   - Total votes cast\n")
            f.write("   - Votes by candidate\n")
            f.write("   - Voter turnout\n")
            f.write("   - Precinct-level results where available\n")
            f.write("   - Registration statistics\n\n")
            
            f.write("4. Important Notes:\n")
            f.write("   - Document data sources\n")
            f.write("   - Note any discrepancies\n")
            f.write("   - Record collection date\n")
            f.write("   - Note any boundary changes\n")
        
        print(f"\nCreated data collection guide: {guide_path}")

if __name__ == "__main__":
    collector = ElectionDataCollector()
    collector.create_election_template()
