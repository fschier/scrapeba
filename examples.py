"""
Example usage of the scrapeba package.

This script demonstrates how to use the scrapeba package to fetch
German labour market data from the Bundesagentur für Arbeit.
"""

# Add package to path for testing
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from scrapeba import get_district, get_data
import pandas as pd

def example_single_district():
    """Example: Fetch data for a single district"""
    print("=" * 60)
    print("Example 1: Fetch data for a single district")
    print("=" * 60)
    
    # Fetch data for district 09571 (Würzburg) for October 2021
    print("\nFetching data for district 09571 (October 2021)...")
    try:
        df = get_district(id="09571", year="2021", month="10")
        
        print(f"\nSuccess! Retrieved data with {len(df)} row(s)")
        print("\nColumns:")
        for col in df.columns:
            print(f"  - {col}")
        
        print("\nData:")
        print(df.to_string())
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This requires internet access to statistik.arbeitsagentur.de")

def example_multiple_districts():
    """Example: Fetch data for all available districts"""
    print("\n" + "=" * 60)
    print("Example 2: Fetch data for all available districts")
    print("=" * 60)
    
    # Note: This will take a long time (400+ districts with 1 second delay)
    # In practice, you might want to filter or limit the districts
    
    print("\nFetching data for all available districts (October 2021)...")
    print("⚠️  This will take a while (400+ districts with 1s delay each)")
    
    try:
        df = get_data(year="2021", month="10")
        
        print(f"\nSuccess! Retrieved data for {len(df)} districts")
        print("\nSummary statistics:")
        print(df.describe())
        
        print("\nSample data (first 5 districts):")
        print(df.head())
        
        # Save to CSV
        output_file = "labour_market_data_2021_10.csv"
        df.to_csv(output_file, index=False)
        print(f"\nData saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This requires internet access to statistik.arbeitsagentur.de")

def example_custom_analysis():
    """Example: Fetch data and perform custom analysis"""
    print("\n" + "=" * 60)
    print("Example 3: Custom analysis of labour market data")
    print("=" * 60)
    
    try:
        # Fetch data for a few specific districts
        districts = ["01001", "02000", "03101"]  # Flensburg, Hamburg, Braunschweig
        
        print(f"\nFetching data for {len(districts)} districts...")
        
        data_list = []
        for district_id in districts:
            try:
                df = get_district(id=district_id, year="2021", month="10")
                data_list.append(df)
            except Exception as e:
                print(f"Failed to fetch {district_id}: {e}")
        
        if data_list:
            # Combine data
            combined_df = pd.concat(data_list, ignore_index=True)
            
            print(f"\nRetrieved data for {len(combined_df)} district(s)")
            
            # Analysis: Unemployment rates
            print("\nUnemployment rates by district:")
            print(combined_df[['district', 'arbeitslos_quote']].to_string(index=False))
            
            # Analysis: Gender distribution
            print("\nGender distribution of unemployed:")
            combined_df['male_percentage'] = (
                combined_df['arbeitslos_m'] / combined_df['arbeitslos'] * 100
            ).round(1)
            print(combined_df[['district', 'arbeitslos_m', 'arbeitslos_w', 'male_percentage']].to_string(index=False))
            
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This requires internet access to statistik.arbeitsagentur.de")

def show_available_data():
    """Show information about available data"""
    print("\n" + "=" * 60)
    print("Available Data Information")
    print("=" * 60)
    
    import pickle
    from pathlib import Path
    
    # Load district information
    data_file = Path(__file__).parent / 'scrapeba' / 'data' / 'available_districts.pkl'
    with open(data_file, 'rb') as f:
        districts = pickle.load(f)
    
    # Show statistics
    available = districts[districts['resp'] == '200']
    unavailable = districts[districts['resp'] != '200']
    
    print(f"\nTotal districts in database: {len(districts)}")
    print(f"Districts with available data: {len(available)}")
    print(f"Districts without data: {len(unavailable)}")
    
    print("\nSample of available districts:")
    print(available[['id', 'landkreis']].head(10).to_string(index=False))
    
    # Load KPI information
    kpi_file = Path(__file__).parent / 'scrapeba' / 'data' / 'kpi_names.pkl'
    with open(kpi_file, 'rb') as f:
        kpi_names = pickle.load(f)
    
    print("\nAvailable KPI (Key Performance Indicators):")
    for i, kpi in enumerate(kpi_names, 1):
        print(f"{i:2d}. {kpi}")

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("SCRAPEBA PACKAGE EXAMPLES")
    print("=" * 60)
    
    # Show available data
    show_available_data()
    
    # Example 1: Single district
    # Uncomment to run (requires internet access):
    # example_single_district()
    
    # Example 2: All districts
    # Uncomment to run (requires internet access and takes a long time):
    # example_multiple_districts()
    
    # Example 3: Custom analysis
    # Uncomment to run (requires internet access):
    # example_custom_analysis()
    
    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)
    print("\nNote: Uncomment example function calls to test with live data.")
    print("Requires internet access to statistik.arbeitsagentur.de")
