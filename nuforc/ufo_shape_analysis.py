"""
UFO Shape Distribution Analysis — NUFORC Dataset
=================================================
This script analyzes the distribution of reported UFO craft shapes
across U.S. geography, using the NUFORC/ufo-sightings Kaggle dataset.

Outputs:
  1. Bar chart of top UFO shapes (overall frequency)
  2. Distribution curve (KDE) of shape counts per state
  3. Geographic heatmap — top shape reported per U.S. state
  4. Stacked bar chart — shape mix by region (NE, SE, MW, W)
  5. Text-mining exploration of the comments column for shape keywords

All charts are saved as PNGs for easy email attachment.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np
from scipy import stats
from collections import Counter
import re
import warnings

warnings.filterwarnings("ignore")
matplotlib.use("Agg")  # non-interactive backend for saving PNGs

# ─── styling ────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "font.family": "sans-serif",
    "axes.titlesize": 14,
    "axes.labelsize": 11,
})
sns.set_style("whitegrid")

OUTPUT_DIR = "charts"
import os
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ════════════════════════════════════════════════════════════════════
# SECTION 1 — Load & clean the data
# ════════════════════════════════════════════════════════════════════

print("Loading data...")
df = pd.read_csv("data/scrubbed.csv", low_memory=False)

# Clean column names (the CSV has a trailing space on 'longitude ')
df.columns = df.columns.str.strip()

print(f"Total records: {len(df):,}")
print(f"\nShape column — unique values: {df['shape'].nunique()}")
print(f"Missing shapes: {df['shape'].isna().sum():,}")

# Normalize shapes: lowercase, strip whitespace
df["shape"] = df["shape"].astype(str).str.strip().str.lower()
df.loc[df["shape"] == "nan", "shape"] = "unknown"

# Quick look at shape value counts
shape_counts = df["shape"].value_counts()
print("\n── Shape Frequency (all) ──")
print(shape_counts.to_string())

# ════════════════════════════════════════════════════════════════════
# CHART 1 — Top 15 UFO shapes (bar chart)
# ════════════════════════════════════════════════════════════════════

print("\n[Chart 1] Top 15 UFO shapes — bar chart")

top_n = 15
top_shapes = shape_counts.head(top_n)

fig, ax = plt.subplots(figsize=(10, 6))
colors = sns.color_palette("crest", n_colors=top_n)
bars = ax.barh(top_shapes.index[::-1], top_shapes.values[::-1], color=colors[::-1])

# Add count labels on bars
for bar, val in zip(bars, top_shapes.values[::-1]):
    ax.text(bar.get_width() + 150, bar.get_y() + bar.get_height() / 2,
            f"{val:,}", va="center", fontsize=9)

ax.set_xlabel("Number of Sightings")
ax.set_title("Top 15 Reported UFO Shapes (NUFORC)")
ax.set_xlim(0, top_shapes.max() * 1.15)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_top_shapes_bar.png")
plt.close()
print(f"  Saved → {OUTPUT_DIR}/01_top_shapes_bar.png")

# ════════════════════════════════════════════════════════════════════
# CHART 2 — Distribution curve (KDE + histogram) of shape popularity
# ════════════════════════════════════════════════════════════════════

print("\n[Chart 2] Distribution curve of shape counts")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 2a — Raw distribution (very skewed, so show log scale too)
axes[0].hist(shape_counts.values, bins=30, color="#5e81ac", edgecolor="white", alpha=0.8)
axes[0].set_xlabel("Sightings per Shape Category")
axes[0].set_ylabel("Number of Shape Categories")
axes[0].set_title("Distribution of Shape Counts (linear)")

# 2b — Log-scale distribution
log_counts = np.log10(shape_counts.values + 1)
axes[1].hist(log_counts, bins=20, color="#a3be8c", edgecolor="white", alpha=0.8)

# Overlay KDE
kde_x = np.linspace(log_counts.min(), log_counts.max(), 200)
kde = stats.gaussian_kde(log_counts)
ax2 = axes[1].twinx()
ax2.plot(kde_x, kde(kde_x), color="#bf616a", lw=2, label="KDE")
ax2.set_ylabel("Density")
ax2.legend(loc="upper right")

axes[1].set_xlabel("log₁₀(Sightings per Shape)")
axes[1].set_ylabel("Number of Shape Categories")
axes[1].set_title("Distribution of Shape Counts (log scale + KDE)")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_shape_distribution_curve.png")
plt.close()
print(f"  Saved → {OUTPUT_DIR}/02_shape_distribution_curve.png")

# ════════════════════════════════════════════════════════════════════
# SECTION 2 — Geography: shapes by U.S. state
# ════════════════════════════════════════════════════════════════════

# Filter to US only and valid states
us_df = df[df["country"] == "us"].copy()
us_df = us_df[us_df["state"].notna() & (us_df["state"].str.len() == 2)]
print(f"\nUS-only records: {len(us_df):,}")

# ── U.S. Census regions ──
regions = {
    "Northeast": ["ct", "me", "ma", "nh", "ri", "vt", "nj", "ny", "pa"],
    "Southeast": ["de", "fl", "ga", "md", "nc", "sc", "va", "dc", "wv",
                   "al", "ky", "ms", "tn", "ar", "la", "ok", "tx"],
    "Midwest":   ["il", "in", "mi", "oh", "wi", "ia", "ks", "mn", "mo",
                   "ne", "nd", "sd"],
    "West":      ["az", "co", "id", "mt", "nv", "nm", "ut", "wy",
                   "ak", "ca", "hi", "or", "wa"],
}
state_to_region = {}
for region, states in regions.items():
    for s in states:
        state_to_region[s] = region

us_df["region"] = us_df["state"].map(state_to_region)

# ════════════════════════════════════════════════════════════════════
# CHART 3 — Top shape per state (choropleth-style table heatmap)
# ════════════════════════════════════════════════════════════════════

print("\n[Chart 3] Most common shape per U.S. state")

# Top shape per state
top_shape_by_state = (
    us_df.groupby("state")["shape"]
    .agg(lambda x: x.value_counts().index[0])
    .reset_index()
    .rename(columns={"shape": "top_shape"})
)

# Count how many states have each shape as #1
state_shape_summary = top_shape_by_state["top_shape"].value_counts()
print("\n── Most-reported shape, by # of states where it's #1 ──")
print(state_shape_summary.to_string())

# Build a pivot: state × top-5 shapes
top5_shapes = shape_counts.head(5).index.tolist()
state_shape_pivot = (
    us_df[us_df["shape"].isin(top5_shapes)]
    .groupby(["state", "shape"])
    .size()
    .unstack(fill_value=0)
)

# Normalize each state row to percentages
state_shape_pct = state_shape_pivot.div(state_shape_pivot.sum(axis=1), axis=0) * 100

# Heatmap of top 5 shapes across states
fig, ax = plt.subplots(figsize=(10, 14))
sns.heatmap(
    state_shape_pct.sort_index(),
    annot=True, fmt=".0f", cmap="YlOrRd",
    linewidths=0.5, ax=ax,
    cbar_kws={"label": "% of top-5 shape sightings"}
)
ax.set_title("Top 5 UFO Shapes — % Share by State")
ax.set_ylabel("State")
ax.set_xlabel("Shape")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_shape_heatmap_by_state.png")
plt.close()
print(f"  Saved → {OUTPUT_DIR}/03_shape_heatmap_by_state.png")

# ════════════════════════════════════════════════════════════════════
# CHART 4 — Stacked bar: shape mix by Census region
# ════════════════════════════════════════════════════════════════════

print("\n[Chart 4] Shape mix by U.S. region")

region_shape = (
    us_df[us_df["shape"].isin(top5_shapes) & us_df["region"].notna()]
    .groupby(["region", "shape"])
    .size()
    .unstack(fill_value=0)
)

# Normalize to %
region_shape_pct = region_shape.div(region_shape.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(10, 6))
region_shape_pct.plot(kind="bar", stacked=True, ax=ax,
                       colormap="Set2", edgecolor="white")
ax.set_ylabel("% of Sightings (top 5 shapes)")
ax.set_xlabel("U.S. Region")
ax.set_title("UFO Shape Mix by U.S. Census Region")
ax.legend(title="Shape", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_shape_by_region_stacked.png")
plt.close()
print(f"  Saved → {OUTPUT_DIR}/04_shape_by_region_stacked.png")

# ════════════════════════════════════════════════════════════════════
# CHART 5 — Geographic scatter: lat/lon colored by shape
# ════════════════════════════════════════════════════════════════════

print("\n[Chart 5] Geographic scatter of top 5 shapes")

geo_df = us_df[
    us_df["shape"].isin(top5_shapes) &
    us_df["latitude"].notna() &
    us_df["longitude"].notna()
].copy()

# Convert latitude/longitude to numeric, drop bad rows
geo_df["latitude"] = pd.to_numeric(geo_df["latitude"], errors="coerce")
geo_df["longitude"] = pd.to_numeric(geo_df["longitude"], errors="coerce")
geo_df = geo_df.dropna(subset=["latitude", "longitude"])

# Filter to continental US bounds
geo_df = geo_df[
    (geo_df["latitude"].between(24, 50)) &
    (geo_df["longitude"].between(-130, -65))
]

fig, ax = plt.subplots(figsize=(14, 8))
palette = {"light": "#ffb347", "triangle": "#ff6961", "circle": "#77dd77",
           "fireball": "#cb99c9", "unknown": "#aec6cf"}

for shape in top5_shapes:
    subset = geo_df[geo_df["shape"] == shape]
    ax.scatter(
        subset["longitude"], subset["latitude"],
        s=3, alpha=0.15, label=shape,
        color=palette.get(shape, "#999999")
    )

ax.set_xlim(-130, -65)
ax.set_ylim(24, 50)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("UFO Sightings — Top 5 Shapes Across Continental U.S.")
ax.legend(markerscale=5, frameon=True, fontsize=10)
ax.set_aspect("equal")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_geo_scatter_top5.png")
plt.close()
print(f"  Saved → {OUTPUT_DIR}/05_geo_scatter_top5.png")

# ════════════════════════════════════════════════════════════════════
# SECTION 3 — Text mining: shape mentions in comments
# ════════════════════════════════════════════════════════════════════

print("\n[Chart 6] Text mining — shape keywords in comments")

# Define shape-related keywords to search for in free text
shape_keywords = [
    "disc", "disk", "saucer", "cigar", "triangle", "triangular",
    "sphere", "spherical", "oval", "egg", "diamond", "rectangle",
    "rectangular", "cylinder", "cylindrical", "boomerang", "chevron",
    "v-shape", "v shape", "orb", "star", "cross", "cone",
    "teardrop", "crescent", "hexagon", "cube", "jellyfish",
    "tic-tac", "tic tac", "pill"
]

# Count keyword occurrences in comments
comments = df["comments"].dropna().str.lower()
keyword_counts = {}
for kw in shape_keywords:
    keyword_counts[kw] = comments.str.contains(re.escape(kw), regex=True).sum()

kw_series = pd.Series(keyword_counts).sort_values(ascending=False)
kw_series = kw_series[kw_series > 0]

print("\n── Shape-related keywords found in comments ──")
print(kw_series.to_string())

# Compare: official "shape" column vs. text mentions
# Group similar keywords
text_shape_groups = {
    "disc/saucer": ["disc", "disk", "saucer"],
    "triangle": ["triangle", "triangular", "v-shape", "v shape"],
    "sphere/orb": ["sphere", "spherical", "orb"],
    "oval/egg": ["oval", "egg"],
    "cigar/cylinder": ["cigar", "cylinder", "cylindrical"],
    "diamond": ["diamond"],
    "rectangle": ["rectangle", "rectangular"],
    "boomerang/chevron": ["boomerang", "chevron"],
    "teardrop": ["teardrop"],
    "tic-tac": ["tic-tac", "tic tac", "pill"],
    "cube": ["cube"],
    "jellyfish": ["jellyfish"],
}

grouped_text_counts = {}
for group_name, keywords in text_shape_groups.items():
    total = sum(keyword_counts.get(kw, 0) for kw in keywords)
    grouped_text_counts[group_name] = total

text_df = pd.Series(grouped_text_counts).sort_values(ascending=False)

# Compare official shape column vs text-mined shapes
# Map official shapes to same groups
official_map = {
    "disc/saucer": ["disk"],
    "triangle": ["triangle", "delta"],
    "sphere/orb": ["sphere"],
    "oval/egg": ["oval", "egg"],
    "cigar/cylinder": ["cigar", "cylinder"],
    "diamond": ["diamond"],
    "rectangle": ["rectangle"],
    "boomerang/chevron": ["boomerang", "chevron"],
    "teardrop": ["teardrop"],
    "tic-tac": [],
    "cube": [],
    "jellyfish": [],
}

official_counts = {}
for group_name, shapes in official_map.items():
    official_counts[group_name] = df[df["shape"].isin(shapes)].shape[0]

official_df = pd.Series(official_counts)

# Side-by-side comparison chart
comparison = pd.DataFrame({
    "Shape Column": official_df,
    "Text in Comments": text_df
}).fillna(0).sort_values("Text in Comments", ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(comparison))
w = 0.35
ax.bar(x - w/2, comparison["Shape Column"], w, label="Official Shape Column", color="#5e81ac")
ax.bar(x + w/2, comparison["Text in Comments"], w, label="Mentioned in Comments", color="#bf616a")
ax.set_xticks(x)
ax.set_xticklabels(comparison.index, rotation=35, ha="right")
ax.set_ylabel("Count")
ax.set_title("Shape Column vs. Text-Mined Shape Mentions in Comments")
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/06_shape_column_vs_text.png")
plt.close()
print(f"  Saved → {OUTPUT_DIR}/06_shape_column_vs_text.png")

# ════════════════════════════════════════════════════════════════════
# CHART 7 — Bonus: shapes not in the official column but found in text
# ════════════════════════════════════════════════════════════════════

print("\n[Chart 7] Emerging shape terms in text (not standard categories)")

# Look for modern/novel terms in comments
novel_terms = ["tic-tac", "tic tac", "jellyfish", "cube", "pill",
               "crescent", "hexagon", "star-shaped", "donut", "ring-shaped"]

novel_counts = {}
for term in novel_terms:
    novel_counts[term] = comments.str.contains(re.escape(term), regex=True).sum()

novel_series = pd.Series(novel_counts).sort_values(ascending=False)
novel_series = novel_series[novel_series > 0]

fig, ax = plt.subplots(figsize=(8, 5))
novel_series.plot(kind="barh", color="#a3be8c", edgecolor="white", ax=ax)
ax.set_xlabel("Mentions in Comments")
ax.set_title("Emerging / Non-Standard Shape Terms in Sighting Comments")
for i, (val, name) in enumerate(zip(novel_series.values, novel_series.index)):
    ax.text(val + 5, i, str(val), va="center", fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/07_novel_shape_terms.png")
plt.close()
print(f"  Saved → {OUTPUT_DIR}/07_novel_shape_terms.png")

# ════════════════════════════════════════════════════════════════════
# Summary stats for email
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("SUMMARY — Key Findings")
print("=" * 60)
print(f"Total sightings analyzed: {len(df):,}")
print(f"Unique shape categories:  {df['shape'].nunique()}")
print(f"Most common shape:        '{shape_counts.index[0]}' ({shape_counts.iloc[0]:,} sightings)")
print(f"Top 3 shapes account for: {shape_counts.head(3).sum() / len(df) * 100:.1f}% of all reports")
print(f"\nUS sightings: {len(us_df):,}")
print(f"Top shape in most states: '{state_shape_summary.index[0]}' (#{1} in {state_shape_summary.iloc[0]} states)")
print(f"\nText mining found 'tic-tac' mentioned {keyword_counts.get('tic-tac', 0) + keyword_counts.get('tic tac', 0)} times")
print(f"  — despite not being an official shape category")
print(f"\nAll charts saved to: {OUTPUT_DIR}/")
print("=" * 60)
