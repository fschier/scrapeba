"""
Extract internal data from R package sysdata.rda file and convert to Python format.
"""

import pyreadr
import pandas as pd
import pickle
from pathlib import Path

def extract_r_data():
    """Extract data from R's sysdata.rda file"""
    
    print("Reading R data file...")
    # Read the RDA file
    result = pyreadr.read_r('R/sysdata.rda')
    
    # Extract the three datasets
    dataset = result['DATASET']
    available_districts = result['available_districts']
    kpi_names = result['kpi_names']
    
    # Convert kpi_names if it's not already a list
    if isinstance(kpi_names, pd.DataFrame):
        kpi_names = kpi_names.iloc[:, 0].tolist()
    elif hasattr(kpi_names, 'tolist'):
        kpi_names = kpi_names.tolist()
    
    return dataset, available_districts, kpi_names

def main():
    """Main function to convert R data to Python format"""
    
    # Extract data from R
    dataset, available_districts, kpi_names = extract_r_data()
    
    print(f"Extracted {len(dataset)} districts from DATASET")
    print(f"Extracted {len(available_districts)} districts from available_districts")
    print(f"Extracted {len(kpi_names)} KPI names")
    
    # Create data directory
    data_dir = Path('scrapeba/data')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as pickle files
    with open(data_dir / 'dataset.pkl', 'wb') as f:
        pickle.dump(dataset, f)
    
    with open(data_dir / 'available_districts.pkl', 'wb') as f:
        pickle.dump(available_districts, f)
    
    with open(data_dir / 'kpi_names.pkl', 'wb') as f:
        pickle.dump(kpi_names, f)
    
    print(f"\nData files saved to {data_dir}")
    print(f"- dataset.pkl: {len(dataset)} districts")
    print(f"- available_districts.pkl: {len(available_districts)} districts")
    
    # Check how many districts have available data
    if 'resp' in available_districts.columns:
        available_count = len(available_districts[available_districts['resp'] == 200])
        print(f"  ({available_count} with resp=200)")
    
    print(f"- kpi_names.pkl: {len(kpi_names)} KPI names")
    
    # Display sample data
    print("\nSample available districts (with resp=200):")
    if 'resp' in available_districts.columns:
        sample = available_districts[available_districts['resp'] == 200].head(10)
        print(sample)
    
    print("\nKPI names:")
    for i, name in enumerate(kpi_names, 1):
        print(f"{i}. {name}")

if __name__ == '__main__':
    main()
