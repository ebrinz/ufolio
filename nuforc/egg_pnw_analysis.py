"""
Egg Shape & Pacific Northwest Concentration Analysis
=====================================================
Question: Is the "egg" shape abnormally concentrated in the PNW?
          Are any other shapes geographically concentrated anywhere?

Method:
  - Compare each shape's % of sightings in PNW vs. national baseline
  - Use chi-squared test to check statistical significance
  - Compute a "concentration ratio" for every shape × region pair
  - Map egg sightings specifically to see the spatial pattern
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np
from scipy import stats
import warnings

warnings.filterwarnings("ignore")
matplotlib.use("Agg")

plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150,
    "font.family": "sans-serif",
    "axes.titlesize": 14, "axes.labelsize": 11,
})
sns.set_style("whitegrid")

OUTPUT_DIR = "charts"

# ════════════════════════════════════════════════════════════════════
# Load & prep
# ════════════════════════════════════════════════════════════════════

df = pd.read_csv("data/scrubbed.csv", low_memory=False)
df.columns = df.columns.str.strip()
df["shape"] = df["shape"].astype(str).str.strip().str.lower()
df.loc[df["shape"] == "nan", "shape"] = "unknown"

us = df[df["country"] == "us"].copy()
us = us[us["state"].notna() & (us["state"].str.len() == 2)]
us["latitude"] = pd.to_numeric(us["latitude"], errors="coerce")
us["longitude"] = pd.to_numeric(us["longitude"], errors="coerce")

# ── Define PNW states ──
pnw_states = {"wa", "or", "id"}   # core PNW
pnw_extended = {"wa", "or", "id", "mt"}  # sometimes Montana included

us["is_pnw"] = us["state"].isin(pnw_states)

# ── Define broader regions for comparison ──
region_map = {
    "PNW":       {"wa", "or", "id"},
    "West Coast": {"ca", "wa", "or"},
    "Southwest":  {"az", "nm", "nv", "ut"},
    "Mountain":   {"co", "mt", "wy", "id"},
    "Midwest":    {"il", "in", "mi", "oh", "wi", "ia", "ks", "mn", "mo", "ne", "nd", "sd"},
    "Northeast":  {"ct", "me", "ma", "nh", "ri", "vt", "nj", "ny", "pa"},
    "Southeast":  {"fl", "ga", "nc", "sc", "va", "al", "tn", "la", "tx", "ms", "ar", "ky", "wv", "md", "de", "dc", "ok"},
}

print("=" * 65)
print("EGG SHAPE — PNW CONCENTRATION TEST")
print("=" * 65)

# ════════════════════════════════════════════════════════════════════
# ANALYSIS 1 — Egg in PNW vs. everywhere else
# ════════════════════════════════════════════════════════════════════

total_us = len(us)
total_pnw = us["is_pnw"].sum()
total_non_pnw = total_us - total_pnw

egg_total = (us["shape"] == "egg").sum()
egg_pnw = ((us["shape"] == "egg") & us["is_pnw"]).sum()
egg_non_pnw = egg_total - egg_pnw

pnw_share_of_us = total_pnw / total_us * 100
egg_pnw_share = egg_pnw / egg_total * 100 if egg_total > 0 else 0

print(f"\nPNW states (WA, OR, ID):")
print(f"  PNW share of all US sightings:  {pnw_share_of_us:.1f}%  ({total_pnw:,} / {total_us:,})")
print(f"  PNW share of EGG sightings:     {egg_pnw_share:.1f}%  ({egg_pnw} / {egg_total})")
print(f"  Concentration ratio:            {egg_pnw_share / pnw_share_of_us:.2f}x")

# Chi-squared test: is egg disproportionately in PNW?
#   Observed: [egg_pnw, egg_non_pnw]
#   Expected: [egg_total * pnw_fraction, egg_total * non_pnw_fraction]
pnw_frac = total_pnw / total_us
expected_egg_pnw = egg_total * pnw_frac
expected_egg_non_pnw = egg_total * (1 - pnw_frac)

chi2, p_value = stats.chisquare(
    [egg_pnw, egg_non_pnw],
    [expected_egg_pnw, expected_egg_non_pnw]
)
print(f"\n  Chi-squared test:")
print(f"    Expected egg in PNW:  {expected_egg_pnw:.1f}")
print(f"    Observed egg in PNW:  {egg_pnw}")
print(f"    χ² = {chi2:.2f},  p = {p_value:.4f}")
print(f"    {'** SIGNIFICANT (p < 0.05) **' if p_value < 0.05 else 'Not significant'}")

# ════════════════════════════════════════════════════════════════════
# ANALYSIS 2 — Per-state egg rate (sightings per 1000)
# ════════════════════════════════════════════════════════════════════

print("\n── Egg sightings per 1,000 total sightings, by state (top 20) ──")

state_totals = us.groupby("state").size().rename("total")
state_egg = us[us["shape"] == "egg"].groupby("state").size().rename("egg")
state_rates = pd.concat([state_totals, state_egg], axis=1).fillna(0)
state_rates["egg_rate"] = state_rates["egg"] / state_rates["total"] * 1000
state_rates = state_rates[state_rates["total"] >= 50]  # min 50 sightings
state_rates = state_rates.sort_values("egg_rate", ascending=False)

print(state_rates[["total", "egg", "egg_rate"]].head(20).to_string(float_format=lambda x: f"{x:.1f}"))

# ════════════════════════════════════════════════════════════════════
# CHART A — Egg rate by state, highlighting PNW
# ════════════════════════════════════════════════════════════════════

top_states = state_rates.head(25)
colors = ["#d08770" if s in pnw_states else "#5e81ac" for s in top_states.index]

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(top_states.index[::-1], top_states["egg_rate"].values[::-1],
               color=colors[::-1], edgecolor="white")
ax.axvline(state_rates["egg_rate"].median(), color="#bf616a", ls="--", lw=1.5,
           label=f"Median: {state_rates['egg_rate'].median():.1f}")
ax.set_xlabel("Egg Sightings per 1,000 Total Sightings")
ax.set_title("Egg-Shape Rate by State (orange = PNW)")
ax.legend()

# Add count annotations
for bar, (idx, row) in zip(bars, list(top_states.iloc[::-1].iterrows())):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f"n={int(row['egg'])}", va="center", fontsize=8, color="#555")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/08_egg_rate_by_state.png")
plt.close()
print(f"\n  Saved → {OUTPUT_DIR}/08_egg_rate_by_state.png")

# ════════════════════════════════════════════════════════════════════
# CHART B — Egg sightings map (scatter) with PNW highlighted
# ════════════════════════════════════════════════════════════════════

egg_geo = us[
    (us["shape"] == "egg") &
    us["latitude"].between(24, 50) &
    us["longitude"].between(-130, -65)
]

fig, ax = plt.subplots(figsize=(14, 8))

# Plot all US sightings as faint background
bg = us[us["latitude"].between(24, 50) & us["longitude"].between(-130, -65)]
ax.scatter(bg["longitude"], bg["latitude"], s=1, alpha=0.03, color="#d8dee9", label="_bg")

# Plot egg sightings
non_pnw_egg = egg_geo[~egg_geo["is_pnw"]]
pnw_egg = egg_geo[egg_geo["is_pnw"]]
ax.scatter(non_pnw_egg["longitude"], non_pnw_egg["latitude"],
           s=15, alpha=0.5, color="#5e81ac", label=f"Egg — rest of US (n={len(non_pnw_egg)})", zorder=3)
ax.scatter(pnw_egg["longitude"], pnw_egg["latitude"],
           s=25, alpha=0.7, color="#d08770", edgecolors="#bf616a", linewidth=0.5,
           label=f"Egg — PNW (n={len(pnw_egg)})", zorder=4)

# Draw PNW bounding box
ax.axvspan(-125, -116, ymin=(42-24)/(50-24), ymax=(49-24)/(50-24),
           alpha=0.08, color="#d08770", label="_pnw_box")
ax.text(-124.5, 48.5, "PNW", fontsize=12, color="#d08770", fontweight="bold")

ax.set_xlim(-130, -65)
ax.set_ylim(24, 50)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Egg-Shaped UFO Sightings — PNW vs. Rest of U.S.")
ax.legend(loc="lower right", fontsize=10)
ax.set_aspect("equal")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/09_egg_map_pnw.png")
plt.close()
print(f"  Saved → {OUTPUT_DIR}/09_egg_map_pnw.png")

# ════════════════════════════════════════════════════════════════════
# ANALYSIS 3 — Which shapes ARE abnormally concentrated somewhere?
#   Compute concentration ratio for every (shape, region) pair
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("ALL SHAPES — REGIONAL CONCENTRATION ANALYSIS")
print("=" * 65)
print("(Concentration ratio = region's share of shape / region's share of all sightings)")
print("(Ratio > 1.0 = over-represented, < 1.0 = under-represented)\n")

# Only shapes with 100+ total sightings
valid_shapes = us["shape"].value_counts()
valid_shapes = valid_shapes[valid_shapes >= 100].index.tolist()

results = []
for region_name, region_states in region_map.items():
    region_total = us[us["state"].isin(region_states)].shape[0]
    region_frac = region_total / total_us

    for shape in valid_shapes:
        shape_total = (us["shape"] == shape).sum()
        shape_in_region = ((us["shape"] == shape) & us["state"].isin(region_states)).sum()

        if shape_total == 0 or region_total == 0:
            continue

        shape_region_share = shape_in_region / shape_total
        concentration = shape_region_share / region_frac

        # Chi-squared for this combo
        expected = shape_total * region_frac
        not_in_region = shape_total - shape_in_region
        expected_not = shape_total * (1 - region_frac)
        if expected >= 5:  # chi-sq validity
            chi2, p = stats.chisquare([shape_in_region, not_in_region],
                                       [expected, expected_not])
        else:
            chi2, p = 0, 1.0

        results.append({
            "shape": shape,
            "region": region_name,
            "shape_total": shape_total,
            "in_region": shape_in_region,
            "region_share_pct": shape_region_share * 100,
            "baseline_pct": region_frac * 100,
            "concentration": concentration,
            "chi2": chi2,
            "p_value": p,
        })

conc_df = pd.DataFrame(results)

# Show the most concentrated (shape, region) pairs
significant = conc_df[(conc_df["p_value"] < 0.01) & (conc_df["in_region"] >= 10)]
top_concentrated = significant.sort_values("concentration", ascending=False).head(25)

print("── Top 25 most concentrated (shape, region) pairs  [p < 0.01] ──")
print(top_concentrated[["shape", "region", "shape_total", "in_region",
                         "region_share_pct", "baseline_pct", "concentration", "p_value"]]
      .to_string(index=False, float_format=lambda x: f"{x:.2f}"))

# ════════════════════════════════════════════════════════════════════
# CHART C — Concentration heatmap: shape × region
# ════════════════════════════════════════════════════════════════════

# Pivot for heatmap — top 15 shapes
top15 = us["shape"].value_counts().head(15).index.tolist()
# Add egg if not already there
if "egg" not in top15:
    top15.append("egg")

heatmap_data = conc_df[conc_df["shape"].isin(top15)].pivot_table(
    index="shape", columns="region", values="concentration"
)

# Sort shapes by overall count
shape_order = [s for s in us["shape"].value_counts().index if s in heatmap_data.index]
heatmap_data = heatmap_data.loc[shape_order]

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(
    heatmap_data, annot=True, fmt=".2f", cmap="RdYlGn_r",
    center=1.0, linewidths=0.5, ax=ax,
    cbar_kws={"label": "Concentration Ratio (1.0 = expected)"},
    vmin=0.7, vmax=1.5
)
ax.set_title("Shape × Region Concentration Ratio\n(>1 = over-represented, <1 = under-represented)")
ax.set_ylabel("Shape")
ax.set_xlabel("Region")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/10_concentration_heatmap.png")
plt.close()
print(f"\n  Saved → {OUTPUT_DIR}/10_concentration_heatmap.png")

# ════════════════════════════════════════════════════════════════════
# CHART D — Statistical significance: which combos are truly anomalous?
# ════════════════════════════════════════════════════════════════════

# Mark significance with stars
sig = conc_df[conc_df["shape"].isin(top15)].copy()
sig["sig_label"] = sig.apply(
    lambda r: f"{r['concentration']:.2f}***" if r["p_value"] < 0.001
    else (f"{r['concentration']:.2f}**" if r["p_value"] < 0.01
    else (f"{r['concentration']:.2f}*" if r["p_value"] < 0.05
    else f"{r['concentration']:.2f}")), axis=1
)

sig_pivot = sig.pivot_table(index="shape", columns="region", values="sig_label", aggfunc="first")
sig_pivot = sig_pivot.loc[[s for s in shape_order if s in sig_pivot.index]]

print("\n── Concentration ratios with significance (* p<.05  ** p<.01  *** p<.001) ──")
print(sig_pivot.to_string())

# ════════════════════════════════════════════════════════════════════
# CHART E — Egg vs. other shapes: PNW concentration comparison
# ════════════════════════════════════════════════════════════════════

pnw_conc = conc_df[conc_df["region"] == "PNW"].sort_values("concentration", ascending=False)
pnw_conc = pnw_conc[pnw_conc["shape_total"] >= 50]

fig, ax = plt.subplots(figsize=(10, 8))
colors_pnw = ["#d08770" if s == "egg" else ("#bf616a" if p < 0.05 else "#b0b0b0")
              for s, p in zip(pnw_conc["shape"], pnw_conc["p_value"])]

ax.barh(pnw_conc["shape"].values[::-1], pnw_conc["concentration"].values[::-1],
        color=colors_pnw[::-1], edgecolor="white")
ax.axvline(1.0, color="#2e3440", ls="-", lw=1, alpha=0.5)
ax.axvline(1.0, color="#bf616a", ls="--", lw=1.5, label="Expected (1.0)")
ax.set_xlabel("PNW Concentration Ratio")
ax.set_title("PNW Concentration by Shape\n(orange=egg, red=significant p<.05, gray=not significant)")
ax.legend()

for i, (_, row) in enumerate(pnw_conc.iloc[::-1].iterrows()):
    sig_mark = "***" if row["p_value"] < 0.001 else ("**" if row["p_value"] < 0.01 else ("*" if row["p_value"] < 0.05 else ""))
    ax.text(row["concentration"] + 0.02, i,
            f"{row['concentration']:.2f}{sig_mark}  (n={int(row['in_region'])})",
            va="center", fontsize=8)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/11_pnw_concentration_all_shapes.png")
plt.close()
print(f"  Saved → {OUTPUT_DIR}/11_pnw_concentration_all_shapes.png")

# ════════════════════════════════════════════════════════════════════
# Final verdict
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("VERDICT — Egg in the PNW")
print("=" * 65)

egg_row = conc_df[(conc_df["shape"] == "egg") & (conc_df["region"] == "PNW")].iloc[0]
print(f"""
  PNW baseline (share of all US sightings): {egg_row['baseline_pct']:.1f}%
  PNW share of egg sightings:               {egg_row['region_share_pct']:.1f}%
  Concentration ratio:                      {egg_row['concentration']:.2f}x
  Chi-squared p-value:                      {egg_row['p_value']:.4f}
  Statistically significant?                {'YES' if egg_row['p_value'] < 0.05 else 'NO'}
""")

# What shapes ARE anomalously concentrated in PNW?
pnw_sig = pnw_conc[pnw_conc["p_value"] < 0.05].sort_values("concentration", ascending=False)
if len(pnw_sig) > 0:
    print("  Shapes SIGNIFICANTLY over-represented in PNW (p < 0.05):")
    for _, row in pnw_sig.iterrows():
        print(f"    {row['shape']:12s}  {row['concentration']:.2f}x  (p={row['p_value']:.4f}, n={int(row['in_region'])})")
else:
    print("  No shapes are significantly over-represented in PNW.")

# What shapes are most concentrated ANYWHERE?
print("\n  Most geographically concentrated shapes overall (top 10):")
top_anywhere = significant.sort_values("concentration", ascending=False).head(10)
for _, row in top_anywhere.iterrows():
    print(f"    {row['shape']:12s} in {row['region']:12s}  {row['concentration']:.2f}x  (p={row['p_value']:.6f}, n={int(row['in_region'])})")
