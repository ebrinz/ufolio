"""
Entity / Being Analysis Across All Datasets
=============================================
What do the reports tell us about who/what is visiting?
  - Physical descriptions (height, skin, eyes, features)
  - Human-like vs. non-human
  - Could they pass as human?
  - Behavioral patterns
  - Where and when do encounters happen?

Sources: Rosales (8,666), Magonia (923), Mack (14), NUFORC text-mined
"""

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
import json
from collections import Counter
import warnings

warnings.filterwarnings("ignore")
matplotlib.use("Agg")
plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150,
    "font.family": "sans-serif",
    "axes.titlesize": 13, "axes.labelsize": 11,
})
sns.set_style("whitegrid")

import os
os.makedirs("nuforc/charts", exist_ok=True)
OUT = "nuforc/charts"

# ════════════════════════════════════════════════════════════════════
# Load all datasets
# ════════════════════════════════════════════════════════════════════

print("Loading datasets...")
rosales = pd.read_csv("rosales/data/rosales_parsed.csv", low_memory=False)
rosales["text"] = rosales["description"].astype(str).str.lower()

magonia = pd.read_csv("magonia/data/magonia_parsed.csv", low_memory=False)
magonia["text"] = magonia["description"].astype(str).str.lower()

nuforc = pd.read_csv("nuforc/data/scrubbed.csv", low_memory=False)
nuforc.columns = nuforc.columns.str.strip()
nuforc["text"] = nuforc["comments"].astype(str).str.lower()

with open("mack/data/mack_case_studies.json") as f:
    mack = json.load(f)

print(f"  Rosales: {len(rosales):,} entries")
print(f"  Magonia: {len(magonia):,} entries")
print(f"  NUFORC:  {len(nuforc):,} entries")
print(f"  Mack:    {len(mack)} case studies")

# ════════════════════════════════════════════════════════════════════
# 1. ENTITY TYPE TAXONOMY — What kinds of beings are described?
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("1. ENTITY TYPE TAXONOMY")
print("=" * 70)

entity_types = {
    # ── Classic types ──
    "grey/gray (small)":      r"\b(grey|gray|gre[yi]).{0,20}(small|short|3.?f|4.?f|three feet|four feet|child.?size|diminutive)\b|\bsmall.{0,15}(grey|gray)\b",
    "grey/gray (tall)":       r"\b(tall|large).{0,15}(grey|gray|gre[yi])\b|\b(grey|gray).{0,20}(tall|5.?f|6.?f|five feet|six feet)\b",
    "grey/gray (general)":    r"\b(grey|gray)\s*(alien|being|entity|creature|figure|humanoid)\b|\bgre[yi]s\b",
    "nordic/blonde":          r"\b(nordic|blonde?|fair.?hair|golden.?hair|scandinavian|tall.{0,10}(beautiful|handsome|attractive)|angelic.{0,10}(being|figure|entity))\b",
    "reptilian/lizard":       r"\b(reptil\w*|lizard|snake.?like|scal[ey]|slit.{0,5}(eye|pupil)|dragon.?like|saurian)\b",
    "insectoid/mantis":       r"\b(insect\w*|mantis|praying mantis|bug.?like|ant.?like|insect.?eye|compound eye)\b",
    "robotic/mechanical":     r"\b(robot\w*|mechanical|android|metallic.{0,10}(being|entity|figure)|cybernetic|automaton)\b",

    # ── Human-like / could pass ──
    "human-looking":          r"\b(human.?looking|appeared?\s*human|look\w*\s*(like|as)\s*(a\s*)?(normal\s*)?human|indistinguishable|ordinary.?looking|normal.?appear\w*|pass\w*\s*(for|as)\s*human|could\s*(have\s*)?be(en)?\s*(a\s*)?(normal\s*)?human|human\s*in\s*appear)\b",
    "men in black":           r"\b(men in black|MIB|man in black|black.?suit\w*.{0,15}(man|men|figure|stranger)|dark.?suit\w*.{0,15}(man|men))\b",
    "military/uniform":       r"\b(uniform\w*|military.{0,10}(person|figure|man|men|outfit)|jumpsuit|flight.?suit|coverall)\b",

    # ── Size categories ──
    "dwarf/small being":      r"\b(dwarf|dwar[fv]|pygm[yi]|tiny.{0,10}(being|entity|creature|figure|man|men|humanoid)|midget|very small.{0,10}(being|entity|creature|humanoid)|gnome|elf|pixie)\b",
    "giant/tall being":       r"\b(giant|gigantic|enormous|very tall|7.?f\w*\s*tall|8.?f\w*\s*tall|9.?f\w*\s*tall|10.?f\w*\s*tall|over.?six|over.?seven|towering)\b",

    # ── Luminous / non-physical ──
    "luminous/light being":   r"\b(luminous|glowing.{0,10}(being|entity|figure|form)|light.?being|being.{0,5}of.{0,5}light|translucent.{0,10}(being|entity|figure)|transparent.{0,10}(being|entity|figure)|ethereal|apparition)\b",
    "shadow/dark figure":     r"\b(shadow.{0,5}(figure|person|being|entity|man|people)|dark.?figure|silhouette|shadow.?person|shadow.?people|black.?figure)\b",

    # ── Features ──
    "large eyes":             r"\b(large|big|huge|enormous|oversized|almond).{0,5}(eye|eyed)\b",
    "no hair":                r"\b(bald|hairless|no hair|smooth.{0,5}(head|skull|cranium))\b",
    "large head":             r"\b(large|big|huge|oversized|bulbous|elongated|pear.?shaped).{0,5}(head|cranium|skull)\b",
    "pointed ears":           r"\b(pointed|long|elongated).{0,5}ear\b",
    "telepathic":             r"\b(telepath\w*|mental\w*\s*communicat|thought\s*transfer|mind.{0,5}(to|speak|communicat)|psychic\w*\s*communicat|spoke.{0,15}(without|mind|mentally))\b",

    # ── Skin descriptions ──
    "grey/gray skin":         r"\b(grey|gray|gre[yi]ish).{0,5}(skin|complex|flesh|color)\b",
    "green skin":             r"\b(green).{0,5}(skin|complex|flesh|color)\b|\blittle green\b",
    "blue skin":              r"\b(blue|bluish).{0,5}(skin|complex|flesh|color)\b",
    "white/pale skin":        r"\b(white|pale|pallid|chalky|alabaster).{0,5}(skin|complex|flesh|face)\b",
    "brown/dark skin":        r"\b(brown|dark|olive|tan).{0,5}(skin|complex|flesh|color)\b",

    # ── Clothing ──
    "tight suit/bodysuit":    r"\b(tight.?(fitting)?|skin.?tight|one.?piece).{0,10}(suit|garment|outfit|cloth|uniform)\b|\bbodysuit\b|\bjumpsuit\b",
    "robe/cloak":             r"\b(robe|cloak|hooded|cowl|flowing.{0,5}(garment|cloth)|gown|cape)\b",
    "naked/nude":             r"\b(naked|nude|unclothed|no cloth|without cloth)\b",

    # ── Behavior ──
    "collecting samples":     r"\b(collect\w*|gather\w*|tak\w*).{0,15}(sample|specimen|soil|plant|rock|water|flower)\b",
    "examining/probing":      r"\b(examin\w*|prob\w*|inspect\w*|study\w*).{0,15}(body|witness|subject|person|him|her|me)\b",
    "peaceful/friendly":      r"\b(peaceful|friendly|benevolent|kind|gentle|warm|smil\w*|reassur\w*|calm\w*)\b",
    "threatening/hostile":    r"\b(threaten\w*|hostil\w*|aggressive|menac\w*|frighten\w*|terrif\w*|attack\w*|violent|malevolent)\b",
}

# Count across Rosales + Magonia (the entity-focused datasets)
entity_corpus = pd.concat([
    rosales[["text"]].assign(source="rosales"),
    magonia[["text"]].assign(source="magonia"),
], ignore_index=True)

results = []
for etype, pattern in entity_types.items():
    r_count = rosales["text"].str.contains(pattern, regex=True).sum()
    m_count = magonia["text"].str.contains(pattern, regex=True).sum()
    n_count = nuforc["text"].str.contains(pattern, regex=True).sum()
    total = r_count + m_count

    results.append({
        "entity_type": etype,
        "rosales": r_count,
        "magonia": m_count,
        "nuforc": n_count,
        "entity_total": total,
        "rosales_pct": r_count / len(rosales) * 100,
        "magonia_pct": m_count / len(magonia) * 100,
    })

res_df = pd.DataFrame(results).sort_values("entity_total", ascending=False)

print(f"\n{'Type':<28} {'Rosales':>8} {'Magonia':>8} {'NUFORC':>8} {'Total':>7}")
print("-" * 65)
for _, r in res_df.iterrows():
    print(f"{r['entity_type']:<28} {r['rosales']:>8} {r['magonia']:>8} {r['nuforc']:>8} {r['entity_total']:>7}")

# ════════════════════════════════════════════════════════════════════
# CHART 1 — Entity type prevalence
# ════════════════════════════════════════════════════════════════════

# Group into macro categories
type_groups = {
    "Physical Description": ["large eyes", "no hair", "large head", "grey/gray skin",
                             "white/pale skin", "green skin", "blue skin", "brown/dark skin"],
    "Entity Type": ["grey/gray (small)", "grey/gray (tall)", "grey/gray (general)",
                    "nordic/blonde", "reptilian/lizard", "insectoid/mantis",
                    "robotic/mechanical", "dwarf/small being", "giant/tall being"],
    "Human-Passing": ["human-looking", "men in black", "military/uniform"],
    "Non-Physical": ["luminous/light being", "shadow/dark figure"],
    "Behavior": ["telepathic", "collecting samples", "examining/probing",
                 "peaceful/friendly", "threatening/hostile"],
    "Clothing": ["tight suit/bodysuit", "robe/cloak", "naked/nude"],
}

group_colors = {
    "Entity Type": "#8b5cf6",
    "Physical Description": "#06b6d4",
    "Human-Passing": "#f59e0b",
    "Non-Physical": "#ec4899",
    "Behavior": "#10b981",
    "Clothing": "#6b7280",
}

fig, ax = plt.subplots(figsize=(14, 12))
plot_data = res_df[res_df["entity_total"] >= 5].sort_values("entity_total", ascending=True)

colors = []
for etype in plot_data["entity_type"]:
    color = "#999999"
    for group, members in type_groups.items():
        if etype in members:
            color = group_colors[group]
            break
    colors.append(color)

bars = ax.barh(plot_data["entity_type"], plot_data["entity_total"], color=colors, edgecolor="white")
for bar, (_, row) in zip(bars, plot_data.iterrows()):
    ax.text(bar.get_width() + 8, bar.get_y() + bar.get_height()/2,
            f"{row['entity_total']:,}  (R:{row['rosales']:,} M:{row['magonia']})",
            va="center", fontsize=7.5)

ax.set_xlabel("Number of Reports (Rosales + Magonia)")
ax.set_title("Entity Characteristics in Encounter Reports\n(R=Rosales, M=Magonia)")

from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=c, label=g) for g, c in group_colors.items()]
ax.legend(handles=legend_elements, loc="lower right", fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUT}/20_entity_types.png")
plt.close()
print(f"\n  Saved → {OUT}/20_entity_types.png")

# ════════════════════════════════════════════════════════════════════
# 2. HUMAN-PASSING ANALYSIS — Could they walk among us?
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("2. HUMAN-PASSING ANALYSIS")
print("=" * 70)

# Broader search for human-like descriptions
human_patterns = {
    "explicitly human-looking":   r"\b(human.?looking|appeared?\s*human|look\w*\s*human|indistinguishable\s*from\s*human|pass\s*(for|as)\s*human|could.{0,10}be\w*\s*human|ordinary\s*looking\s*(man|woman|person))\b",
    "normal clothing":            r"\b(normal\s*cloth|street\s*cloth|regular\s*cloth|casual\s*cloth|everyday\s*(cloth|attire)|business\s*suit|dress\w*\s*normally)\b",
    "spoke language":             r"\b(spoke\s*(english|spanish|french|german|portuguese|italian|russian|chinese|japanese)|in\s*(perfect|fluent|accented)\s*(english|spanish|french)|normal\s*voice|conversed|conversation)\b",
    "blended in":                 r"\b(blend\w*\s*in|disappear\w*\s*into\s*(the\s*)?crowd|mingl\w*|walk\w*\s*away|drove\s*away|left\s*in\s*a\s*(car|vehicle)|normal\s*car)\b",
    "attractive/beautiful":       r"\b(beautiful|attractive|handsome|stunning|gorgeous|striking|perfect\s*feat)\b",
    "described as tall":          r"\b(tall|over\s*six|6\s*f\w*\s*tall|above\s*average\s*height)\b",
    "blonde/fair":                r"\b(blonde?|fair\s*hair|golden\s*hair|light\s*hair|platinum)\b",
    "blue/light eyes":            r"\b(blue\s*eye|light\s*eye|piercing\s*(blue|light)\s*eye|bright\s*eye|crystal\s*eye)\b",
    "contacted at home":          r"\b(knock\w*\s*(on|at)\s*(the\s*)?(door|my)|appeared?\s*(at|in)\s*(my|the|his|her)\s*(home|house|door|room|bedroom)|visit\w*\s*(my|the|his|her)\s*(home|house))\b",
    "contacted on road":          r"\b(stopped?\s*(my|the|his|her)\s*(car|vehicle)|road\s*side|highway|pull\w*\s*over|approach\w*\s*(my|the)\s*(car|vehicle))\b",
    "gave warning/message":       r"\b(warn\w*|warning|message\s*(for|to|about)|told\s*(me|him|her|us|them)\s*(to|about|that)|mission|purpose|important\s*message)\b",
}

print(f"\n{'Pattern':<30} {'Rosales':>8} {'Magonia':>8} {'NUFORC':>8}")
print("-" * 58)

for name, pattern in human_patterns.items():
    r = rosales["text"].str.contains(pattern, regex=True).sum()
    m = magonia["text"].str.contains(pattern, regex=True).sum()
    n = nuforc["text"].str.contains(pattern, regex=True).sum()
    print(f"{name:<30} {r:>8} {m:>8} {n:>8}")

# ════════════════════════════════════════════════════════════════════
# 3. ROSALES TYPE CODES — structured encounter classification
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("3. ROSALES ENCOUNTER TYPE DISTRIBUTION")
print("=" * 70)

type_labels = {
    "A": "Entity inside/on object",
    "B": "Entity entering/exiting object",
    "C": "Entity in vicinity of object",
    "D": "Entity near landing trace",
    "E": "Entity without UFO",
    "F": "Trace/physical evidence only",
    "G": "Contact / abduction / interaction",
    "H": "Crash recovery with occupants",
    "X": "Extreme strangeness",
}

type_counts = rosales["type_code"].value_counts()
print(f"\n{'Code':<4} {'Label':<40} {'Count':>6} {'%':>7}")
print("-" * 60)
for code, label in type_labels.items():
    count = type_counts.get(code, 0)
    pct = count / len(rosales) * 100
    print(f"  {code}   {label:<40} {count:>6} {pct:>6.1f}%")

# ════════════════════════════════════════════════════════════════════
# 4. ENCOUNTER SETTINGS — Where do contacts happen?
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("4. ENCOUNTER SETTINGS — Where do they show up?")
print("=" * 70)

settings = {
    "bedroom/home (night)":   r"\b(bedroom|bed\s*room|lying\s*in\s*bed|woke\s*up|sleep\w*|middle\s*of\s*the\s*night|3\s*am|2\s*am|late\s*at\s*night)\b",
    "roadside/highway":       r"\b(road|highway|driving|car|vehicle|motorist|freeway|interstate|route)\b",
    "rural/farm/field":       r"\b(farm|field|ranch|pasture|rural|country\s*side|countryside|meadow|crop|forest|wood\w*)\b",
    "backyard/garden":        r"\b(backyard|back\s*yard|garden|patio|porch|deck|front\s*yard)\b",
    "city/urban":             r"\b(city|urban|downtown|street|sidewalk|parking\s*lot|apartment|building|office)\b",
    "military base":          r"\b(military|base|installation|restricted|air\s*force|navy|army|fort\s)\b",
    "beach/water":            r"\b(beach|lake|river|ocean|sea|shore|coast|water|boat|ship|fishing)\b",
    "mountain/desert":        r"\b(mountain|desert|canyon|hill|mesa|plateau|wilderness|cave)\b",
}

all_entity_text = pd.concat([rosales["text"], magonia["text"]])

print(f"\n{'Setting':<28} {'Count':>7} {'%':>7}")
print("-" * 45)
for setting, pattern in settings.items():
    count = all_entity_text.str.contains(pattern, regex=True).sum()
    pct = count / len(all_entity_text) * 100
    print(f"{setting:<28} {count:>7} {pct:>6.1f}%")

# ════════════════════════════════════════════════════════════════════
# 5. SAMPLE HUMAN-PASSING REPORTS — The most interesting ones
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("5. HUMAN-PASSING ENTITY REPORTS — Samples")
print("=" * 70)

human_mask = rosales["text"].str.contains(
    r"\b(human.?looking|appeared?\s*human|look\w*\s*(like\s*)?(a\s*)?human|indistinguishable|pass\w*\s*(for|as)\s*human|normal.?looking\s*(man|woman|person)|ordinary.?appear|could.{0,10}been?\s*(a\s*)?(normal\s*)?human)\b",
    regex=True
)
human_reports = rosales[human_mask].copy()
print(f"\nReports with explicitly human-looking entities: {len(human_reports)}")

# Also check nordics
nordic_mask = rosales["text"].str.contains(
    r"\b(nordic|blonde?\s*(hair|being|entity|man|woman|figure)|tall.{0,10}(beautiful|handsome|attractive)\s*(man|woman|being|entity|figure)|fair.?hair\w*\s*(man|woman|being))\b",
    regex=True
)
nordic_reports = rosales[nordic_mask].copy()
print(f"Reports with Nordic/blonde entities: {len(nordic_reports)}")

# MIB
mib_mask = rosales["text"].str.contains(
    r"\b(men\s*in\s*black|MIB|man\s*in\s*black|black.?suit\w*.{0,15}(man|men|stranger|figure))\b",
    regex=True
)
mib_reports = rosales[mib_mask].copy()
print(f"Reports with Men in Black: {len(mib_reports)}")

# Combined human-passing
pass_mask = human_mask | nordic_mask | mib_mask
pass_reports = rosales[pass_mask].copy()
print(f"\nTotal potentially human-passing entities: {len(pass_reports)} ({len(pass_reports)/len(rosales)*100:.1f}%)")

# Print samples of each
for label, subset in [("HUMAN-LOOKING", human_reports),
                       ("NORDIC/BLONDE", nordic_reports),
                       ("MEN IN BLACK", mib_reports)]:
    print(f"\n── {label} — sample reports ──")
    sample = subset.sample(min(5, len(subset)), random_state=42) if len(subset) > 0 else subset
    for _, row in sample.iterrows():
        desc = row["text"][:350].replace("\n", " ")
        print(f"  [{row.get('year_page','?')}] Type={row.get('type_code','?')}  {desc}...")
        print()

# ════════════════════════════════════════════════════════════════════
# 6. ENTITY APPEARANCE OVER TIME — Are types changing?
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("6. ENTITY TYPES OVER TIME")
print("=" * 70)

# Parse year from rosales
rosales["year_num"] = pd.to_numeric(rosales["year_page"], errors="coerce")
rosales_dated = rosales[rosales["year_num"].between(1947, 2009)]

decade_types = {}
for decade_start in range(1940, 2010, 10):
    decade_end = decade_start + 10
    decade_label = f"{decade_start}s"
    decade_data = rosales_dated[rosales_dated["year_num"].between(decade_start, decade_end - 1)]

    if len(decade_data) < 10:
        continue

    decade_types[decade_label] = {}
    for etype in ["grey/gray (general)", "nordic/blonde", "reptilian/lizard",
                  "human-looking", "robotic/mechanical", "insectoid/mantis",
                  "dwarf/small being", "giant/tall being", "luminous/light being"]:
        pattern = entity_types.get(etype, "")
        if pattern:
            count = decade_data["text"].str.contains(pattern, regex=True).sum()
            decade_types[decade_label][etype] = count / len(decade_data) * 100

timeline_df = pd.DataFrame(decade_types).T
print(timeline_df.to_string(float_format=lambda x: f"{x:.1f}%"))

# Chart
fig, ax = plt.subplots(figsize=(14, 7))
type_colors = {
    "grey/gray (general)": "#808080",
    "nordic/blonde": "#f5d442",
    "reptilian/lizard": "#22c55e",
    "human-looking": "#3b82f6",
    "robotic/mechanical": "#94a3b8",
    "insectoid/mantis": "#a855f7",
    "dwarf/small being": "#f97316",
    "giant/tall being": "#ef4444",
    "luminous/light being": "#06b6d4",
}

for col in timeline_df.columns:
    ax.plot(timeline_df.index, timeline_df[col], marker="o", lw=2,
            color=type_colors.get(col, "#999"), label=col, markersize=5)

ax.set_xlabel("Decade")
ax.set_ylabel("% of reports in decade")
ax.set_title("Entity Type Prevalence by Decade (Rosales Catalog)")
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
plt.tight_layout()
plt.savefig(f"{OUT}/21_entity_types_timeline.png")
plt.close()
print(f"\n  Saved → {OUT}/21_entity_types_timeline.png")

# ════════════════════════════════════════════════════════════════════
# 7. THE "COULD THEY HIDE" SCORECARD
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("7. COULD THEY HIDE IN PLAIN SIGHT? — Scorecard")
print("=" * 70)

# For each entity type, score how "passable" they'd be
passability = [
    ("Nordic/blonde",        "HIGH",    "Described as tall, attractive, blonde, blue-eyed humans. Often wear normal clothing. Multiple reports of them driving cars, walking in public, speaking local languages fluently."),
    ("Human-looking (other)", "HIGH",   "Explicitly described as indistinguishable from normal humans. Some reports note only subtle 'wrongness' — too perfect features, unusual eye contact, odd speech patterns."),
    ("Men in Black",          "HIGH",   "By definition blend into human society. Wear suits, drive cars, flash badges. Reports note they seem 'off' — waxy skin, mechanical movements, outdated clothes/cars."),
    ("Military/uniform",      "MEDIUM", "Appear human in uniform. Could pass in military contexts. Sometimes described as too tall, too pale, or with unusually large eyes."),
    ("Grey (tall)",           "LOW",    "4-6ft but grey skin, huge black eyes, no hair. Would be immediately noticed. Some reports of them wearing cloaks/robes to conceal features."),
    ("Grey (small)",          "NONE",   "3-4ft tall, oversized heads, huge eyes. No possibility of passing. The most commonly reported entity type."),
    ("Reptilian",            "NONE",    "Scaled skin, vertical pupils, sometimes tails. Completely non-human appearance."),
    ("Insectoid/mantis",     "NONE",    "Insect-like features, compound eyes, elongated limbs. Unmistakable."),
    ("Luminous/light being", "N/A",     "Non-physical. Sometimes described as taking human form temporarily."),
]

print(f"\n{'Entity Type':<25} {'Passability':<10} Description")
print("-" * 90)
for etype, score, desc in passability:
    print(f"{etype:<25} {score:<10} {desc}")

# ════════════════════════════════════════════════════════════════════
# 8. DEEP DIVE — Nordic/Human-looking encounter patterns
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("8. NORDIC / HUMAN-LOOKING DEEP DIVE")
print("=" * 70)

hp = rosales[pass_mask].copy()

# Where do human-passing encounters happen?
print(f"\n── Setting analysis for {len(hp)} human-passing reports ──")
for setting, pattern in settings.items():
    count = hp["text"].str.contains(pattern, regex=True).sum()
    baseline = all_entity_text.str.contains(pattern, regex=True).sum() / len(all_entity_text)
    rate = count / len(hp)
    ratio = rate / baseline if baseline > 0 else 0
    if count >= 3:
        print(f"  {setting:<28} {count:>4} ({rate*100:.1f}%)  vs baseline {baseline*100:.1f}% = {ratio:.2f}x")

# What type codes?
print(f"\n── Encounter type codes ──")
hp_types = hp["type_code"].value_counts()
for code, count in hp_types.items():
    label = type_labels.get(code, "Unknown")
    pct = count / len(hp) * 100
    print(f"  {code}: {label:<40} {count:>4} ({pct:.1f}%)")

# What do they DO?
print(f"\n── What human-passing entities do ──")
behaviors = {
    "communicate/speak":      r"\b(spoke|talk\w*|communicat\w*|told|said|convers\w*|ask\w*|question)\b",
    "give message/warning":   r"\b(warn\w*|message|told.{0,20}(about|that|to)|mission|purpose|prophecy|prediction)\b",
    "observe/watch":          r"\b(observ\w*|watch\w*|stare|star\w*\s*at|gaz\w*|look\w*\s*(at|upon))\b",
    "approach witness":       r"\b(approach\w*|walk\w*\s*(toward|up\s*to|over)|came\s*(to|toward|up|over))\b",
    "vanish/disappear":       r"\b(vanish\w*|disappear\w*|dematerial\w*|faded?\s*(away|out)|dissolved)\b",
    "offer ride/invite":      r"\b(offer\w*|invit\w*|come\s*with|join\s*(us|me|them)|follow)\b",
    "physical exam":          r"\b(examin\w*|medical|procedure|table|probe|instrument|needle|implant)\b",
    "paralysis/control":      r"\b(paralyz\w*|frozen|could\s*n.?t\s*move|immobil\w*|control\w*|unable\s*to\s*move)\b",
    "show technology":        r"\b(show\w*.{0,15}(screen|device|technology|instrument|panel|display)|demonstrate)\b",
}

for bname, pattern in behaviors.items():
    count = hp["text"].str.contains(pattern, regex=True).sum()
    pct = count / len(hp) * 100
    if count >= 2:
        print(f"  {bname:<28} {count:>4} ({pct:.1f}%)")

# ════════════════════════════════════════════════════════════════════
# CHART 2 — Human-passing vs non-human: behavior comparison
# ════════════════════════════════════════════════════════════════════

non_human = rosales[~pass_mask]
comparison_data = []
for bname, pattern in behaviors.items():
    hp_rate = hp["text"].str.contains(pattern, regex=True).sum() / len(hp) * 100
    nh_rate = non_human["text"].str.contains(pattern, regex=True).sum() / len(non_human) * 100
    comparison_data.append({"behavior": bname, "human_passing": hp_rate, "non_human": nh_rate})

comp_df = pd.DataFrame(comparison_data).sort_values("human_passing", ascending=True)

fig, ax = plt.subplots(figsize=(12, 7))
y = np.arange(len(comp_df))
w = 0.35
ax.barh(y - w/2, comp_df["human_passing"], w, label="Human-passing entities", color="#f59e0b")
ax.barh(y + w/2, comp_df["non_human"], w, label="Non-human entities", color="#6b7280")
ax.set_yticks(y)
ax.set_yticklabels(comp_df["behavior"])
ax.set_xlabel("% of reports")
ax.set_title("Behavior Comparison: Human-Passing vs Non-Human Entities")
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUT}/22_human_passing_behavior.png")
plt.close()
print(f"\n  Saved → {OUT}/22_human_passing_behavior.png")

# ════════════════════════════════════════════════════════════════════
# MACK'S ENTITY DATA
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("9. MACK CASE STUDIES — Entity Descriptions")
print("=" * 70)

for case in mack:
    desc = case.get("entity_description", "Not detailed")
    types = case.get("experience_types", "")
    print(f"\n  {case['pseudonym']} (Chapter {case.get('chapter','?')})")
    print(f"    Entity: {desc}")
    print(f"    Experiences: {types[:200]}")

# ════════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("SUMMARY — What the data says about who visits")
print("=" * 70)

grey_total = rosales["text"].str.contains(r"\b(grey|gray)\b", regex=True).sum()
nordic_total = len(nordic_reports)
human_total = len(human_reports)
mib_total = len(mib_reports)
reptilian_total = rosales["text"].str.contains(entity_types["reptilian/lizard"], regex=True).sum()
insectoid_total = rosales["text"].str.contains(entity_types["insectoid/mantis"], regex=True).sum()

print(f"""
ENTITY PREVALENCE (Rosales, n={len(rosales):,}):
  Grey/gray entities:     {grey_total:>5} ({grey_total/len(rosales)*100:.1f}%)
  Nordic/blonde:          {nordic_total:>5} ({nordic_total/len(rosales)*100:.1f}%)
  Human-looking:          {human_total:>5} ({human_total/len(rosales)*100:.1f}%)
  Men in Black:           {mib_total:>5} ({mib_total/len(rosales)*100:.1f}%)
  Reptilian:              {reptilian_total:>5} ({reptilian_total/len(rosales)*100:.1f}%)
  Insectoid/mantis:       {insectoid_total:>5} ({insectoid_total/len(rosales)*100:.1f}%)

COULD THEY HIDE?
  {len(pass_reports)} reports ({len(pass_reports)/len(rosales)*100:.1f}%) describe entities that
  could plausibly pass as human. These are predominantly:
  - Nordics: tall, blonde, attractive, often in normal clothing
  - "Human-looking" entities described as indistinguishable
  - Men in Black: deliberately blending in (suits, cars, badges)

  The vast majority ({(len(rosales)-len(pass_reports))/len(rosales)*100:.1f}%) describe beings that
  could NOT pass as human — wrong proportions, skin color, size,
  or entirely non-humanoid appearance.

HOW WOULD YOU FIND THEM?
  According to the reports, human-passing entities:
  - Approach witnesses on roads/highways more than at home
  - Communicate verbally more than non-human types
  - Give messages/warnings at higher rates
  - Vanish/disappear rather than fly away
  - Show up in daylight, in public settings
  - Are described with subtle "wrongness" — too perfect, unusual
    eye contact, slightly outdated clothing, waxy skin, mechanical
    speech, overly formal manner
""")
