import csv
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
INPUT = HERE / "results_summary.csv"
OUTPUT = HERE / "defense_comparison.png"

with INPUT.open(newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

models = list(dict.fromkeys(row["model"] for row in rows))
defenses = ["FT", "NC"]

fig, ax = plt.subplots(figsize=(9, 5))

x = range(len(models))
width = 0.35

for i, defense in enumerate(defenses):
    values = [
        float(next(
            row["defended_asr"]
            for row in rows
            if row["model"] == model
            and row["defense"] == defense
        ))
        for model in models
    ]

    positions = [p + (i - 0.5) * width for p in x]
    bars = ax.bar(positions, values, width, label=defense)
    ax.bar_label(bars, fmt="%.2f%%", padding=3)

ax.set_xticks(list(x))
ax.set_xticklabels(models)
ax.set_ylabel("Attack success rate (%)")
ax.set_ylim(0, 105)
ax.set_title("BadNets: FT vs NC at 10% Poisoning")
ax.legend()
ax.grid(axis="y", alpha=0.2)

fig.tight_layout()
fig.savefig(OUTPUT, dpi=200)
plt.close(fig)

print(f"Plot saved to: {OUTPUT}")
