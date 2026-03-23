#!/usr/bin/env python3
"""Parse the Vallee Magonia database JSON into a clean CSV."""

import json
import csv
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
RAW_JSON = DATA_DIR / "magonia_raw.json"
OUTPUT_CSV = DATA_DIR / "magonia_parsed.csv"

# Country extraction: map common location suffixes/keywords to countries
COUNTRY_PATTERNS = [
    # Explicit country names (order matters — check longer/more specific first)
    (r'\bUnited States\b', 'United States'),
    (r'\bGreat Britain\b', 'United Kingdom'),
    (r'\bEngland\b', 'United Kingdom'),
    (r'\bScotland\b', 'United Kingdom'),
    (r'\bWales\b', 'United Kingdom'),
    (r'\bNorthern Ireland\b', 'United Kingdom'),
    (r'\bSoviet Union\b', 'Soviet Union'),
    (r'\bNew Zealand\b', 'New Zealand'),
    (r'\bSouth Africa\b', 'South Africa'),
    (r'\bPapua\b', 'Papua New Guinea'),
    (r'\bNew Guinea\b', 'Papua New Guinea'),
    (r'\bNew Caledonia\b', 'New Caledonia'),
]

# Simple trailing-country patterns (location typically ends with ", Country")
TRAILING_COUNTRIES = [
    'France', 'Brazil', 'Argentina', 'Italy', 'Spain', 'Australia',
    'Canada', 'Mexico', 'Chile', 'Peru', 'Colombia', 'Venezuela',
    'Germany', 'Sweden', 'Norway', 'Finland', 'Denmark', 'Belgium',
    'Netherlands', 'Portugal', 'Switzerland', 'Austria', 'Poland',
    'Romania', 'Hungary', 'Czechoslovakia', 'Yugoslavia', 'Greece',
    'Turkey', 'Iran', 'Iraq', 'India', 'Japan', 'China', 'Korea',
    'Philippines', 'Indonesia', 'Malaysia', 'Thailand',
    'Egypt', 'Morocco', 'Algeria', 'Tunisia', 'Nigeria', 'Kenya',
    'Madagascar', 'Mozambique', 'Angola', 'Reunion', 'Congo',
    'Uruguay', 'Paraguay', 'Bolivia', 'Ecuador', 'Guyana',
    'Ireland', 'Iceland', 'Luxembourg', 'Malta', 'Cyprus',
    'Lebanon', 'Israel', 'Jordan', 'Pakistan', 'Afghanistan',
    'Burma', 'Vietnam', 'Taiwan', 'Cuba', 'Jamaica', 'Barbados',
    'Trinidad', 'Martinique', 'Guadeloupe', 'Fiji',
    'Russia', 'Ukraine', 'Belarus',
]

# US state abbreviations and names for detecting US locations
US_STATES = {
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
    'DC',
}

US_STATE_NAMES = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
    'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
    'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
    'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
    'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
    'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
    'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
    'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
    'West Virginia', 'Wisconsin', 'Wyoming', 'District of Columbia',
]


def extract_country(location: str) -> str:
    """Extract country from a location string."""
    if not location:
        return ''

    # Check regex patterns first
    for pattern, country in COUNTRY_PATTERNS:
        if re.search(pattern, location, re.IGNORECASE):
            return country

    # Check if location ends with a known country
    parts = [p.strip() for p in location.split(',')]
    if parts:
        last = parts[-1].strip()
        for c in TRAILING_COUNTRIES:
            if last.lower() == c.lower():
                return c

    # Check for US state abbreviation as last token (e.g. "Springfield, IL")
    if len(parts) >= 2:
        last = parts[-1].strip()
        if last.upper() in US_STATES:
            return 'United States'

    # Check for US state name as last token
    if parts:
        last = parts[-1].strip()
        for state in US_STATE_NAMES:
            if last.lower() == state.lower():
                return 'United States'

    # Some locations are just regions
    region_map = {
        'persian gulf': 'Persian Gulf',
        'atlantic ocean': 'Atlantic Ocean',
        'pacific ocean': 'Pacific Ocean',
        'north sea': 'North Sea',
        'mediterranean': 'Mediterranean',
    }
    loc_lower = location.lower()
    for key, val in region_map.items():
        if key in loc_lower:
            return val

    return ''


def parse_date(date_str: str) -> str:
    """Parse various date formats into YYYY-MM-DD (or partial)."""
    if not date_str:
        return ''

    date_str = date_str.strip()

    # Full date: M/D/YYYY or MM/DD/YYYY
    m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})$', date_str)
    if m:
        month, day, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f'{year:04d}-{month:02d}-{day:02d}'

    # Month/Year: M/YYYY
    m = re.match(r'^(\d{1,2})/(\d{4})$', date_str)
    if m:
        month, year = int(m.group(1)), int(m.group(2))
        return f'{year:04d}-{month:02d}'

    # Year only
    m = re.match(r'^(\d{4})$', date_str)
    if m:
        return m.group(1)

    # Spring/Summer/Fall/Winter YYYY
    m = re.match(r'^(Spring|Summer|Fall|Winter|Early|Late|Mid)\s+(\d{4})$', date_str, re.IGNORECASE)
    if m:
        return f'{int(m.group(2)):04d}'

    # Try other common formats
    m = re.match(r'^(\d{4})/(\d{1,2})/(\d{1,2})$', date_str)
    if m:
        year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f'{year:04d}-{month:02d}-{day:02d}'

    return date_str  # return as-is if unparseable


def strip_markdown_links(text: str) -> str:
    """Convert markdown links [text](url) to just text."""
    return re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)


def main():
    # Load JSON
    with open(RAW_JSON, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    entries = data.get('Magonia Timeline', [])
    print(f"Loaded {len(entries)} raw entries from JSON\n")

    # Parse entries
    rows = []
    for entry in entries:
        source_id = entry.get('source_id', '')
        raw_date = entry.get('date', '')
        time_val = entry.get('time', '')
        location = entry.get('location', '')
        desc = entry.get('desc', '')
        ref = entry.get('ref', '')

        parsed_date = parse_date(raw_date)
        country = extract_country(location)
        ref_clean = strip_markdown_links(ref)

        rows.append({
            'source_id': source_id,
            'date_raw': raw_date,
            'date_parsed': parsed_date,
            'time': time_val,
            'location': location,
            'country': country,
            'description': desc,
            'references': ref_clean,
        })

    # Write CSV
    fieldnames = ['source_id', 'date_raw', 'date_parsed', 'time', 'location',
                  'country', 'description', 'references']
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} entries to {OUTPUT_CSV}\n")

    # --- Summary Stats ---
    print("=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)

    # Date range
    years = []
    for r in rows:
        m = re.match(r'^(\d{4})', r['date_parsed'])
        if m:
            years.append(int(m.group(1)))
    if years:
        print(f"\nDate range: {min(years)} - {max(years)}")
        print(f"Entries with parseable year: {len(years)}/{len(rows)}")

    # Top countries
    countries = Counter(r['country'] for r in rows if r['country'])
    print(f"\nCountries identified: {len(countries)}")
    print(f"Entries with country: {sum(countries.values())}/{len(rows)}")
    print("\nTop 15 countries:")
    for country, count in countries.most_common(15):
        print(f"  {country:25s} {count:4d}")

    # Entries without country
    no_country = [r for r in rows if not r['country']]
    if no_country:
        print(f"\nSample locations without country assignment ({len(no_country)} total):")
        for r in no_country[:10]:
            print(f"  - {r['location']}")

    # Decade distribution
    decade_counts = Counter((y // 10) * 10 for y in years)
    print("\nEntries by decade:")
    for decade in sorted(decade_counts):
        bar = '#' * (decade_counts[decade] // 5)
        print(f"  {decade}s: {decade_counts[decade]:4d}  {bar}")

    # Sample entries
    print("\n" + "=" * 60)
    print("SAMPLE ENTRIES (first 3)")
    print("=" * 60)
    for r in rows[:3]:
        print(f"\n  ID:       {r['source_id']}")
        print(f"  Date:     {r['date_parsed']} (raw: {r['date_raw']})")
        print(f"  Time:     {r['time']}")
        print(f"  Location: {r['location']}")
        print(f"  Country:  {r['country']}")
        print(f"  Desc:     {r['description'][:120]}...")
        print(f"  Refs:     {r['references'][:100]}")


if __name__ == '__main__':
    main()
