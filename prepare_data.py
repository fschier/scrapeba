"""
Prepare internal data for scrapeba package.

This script:
1. Downloads district information from destatis.de
2. Checks which districts have available data on arbeitsagentur.de
3. Creates internal data files for the package
"""

import pandas as pd
import requests
from pathlib import Path
import pickle

def download_district_data():
    """Download and process district data from destatis.de"""
    url = "https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GVAuszugQ/AuszugGV3QAktuell.xlsx?__blob=publicationFile"
    
    print("Downloading district data from destatis.de...")
    response = requests.get(url)
    
    # Save temporarily
    temp_file = Path("temp_districts.xlsx")
    with open(temp_file, 'wb') as f:
        f.write(response.content)
    
    # Read Excel file (sheet 2, skip first 6 rows)
    df = pd.read_excel(temp_file, sheet_name=1, skiprows=6, header=None)
    
    # Select columns 3-5 and 8 (using 0-based indexing: 2-4 and 7)
    df = df.iloc[:, [2, 3, 4, 7]]
    
    # Combine first three columns to create district ID
    df['id'] = df.iloc[:, 0].astype(str) + df.iloc[:, 1].astype(str) + df.iloc[:, 2].astype(str)
    
    # Rename the 4th column to 'landkreis'
    df = df.rename(columns={df.columns[3]: 'landkreis'})
    
    # Select only id and landkreis columns
    df = df[['id', 'landkreis']]
    
    # Filter out rows with 'nan' or 'NA' in id
    df = df[~df['id'].str.contains('nan', case=False, na=True)]
    
    # Remove duplicates based on id
    df = df.drop_duplicates(subset=['id'], keep='first')
    
    # Clean up temp file
    temp_file.unlink()
    
    print(f"Found {len(df)} districts")
    return df

def check_available_districts(dataset):
    """Check which districts have available data on arbeitsagentur.de"""
    print("Checking which districts have available data...")
    
    def get_response_code(district_id):
        """Check if URL for a district returns 200 status code"""
        url = f"https://statistik.arbeitsagentur.de/Statistikdaten/Detail/202108/ama/amr-amr/amr-{district_id}-0-202108-xlsx.xlsx?__blob=publicationFile&v=1"
        try:
            response = requests.head(url, timeout=10)
            return response.status_code
        except:
            return 0
    
    # Check response codes for all districts
    dataset['resp'] = dataset['id'].apply(get_response_code)
    
    available = dataset[dataset['resp'] == 200]
    print(f"Found {len(available)} districts with available data")
    
    return dataset

def create_kpi_names():
    """Create KPI names mapping"""
    kpi_names = [
        "arbeitssuchend",                # Bestand an Arbeitssuchenden
        "arbeitslos",                    # Bestand an Arbeitslosen
        "arbeitslos_m",                  # Arbeitslosen M
        "arbeitslos_w",                  # Arbeitslosen W
        "arbeitslos_zugang",             # Zugang an Arbeitslosen
        "arbeitslos_abgang",             # Abgang an Arbeitslosen
        "arbeitslos_quote",              # ALQ
        "arbeitsstellen_zugang",         # Zugang Gemeldete Arbeitstellen
        "arbeitsstellen_jahreszugang",   # Zugang seit Jahresbeginn
        "arbeitsstellen"                 # Bestand gemeldete Arbeitstellen
    ]
    return kpi_names

def main():
    """Main function to prepare all internal data"""
    # Create data directory if it doesn't exist
    data_dir = Path(__file__).parent / 'scrapeba' / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Download and process district data
    dataset = download_district_data()
    
    # Check available districts
    available_districts = check_available_districts(dataset)
    
    # Create KPI names
    kpi_names = create_kpi_names()
    
    # Save as pickle files
    with open(data_dir / 'dataset.pkl', 'wb') as f:
        pickle.dump(dataset, f)
    
    with open(data_dir / 'available_districts.pkl', 'wb') as f:
        pickle.dump(available_districts, f)
    
    with open(data_dir / 'kpi_names.pkl', 'wb') as f:
        pickle.dump(kpi_names, f)
    
    print(f"\nData files saved to {data_dir}")
    print(f"- dataset.pkl: {len(dataset)} districts")
    print(f"- available_districts.pkl: {len(available_districts[available_districts['resp'] == 200])} available districts")
    print(f"- kpi_names.pkl: {len(kpi_names)} KPI names")

if __name__ == '__main__':
    main()
