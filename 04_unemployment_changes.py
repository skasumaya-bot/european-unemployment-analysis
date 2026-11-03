from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# 1. Read the prepared dataset.
PROJECT_FOLDER = Path(__file__).resolve().parent

INPUT_FILE = (
    PROJECT_FOLDER / "data" / "unemployment_2015_2024.csv"
)

OUTPUT_FOLDER = PROJECT_FOLDER / "outputs"
OUTPUT_FOLDER.mkdir(exist_ok=True)

df = pd.read_csv(INPUT_FILE)

# 2. Select the starting and ending quarters.
START_QUARTER = "2015Q1"
END_QUARTER = "2024Q4"

comparison = (
    df[df["quarter"].isin([START_QUARTER, END_QUARTER])]
    .pivot(
        index="country",
        columns="quarter",
        values="unemployment_rate",
    )
    .reindex(columns=[START_QUARTER, END_QUARTER])
)

if comparison.isna().any().any():
    raise ValueError("Some countries are missing a starting or ending value.")

# 3. Calculate the change in percentage points.
comparison["change_pp"] = (
    comparison[END_QUARTER] - comparison[START_QUARTER]
)

comparison = comparison.sort_values("change_pp")
comparison.columns.name = None

TABLE_FILE = OUTPUT_FOLDER / "unemployment_changes.csv"

comparison.to_csv(
    TABLE_FILE,
    float_format="%.3f",
)

# 4. Draw the chart.
colors = [
    "#2878A0" if value < 0 else "#D17A28"
    for value in comparison["change_pp"]
]

fig, ax = plt.subplots(figsize=(11, 11))

ax.barh(
    comparison.index,
    comparison["change_pp"],
    color=colors,
)

ax.axvline(0, color="black", linewidth=0.8)
ax.invert_yaxis()

# Add a value beside each bar.
for position, value in enumerate(comparison["change_pp"]):
    offset = 0.15 if value >= 0 else -0.15

    ax.text(
        value + offset,
        position,
        f"{value:+.1f}",
        va="center",
        ha="left" if value >= 0 else "right",
        fontsize=9,
    )

ax.set_title(
    "Change in Unemployment Rates\n"
    "2024Q4 compared with 2015Q1",
    fontsize=14,
    pad=15,
)

ax.set_xlabel(
    "Change in percentage points "
    "(negative = decrease; positive = increase)"
)

ax.set_ylabel("")
ax.margins(x=0.18)
ax.grid(axis="x", alpha=0.25)
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.text(
    0.01,
    0.01,
    "Source: supplied dataset, originally sourced from Trading Economics.\n"
    "Illustrative comparison. Seasonal adjustment and cross-country "
    "comparability have not been verified.",
    fontsize=8,
)

fig.tight_layout(rect=[0, 0.055, 1, 1])

CHART_FILE = OUTPUT_FOLDER / "unemployment_changes.png"

fig.savefig(
    CHART_FILE,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)

# 5. Display the results.
print("\nUNEMPLOYMENT CHANGES")
print("-" * 60)
print(comparison.round(2).to_string())

print(
    "\nNote: this compares two quarters, "
    "not the full path between them."
)

print(f"\nTable saved to:\n{TABLE_FILE}")
print(f"\nChart saved to:\n{CHART_FILE}")