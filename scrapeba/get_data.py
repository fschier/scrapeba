"""
Get data for all districts.
"""

import pandas as pd
import pickle
from pathlib import Path
from tqdm import tqdm
import time
from .get_district import get_district

def _load_available_districts():
    """Load available districts from internal data"""
    data_file = Path(__file__).parent / 'data' / 'available_districts.pkl'
    with open(data_file, 'rb') as f:
        return pickle.load(f)

def get_data(year="2021", month="10"):
    """
    Get data for all available districts.
    
    Downloads labour market data for all districts that have available data
    on the Bundesagentur für Arbeit website.
    
    Parameters
    ----------
    year : str or int, optional
        Year (default: "2021")
    month : str or int, optional
        Month (default: "10")
    
    Returns
    -------
    pandas.DataFrame
        A consolidated dataframe containing labour market indicators for all
        available districts for the specified time period.
    
    Examples
    --------
    >>> get_data(year="2021", month="10")
    """
    # Convert to strings if needed
    year = str(year)
    month = str(month)
    
    # Load available districts (those with resp == 200)
    available_districts = _load_available_districts()
    
    # Handle resp column - it might be string or int
    if available_districts['resp'].dtype == 'object':
        available_ids = available_districts[available_districts['resp'] == '200']['id'].tolist()
    else:
        available_ids = available_districts[available_districts['resp'] == 200]['id'].tolist()
    
    print(f"Fetching data for {len(available_ids)} districts...")
    
    # Initialize list to collect dataframes
    data_list = []
    
    # Progress bar
    for district_id in tqdm(available_ids, desc="Downloading districts"):
        try:
            tmp = get_district(id=district_id, year=year, month=month)
            data_list.append(tmp)
            
            # Sleep to avoid overwhelming the server
            time.sleep(1)
        except Exception as e:
            print(f"\nWarning: Failed to fetch data for district {district_id}: {str(e)}")
            continue
    
    # Concatenate all dataframes
    if data_list:
        data_output = pd.concat(data_list, ignore_index=True)
        print(f"\nSuccessfully fetched data for {len(data_list)} districts")
        return data_output
    else:
        raise Exception("No data was successfully fetched")
