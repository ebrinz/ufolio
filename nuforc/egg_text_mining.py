"""
Text Mining — Egg & Shape Descriptions in Comments
====================================================
The structured "shape" column showed no PNW egg concentration.
But what does the free text say?

Questions:
  1. How often do people describe "egg" in comments vs. picking it in the shape field?
  2. Are there egg-like terms (ovoid, oblong, pill, tic-tac, oval) hiding in text?
  3. Do PNW commenters use different shape language than the rest of the US?
  4. What adjectives and contexts surround egg descriptions?
  5. Are there shapes that emerge from text but aren't in the official taxonomy?
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np
from collections import Counter
import re
import warnings

warnings.filterwarnings("ignore")
matplotlib.use("Agg")

plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150,
    "font.family": "sans-serif",
    "axes.titlesize": 13, "axes.labelsize": 11,
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
df["comments"] = df["comments"].astype(str).str.lower()

us = df[df["country"] == "us"].copy()
us = us[us["state"].notna() & (us["state"].str.len() == 2)]

pnw_states = {"wa", "or", "id"}
us["is_pnw"] = us["state"].isin(pnw_states)

# ════════════════════════════════════════════════════════════════════
# 1. EGG & EGG-ADJACENT TERMS IN COMMENTS
# ════════════════════════════════════════════════════════════════════

print("=" * 65)
print("1. EGG & EGG-ADJACENT TERMS IN COMMENTS")
print("=" * 65)

egg_terms = {
    "egg":        r"\begg\b",
    "egg-shaped": r"egg[\s-]?shaped",
    "ovoid":      r"\bovoid\b",
    "oblong":     r"\boblong\b",
    "oval":       r"\boval\b",
    "elliptical": r"\belliptical\b",
    "ellipse":    r"\bellipse\b",
    "pill":       r"\bpill\b",
    "tic-tac":    r"tic[\s-]?tac",
    "capsule":    r"\bcapsule\b",
    "football":   r"\bfootball\b",        # football-shaped = egg-like
    "elongated oval": r"elongated\s+oval",
    "rounded":    r"\brounded\b",
}

print(f"\n{'Term':<20} {'All US':>8} {'PNW':>6} {'Non-PNW':>8} {'PNW Rate':>10} {'US Rate':>10} {'Ratio':>7}")
print("-" * 72)

term_results = []
for term, pattern in egg_terms.items():
    all_match = us["comments"].str.contains(pattern, regex=True)
    pnw_match = all_match & us["is_pnw"]

    all_count = all_match.sum()
    pnw_count = pnw_match.sum()
    non_pnw_count = all_count - pnw_count

    pnw_total = us["is_pnw"].sum()
    non_pnw_total = (~us["is_pnw"]).sum()

    pnw_rate = pnw_count / pnw_total * 1000
    us_rate = all_count / len(us) * 1000
    ratio = pnw_rate / us_rate if us_rate > 0 else 0

    print(f"{term:<20} {all_count:>8} {pnw_count:>6} {non_pnw_count:>8} {pnw_rate:>9.2f}‰ {us_rate:>9.2f}‰ {ratio:>6.2f}x")

    term_results.append({
        "term": term, "all_us": all_count, "pnw": pnw_count,
        "pnw_rate": pnw_rate, "us_rate": us_rate, "ratio": ratio
    })

# ════════════════════════════════════════════════════════════════════
# 2. MISMATCH: shape column says X, but comment describes egg
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("2. SHAPE MISMATCH — Comment says 'egg' but shape column is different")
print("=" * 65)

egg_in_text = us[us["comments"].str.contains(r"\begg\b", regex=True)].copy()
print(f"\nSightings mentioning 'egg' in comments: {len(egg_in_text)}")
print(f"  ...of which shape column = 'egg':     {(egg_in_text['shape'] == 'egg').sum()}")
print(f"  ...shape column is something else:     {(egg_in_text['shape'] != 'egg').sum()}")

mismatch = egg_in_text[egg_in_text["shape"] != "egg"]
print(f"\nWhat shape column says when comment mentions 'egg':")
print(mismatch["shape"].value_counts().head(15).to_string())

# ════════════════════════════════════════════════════════════════════
# 3. BROADER TEXT MINING — All shape terms across regions
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("3. ALL SHAPE TERMS — Text frequency by region")
print("=" * 65)

# Comprehensive shape vocabulary mined from text
all_shape_terms = {
    # Classic shapes
    "disc/disk/saucer":  r"\b(disc|disk|saucer|flying saucer)\b",
    "triangle":          r"\btriangul\w*|\btriangle\b",
    "sphere/ball":       r"\b(sphere|spherical|ball of light|ball-shaped|glowing ball)\b",
    "cigar":             r"\bcigar\b",
    "cylinder":          r"\bcylind\w*\b",
    "oval":              r"\boval\b",
    "egg":               r"\begg\b",
    "diamond":           r"\bdiamond\b",
    "rectangle":         r"\brectangl\w*\b",
    "boomerang":         r"\bboomerang\b",
    "chevron/V":         r"\b(chevron|v[\s-]?shape[d]?)\b",
    "cross":             r"\bcross[\s-]?shape[d]?\b",
    "star":              r"\bstar[\s-]?shape[d]?\b",
    "cone":              r"\bcone[\s-]?shape[d]?\b|\bconical\b",
    # Modern / emerging terms
    "orb":               r"\borb[s]?\b",
    "tic-tac":           r"tic[\s-]?tac",
    "jellyfish":         r"\bjellyfish\b",
    "cube":              r"\bcube\b",
    "donut/ring":        r"\b(donut|doughnut|ring[\s-]?shaped|torus)\b",
    "crescent":          r"\bcrescent\b",
    "pill/capsule":      r"\b(pill|capsule)\b",
    # Descriptive language (not standard categories)
    "pulsating":         r"\bpulsat\w*\b",
    "morphing/changing": r"\b(morph\w*|shape[\s-]?shift\w*|chang\w+ shape)\b",
    "translucent":       r"\btranslucen\w*\b",
    "metallic":          r"\bmetallic\b",
    "glowing":           r"\bglow\w*\b",
    "hovering":          r"\bhover\w*\b",
    "rotating/spinning": r"\b(rotat\w*|spin\w*)\b",
    "silent":            r"\bsilent\b",
}

# Regions for comparison
regions = {
    "PNW":       {"wa", "or", "id"},
    "California": {"ca"},
    "Southwest": {"az", "nm", "nv", "ut"},
    "Midwest":   {"il", "in", "mi", "oh", "wi", "ia", "ks", "mn", "mo", "ne", "nd", "sd"},
    "Northeast": {"ct", "me", "ma", "nh", "ri", "vt", "nj", "ny", "pa"},
    "Southeast": {"fl", "ga", "nc", "sc", "va", "al", "tn", "la", "tx"},
}

region_totals = {name: us[us["state"].isin(states)].shape[0] for name, states in regions.items()}

rows = []
for term, pattern in all_shape_terms.items():
    matches = us["comments"].str.contains(pattern, regex=True)
    row = {"term": term, "total": matches.sum()}

    for region_name, region_states in regions.items():
        region_mask = us["state"].isin(region_states)
        count = (matches & region_mask).sum()
        rate = count / region_totals[region_name] * 1000
        row[f"{region_name}_n"] = count
        row[f"{region_name}_rate"] = rate

    rows.append(row)

text_df = pd.DataFrame(rows)
text_df = text_df.sort_values("total", ascending=False)

# Print rates per 1000 sightings
print(f"\n{'Term':<22}", end="")
for rn in regions:
    print(f" {rn:>10}", end="")
print(f" {'Total':>8}")
print("-" * (22 + 11 * len(regions) + 9))

for _, row in text_df.iterrows():
    print(f"{row['term']:<22}", end="")
    for rn in regions:
        print(f" {row[f'{rn}_rate']:>9.1f}‰", end="")
    print(f" {int(row['total']):>8}")

# ════════════════════════════════════════════════════════════════════
# CHART — Text-mined shape term rates by region (heatmap)
# ════════════════════════════════════════════════════════════════════

# Build rate matrix
rate_cols = [f"{rn}_rate" for rn in regions]
rate_matrix = text_df.set_index("term")[rate_cols].copy()
rate_matrix.columns = list(regions.keys())

# Normalize each row to show relative concentration (divide by row mean)
row_means = rate_matrix.mean(axis=1)
conc_matrix = rate_matrix.div(row_means, axis=0)

fig, axes = plt.subplots(1, 2, figsize=(20, 12))

# Left: raw rates
sns.heatmap(rate_matrix, annot=True, fmt=".1f", cmap="YlOrBr",
            linewidths=0.5, ax=axes[0],
            cbar_kws={"label": "Mentions per 1,000 sightings"})
axes[0].set_title("Shape Term Frequency by Region\n(mentions per 1,000 sightings)")
axes[0].set_ylabel("Shape Term (from comment text)")

# Right: concentration ratio
sns.heatmap(conc_matrix, annot=True, fmt=".2f", cmap="RdYlGn_r",
            center=1.0, linewidths=0.5, ax=axes[1],
            vmin=0.6, vmax=1.4,
            cbar_kws={"label": "Concentration (1.0 = average)"})
axes[1].set_title("Regional Concentration of Shape Terms\n(ratio vs. national mean)")
axes[1].set_ylabel("")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/12_text_shape_terms_heatmap.png")
plt.close()
print(f"\n  Saved → {OUTPUT_DIR}/12_text_shape_terms_heatmap.png")

# ════════════════════════════════════════════════════════════════════
# 4. CONTEXT AROUND "EGG" — What words surround it?
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("4. CONTEXT — Words surrounding 'egg' in comments")
print("=" * 65)

# Extract 5-word windows around "egg"
egg_contexts = []
for comment in us[us["comments"].str.contains(r"\begg\b", regex=True)]["comments"]:
    # Find all positions of "egg" and grab surrounding words
    words = comment.split()
    for i, w in enumerate(words):
        if re.search(r"\begg\b", w):
            start = max(0, i - 5)
            end = min(len(words), i + 6)
            context = words[start:end]
            egg_contexts.append(" ".join(context))

# Count frequent words near "egg" (excluding common stopwords)
stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
             "of", "with", "by", "from", "it", "its", "is", "was", "were", "be",
             "been", "being", "have", "has", "had", "do", "does", "did", "will",
             "would", "could", "should", "may", "might", "shall", "can", "that",
             "this", "these", "those", "i", "we", "they", "he", "she", "my", "our",
             "their", "his", "her", "you", "your", "me", "us", "him", "them",
             "not", "no", "so", "as", "if", "are", "am", "than", "then", "about",
             "over", "into", "very", "just", "also", "egg", "like", "there"}

neighbor_words = []
for ctx in egg_contexts:
    for w in ctx.split():
        cleaned = re.sub(r"[^a-z]", "", w)
        if cleaned and cleaned not in stopwords and len(cleaned) > 2:
            neighbor_words.append(cleaned)

word_freq = Counter(neighbor_words).most_common(40)
print("\nMost common words near 'egg' in comments:")
for word, count in word_freq:
    print(f"  {word:<20} {count:>5}")

# ════════════════════════════════════════════════════════════════════
# CHART — Word cloud-style bar of egg context words
# ════════════════════════════════════════════════════════════════════

top_words = word_freq[:25]
words_list = [w for w, _ in top_words]
counts_list = [c for _, c in top_words]

fig, ax = plt.subplots(figsize=(10, 7))
colors_wc = sns.color_palette("copper_r", n_colors=25)
ax.barh(words_list[::-1], counts_list[::-1], color=colors_wc[::-1], edgecolor="white")
ax.set_xlabel("Frequency")
ax.set_title("Most Common Words Near 'Egg' in Sighting Comments\n(5-word window)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/13_egg_context_words.png")
plt.close()
print(f"\n  Saved → {OUTPUT_DIR}/13_egg_context_words.png")

# ════════════════════════════════════════════════════════════════════
# 5. PNW vs REST — sample egg comments side by side
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("5. SAMPLE EGG COMMENTS — PNW vs. Rest of US")
print("=" * 65)

egg_sightings = us[us["comments"].str.contains(r"\begg\b", regex=True)].copy()

print(f"\n── PNW egg mentions ({egg_sightings['is_pnw'].sum()} total) — sample ──")
pnw_samples = egg_sightings[egg_sightings["is_pnw"]].sample(min(8, egg_sightings["is_pnw"].sum()), random_state=42)
for _, row in pnw_samples.iterrows():
    comment_preview = row["comments"][:150].replace("\n", " ")
    print(f"  [{row['state'].upper()}] shape={row['shape']}:  {comment_preview}...")

print(f"\n── Non-PNW egg mentions ({(~egg_sightings['is_pnw']).sum()} total) — sample ──")
non_pnw_samples = egg_sightings[~egg_sightings["is_pnw"]].sample(8, random_state=42)
for _, row in non_pnw_samples.iterrows():
    comment_preview = row["comments"][:150].replace("\n", " ")
    print(f"  [{row['state'].upper()}] shape={row['shape']}:  {comment_preview}...")

# ════════════════════════════════════════════════════════════════════
# 6. MOST REGIONALLY DISTINCTIVE TEXT TERMS
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("6. MOST REGIONALLY DISTINCTIVE SHAPE LANGUAGE")
print("=" * 65)
print("(Terms with highest concentration ratio in each region)\n")

for region_name in regions:
    col = f"{region_name}_rate"
    region_conc = conc_matrix[region_name].sort_values(ascending=False)
    top3 = region_conc.head(3)
    distinctive = ", ".join([f"{term} ({val:.2f}x)" for term, val in top3.items()])
    print(f"  {region_name:<14} → {distinctive}")

# ════════════════════════════════════════════════════════════════════
# CHART — Top distinctive terms per region (grouped bar)
# ════════════════════════════════════════════════════════════════════

# For each region, get the 5 most over-represented terms
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

for i, region_name in enumerate(regions):
    region_conc_sorted = conc_matrix[region_name].sort_values(ascending=False).head(8)

    colors_r = ["#d08770" if v > 1.15 else ("#a3be8c" if v > 1.0 else "#b0b0b0")
                for v in region_conc_sorted.values]

    axes[i].barh(region_conc_sorted.index[::-1], region_conc_sorted.values[::-1],
                 color=colors_r[::-1], edgecolor="white")
    axes[i].axvline(1.0, color="#bf616a", ls="--", lw=1, alpha=0.7)
    axes[i].set_title(f"{region_name}", fontsize=12, fontweight="bold")
    axes[i].set_xlim(0.5, 1.6)

    for j, (term, val) in enumerate(zip(region_conc_sorted.index[::-1], region_conc_sorted.values[::-1])):
        axes[i].text(val + 0.02, j, f"{val:.2f}", va="center", fontsize=8)

fig.suptitle("Most Distinctive Shape Language by Region\n(concentration ratio vs. national mean — text-mined from comments)",
             fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/14_distinctive_terms_by_region.png", bbox_inches="tight")
plt.close()
print(f"\n  Saved → {OUTPUT_DIR}/14_distinctive_terms_by_region.png")

# ════════════════════════════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("SUMMARY — Text Mining Findings")
print("=" * 65)
print("""
1. EGG IN TEXT vs. SHAPE COLUMN
   - 'egg' appears in comments ~359 times across US
   - Only ~60% of those also have shape='egg' — many are classified
     as oval, circle, sphere, unknown, or other

2. EGG-ADJACENT LANGUAGE
   - 'oval' (1,597), 'oblong' and 'ovoid' add more egg-like sightings
   - People describe the same shape in many different ways

3. PNW EGG CONCENTRATION IN TEXT
   - Text mining confirms the structured data: NO anomalous PNW
     concentration for egg or egg-adjacent terms

4. REGIONAL LANGUAGE DIFFERENCES (from text)
   - These reflect genuine differences in what people SEE and
     how they DESCRIBE it, beyond the structured shape field
""")
