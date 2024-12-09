import requests
import json
from pathlib import Path
import pandas as pd
from datetime import datetime

class FECDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.open.fec.gov/v1"
        self.data_dir = Path('data/campaign_finance')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def test_api_connection(self):
        """Test the API connection and key validity"""
        try:
            test_url = f"{self.base_url}/candidates"
            params = {
                'api_key': self.api_key,
                'per_page': 1
            }
            
            print("Testing API connection...")
            response = requests.get(test_url, params=params)
            
            if response.status_code == 200:
                print("✓ API connection successful!")
                return True
            else:
                print(f"✗ API connection failed: {response.status_code}")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Error testing API connection: {str(e)}")
            return False
    
    def fetch_ca13_candidates(self):
        """Fetch current CA-13 candidates"""
        try:
            params = {
                'api_key': self.api_key,
                'state': 'CA',
                'district': '13',
                'election_year': 2024,
                'per_page': 100
            }
            
            print("\nFetching CA-13 candidates...")
            response = requests.get(f"{self.base_url}/candidates/search", params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Save raw candidate data
                with open(self.data_dir / 'ca13_candidates_raw.json', 'w') as f:
                    json.dump(data, f, indent=2)
                
                # Print candidate summary
                print("\nFound Candidates:")
                print("-" * 50)
                for candidate in data['results']:
                    print(f"Name: {candidate.get('name')}")
                    print(f"Party: {candidate.get('party')}")
                    print(f"Candidate ID: {candidate.get('candidate_id')}")
                    print("-" * 50)
                
                return data['results']
            else:
                print(f"Error fetching candidates: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    
    def fetch_candidate_financials(self, candidate_id):
        """Fetch financial data for a specific candidate"""
        try:
            params = {
                'api_key': self.api_key,
                'candidate_id': candidate_id,
                'per_page': 100
            }
            
            response = requests.get(f"{self.base_url}/candidate/{candidate_id}/totals", params=params)
            
            if response.status_code == 200:
                return response.json()['results']
            else:
                print(f"Error fetching financials for candidate {candidate_id}: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    
    def fetch_and_save_all_data(self):
        """Fetch and save all relevant data for CA-13"""
        print("\nStarting comprehensive data collection for CA-13...")
        
        # 1. Get candidates
        candidates = self.fetch_ca13_candidates()
        if not candidates:
            return False
        
        # 2. Get financial data for each candidate
        comprehensive_data = {
            'district': 'CA-13',
            'fetch_date': datetime.now().isoformat(),
            'candidates': {}
        }
        
        print("\nFetching financial data for each candidate...")
        for candidate in candidates:
            candidate_id = candidate.get('candidate_id')
            if candidate_id:
                print(f"\nProcessing {candidate.get('name')}...")
                financials = self.fetch_candidate_financials(candidate_id)
                
                if financials:
                    comprehensive_data['candidates'][candidate.get('name')] = {
                        'candidate_info': candidate,
                        'financial_data': financials
                    }
        
        # Save comprehensive data
        output_path = self.data_dir / 'ca13_comprehensive_data.json'
        with open(output_path, 'w') as f:
            json.dump(comprehensive_data, f, indent=2)
        
        print(f"\n✓ All data saved to: {output_path}")
        return True

if __name__ == "__main__":
    API_KEY = "dO8yZTF2MG41iRjWCXmXlgUU2WZYGRtHJwjbqm6R"
    
    print("CA-13 FEC Data Fetcher")
    print("=" * 50)
    
    # Initialize fetcher
    fetcher = FECDataFetcher(API_KEY)
    
    # Test API connection
    if fetcher.test_api_connection():
        # Fetch all data
        fetcher.fetch_and_save_all_data()
    else:
        print("Please verify your API key and try again.")
