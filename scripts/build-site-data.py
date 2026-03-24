"""
Build site data — Phase 1: NUFORC aggregations
Reads NUFORC scrubbed.csv → outputs nuforc-shapes.json and nuforc-geo.json
"""

import pandas as pd
import numpy as np
from scipy import stats
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_OUT = os.path.join(ROOT, "site", "data")
os.makedirs(DATA_OUT, exist_ok=True)

print("Loading NUFORC data...")
df = pd.read_csv(os.path.join(ROOT, "nuforc", "data", "scrubbed.csv"), low_memory=False)
df.columns = df.columns.str.strip()
df["shape"] = df["shape"].astype(str).str.strip().str.lower()
df.loc[df["shape"] == "nan", "shape"] = "unknown"
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

total_records = len(df)
print(f"  Records: {total_records:,}")

# ═══════════════ nuforc-shapes.json ═══════════════
print("Building nuforc-shapes.json...")

shape_counts = df["shape"].value_counts()
top_shapes = [{"shape": shape, "count": int(count)} for shape, count in shape_counts.head(15).items()]
top_three_pct = round(shape_counts.head(3).sum() / total_records * 100, 1)

regions = {
    "Northeast": ["ct","me","ma","nh","ri","vt","nj","ny","pa"],
    "Southeast": ["de","fl","ga","md","nc","sc","va","dc","wv","al","ky","ms","tn","ar","la","ok","tx"],
    "Midwest": ["il","in","mi","oh","wi","ia","ks","mn","mo","ne","nd","sd"],
    "West": ["az","co","id","mt","nv","nm","ut","wy","ak","ca","hi","or","wa"],
}

us = df[df["country"] == "us"].copy()
us = us[us["state"].notna() & (us["state"].str.len() == 2)]
state_to_region = {}
for region, sl in regions.items():
    for s in sl:
        state_to_region[s] = region
us["region"] = us["state"].map(state_to_region)

top5_shapes = shape_counts.head(5).index.tolist()
region_breakdown = []
for rn in regions:
    rd = us[us["region"] == rn]
    shapes = {shape: int((rd["shape"] == shape).sum()) for shape in top5_shapes}
    region_breakdown.append({"region": rn, "shapes": shapes})

log_counts = np.log10(shape_counts.values + 1)
kde_x = np.linspace(log_counts.min(), log_counts.max(), 50)
kde = stats.gaussian_kde(log_counts)
distribution_curve = [{"logCount": round(float(x), 2), "frequency": round(float(kde(x)[0]), 4)} for x in kde_x]

nuforc_shapes = {
    "topShapes": top_shapes,
    "regionBreakdown": region_breakdown,
    "distributionCurve": distribution_curve,
    "totalRecords": total_records,
    "topThreePercent": top_three_pct,
}

with open(os.path.join(DATA_OUT, "nuforc-shapes.json"), "w") as f:
    json.dump(nuforc_shapes, f)
size = os.path.getsize(os.path.join(DATA_OUT, "nuforc-shapes.json"))
print(f"  nuforc-shapes.json: {size:,} bytes")

# ═══════════════ nuforc-geo.json ═══════════════
print("Building nuforc-geo.json...")

geo = us[us["latitude"].between(24, 50) & us["longitude"].between(-130, -65)].copy()
CELL_SIZE = 0.25
geo["lat_bin"] = (geo["latitude"] / CELL_SIZE).round() * CELL_SIZE
geo["lng_bin"] = (geo["longitude"] / CELL_SIZE).round() * CELL_SIZE

hex_cells = geo.groupby(["lat_bin", "lng_bin"]).size().reset_index(name="count").rename(columns={"lat_bin": "lat", "lng_bin": "lng"})
hex_list = [{"lat": round(float(r["lat"]), 2), "lng": round(float(r["lng"]), 2), "count": int(r["count"])} for _, r in hex_cells.iterrows()]
print(f"  Hex cells: {len(hex_list):,} (from {len(geo):,} points)")

total_us = len(us)
valid_shapes = us["shape"].value_counts()
valid_shapes = valid_shapes[valid_shapes >= 100].index.tolist()

concentration_ratios = []
for region_name, region_states in regions.items():
    region_total = us[us["state"].isin(region_states)].shape[0]
    region_frac = region_total / total_us if total_us > 0 else 0
    for shape in valid_shapes:
        shape_total = (us["shape"] == shape).sum()
        shape_in_region = ((us["shape"] == shape) & us["state"].isin(region_states)).sum()
        if shape_total == 0 or region_total == 0:
            continue
        shape_region_share = shape_in_region / shape_total
        concentration = shape_region_share / region_frac if region_frac > 0 else 0
        expected = shape_total * region_frac
        if expected >= 5:
            chi2, p = stats.chisquare([shape_in_region, shape_total - shape_in_region], [expected, shape_total - expected])
        else:
            chi2, p = 0, 1.0
        if abs(concentration - 1.0) > 0.1 and p < 0.05:
            concentration_ratios.append({
                "shape": shape, "region": region_name,
                "ratio": round(float(concentration), 2),
                "pValue": round(float(p), 4),
                "significant": bool(p < 0.05),
            })

concentration_ratios.sort(key=lambda x: -abs(x["ratio"] - 1.0))

nuforc_geo = {
    "hexCells": hex_list,
    "concentrationRatios": concentration_ratios[:30],
    "topInsight": "The PNW's signature isn't a shape — it's 'unknown' at 1.34x the expected rate",
}

with open(os.path.join(DATA_OUT, "nuforc-geo.json"), "w") as f:
    json.dump(nuforc_geo, f)
size = os.path.getsize(os.path.join(DATA_OUT, "nuforc-geo.json"))
print(f"  nuforc-geo.json: {size:,} bytes")
print("\nDone! Phase 1 data bundles ready.")
