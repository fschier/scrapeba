# scrapeba

> 🔄 **Python version of the R package for scraping German labour market data**

Scrape and consolidate data on the German labour market from the Bundesagentur für Arbeit.

This Python package provides tools to download and process labour market data from the German Federal Employment Agency (Bundesagentur für Arbeit). It is a complete conversion of the [original R package](https://github.com/fschier/scrapeba) with identical functionality.

## Features

✅ Download Excel files from Bundesagentur für Arbeit  
✅ Extract specific labour market indicators  
✅ Transform data into formatted pandas DataFrames  
✅ Support for single district or all districts (400+)  
✅ Progress tracking with tqdm  
✅ Automatic rate limiting (1s between requests)  
✅ Comprehensive error handling  

## Installation

```bash
# Clone the repository
git clone https://github.com/fschier/scrapeba.git
cd scrapeba

# Install the package
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from scrapeba import get_district, get_data

# Get data for a specific district
df = get_district(id="09571", year="2021", month="10")
print(df)

# Get data for all available districts (takes ~7-8 minutes)
df_all = get_data(year="2021", month="10")
df_all.to_csv("labour_market_data.csv", index=False)
```

## Available Data

The package retrieves the following labour market indicators (KPIs):

- **arbeitssuchend**: Number of job seekers
- **arbeitslos**: Number of unemployed persons
- **arbeitslos_m**: Number of unemployed men
- **arbeitslos_w**: Number of unemployed women
- **arbeitslos_zugang**: Inflow of unemployed
- **arbeitslos_abgang**: Outflow of unemployed
- **arbeitslos_quote**: Unemployment rate (%)
- **arbeitsstellen_zugang**: Inflow of job vacancies
- **arbeitsstellen_jahreszugang**: Job vacancies inflow since beginning of year
- **arbeitsstellen**: Number of job vacancies

Data is available for **400+ German districts** (Landkreise and kreisfreie Städte).

## Documentation

- 📖 **[Installation Guide](INSTALL.md)** - Detailed installation and setup instructions
- 🔄 **[R to Python Mapping](R_TO_PYTHON_MAPPING.md)** - Technical conversion details
- 📊 **[Comparison Guide](COMPARISON.md)** - Side-by-side R vs Python comparison
- 💡 **[Examples](examples.py)** - Usage examples and sample code

## Example Usage

### Analyze Major Cities

```python
from scrapeba import get_district
import pandas as pd

# Fetch data for major German cities
cities = {
    "02000": "Hamburg",
    "11000": "Berlin", 
    "05315": "Köln",
    "09162": "München"
}

data_list = []
for district_id in cities.keys():
    df = get_district(id=district_id, year="2021", month="10")
    data_list.append(df)

# Combine and analyze
combined = pd.concat(data_list, ignore_index=True)
print(combined[['district', 'arbeitslos_quote']].sort_values('arbeitslos_quote'))
```

### Find District IDs

```python
import pickle

# Load available districts
with open('scrapeba/data/available_districts.pkl', 'rb') as f:
    districts = pickle.load(f)

# Search for a specific district
search = "München"
matches = districts[districts['landkreis'].str.contains(search, case=False)]
print(matches[['id', 'landkreis']])
```

## Data Sources

Data is sourced from:
- **Bundesagentur für Arbeit** (Federal Employment Agency): https://statistik.arbeitsagentur.de/
- **Destatis** (Federal Statistical Office): https://www.destatis.de/

## Requirements

- Python 3.8 or higher
- pandas >= 1.3.0
- openpyxl >= 3.0.0
- requests >= 2.26.0
- tqdm >= 4.62.0

## Project Structure

```
scrapeba/
├── scrapeba/              # Main package
│   ├── __init__.py       # Package initialization
│   ├── get_district.py   # Single district data fetching
│   ├── get_data.py       # Bulk data fetching
│   └── data/             # Internal data files
│       ├── available_districts.pkl
│       ├── dataset.pkl
│       └── kpi_names.pkl
├── setup.py              # Package configuration
├── requirements.txt      # Dependencies
├── examples.py           # Usage examples
└── extract_r_data.py     # R data conversion script
```

## Notes

- Each request includes a 1-second delay to avoid overwhelming the server
- Fetching all 400+ districts takes approximately 7-8 minutes
- Data availability depends on Bundesagentur für Arbeit servers
- Some districts may not have data for all time periods
- Requires internet access to statistik.arbeitsagentur.de

## Migrating from R

If you're familiar with the R version of this package:

```r
# R version
library(scrapeba)
df <- get_district(id = "09571", year = "2021", month = "10")
```

```python
# Python version
from scrapeba import get_district
df = get_district(id="09571", year="2021", month="10")
```

See [COMPARISON.md](COMPARISON.md) for a detailed comparison.

## License

MIT License - see [LICENSE](LICENSE) file for details

## Author

**Felix Schier**  
Email: felix.schier@t-online.de  
GitHub: [@fschier](https://github.com/fschier)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Original R Package

This is a Python conversion of the original R package:  
https://github.com/fschier/scrapeba

The Python version maintains identical functionality and API design as the R version.
