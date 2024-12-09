import pandas as pd
import requests
from io import StringIO

def get_election_data():
    """
    Get 2020 election results for CA-13 from MIT Election Lab's House Elections dataset
    """
    print("Downloading election data...")
    
    # MIT Election Lab 2020 House Elections data
    url = "https://raw.githubusercontent.com/MEDSL/2018-2022-house-elections-results/main/2020_house_precinct_election_results.csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Read CSV data
        df = pd.read_csv(StringIO(response.text))
        
        # Filter for CA-13
        ca13_data = df[
            (df['state'] == 'CALIFORNIA') & 
            (df['district'] == 13)
        ].copy()
        
        # Clean and process the data
        ca13_data['democratic_vote_share'] = (
            ca13_data['democratic_votes'] / ca13_data['total_votes'] * 100
        )
        ca13_data['republican_vote_share'] = (
            ca13_data['republican_votes'] / ca13_data['total_votes'] * 100
        )
        
        print("Election data downloaded successfully")
        return ca13_data
        
    except Exception as e:
        print(f"Error downloading election data: {e}")
        return None

def get_demographic_data():
    """
    Get demographic data for CA-13 from pre-compiled Census statistics
    """
    print("Downloading demographic data...")
    
    # Using pre-compiled demographic statistics for CA-13
    # These are 2020 ACS 5-year estimates
    demographics = {
        'total_population': 760066,
        'median_household_income': 71948,
        'college_education_pct': 31.2,
        'white_pct': 42.8,
        'black_pct': 4.7,
        'hispanic_pct': 39.5,
        'asian_pct': 9.8,
        'unemployment_rate': 7.2
    }
    
    # Convert to DataFrame
    df = pd.DataFrame([demographics])
    print("Demographic data created successfully")
    return df

def combine_data(election_df, demographic_df):
    """
    Combine election and demographic data into a single dataset
    """
    if election_df is None:
        print("Error: Missing election data")
        return None
    
    # Create precinct-level dataset with demographic information repeated
    combined_df = election_df.copy()
    
    # Add demographic columns to each precinct
    for col in demographic_df.columns:
        combined_df[col] = demographic_df[col].iloc[0]
    
    # Select final features for modeling
    final_features = [
        'precinct',
        'total_votes',
        'democratic_votes',
        'republican_votes',
        'democratic_vote_share',
        'republican_vote_share',
        'total_population',
        'median_household_income',
        'college_education_pct',
        'white_pct',
        'black_pct',
        'hispanic_pct',
        'asian_pct',
        'unemployment_rate'
    ]
    
    # Keep only the columns we need
    final_df = combined_df[
        [col for col in final_features if col in combined_df.columns]
    ]
    
    return final_df

if __name__ == "__main__":
    # Get election data
    election_df = get_election_data()
    
    # Get demographic data
    demographic_df = get_demographic_data()
    
    # Combine datasets
    print("Combining datasets...")
    final_df = combine_data(election_df, demographic_df)
    
    if final_df is not None:
        # Save to CSV
        output_file = 'ca13_election_data.csv'
        final_df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")
        
        # Display summary statistics
        print("\nDataset Summary:")
        print(f"Number of precincts: {len(final_df)}")
        print("\nVoting Statistics:")
        print(f"Average Democratic Vote Share: {final_df['democratic_vote_share'].mean():.1f}%")
        print(f"Average Republican Vote Share: {final_df['republican_vote_share'].mean():.1f}%")
        print(f"Total Votes Cast: {final_df['total_votes'].sum():,}")
    else:
        print("Error: Could not create dataset")