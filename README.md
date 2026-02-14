# scrapeba

Scrape and consolidate data on the German labour market from the Bundesagentur für Arbeit.

This Python package provides tools to download and process labour market data from the German Federal Employment Agency (Bundesagentur für Arbeit).

## Installation

```bash
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

## Data Preparation

Before using the package, you need to prepare the internal data files:

```bash
python prepare_data.py
```

This will:
1. Download district information from destatis.de
2. Check which districts have available data
3. Create internal data files for the package

## Usage

### Get data for a specific district

```python
from scrapeba import get_district

# Get data for a specific district, year, and month
df = get_district(id="09571", year="2021", month="10")
print(df)
```

### Get data for all available districts

```python
from scrapeba import get_data

# Get data for all districts
df = get_data(year="2021", month="10")
print(df)
```

## Output Data

The functions return a pandas DataFrame with the following columns:

- `district`: District name
- `year`: Year of the data
- `month`: Month of the data
- `id`: District ID
- `arbeitssuchend`: Number of job seekers
- `arbeitslos`: Number of unemployed
- `arbeitslos_m`: Number of unemployed (male)
- `arbeitslos_w`: Number of unemployed (female)
- `arbeitslos_zugang`: Inflow of unemployed
- `arbeitslos_abgang`: Outflow of unemployed
- `arbeitslos_quote`: Unemployment rate
- `arbeitsstellen_zugang`: Inflow of job vacancies
- `arbeitsstellen_jahreszugang`: Inflow of job vacancies since beginning of year
- `arbeitsstellen`: Number of job vacancies

## Data Source

Data is sourced from:
- Bundesagentur für Arbeit: https://statistik.arbeitsagentur.de/
- Destatis (Federal Statistical Office): https://www.destatis.de/

## License

MIT License - see LICENSE file for details

## Author

Felix Schier - felix.schier@t-online.de

## Original R Package

This is a Python conversion of the original R package available at: https://github.com/fschier/scrapeba
