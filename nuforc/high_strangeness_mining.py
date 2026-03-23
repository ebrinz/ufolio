"""
High Strangeness Text Mining — NUFORC Dataset
===============================================
Mining comments for reports involving:
  1. Consciousness / awareness / telepathy / psychic phenomena
  2. Contact / communication / abduction / encounter
  3. Physical effects (EMF, vehicle interference, physiological)
  4. Time anomalies (missing time, time distortion)
  5. Recurring / repeat witnesses
  6. Multiple witnesses / corroborated sightings
  7. Military / official involvement mentioned
  8. Animal reactions

Filtering approach:
  - Require minimum comment length (filters low-effort posts)
  - Score reports by credibility signals (multiple witnesses, specific
    details, dates/times, lack of hedging language)
  - Flag and exclude stoner/joke indicators
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
df["comments"] = df["comments"].astype(str).str.lower()
df["comment_len"] = df["comments"].str.len()

us = df[df["country"] == "us"].copy()
us = us[us["state"].notna() & (us["state"].str.len() == 2)]

pnw_states = {"wa", "or", "id"}
us["is_pnw"] = us["state"].isin(pnw_states)

total = len(us)
print(f"US records: {total:,}")
print(f"Median comment length: {us['comment_len'].median():.0f} chars")

# ════════════════════════════════════════════════════════════════════
# CREDIBILITY FILTER
# ════════════════════════════════════════════════════════════════════
# We want to surface genuinely interesting reports, not noise.
# Score each report on credibility signals.

print("\n" + "=" * 70)
print("BUILDING CREDIBILITY FILTER")
print("=" * 70)

# Positive signals (add to credibility score)
credibility_patterns = {
    "multiple_witnesses":  r"\b(my (wife|husband|friend|son|daughter|partner|girlfriend|boyfriend)|we (both|all|were)|witness(es)?|companion|passenger|neighbor)\b",
    "specific_time":       r"\b\d{1,2}:\d{2}\s*(am|pm|a\.m|p\.m)?\b",
    "specific_direction":  r"\b(north|south|east|west|northeast|northwest|southeast|southwest|heading|bearing|azimuth)\b",
    "duration_detail":     r"\b(approximately|about|roughly|lasted|duration|seconds|minutes)\b",
    "official_report":     r"\b(police|sheriff|faa|mufon|filed|reported|911|authorities|air force|military)\b",
    "professional":        r"\b(pilot|engineer|officer|professor|scientist|astronomer|doctor|nurse|teacher|military|retired)\b",
    "detailed_description": r"\b(altitude|elevation|degrees|estimated|angular|trajectory|velocity)\b",
}

# Negative signals (subtract from credibility / flag as suspect)
suspect_patterns = {
    "joke_language":    r"\b(lol|lmao|dude|bro|stoned|high|weed|drunk|beer|tripping|hallucin|crazy i know|sounds crazy)\b",
    "vague_hedging":    r"\b(might have been|could have been|probably just|maybe it was just|i guess|not sure if)\b",
    "known_objects":    r"\b(turns out|turned out to be|it was (just|actually|probably) a|later found out|realized it was)\b",
}

for name, pattern in credibility_patterns.items():
    us[f"cred_{name}"] = us["comments"].str.contains(pattern, regex=True).astype(int)

for name, pattern in suspect_patterns.items():
    us[f"sus_{name}"] = us["comments"].str.contains(pattern, regex=True).astype(int)

cred_cols = [c for c in us.columns if c.startswith("cred_")]
sus_cols = [c for c in us.columns if c.startswith("sus_")]

us["credibility"] = us[cred_cols].sum(axis=1) - us[sus_cols].sum(axis=1)

# Minimum bar: comment > 100 chars, credibility >= 0
credible = us[(us["comment_len"] > 100) & (us["credibility"] >= 0)].copy()
print(f"Credible reports (len>100, score>=0): {len(credible):,} / {total:,} ({len(credible)/total*100:.1f}%)")

# ════════════════════════════════════════════════════════════════════
# HIGH STRANGENESS CATEGORIES
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("HIGH STRANGENESS CATEGORIES")
print("=" * 70)

categories = {
    # ── Consciousness / Psi / Telepathy ──
    "telepathy": r"\b(telepath\w*|mental\w* communicat\w*|heard.{0,20}(voice|thought|mind)|psychic|mind.{0,10}(contact|read|link)|thought transfer)\b",
    "awareness_of_observer": r"\b(knew (i|we) (was|were)|aware of (me|us|my)|seemed to (notice|sense|know|react)|respond\w* to (me|us|my)|turned toward|acknowledged)\b",
    "consciousness": r"\b(conscious\w*|altered state|expanded awareness|heightened sense|out of body|astral|transcenden\w*|awakening|kundalini|vibration\w* (rose|increas|felt))\b",
    "compelled_drawn": r"\b(compel\w*|drawn to|felt (compelled|drawn|urged|pulled|called)|irresistible urge|couldn.t look away|transfixed|mesmeriz\w*|hypnoti\w*)\b",
    "dream_vision": r"\b(vivid dream|lucid dream|premonition|vision of|prophetic|precogniti\w*|dream.{0,30}(ufo|craft|ship|alien|being))\b",

    # ── Contact / Encounter ──
    "beings_entities": r"\b(being[s]?|entit\w+|creature[s]?|humanoid|occupant|figure[s]?|silhouette).{0,30}(seen|saw|observed|appeared|emerged|standing|inside|near|beside)\b",
    "communication": r"\b(communicat\w*|message|told (me|us)|spoke|said.{0,20}(to me|to us)|conveyed|impart\w*)\b",
    "abduction": r"\b(abduct\w*|taken aboard|inside.{0,20}(craft|ship|object)|missing time|paralyz\w*|couldn.t move|frozen|levitat\w*|beam\w*.{0,15}(up|light|down))\b",
    "close_encounter": r"\b(close encounter|face to face|within.{0,10}(feet|yards|meters)|hovered (over|above) (me|us|my|our|the house|the car))\b",

    # ── Physical / Physiological Effects ──
    "emf_electrical": r"\b(radio.{0,15}(static|interference|stopped)|tv.{0,10}(static|interference)|power.{0,10}(out|failure|went out)|lights.{0,15}(flickered|dimmed|went out)|compass|electromagnetic|emf|electrical.{0,10}(interference|disturbance))\b",
    "vehicle_effects": r"\b(car.{0,20}(stalled|died|stopped|engine|lights)|engine.{0,15}(died|stopped|stalled|cut)|headlights.{0,10}(dimmed|flickered|went out)|vehicle.{0,15}(malfunction|stopped))\b",
    "physiological": r"\b(headache|nausea|dizzy|dizziness|tingling|burning|skin.{0,10}(burn|red|hot|mark|rash)|hair.{0,10}stood|goosebumps|chills|warmth|heat.{0,10}(from|emanat|felt)|eye.{0,10}(burn|hurt|pain)|sick after|ill after)\b",
    "sound_effects": r"\b(humming|hum\b|buzzing|buzz\b|rumbl\w*|vibrat\w*|low.{0,5}(frequency|pitch|hum|rumble)|infrasound|pulsing sound|throbbing sound|whirring)\b",

    # ── Time Anomalies ──
    "missing_time": r"\b(missing time|lost time|time.{0,10}(gap|loss|missing|unaccounted|skip)|couldn.t account|hours?.{0,10}(missing|gone|lost|disappeared))\b",
    "time_distortion": r"\b(time.{0,15}(slow|stop|stood still|froze|distort|warp|dilat)|slow motion|everything.{0,15}(froze|stopped|still))\b",

    # ── Multiple / Recurring ──
    "repeat_witness": r"\b(not.{0,10}first time|seen.{0,10}before|happened.{0,10}(before|again|previous)|second time|third time|multiple (times|occasions|sighting)|keep seeing|seen.{0,10}(many|several|numerous) times|regular\w* (see|sight|appear))\b",
    "mass_sighting": r"\b(many (people|witness)|crowd|group of (people|us)|everyone|neighborhood|block|community|entire.{0,10}(town|city|neighborhood)|hundreds|dozens|news|newspaper|local.{0,10}(report|news|media))\b",

    # ── Military / Official ──
    "military_present": r"\b(military|jet[s]?.{0,15}(scrambl|follow|intercept|chas)|fighter|f-16|f-15|helicopter[s]?.{0,15}(follow|after|scrambl|appear|show)|base.{0,10}(nearby|close|near)|air force|norad|interceptor)\b",

    # ── Animal Reactions ──
    "animal_reaction": r"\b(dog[s]?.{0,20}(bark|howl|whimper|react|scared|hid|agitat|went crazy|frantic)|cat[s]?.{0,15}(hiss|react|scared|hid|agitat|frantic)|animal[s]?.{0,15}(react|agitat|disturb|scared|silent)|bird[s]?.{0,15}(silent|stop|fled|scatter|quiet)|horse[s]?.{0,15}(spooked|scared|agitat|react))\b",

    # ── Landed / Ground Trace ──
    "landing_trace": r"\b(land\w*.{0,15}(ground|field|yard|road|grass)|ground.{0,15}(mark|burn|scorch|imprint|depress|trace|circle|ring)|crop.{0,10}(circle|ring)|physical.{0,10}(evidence|trace|mark))\b",

    # ── Structured Craft Details (high-quality observation) ──
    "structured_craft": r"\b(window[s]?|port[s]?|dome|panel[s]?|seam[s]?|rivet|antenna|landing.{0,5}(gear|leg|strut)|door|hatch|symbol[s]?|marking[s]?|insignia|writing|hieroglyph)\b",
}

results = []
for cat_name, pattern in categories.items():
    matches = credible["comments"].str.contains(pattern, regex=True)
    count = matches.sum()
    pnw_count = (matches & credible["is_pnw"]).sum()

    # Average credibility score of matching reports
    avg_cred = credible.loc[matches, "credibility"].mean() if count > 0 else 0
    avg_len = credible.loc[matches, "comment_len"].mean() if count > 0 else 0

    pnw_baseline = credible["is_pnw"].mean()
    pnw_rate = pnw_count / count if count > 0 else 0
    pnw_ratio = pnw_rate / pnw_baseline if pnw_baseline > 0 else 0

    results.append({
        "category": cat_name,
        "count": count,
        "pct_of_credible": count / len(credible) * 100,
        "avg_credibility": avg_cred,
        "avg_comment_len": avg_len,
        "pnw_count": pnw_count,
        "pnw_ratio": pnw_ratio,
    })

    # Tag matching reports
    credible.loc[matches, f"hs_{cat_name}"] = True

res_df = pd.DataFrame(results).sort_values("count", ascending=False)

print(f"\n{'Category':<25} {'Count':>6} {'% of DB':>8} {'Avg Cred':>9} {'Avg Len':>8} {'PNW n':>6} {'PNW ratio':>10}")
print("-" * 80)
for _, r in res_df.iterrows():
    print(f"{r['category']:<25} {r['count']:>6} {r['pct_of_credible']:>7.2f}% {r['avg_credibility']:>8.1f} {r['avg_comment_len']:>8.0f} {r['pnw_count']:>6} {r['pnw_ratio']:>9.2f}x")

# ════════════════════════════════════════════════════════════════════
# CHART 1 — High strangeness category prevalence
# ════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(12, 9))

# Group by theme
theme_colors = {
    "telepathy": "#8b5cf6", "awareness_of_observer": "#8b5cf6",
    "consciousness": "#8b5cf6", "compelled_drawn": "#8b5cf6", "dream_vision": "#8b5cf6",
    "beings_entities": "#ec4899", "communication": "#ec4899",
    "abduction": "#ec4899", "close_encounter": "#ec4899",
    "emf_electrical": "#f59e0b", "vehicle_effects": "#f59e0b",
    "physiological": "#f59e0b", "sound_effects": "#f59e0b",
    "missing_time": "#06b6d4", "time_distortion": "#06b6d4",
    "repeat_witness": "#10b981", "mass_sighting": "#10b981",
    "military_present": "#6b7280",
    "animal_reaction": "#84cc16",
    "landing_trace": "#d97706",
    "structured_craft": "#3b82f6",
}

plot_df = res_df.sort_values("count", ascending=True)
colors = [theme_colors.get(c, "#999") for c in plot_df["category"]]

bars = ax.barh(plot_df["category"], plot_df["count"], color=colors, edgecolor="white")
for bar, (_, row) in zip(bars, plot_df.iterrows()):
    ax.text(bar.get_width() + 20, bar.get_y() + bar.get_height()/2,
            f"{row['count']:,}  ({row['pct_of_credible']:.1f}%)", va="center", fontsize=8)

ax.set_xlabel("Number of Credible Reports")
ax.set_title("High Strangeness Categories in NUFORC Reports\n(filtered: comment >100 chars, credibility score ≥ 0)")

# Legend for themes
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#8b5cf6", label="Consciousness / Psi"),
    Patch(facecolor="#ec4899", label="Contact / Encounter"),
    Patch(facecolor="#f59e0b", label="Physical Effects"),
    Patch(facecolor="#06b6d4", label="Time Anomalies"),
    Patch(facecolor="#10b981", label="Multiple/Recurring"),
    Patch(facecolor="#3b82f6", label="Structured Craft"),
    Patch(facecolor="#84cc16", label="Animal Reaction"),
    Patch(facecolor="#6b7280", label="Military"),
    Patch(facecolor="#d97706", label="Landing/Trace"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=9)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/15_high_strangeness_categories.png")
plt.close()
print(f"\n  Saved → {OUTPUT_DIR}/15_high_strangeness_categories.png")

# ════════════════════════════════════════════════════════════════════
# CO-OCCURRENCE — Which categories appear together?
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("CO-OCCURRENCE — Categories that appear together")
print("=" * 70)

hs_cols = [c for c in credible.columns if c.startswith("hs_")]
credible[hs_cols] = credible[hs_cols].fillna(False)

# Count reports with 2+ categories
credible["hs_count"] = credible[hs_cols].sum(axis=1)
multi_hs = credible[credible["hs_count"] >= 2]
print(f"\nReports with 2+ high-strangeness categories: {len(multi_hs):,}")
print(f"Reports with 3+ categories: {(credible['hs_count'] >= 3).sum():,}")
print(f"Reports with 4+ categories: {(credible['hs_count'] >= 4).sum():,}")

# Build co-occurrence matrix
cat_names = [c.replace("hs_", "") for c in hs_cols]
cooccur = np.zeros((len(hs_cols), len(hs_cols)))
for i, col_i in enumerate(hs_cols):
    for j, col_j in enumerate(hs_cols):
        if i != j:
            cooccur[i, j] = (credible[col_i] & credible[col_j]).sum()

cooccur_df = pd.DataFrame(cooccur, index=cat_names, columns=cat_names)

# Top co-occurring pairs
pairs = []
for i in range(len(cat_names)):
    for j in range(i+1, len(cat_names)):
        pairs.append((cat_names[i], cat_names[j], int(cooccur[i,j])))

pairs.sort(key=lambda x: -x[2])
print(f"\n── Top 20 co-occurring pairs ──")
for a, b, count in pairs[:20]:
    print(f"  {a:<25} + {b:<25} = {count:>4}")

# ════════════════════════════════════════════════════════════════════
# CHART 2 — Co-occurrence heatmap
# ════════════════════════════════════════════════════════════════════

# Filter to categories with enough data
active_cats = [c for c in cat_names if credible[f"hs_{c}"].sum() >= 20]
active_cooccur = cooccur_df.loc[active_cats, active_cats]

fig, ax = plt.subplots(figsize=(14, 11))
mask = np.triu(np.ones_like(active_cooccur, dtype=bool), k=0)
sns.heatmap(active_cooccur, mask=mask, annot=True, fmt=".0f", cmap="magma_r",
            linewidths=0.5, ax=ax, cbar_kws={"label": "Co-occurring reports"})
ax.set_title("High Strangeness Co-Occurrence Matrix\n(how often two categories appear in the same report)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/16_cooccurrence_heatmap.png")
plt.close()
print(f"\n  Saved → {OUTPUT_DIR}/16_cooccurrence_heatmap.png")

# ════════════════════════════════════════════════════════════════════
# THE "DEEP END" — Reports with 3+ strangeness categories
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("THE DEEP END — Most multi-category reports (3+ strangeness factors)")
print("=" * 70)

deep = credible[credible["hs_count"] >= 3].copy()
deep = deep.sort_values(["hs_count", "credibility"], ascending=[False, False])

print(f"\n{len(deep)} reports with 3+ strangeness categories\n")

for idx, (_, row) in enumerate(deep.head(15).iterrows()):
    cats_present = [c.replace("hs_", "") for c in hs_cols if row.get(c, False)]
    comment = row["comments"][:300].replace("\n", " ")
    print(f"── Report #{idx+1}  |  state={row['state'].upper()}  |  shape={row['shape']}  |  cred={row['credibility']}")
    print(f"   Categories: {', '.join(cats_present)}")
    print(f"   \"{comment}...\"")
    print()

# ════════════════════════════════════════════════════════════════════
# CONSCIOUSNESS CLUSTER — Deep dive
# ════════════════════════════════════════════════════════════════════

print("=" * 70)
print("CONSCIOUSNESS / PSI CLUSTER — Deep dive")
print("=" * 70)

psi_cats = ["telepathy", "awareness_of_observer", "consciousness",
            "compelled_drawn", "dream_vision"]

psi_mask = credible[[f"hs_{c}" for c in psi_cats]].any(axis=1)
psi_reports = credible[psi_mask].copy()

print(f"\nTotal psi/consciousness reports: {psi_reports.shape[0]}")
print(f"Average credibility score: {psi_reports['credibility'].mean():.2f} (vs overall {credible['credibility'].mean():.2f})")
print(f"Average comment length: {psi_reports['comment_len'].mean():.0f} (vs overall {credible['comment_len'].mean():.0f})")

# What shapes are psi reports associated with?
print(f"\n── Shapes in psi/consciousness reports ──")
psi_shapes = psi_reports["shape"].value_counts().head(10)
baseline_shapes = credible["shape"].value_counts(normalize=True).head(10)
psi_shapes_pct = psi_reports["shape"].value_counts(normalize=True).head(10)

shape_compare = pd.DataFrame({
    "psi_pct": psi_shapes_pct * 100,
    "baseline_pct": baseline_shapes * 100,
}).dropna()
shape_compare["ratio"] = shape_compare["psi_pct"] / shape_compare["baseline_pct"]
print(shape_compare.to_string(float_format=lambda x: f"{x:.1f}"))

# Geographic distribution of psi reports
print(f"\n── Psi reports by state (top 15) ──")
psi_state = psi_reports.groupby("state").size().sort_values(ascending=False)
state_totals = credible.groupby("state").size()
psi_rates = (psi_state / state_totals * 1000).sort_values(ascending=False)
psi_rates_top = psi_rates[state_totals >= 100].head(15)
for state, rate in psi_rates_top.items():
    n = psi_state.get(state, 0)
    print(f"  {state.upper()}: {rate:.1f} per 1000  (n={n})")

# ════════════════════════════════════════════════════════════════════
# CHART 3 — Psi cluster analysis
# ════════════════════════════════════════════════════════════════════

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 3a — Psi subcategory counts
psi_counts = {cat: credible[f"hs_{cat}"].sum() for cat in psi_cats}
psi_series = pd.Series(psi_counts).sort_values()
axes[0,0].barh(psi_series.index, psi_series.values, color="#8b5cf6", edgecolor="white")
axes[0,0].set_title("Consciousness / Psi Subcategories")
axes[0,0].set_xlabel("Number of Reports")
for i, (cat, val) in enumerate(psi_series.items()):
    axes[0,0].text(val + 5, i, str(val), va="center", fontsize=9)

# 3b — Shape distribution in psi reports vs baseline
x = np.arange(len(shape_compare))
w = 0.35
axes[0,1].bar(x - w/2, shape_compare["baseline_pct"], w, label="All reports", color="#b0b0b0")
axes[0,1].bar(x + w/2, shape_compare["psi_pct"], w, label="Psi reports", color="#8b5cf6")
axes[0,1].set_xticks(x)
axes[0,1].set_xticklabels(shape_compare.index, rotation=40, ha="right")
axes[0,1].set_ylabel("% of reports")
axes[0,1].set_title("Shape Distribution: Psi Reports vs. Baseline")
axes[0,1].legend()

# 3c — Psi reports over time
psi_reports["year"] = pd.to_datetime(psi_reports["datetime"], format="mixed", errors="coerce").dt.year
credible["year"] = pd.to_datetime(credible["datetime"], format="mixed", errors="coerce").dt.year

psi_by_year = psi_reports.groupby("year").size()
all_by_year = credible.groupby("year").size()
psi_rate_year = (psi_by_year / all_by_year * 100).dropna()
psi_rate_year = psi_rate_year[(psi_rate_year.index >= 1990) & (psi_rate_year.index <= 2014)]

axes[1,0].plot(psi_rate_year.index, psi_rate_year.values, color="#8b5cf6", lw=2, marker="o", markersize=4)
axes[1,0].fill_between(psi_rate_year.index, psi_rate_year.values, alpha=0.15, color="#8b5cf6")
axes[1,0].set_xlabel("Year")
axes[1,0].set_ylabel("% of reports mentioning psi/consciousness")
axes[1,0].set_title("Psi/Consciousness Mention Rate Over Time")

# 3d — Psi rate by state (top 15, min 100 sightings)
top15_psi = psi_rates[state_totals >= 100].head(15).sort_values()
colors_state = ["#8b5cf6" if s in pnw_states else "#b0b0b0" for s in top15_psi.index]
axes[1,1].barh(top15_psi.index.str.upper(), top15_psi.values, color=colors_state, edgecolor="white")
axes[1,1].set_xlabel("Psi mentions per 1,000 sightings")
axes[1,1].set_title("Psi/Consciousness Rate by State (purple = PNW)")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/17_psi_cluster_analysis.png")
plt.close()
print(f"\n  Saved → {OUTPUT_DIR}/17_psi_cluster_analysis.png")

# ════════════════════════════════════════════════════════════════════
# PHYSICAL EFFECTS CLUSTER
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("PHYSICAL EFFECTS CLUSTER")
print("=" * 70)

phys_cats = ["emf_electrical", "vehicle_effects", "physiological", "sound_effects"]
phys_mask = credible[[f"hs_{c}" for c in phys_cats]].any(axis=1)
phys_reports = credible[phys_mask].copy()

print(f"\nTotal physical-effects reports: {phys_reports.shape[0]}")
print(f"Average credibility: {phys_reports['credibility'].mean():.2f} (vs overall {credible['credibility'].mean():.2f})")

# How often do physical effects co-occur with psi?
both = (psi_mask & phys_mask).sum()
print(f"\nReports with BOTH physical effects AND psi/consciousness: {both}")
print(f"  That's {both / psi_mask.sum() * 100:.1f}% of psi reports also mention physical effects")
print(f"  vs {phys_mask.sum() / len(credible) * 100:.1f}% baseline rate of physical effects")

# ════════════════════════════════════════════════════════════════════
# SAMPLE HIGH-CREDIBILITY PSI + PHYSICAL REPORTS
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("HIGHEST-CREDIBILITY PSI + PHYSICAL EFFECT REPORTS")
print("=" * 70)

both_reports = credible[psi_mask & phys_mask].sort_values("credibility", ascending=False)
for idx, (_, row) in enumerate(both_reports.head(10).iterrows()):
    cats_present = [c.replace("hs_", "") for c in hs_cols if row.get(c, False)]
    comment = row["comments"][:400].replace("\n", " ")
    print(f"\n── Report #{idx+1}  |  {row['state'].upper()}  |  shape={row['shape']}  |  cred={row['credibility']}")
    print(f"   Categories: {', '.join(cats_present)}")
    print(f"   \"{comment}\"")

# ════════════════════════════════════════════════════════════════════
# CHART 4 — Physical effects + strangeness overlap
# ════════════════════════════════════════════════════════════════════

# Venn-style: what % of each category also has physical effects?
overlap_rates = {}
for cat in categories:
    cat_mask = credible.get(f"hs_{cat}", pd.Series(False, index=credible.index)).fillna(False)
    if cat_mask.sum() >= 10:
        overlap = (cat_mask & phys_mask).sum()
        overlap_rates[cat] = overlap / cat_mask.sum() * 100

overlap_series = pd.Series(overlap_rates).sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, 8))
colors_ov = ["#f59e0b" if v > 30 else ("#e0e0e0" if v < 15 else "#fbbf24") for v in overlap_series.values]
ax.barh(overlap_series.index, overlap_series.values, color=colors_ov, edgecolor="white")
ax.axvline(phys_mask.sum() / len(credible) * 100, color="#bf616a", ls="--", lw=1.5,
           label=f"Baseline physical effect rate: {phys_mask.sum()/len(credible)*100:.1f}%")
ax.set_xlabel("% of category that ALSO reports physical effects")
ax.set_title("Physical Effect Co-Occurrence by Strangeness Category\n(do certain experiences correlate with physical symptoms?)")
ax.legend(loc="lower right")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/18_physical_overlap.png")
plt.close()
print(f"\n  Saved → {OUTPUT_DIR}/18_physical_overlap.png")

# ════════════════════════════════════════════════════════════════════
# CHART 5 — Timeline: strangeness categories over the decades
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEMPORAL TRENDS")
print("=" * 70)

key_cats = ["telepathy", "consciousness", "compelled_drawn",
            "beings_entities", "abduction", "missing_time",
            "structured_craft", "animal_reaction", "military_present"]

fig, ax = plt.subplots(figsize=(14, 7))

for cat in key_cats:
    col = f"hs_{cat}"
    if col in credible.columns:
        cat_by_year = credible[credible[col].fillna(False)].groupby("year").size()
        rate = (cat_by_year / all_by_year * 100).dropna()
        rate = rate[(rate.index >= 1990) & (rate.index <= 2014)]
        if len(rate) > 3:
            # Smooth with rolling average
            rate_smooth = rate.rolling(3, center=True, min_periods=1).mean()
            ax.plot(rate_smooth.index, rate_smooth.values, lw=2, label=cat, marker=".", markersize=4)

ax.set_xlabel("Year")
ax.set_ylabel("% of reports in that year")
ax.set_title("High Strangeness Trends Over Time (3-year rolling average)")
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/19_strangeness_timeline.png")
plt.close()
print(f"  Saved → {OUTPUT_DIR}/19_strangeness_timeline.png")

# ════════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("KEY FINDINGS")
print("=" * 70)

any_hs = credible[[f"hs_{c}" for c in categories if f"hs_{c}" in credible.columns]].any(axis=1)
print(f"""
SCALE:
  {any_hs.sum():,} credible reports ({any_hs.sum()/len(credible)*100:.1f}%) contain at least
  one high-strangeness element.

TOP CATEGORIES:
  1. Sound effects (humming/buzzing/vibrating): {res_df.set_index('category').loc['sound_effects','count']:,}
  2. Structured craft details (windows/symbols): {res_df.set_index('category').loc['structured_craft','count']:,}
  3. Compelled/drawn/transfixed:                 {res_df.set_index('category').loc['compelled_drawn','count']:,}
  4. Physiological effects:                      {res_df.set_index('category').loc['physiological','count']:,}
  5. Military presence:                          {res_df.set_index('category').loc['military_present','count']:,}

CONSCIOUSNESS/PSI:
  {psi_mask.sum()} reports mention telepathy, awareness, consciousness,
  being compelled/drawn, or prophetic dreams.
  These reports are LONGER (avg {psi_reports['comment_len'].mean():.0f} vs {credible['comment_len'].mean():.0f} chars)
  and score HIGHER on credibility ({psi_reports['credibility'].mean():.2f} vs {credible['credibility'].mean():.2f}).

PHYSICAL + PSI OVERLAP:
  {both} reports describe BOTH consciousness phenomena AND physical effects.
  Psi reporters are {both/psi_mask.sum()*100:.1f}% likely to also report physical effects
  vs {phys_mask.sum()/len(credible)*100:.1f}% baseline — a {(both/psi_mask.sum()) / (phys_mask.sum()/len(credible)):.1f}x elevation.

MULTI-CATEGORY REPORTS:
  {(credible['hs_count'] >= 3).sum()} reports hit 3+ strangeness categories.
  These are the "deep end" — long, detailed, high-credibility accounts
  that describe multiple correlated anomalous phenomena.
""")
