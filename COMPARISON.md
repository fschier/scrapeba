# Side-by-Side Comparison: R vs Python Implementation

## Installation

| R | Python |
|---|--------|
| `devtools::install_github("fschier/scrapeba")` | `pip install -e .` |
| `library(scrapeba)` | `from scrapeba import get_district, get_data` |

## Basic Usage

### Get Single District Data

**R:**
```r
library(scrapeba)
df <- get_district(id = "09571", year = "2021", month = "10")
head(df)
```

**Python:**
```python
from scrapeba import get_district
df = get_district(id="09571", year="2021", month="10")
print(df.head())
```

### Get All Districts Data

**R:**
```r
library(scrapeba)
df_all <- get_data(year = "2021", month = "10")
write.csv(df_all, "output.csv", row.names = FALSE)
```

**Python:**
```python
from scrapeba import get_data
df_all = get_data(year="2021", month="10")
df_all.to_csv("output.csv", index=False)
```

## Key Technical Differences

| Aspect | R Implementation | Python Implementation |
|--------|------------------|----------------------|
| **Data Manipulation** | dplyr, tidyr | pandas |
| **HTTP Requests** | Built into rio::import | requests library |
| **Excel Reading** | rio package | openpyxl + pandas |
| **Progress Bar** | utils::txtProgressBar | tqdm |
| **Data Storage** | .rda files | .pkl files |
| **Pipe Operator** | `%>%` (magrittr) | Method chaining `.` |
| **Indexing** | 1-based | 0-based |
| **String Formatting** | paste0() | f-strings |

## Implementation Details

### Row Selection

**R (1-indexed):**
```r
data %>% dplyr::slice(
  13,  # Bestand an Arbeitssuchenden
  15,  # Bestand an Arbeitslosen
  16,  # Arbeitslosen M
  ...
)
```

**Python (0-indexed):**
```python
row_indices = [
    12,  # Bestand an Arbeitssuchenden (row 13)
    14,  # Bestand an Arbeitslosen (row 15)
    15,  # Arbeitslosen M (row 16)
    ...
]
df = df.iloc[row_indices]
```

### Data Reshaping

**R:**
```r
data %>%
  cbind(kpi_names = scrapeba:::kpi_names) %>%
  dplyr::select(-kpi) %>%
  tidyr::pivot_wider(names_from = kpi_names, values_from = value)
```

**Python:**
```python
df['kpi_names'] = kpi_names
df = df.drop('kpi', axis=1)
result = df.pivot_table(
    index=['district', 'year', 'month', 'id'],
    columns='kpi_names',
    values='value',
    aggfunc='first'
).reset_index()
```

### Column Selection

**R:**
```r
data %>% dplyr::select(1, 4)
```

**Python:**
```python
df = df.iloc[:, [0, 3]]
```

### Filtering

**R:**
```r
available_districts %>%
  dplyr::filter(resp == 200) %>%
  dplyr::pull(id)
```

**Python:**
```python
available_districts[available_districts['resp'] == '200']['id'].tolist()
```

## Data Output

Both implementations return identical data structures:

| Column Name | Type | Description |
|------------|------|-------------|
| district | string | District name |
| year | string | Year |
| month | string | Month |
| id | string | District ID |
| arbeitssuchend | numeric | Job seekers |
| arbeitslos | numeric | Unemployed |
| arbeitslos_m | numeric | Unemployed (male) |
| arbeitslos_w | numeric | Unemployed (female) |
| arbeitslos_zugang | numeric | Inflow unemployed |
| arbeitslos_abgang | numeric | Outflow unemployed |
| arbeitslos_quote | numeric | Unemployment rate |
| arbeitsstellen_zugang | numeric | Job vacancies inflow |
| arbeitsstellen_jahreszugang | numeric | Job vacancies YTD |
| arbeitsstellen | numeric | Job vacancies |

## Performance

Both implementations:
- Include 1-second delay between requests
- Process 400+ districts in ~7-8 minutes
- Use identical API endpoints
- Handle errors gracefully

## Functionality Parity

✅ Both implementations provide:
- Single district data retrieval
- Bulk district data retrieval
- Progress tracking
- Error handling
- Internal data caching
- Identical output format
- Same data source URLs

## Migration Guide

For users switching from R to Python:

1. **Replace library call:**
   - R: `library(scrapeba)`
   - Python: `from scrapeba import get_district, get_data`

2. **Use parentheses for arguments:**
   - R: `get_district(id = "09571")`
   - Python: `get_district(id="09571")`

3. **Use Python methods for data manipulation:**
   - R: `head(df)`, `summary(df)`
   - Python: `df.head()`, `df.describe()`

4. **Save data differently:**
   - R: `write.csv(df, "file.csv", row.names = FALSE)`
   - Python: `df.to_csv("file.csv", index=False)`

## Example: Complete Workflow

### R Version
```r
library(scrapeba)

# Get data
df <- get_district(id = "09571", year = "2021", month = "10")

# Analyze
summary(df$arbeitslos_quote)

# Save
write.csv(df, "output.csv", row.names = FALSE)
```

### Python Version
```python
from scrapeba import get_district

# Get data
df = get_district(id="09571", year="2021", month="10")

# Analyze
print(df['arbeitslos_quote'].describe())

# Save
df.to_csv("output.csv", index=False)
```

Both versions achieve the same result with nearly identical syntax!
