# Installation and Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

### Option 1: Install from source (recommended for development)

```bash
# Clone the repository
git clone https://github.com/fschier/scrapeba.git
cd scrapeba

# Install in development mode
pip install -e .
```

### Option 2: Install dependencies only

```bash
# If you don't want to install the package, just install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Verify Installation

```python
import scrapeba
print(f"scrapeba version: {scrapeba.__version__}")
```

### 2. Basic Usage

#### Fetch data for a single district

```python
from scrapeba import get_district

# Get data for Würzburg (district 09571) in October 2021
df = get_district(id="09571", year="2021", month="10")
print(df)
```

#### Fetch data for all available districts

```python
from scrapeba import get_data

# Get data for all districts in October 2021
# Warning: This takes time (400+ districts with 1 second delay each)
df_all = get_data(year="2021", month="10")
print(df_all.head())

# Save to CSV
df_all.to_csv("labour_market_data.csv", index=False)
```

### 3. Example: Analyze unemployment rates

```python
from scrapeba import get_district
import pandas as pd

# Fetch data for several major cities
cities = {
    "02000": "Hamburg",
    "11000": "Berlin",
    "05315": "Köln",
    "09162": "München"
}

data_list = []
for district_id, city_name in cities.items():
    df = get_district(id=district_id, year="2021", month="10")
    data_list.append(df)

# Combine and analyze
combined = pd.concat(data_list, ignore_index=True)
print("\nUnemployment rates in major cities:")
print(combined[['district', 'arbeitslos_quote']].sort_values('arbeitslos_quote', ascending=False))
```

## Output Data Structure

The functions return a pandas DataFrame with these columns:

| Column | Description |
|--------|-------------|
| `district` | District name (in German) |
| `year` | Year of data |
| `month` | Month of data |
| `id` | District ID |
| `arbeitssuchend` | Number of job seekers |
| `arbeitslos` | Number of unemployed persons |
| `arbeitslos_m` | Number of unemployed men |
| `arbeitslos_w` | Number of unemployed women |
| `arbeitslos_zugang` | Inflow of unemployed |
| `arbeitslos_abgang` | Outflow of unemployed |
| `arbeitslos_quote` | Unemployment rate (%) |
| `arbeitsstellen_zugang` | Inflow of job vacancies |
| `arbeitsstellen_jahreszugang` | Job vacancies inflow since year start |
| `arbeitsstellen` | Number of job vacancies |

## Finding District IDs

To find available district IDs:

```python
import pickle
from pathlib import Path

# Load available districts
with open('scrapeba/data/available_districts.pkl', 'rb') as f:
    districts = pickle.load(f)

# Show all districts with available data
available = districts[districts['resp'] == '200']
print(available[['id', 'landkreis']])

# Search for a specific district
search_term = "München"
matches = available[available['landkreis'].str.contains(search_term, case=False)]
print(matches[['id', 'landkreis']])
```

## Troubleshooting

### Import Error

If you get an import error, make sure you installed the dependencies:
```bash
pip install -r requirements.txt
```

### Network Error

The package requires internet access to download data from:
- https://statistik.arbeitsagentur.de/

If you're behind a firewall or proxy, configure your Python environment accordingly.

### Missing Data Files

If you get an error about missing `.pkl` files, you need to extract the data first:

```bash
# Extract data from R package (requires pyreadr)
pip install pyreadr
python extract_r_data.py
```

## Advanced Usage

For more examples, see:
- `examples.py` - Comprehensive usage examples
- `test_package.py` - Package tests
- `R_TO_PYTHON_MAPPING.md` - R to Python conversion details

## Notes

- Each request to the server has a 1-second delay to avoid overwhelming the server
- Fetching data for all 400+ districts takes approximately 7-8 minutes
- Data availability depends on the Bundesagentur für Arbeit servers
- Some districts may not have data for all time periods

## Support

For issues and questions:
- GitHub Issues: https://github.com/fschier/scrapeba/issues
- Email: felix.schier@t-online.de
