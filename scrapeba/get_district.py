"""
Get labour data for a specific district and timestamp.
"""

import pandas as pd
import requests
from io import BytesIO
import pickle
from pathlib import Path
import warnings

def _load_kpi_names():
    """Load KPI names from internal data"""
    data_file = Path(__file__).parent / 'data' / 'kpi_names.pkl'
    with open(data_file, 'rb') as f:
        return pickle.load(f)

def get_district(id="09571", year="2021", month="10"):
    """
    Get labour data for district and timestamp.
    
    Downloads an Excel file from the Bundesagentur für Arbeit, extracts specific
    labour market indicators, and returns them as a formatted dataframe.
    
    Parameters
    ----------
    id : str or int, optional
        District ID (default: "09571")
    year : str or int, optional
        Year (default: "2021")
    month : str or int, optional
        Month (default: "10")
    
    Returns
    -------
    pandas.DataFrame
        A dataframe containing labour market indicators for the specified district
        and time period.
    
    Examples
    --------
    >>> get_district(id="09571", year="2021", month="10")
    """
    # Convert to strings if needed
    id = str(id)
    year = str(year)
    month = str(month)
    
    # Construct file URL
    file_url = (
        f"https://statistik.arbeitsagentur.de/Statistikdaten/Detail/"
        f"{year}{month}/ama/amr-amr/amr-{id}-0-{year}{month}-xlsx.xlsx"
        f"?__blob=publicationFile&v=1"
    )
    
    # Download and read Excel file
    try:
        response = requests.get(file_url, timeout=30)
        response.raise_for_status()
        
        # Read Excel file from memory, sheet 5 (0-indexed: sheet 4)
        # Suppress warnings about data validation
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = pd.read_excel(
                BytesIO(response.content),
                sheet_name=4,  # 5th sheet (0-indexed)
                header=None
            )
    except Exception as e:
        raise Exception(f"Failed to download or read data for district {id}: {str(e)}")
    
    # Select columns 1 and 4 (0-indexed: 0 and 3)
    df = df.iloc[:, [0, 3]]
    df.columns = ['kpi', 'value']
    
    # Extract district name from row 4 (0-indexed: row 3)
    district_name = df.iloc[3, 0]
    
    # Extract specific rows (0-indexed)
    row_indices = [
        12,  # Bestand an Arbeitssuchenden (row 13)
        14,  # Bestand an Arbeitslosen (row 15)
        15,  # Arbeitslosen M (row 16)
        16,  # Arbeitslosen W (row 17)
        27,  # Zugang an Arbeitslosen (row 28)
        34,  # Abgang an Arbeitslosen (row 35)
        41,  # ALQ (row 42)
        61,  # Zugang Gemeldete Arbeitstellen (row 62)
        62,  # Zugang seit Jahresbeginn (row 63)
        63,  # Bestand gemeldete Arbeitstellen (row 64)
    ]
    
    df = df.iloc[row_indices].copy()
    
    # Add metadata columns
    df['district'] = district_name
    df['year'] = year
    df['month'] = month
    df['id'] = id
    
    # Load KPI names
    kpi_names = _load_kpi_names()
    df['kpi_names'] = kpi_names
    
    # Drop the original kpi column
    df = df.drop('kpi', axis=1)
    
    # Pivot to wide format
    result = df.pivot_table(
        index=['district', 'year', 'month', 'id'],
        columns='kpi_names',
        values='value',
        aggfunc='first'
    ).reset_index()
    
    return result
