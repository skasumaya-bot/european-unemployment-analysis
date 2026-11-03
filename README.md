# European Unemployment Analysis: A Python Demonstration

This project uses Python to explore unemployment figures across 27 European countries from 2015Q1 to 2024Q4.

It demonstrates data preparation, data-quality checks, summary statistics, and visualization.

## Data

The project uses a supplied Excel dataset containing unemployment figures originally sourced from Trading Economics.

| Item | Description |
|---|---|
| Countries | 27 European countries |
| Period | 2015Q1–2024Q4 |
| Frequency | Quarterly |
| Observations | 1,080 |
| Main variable | Unemployment rate (%) |

The analysis uses three columns from the supplied workbook:

- `country_name`: country name.

- `quarter`: year and quarter.

- `unemp`: unemployment rate.

This is a demonstration project. Definitions, seasonal adjustment, and cross-country comparability have not been independently verified. The figures should therefore be treated as illustrative.

## Questions

- How do average unemployment rates differ across countries?

- How does unemployment change over time within each country?

- How do unemployment rates in 2024Q4 compare with 2015Q1?

## Data preparation

The preparation script:

1. Reads the supplied Excel workbook.

2. Selects the country, quarter, and unemployment columns.

3. Keeps all 27 countries for 2015Q1–2024Q4.

4. Checks quarter labels, duplicates, missing values, and country coverage.

5. Saves a prepared CSV dataset.

The selected dataset contains 40 observations per country, with no missing unemployment values or duplicate country-quarter observations.

## Main results

In the supplied dataset:

- Greece has the highest average unemployment rate over the period, at 17.43%, followed by Spain at 15.43%.

- Denmark has the lowest average rate, at 3.10%.

- Greece has the largest variation over time, with a standard deviation of 5.12 percentage points.

- Unemployment is lower in 2024Q4 than in 2015Q1 in 26 of the 27 countries.

- Estonia records an increase of approximately 0.83 percentage points.

### Largest decreases between the starting and ending quarters

| Country | 2015Q1 (%) | 2024Q4 (%) | Change (percentage points) |
|---|---:|---:|---:|
| Greece | 25.83 | 9.53 | -16.30 |
| Croatia | 19.80 | 4.93 | -14.87 |
| Spain | 23.50 | 10.80 | -12.70 |
| Cyprus | 16.47 | 4.73 | -11.73 |
| Slovenia | 13.20 | 4.67 | -8.53 |

Changes are calculated from the underlying values before rounding.

These results describe the supplied data. They do not establish the causes of unemployment changes.

## Charts

### Average unemployment rates

Each country's average is calculated from its 40 quarterly observations.

![Average unemployment rates](outputs/average_unemployment_by_country.png)

### Quarterly trends

Separate country panels show unemployment over time. Every panel uses the same vertical scale.

![Quarterly unemployment trends](outputs/unemployment_trends_27_countries.png)

### Change between 2015Q1 and 2024Q4

Negative values indicate a decrease. Positive values indicate an increase.

![Changes in unemployment rates](outputs/unemployment_changes.png)

## Project files

| File | Purpose |
|---|---|
| `01_prepare_data.py` | Prepare and check the data |
| `02_country_comparison.py` | Calculate country summaries and plot average rates |
| `03_unemployment_trends.py` | Create separate trend charts for all countries |
| `04_unemployment_changes.py` | Compare starting and ending unemployment rates |
| `data/unemployment_2015_2024.csv` | Prepared dataset |
| `outputs/country_summary.csv` | Country summary statistics |
| `outputs/unemployment_changes.csv` | Starting and ending rates and their differences |
| `requirements.txt` | Required Python packages |

## How to run

Place the original workbook, `FD214_103 (1).xlsx`, in the same folder as the Python scripts.

Install the required packages:

```bash

python -m pip install -r requirements.txt

```

Run the scripts in this order:

```bash

python 01_prepare_data.py

python 02_country_comparison.py

python 03_unemployment_trends.py

python 04_unemployment_changes.py

```

The scripts create the `data` and `outputs` folders automatically. Running them again overwrites the generated files, while leaving the original workbook unchanged.

## Limitations

- Cross-country definitions and seasonal adjustment have not been verified.

- Comparing 2015Q1 with 2024Q4 may reflect seasonal differences because these are different quarters of the year.

- Period averages hide changes within the study period.

- The analysis is descriptive and does not estimate policy effects.

- The original source documentation and any data transformations should be checked before using this dataset for formal research.

## Skills demonstrated

- Reading Excel files with pandas.

- Preparing country-quarter data.

- Checking missing values, duplicates, and panel completeness.

- Calculating descriptive statistics.

- Creating charts with Matplotlib.

- Explaining changes in percentage points.

- Documenting a Python analysis.

## Author

Sumaya Khan Auntu

