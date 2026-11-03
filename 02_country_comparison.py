from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# 1. Read the prepared dataset.
PROJECT_FOLDER = Path(__file__).resolve().parent
INPUT_FILE = (
    PROJECT_FOLDER / "data" / "unemployment_2015_2024.csv"
)

df = pd.read_csv(INPUT_FILE)

# 2. Calculate descriptive statistics for each country.
summary = (
    df.groupby("country")["unemployment_rate"]
    .agg(
        observations="count",
        average_rate="mean",
        minimum_rate="min",
        maximum_rate="max",
        standard_deviation="std",
    )
    .sort_values("average_rate")
)

# 3. Create a folder for the results.
OUTPUT_FOLDER = PROJECT_FOLDER / "outputs"
OUTPUT_FOLDER.mkdir(exist_ok=True)

summary.to_csv(
    OUTPUT_FOLDER / "country_summary.csv",
    float_format="%.3f",
)

# 4. Plot the average unemployment rate for each country.
fig, ax = plt.subplots(figsize=(10, 11))

ax.barh(
    summary.index,
    summary["average_rate"],
    color="#2878A0",
)

# Add a value beside each bar.
for position, value in enumerate(summary["average_rate"]):
    ax.text(
        value + 0.15,
        position,
        f"{value:.1f}",
        va="center",
        fontsize=9,
    )

ax.set_title(
    "Average Unemployment Rates Across 27 European Countries\n"
    "2015Q1–2024Q4",
    fontsize=14,
    pad=15,
)

ax.set_xlabel("Average unemployment rate (%)")
ax.set_ylabel("")

ax.set_xlim(0, summary["average_rate"].max() + 2)
ax.grid(axis="x", alpha=0.25)
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.text(
    0.01,
    0.01,
    "Data: supplied workbook. Each average uses 40 quarterly observations.",
    fontsize=9,
)

fig.tight_layout(rect=[0, 0.035, 1, 1])

CHART_FILE = OUTPUT_FOLDER / "average_unemployment_by_country.png"

fig.savefig(CHART_FILE, dpi=300, bbox_inches="tight")
plt.close(fig)

# 5. Display the results.
print("\nCOUNTRY SUMMARY")
print("-" * 65)
print(summary.round(2).to_string())

print(f"\nChart saved to:\n{CHART_FILE}")
print(
    "\nSummary saved to:\n"
    f"{OUTPUT_FOLDER / 'country_summary.csv'}"
)