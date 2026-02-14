# R to Python Conversion Guide

This document shows the mapping between the original R package and the Python package.

## Package Structure

### R Package
```
scrapeba/
├── DESCRIPTION          # Package metadata
├── NAMESPACE            # Exported functions
├── R/
│   ├── get_data.R      # Main function for all districts
│   ├── get_district.R  # Function for single district
│   ├── utils-pipe.R    # Pipe operator (magrittr)
│   └── sysdata.rda     # Internal data
├── data-raw/
│   └── DATASET.R       # Data preparation script
└── man/                # Documentation
```

### Python Package
```
scrapeba/
├── setup.py                      # Package configuration (replaces DESCRIPTION)
├── requirements.txt              # Dependencies
├── scrapeba/
│   ├── __init__.py              # Package initialization (replaces NAMESPACE)
│   ├── get_data.py              # Main function for all districts
│   ├── get_district.py          # Function for single district
│   └── data/
│       ├── available_districts.pkl  # Internal data
│       ├── dataset.pkl              # Internal data
│       └── kpi_names.pkl            # Internal data
├── extract_r_data.py            # Extract R data (replaces data-raw/DATASET.R)
├── prepare_data.py              # Alternative data preparation
├── test_package.py              # Test suite
└── examples.py                  # Usage examples
```

## Dependencies Mapping

### R Dependencies
```r
Imports: 
    dplyr,      # Data manipulation
    magrittr,   # Pipe operator
    rio,        # Import/export data
    tidyr       # Data tidying
```

### Python Dependencies
```python
install_requires=[
    "pandas>=1.3.0",      # Data manipulation (replaces dplyr, tidyr)
    "openpyxl>=3.0.0",    # Excel file reading (replaces rio)
    "requests>=2.26.0",   # HTTP requests
    "tqdm>=4.62.0",       # Progress bar (replaces txtProgressBar)
]
```

## Function Mapping

### 1. get_district()

#### R Code
```r
get_district <- function(id = "09571", year = "2021", month = "10"){
  file <- paste0("https://statistik.arbeitsagentur.de/...", id, "...")
  
  data <- rio::import(file = file, format = "xlsx", which = 5, col_names = FALSE) %>%
    dplyr::select(1,4) %>%
    dplyr::rename(kpi = 1, value = 2)
  
  district <- data[4,1]
  
  data <- data %>%
    dplyr::slice(13, 15, 16, ...) %>%
    dplyr::mutate(district = district, year = year, month = month, id = id) %>%
    cbind(kpi_names = scrapeba:::kpi_names) %>%
    dplyr::select(-kpi) %>%
    tidyr::pivot_wider(names_from = kpi_names, values_from = value)
  
  return(data)
}
```

#### Python Code
```python
def get_district(id="09571", year="2021", month="10"):
    file_url = f"https://statistik.arbeitsagentur.de/...{id}..."
    
    response = requests.get(file_url, timeout=30)
    df = pd.read_excel(BytesIO(response.content), sheet_name=4, header=None)
    
    df = df.iloc[:, [0, 3]]
    df.columns = ['kpi', 'value']
    
    district_name = df.iloc[3, 0]
    
    df = df.iloc[row_indices].copy()
    df['district'] = district_name
    df['year'] = year
    df['month'] = month
    df['id'] = id
    
    kpi_names = _load_kpi_names()
    df['kpi_names'] = kpi_names
    df = df.drop('kpi', axis=1)
    
    result = df.pivot_table(
        index=['district', 'year', 'month', 'id'],
        columns='kpi_names',
        values='value',
        aggfunc='first'
    ).reset_index()
    
    return result
```

### 2. get_data()

#### R Code
```r
get_data <- function(year = "2021", month = "10"){
  id <- scrapeba:::available_districts %>%
    dplyr::filter(resp == 200) %>%
    dplyr::pull(id)
  
  pb = utils::txtProgressBar(min = 0, max = 400, initial = 0)
  
  for(i in id){
    tmp <- get_district(id = i, year = year, month = month)
    
    if (!exists("data_output")) {
      data_output <- tmp
    } else {
      data_output <- rbind(data_output, tmp)
    }
    
    stepi = stepi + 1
    utils::setTxtProgressBar(pb, stepi)
    Sys.sleep(1)
  }
  
  return(data_output)
}
```

#### Python Code
```python
def get_data(year="2021", month="10"):
    available_districts = _load_available_districts()
    available_ids = available_districts[available_districts['resp'] == '200']['id'].tolist()
    
    data_list = []
    
    for district_id in tqdm(available_ids, desc="Downloading districts"):
        try:
            tmp = get_district(id=district_id, year=year, month=month)
            data_list.append(tmp)
            time.sleep(1)
        except Exception as e:
            print(f"\nWarning: Failed to fetch data for district {district_id}: {str(e)}")
            continue
    
    if data_list:
        data_output = pd.concat(data_list, ignore_index=True)
        return data_output
    else:
        raise Exception("No data was successfully fetched")
```

## Key Differences

### 1. Pipe Operator
- **R**: Uses `%>%` from magrittr package
- **Python**: Uses method chaining with pandas (e.g., `df.filter().groupby()`)

### 2. Data Selection
- **R**: Uses dplyr verbs: `select()`, `filter()`, `mutate()`, `slice()`
- **Python**: Uses pandas: `.iloc[]`, `.loc[]`, bracket notation

### 3. Data Reshaping
- **R**: Uses `tidyr::pivot_wider()`
- **Python**: Uses `pd.pivot_table()` or `df.pivot()`

### 4. Progress Bar
- **R**: Uses `utils::txtProgressBar()`
- **Python**: Uses `tqdm` package

### 5. Internal Data Storage
- **R**: Uses `.rda` files loaded with `load()`
- **Python**: Uses `.pkl` files loaded with `pickle`

### 6. Row Indexing
- **R**: 1-indexed (row 13 is the 13th row)
- **Python**: 0-indexed (row 12 is the 13th row)

## Usage Examples

### R Usage
```r
library(scrapeba)

# Get single district
df <- get_district(id = "09571", year = "2021", month = "10")

# Get all districts
df_all <- get_data(year = "2021", month = "10")
```

### Python Usage
```python
from scrapeba import get_district, get_data

# Get single district
df = get_district(id="09571", year="2021", month="10")

# Get all districts
df_all = get_data(year="2021", month="10")
```

## Installation

### R Package
```r
# Install from GitHub
devtools::install_github("fschier/scrapeba")
```

### Python Package
```bash
# Install from local directory
pip install -e .

# Or install dependencies
pip install -r requirements.txt
```

## Data Preparation

### R Package
```r
# Run the data-raw/DATASET.R script
source("data-raw/DATASET.R")
```

### Python Package
```bash
# Extract data from R package
python extract_r_data.py

# Or prepare fresh data (requires internet)
python prepare_data.py
```

## Functional Equivalence

Both packages provide the same functionality:
1. ✅ Download Excel files from Bundesagentur für Arbeit
2. ✅ Extract specific labour market indicators
3. ✅ Transform data into formatted dataframes
4. ✅ Support for single district or all districts
5. ✅ Progress tracking during bulk downloads
6. ✅ Internal data storage for district information
7. ✅ Proper error handling

The Python package maintains the same API design and data structure as the R package, making it easy for users familiar with the R version to transition to Python.
