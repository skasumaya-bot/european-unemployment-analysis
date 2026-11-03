from pathlib import Path
import pandas as pd


# 1. Locate the input file.
PROJECT_FOLDER = Path(__file__).resolve().parent
INPUT_FILE = PROJECT_FOLDER / "FD214_103 (1).xlsx"

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Excel file not found:\n{INPUT_FILE}\n"
        "Put the Excel file in the same folder as this script."
    )

# 2. Read the first worksheet.
df = pd.read_excel(INPUT_FILE, sheet_name=0)

required_columns = ["country_name", "quarter", "unemp"]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

df = df[required_columns].copy()

# Remove completely empty rows.
df = df.dropna(how="all")

df = df.rename(columns={
    "country_name": "country",
    "unemp": "unemployment_rate",
})

# 3. Check country names and quarter labels.
df["country"] = df["country"].astype("string").str.strip()
df["quarter"] = df["quarter"].astype("string").str.strip()

if df["country"].isna().any() or df["country"].eq("").any():
    raise ValueError("Some rows have missing country names.")

valid_quarters = df["quarter"].str.fullmatch(
    r"\d{4}Q[1-4]", na=False
)

if not valid_quarters.all():
    print(df.loc[~valid_quarters, ["country", "quarter"]])
    raise ValueError("Some quarter labels are missing or invalid.")

# Keep every country present in the workbook.
countries = sorted(df["country"].unique().tolist())

df["quarter"] = pd.PeriodIndex(df["quarter"], freq="Q")

# 4. Select 2015Q1–2024Q4.
start = pd.Period("2015Q1", freq="Q")
end = pd.Period("2024Q4", freq="Q")

df = df[df["quarter"].between(start, end)].copy()

df["unemployment_rate"] = pd.to_numeric(
    df["unemployment_rate"],
    errors="raise",
)

df = df.sort_values(
    ["country", "quarter"]
).reset_index(drop=True)

# 5. Check duplicates, missing quarters, and missing values.
duplicate_mask = df.duplicated(
    ["country", "quarter"], keep=False
)

if duplicate_mask.any():
    print(df.loc[duplicate_mask].to_string(index=False))
    raise ValueError("Duplicate country-quarter observations found.")

quarters = pd.period_range(start, end, freq="Q")

expected_pairs = {
    (country, quarter)
    for country in countries
    for quarter in quarters
}

actual_pairs = set(zip(df["country"], df["quarter"]))
missing_pairs = sorted(expected_pairs - actual_pairs)

missing_values = df["unemployment_rate"].isna().sum()

print("\nDATA CHECK")
print("-" * 50)
print(f"Countries in the workbook: {len(countries)}")
print(f"Countries in the selected period: {df['country'].nunique()}")
print(f"Expected observations: {len(expected_pairs)}")
print(f"Actual observations: {len(df)}")
print("Duplicate observations: 0")
print(f"Missing country-quarter combinations: {len(missing_pairs)}")
print(f"Missing unemployment values: {missing_values}")

print("\nObservations per country:")
print(
    df.groupby("country")
    .size()
    .rename("observations")
    .to_string()
)

if missing_pairs:
    print("\nMissing country-quarter combinations:")
    for country, quarter in missing_pairs:
        print(country, quarter)

if missing_pairs or missing_values:
    raise ValueError(
        "Missing data found. Share the results before proceeding."
    )

# Unemployment percentages should be between 0 and 100.
if not df["unemployment_rate"].between(0, 100).all():
    raise ValueError(
        "Some unemployment values are outside the range 0–100."
    )

# 6. Save a prepared copy. The original Excel file stays unchanged.
DATA_FOLDER = PROJECT_FOLDER / "data"
DATA_FOLDER.mkdir(exist_ok=True)

OUTPUT_FILE = DATA_FOLDER / "unemployment_2015_2024.csv"
df.to_csv(OUTPUT_FILE, index=False)

print("\nFirst 10 observations:")
print(df.head(10).to_string(index=False))

print(f"\nPrepared dataset saved to:\n{OUTPUT_FILE}")
print("\nData preparation completed successfully.")