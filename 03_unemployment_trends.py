from pathlib import Path
import math

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# 1. Read the prepared data.
PROJECT_FOLDER = Path(__file__).resolve().parent

INPUT_FILE = (
    PROJECT_FOLDER / "data" / "unemployment_2015_2024.csv"
)

OUTPUT_FOLDER = PROJECT_FOLDER / "outputs"
OUTPUT_FOLDER.mkdir(exist_ok=True)

df = pd.read_csv(INPUT_FILE)

# Convert quarter labels into dates for plotting.
df["date"] = pd.PeriodIndex(
    df["quarter"], freq="Q"
).to_timestamp()

df = df.sort_values(["country", "date"])

countries = sorted(df["country"].unique())

# 2. Set up a grid with three country charts per row.
columns = 3
rows = math.ceil(len(countries) / columns)

fig, axes = plt.subplots(
    rows,
    columns,
    figsize=(15, rows * 2.3),
    sharex=True,
    sharey=True,
    squeeze=False,
)

# Use the same unemployment scale in every chart.
# This makes differences in levels visible.
upper_limit = max(
    5,
    math.ceil(df["unemployment_rate"].max() / 5) * 5,
)

# 3. Draw one chart for each country.
for ax, country in zip(axes.flat, countries):
    country_data = df[df["country"] == country]

    ax.plot(
        country_data["date"],
        country_data["unemployment_rate"],
        color="#2878A0",
        linewidth=1.8,
    )

    ax.set_title(country, fontsize=11)
    ax.set_ylim(0, upper_limit)

    ax.xaxis.set_major_locator(
        mdates.YearLocator(3)
    )
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%Y")
    )

    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=8)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# Hide unused panels if the country count changes.
for ax in list(axes.flat)[len(countries):]:
    ax.set_visible(False)

# 4. Add the title and labels.
fig.suptitle(
    "Quarterly Unemployment Trends Across 27 European Countries\n"
    "2015Q1–2024Q4",
    fontsize=17,
    y=0.995,
)

fig.supylabel(
    "Unemployment rate (%)",
    fontsize=12,
)

fig.supxlabel(
    "Year",
    fontsize=12,
    y=0.035,
)

fig.text(
    0.5,
    0.012,
    "Source: supplied dataset, originally sourced from Trading Economics.\n"
    "Demonstration project; cross-country comparability has not been verified.",
    ha="center",
    fontsize=9,
)

fig.tight_layout(
    rect=[0.03, 0.055, 1, 0.965]
)

# 5. Save the figure.
OUTPUT_FILE = (
    OUTPUT_FOLDER / "unemployment_trends_27_countries.png"
)

fig.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)

print("\nTREND CHARTS COMPLETED")
print("-" * 50)
print(f"Countries plotted: {len(countries)}")
print(f"Observations plotted: {len(df)}")
print(f"\nChart saved to:\n{OUTPUT_FILE}")