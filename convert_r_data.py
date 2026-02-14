"""
Extract internal data from R package and convert to Python format.

This script extracts the sysdata.rda file from the R package and converts
it to Python pickle files.
"""

import subprocess
import pandas as pd
import pickle
from pathlib import Path
import tempfile
import os

def extract_r_data():
    """Extract data from R's sysdata.rda file"""
    
    # Create R script to extract and save data
    r_script = """
    load('R/sysdata.rda')
    
    # Save as CSV files
    write.csv(DATASET, 'temp_dataset.csv', row.names = FALSE)
    write.csv(available_districts, 'temp_available_districts.csv', row.names = FALSE)
    
    # Save kpi_names as text file
    writeLines(kpi_names, 'temp_kpi_names.txt')
    """
    
    # Write R script to temp file
    with open('temp_extract.R', 'w') as f:
        f.write(r_script)
    
    # Run R script
    print("Extracting data from R package...")
    result = subprocess.run(['Rscript', 'temp_extract.R'], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print("STDERR:", result.stderr)
        raise Exception("Failed to extract R data")
    
    # Read the CSV files
    dataset = pd.read_csv('temp_dataset.csv')
    available_districts = pd.read_csv('temp_available_districts.csv')
    
    # Read kpi_names
    with open('temp_kpi_names.txt', 'r') as f:
        kpi_names = [line.strip() for line in f]
    
    # Clean up temp files
    for f in ['temp_extract.R', 'temp_dataset.csv', 'temp_available_districts.csv', 'temp_kpi_names.txt']:
        if os.path.exists(f):
            os.remove(f)
    
    return dataset, available_districts, kpi_names

def main():
    """Main function to convert R data to Python format"""
    
    # Extract data from R
    dataset, available_districts, kpi_names = extract_r_data()
    
    print(f"Extracted {len(dataset)} districts")
    print(f"Extracted {len(available_districts)} available districts")
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
    print(f"  ({len(available_districts[available_districts['resp'] == 200])} with available data)")
    print(f"- kpi_names.pkl: {len(kpi_names)} KPI names")
    
    # Display sample data
    print("\nSample available districts:")
    print(available_districts[available_districts['resp'] == 200].head())
    print("\nKPI names:")
    for i, name in enumerate(kpi_names, 1):
        print(f"{i}. {name}")

if __name__ == '__main__':
    main()
