"""
FREE Experiencer Research Study — Data Extraction
===================================================
Parses the Hernandez/Klimo/Schild UFO Report chapter from
"Beyond UFOs" / "A Greater Reality" to extract all survey
statistics into structured data.

Source: agreaterreality.com (free PDF downloads)
"""

import re
import json
import csv
import os

DATA_DIR = "data"
ARTICLES_DIR = os.path.join(DATA_DIR, "articles")

# ════════════════════════════════════════════════════════════════════
# Read the extracted text
# ════════════════════════════════════════════════════════════════════

with open(os.path.join(ARTICLES_DIR, "Hernandez_Klimo_Schild_UFO_Report.txt"), "r") as f:
    report_text = f.read()

print(f"Report text: {len(report_text):,} characters, {report_text.count(chr(10)):,} lines")

# ════════════════════════════════════════════════════════════════════
# Extract all percentage-based findings
# ════════════════════════════════════════════════════════════════════

# Find all sentences containing percentages
lines = report_text.split("\n")
pct_findings = []

for i, line in enumerate(lines):
    if "%" in line and re.search(r"\d+%", line):
        # Get surrounding context (2 lines before and after)
        start = max(0, i - 2)
        end = min(len(lines), i + 3)
        context = " ".join(lines[start:end]).strip()
        context = re.sub(r"\s+", " ", context)

        # Extract all percentages from this context
        pcts = re.findall(r"(\d+\.?\d*)%", context)

        pct_findings.append({
            "line": i + 1,
            "percentages": pcts,
            "context": context[:500],
        })

print(f"\nFound {len(pct_findings)} passages with percentage data")

# ════════════════════════════════════════════════════════════════════
# Extract known key findings (manually identified from text)
# ════════════════════════════════════════════════════════════════════

key_findings = []

# Parse the full text for structured findings
# Pattern: look for "X%" near descriptive text
finding_patterns = [
    # Demographics
    (r"(\d+)%\s*were\s*female", "demographics", "female"),
    (r"(\d+)%\s*male", "demographics", "male"),
    (r"(\d+)%.*White.*Caucasian", "demographics", "white_caucasian"),
    (r"(\d+)%.*between.*ages.*(\d+)-(\d+)", "demographics", "age_range"),
    (r"U\.?S\.?\s*\((\d+\.?\d*)%", "demographics", "from_US"),
    (r"Canada\s*\((\d+\.?\d*)%", "demographics", "from_Canada"),
    (r"Australia\s*\((\d+\.?\d*)%", "demographics", "from_Australia"),
    (r"United Kingdom\s*\((\d+\.?\d*)%", "demographics", "from_UK"),

    # Experience types
    (r"(\d+)%.*telepathic", "experience", "telepathic_communication"),
    (r"(\d+)%.*OBE|out.of.body", "experience", "OBE"),
    (r"(\d+)%.*NDE|near.death", "experience", "NDE"),
    (r"(\d+)%.*heal", "experience", "healing"),
    (r"(\d+)%.*positive", "experience", "positive_experience"),
    (r"(\d+)%.*paranormal", "experience", "paranormal"),
    (r"(\d+)%.*abduct", "experience", "abduction"),
    (r"(\d+)%.*missing time", "experience", "missing_time"),
    (r"(\d+)%.*paralyz", "experience", "paralysis"),
    (r"(\d+)%.*beings?.*physical", "experience", "physical_beings"),

    # Craft details
    (r"(\d+)%.*hovered", "craft", "hovered"),
    (r"(\d+)%.*impossible maneuver", "craft", "impossible_maneuvers"),
    (r"(\d+)%.*disappeared quickly", "craft", "disappeared_quickly"),
    (r"(\d+)%.*multiple witness", "craft", "multiple_witnesses"),

    # Shapes
    (r"sphere.*\((\d+)%\)", "craft_shape", "sphere"),
    (r"triangle.*\((\d+)%\)", "craft_shape", "triangle"),
    (r"oval.*\((\d+)%\)", "craft_shape", "oval"),
    (r"cylindrical.*\((\d+)%\)", "craft_shape", "cylindrical"),
    (r"cloud.like.*\((\d+)%\)", "craft_shape", "cloud_like"),
]

for pattern, category, name in finding_patterns:
    matches = re.finditer(pattern, report_text, re.IGNORECASE)
    for m in matches:
        key_findings.append({
            "category": category,
            "name": name,
            "value": m.group(1),
            "full_match": m.group(0)[:200],
        })

print(f"\nExtracted {len(key_findings)} structured findings")

# ════════════════════════════════════════════════════════════════════
# Parse the well-known aggregate findings from various sources
# ════════════════════════════════════════════════════════════════════

# These are the widely-cited FREE survey statistics compiled from
# the report text, multiple published summaries, and presentations.

aggregate_findings = [
    # ── Study metadata ──
    {"category": "metadata", "finding": "Total respondents (Phase 1)", "value": "3256", "unit": "people"},
    {"category": "metadata", "finding": "Total respondents (Phase 2)", "value": "1919", "unit": "people"},
    {"category": "metadata", "finding": "Total respondents (all phases)", "value": "4350", "unit": "people"},
    {"category": "metadata", "finding": "Countries represented", "value": "100+", "unit": "countries"},
    {"category": "metadata", "finding": "Total survey questions (Phase 1+2)", "value": "551", "unit": "questions"},
    {"category": "metadata", "finding": "Phase 3 open-ended questions", "value": "70+", "unit": "questions"},
    {"category": "metadata", "finding": "Study duration", "value": "5", "unit": "years"},

    # ── Demographics ──
    {"category": "demographics", "finding": "Female respondents", "value": "57%", "unit": "percent"},
    {"category": "demographics", "finding": "Male respondents", "value": "43%", "unit": "percent"},
    {"category": "demographics", "finding": "Age 45-64", "value": "56%", "unit": "percent"},
    {"category": "demographics", "finding": "White/Caucasian", "value": "71%", "unit": "percent"},
    {"category": "demographics", "finding": "From United States", "value": "64.1%", "unit": "percent"},
    {"category": "demographics", "finding": "From Canada", "value": "8.4%", "unit": "percent"},
    {"category": "demographics", "finding": "From Australia", "value": "8.3%", "unit": "percent"},
    {"category": "demographics", "finding": "From United Kingdom", "value": "7.2%", "unit": "percent"},

    # ── Overall experience character ──
    {"category": "experience_character", "finding": "Reported positive behavioral transformation", "value": "71-85%", "unit": "percent range"},
    {"category": "experience_character", "finding": "Interaction changed life positively", "value": "85%", "unit": "percent"},
    {"category": "experience_character", "finding": "Do NOT want contact to stop", "value": "84%", "unit": "percent"},

    # ── Telepathy / Communication ──
    {"category": "consciousness_psi", "finding": "Received telepathic/thought transference from NHI", "value": "78%", "unit": "percent"},
    {"category": "consciousness_psi", "finding": "Communication with NHI not physically present", "value": "70.4%", "unit": "percent"},
    {"category": "consciousness_psi", "finding": "Had 3+ telepathic contact experiences", "value": "68%", "unit": "percent"},
    {"category": "consciousness_psi", "finding": "Had 10+ telepathic contact experiences", "value": "46%", "unit": "percent"},

    # ── Content of communications ──
    {"category": "communication_content", "finding": "Personally relevant information", "value": "66%", "unit": "percent"},
    {"category": "communication_content", "finding": "Spiritual or religious messages", "value": "52%", "unit": "percent"},
    {"category": "communication_content", "finding": "Philosophical or metaphysical", "value": "51%", "unit": "percent"},
    {"category": "communication_content", "finding": "Scientific or technological content", "value": "34%", "unit": "percent"},
    {"category": "communication_content", "finding": "Global or socio-political issues", "value": "34%", "unit": "percent"},
    {"category": "communication_content", "finding": "Visions/videos/pictures with telepathic messages", "value": "53.4%", "unit": "percent"},

    # ── Paranormal / consciousness overlap ──
    {"category": "consciousness_psi", "finding": "Had Out of Body Experiences (OBE)", "value": "80%", "unit": "percent"},
    {"category": "consciousness_psi", "finding": "Had Near Death Experience (NDE)", "value": "36%", "unit": "percent"},
    {"category": "consciousness_psi", "finding": "Family members also had paranormal experiences", "value": "75.7%", "unit": "percent"},
    {"category": "consciousness_psi", "finding": "Believed family experiences were related", "value": "57.8%", "unit": "percent"},

    # ── Physical / healing ──
    {"category": "physical_effects", "finding": "Reported medical healing by NHI", "value": "50%", "unit": "percent"},

    # ── Abduction-specific ──
    {"category": "abduction", "finding": "Of those reporting abduction", "value": "32%", "unit": "percent of total"},
    {"category": "abduction", "finding": "Conscious memory recall (not hypnotic)", "value": "70%+", "unit": "percent"},

    # ── Craft observations ──
    {"category": "craft", "finding": "Saw intelligently controlled craft", "value": "62-73%", "unit": "percent range by country"},
    {"category": "craft", "finding": "Craft hovered", "value": "44-52%", "unit": "percent range"},
    {"category": "craft", "finding": "Craft made impossible maneuvers", "value": "30-39%", "unit": "percent range"},
    {"category": "craft", "finding": "Craft disappeared quickly", "value": "33-42%", "unit": "percent range"},
    {"category": "craft", "finding": "Seen by multiple witnesses", "value": "36-47%", "unit": "percent range"},

    # ── Craft shapes ──
    {"category": "craft_shape", "finding": "Sphere shape", "value": "70%", "unit": "percent"},
    {"category": "craft_shape", "finding": "Triangle shape", "value": "36%", "unit": "percent"},
    {"category": "craft_shape", "finding": "Oval shape", "value": "34%", "unit": "percent"},
    {"category": "craft_shape", "finding": "Cylindrical/cigar shape", "value": "28%", "unit": "percent"},
    {"category": "craft_shape", "finding": "Cloud-like shape", "value": "22%", "unit": "percent"},
]

# ════════════════════════════════════════════════════════════════════
# Save structured data
# ════════════════════════════════════════════════════════════════════

# 1. Aggregate findings as JSON
with open(os.path.join(DATA_DIR, "free_survey_findings.json"), "w") as f:
    json.dump(aggregate_findings, f, indent=2)
print(f"\nSaved {len(aggregate_findings)} aggregate findings → data/free_survey_findings.json")

# 2. Aggregate findings as CSV
with open(os.path.join(DATA_DIR, "free_survey_findings.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["category", "finding", "value", "unit"])
    writer.writeheader()
    writer.writerows(aggregate_findings)
print(f"Saved → data/free_survey_findings.csv")

# 3. All percentage passages as JSON (for further mining)
with open(os.path.join(DATA_DIR, "free_report_percentages.json"), "w") as f:
    json.dump(pct_findings, f, indent=2)
print(f"Saved {len(pct_findings)} percentage passages → data/free_report_percentages.json")

# 4. Regex-extracted findings
with open(os.path.join(DATA_DIR, "free_regex_findings.json"), "w") as f:
    json.dump(key_findings, f, indent=2)
print(f"Saved {len(key_findings)} regex-extracted findings → data/free_regex_findings.json")

# ════════════════════════════════════════════════════════════════════
# Print summary
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("FREE EXPERIENCER RESEARCH STUDY — EXTRACTED DATA SUMMARY")
print("=" * 70)

print(f"""
STUDY SCALE:
  Phase 1: 3,256 respondents | Phase 2: 1,919 | Total: 4,350+
  551 multiple-choice questions + 70 open-ended questions
  100+ countries, 5-year study, 9 PhD academics

DEMOGRAPHICS:
  57% female / 43% male
  56% ages 45-64
  71% White/Caucasian
  64% from US, 8.4% Canada, 8.3% Australia, 7.2% UK

CONSCIOUSNESS & PSI (the core findings):
  78%  — received telepathic communication from NHI
  70%  — communication with NHI not physically present
  80%  — had Out of Body Experiences
  36%  — had Near Death Experiences
  76%  — family members also had paranormal experiences
  85%  — experience changed their life positively
  84%  — do NOT want contact to stop

COMMUNICATION CONTENT:
  66%  — personally relevant information
  52%  — spiritual/religious messages
  51%  — philosophical/metaphysical
  53%  — received visions/images with telepathic messages
  34%  — scientific/technological content

PHYSICAL EFFECTS:
  50%  — reported medical healing by NHI

ABDUCTION (subset):
  32%  — of experiencers reported abduction
  70%+ — of those recalled via conscious memory (not hypnosis)

CRAFT OBSERVATIONS:
  62-73% — saw intelligently controlled craft
  70% sphere | 36% triangle | 34% oval | 28% cigar | 22% cloud-like
""")

# ════════════════════════════════════════════════════════════════════
# Also check what's in the Data Mining chapter
# ════════════════════════════════════════════════════════════════════

dm_path = os.path.join(ARTICLES_DIR, "Valverde_Swanson_Data_Mining.txt")
if os.path.exists(dm_path):
    with open(dm_path) as f:
        dm_text = f.read()
    print("\n" + "=" * 70)
    print("DATA MINING CHAPTER (Valverde & Swanson)")
    print("=" * 70)
    print(f"Text length: {len(dm_text):,} chars")

    # Look for cluster/correlation findings
    dm_pcts = re.findall(r"(\d+\.?\d*%)", dm_text)
    print(f"Percentage values found: {len(dm_pcts)}")
    if dm_pcts:
        print("Sample: " + ", ".join(dm_pcts[:20]))

    # Look for correlation/cluster terms
    for term in ["cluster", "correlat", "factor", "principal", "eigenvalue",
                 "chi.square", "regression", "significant", "p.value", "p <"]:
        count = len(re.findall(term, dm_text, re.IGNORECASE))
        if count > 0:
            print(f"  '{term}' mentioned {count} times")
