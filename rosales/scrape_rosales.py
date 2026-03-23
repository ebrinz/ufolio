#!/usr/bin/env python3
"""
Scraper for Albert Rosales' Humanoid Encounters catalog from the Wayback Machine.
Fetches archived SHTML pages, parses structured entries, and saves to CSV.
"""

import csv
import logging
import os
import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# --- Configuration ---
BASE_DIR = Path("/Users/crashy/Development/ufolio/rosales")
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_CSV = BASE_DIR / "data" / "rosales_parsed.csv"

RAW_DIR.mkdir(parents=True, exist_ok=True)

KNOWN_PAGES = [
    "ancient", "1900", "1910", "1930", "1940", "1942", "1943", "1944",
    "1945", "1946", "1947", "1948", "1949", "1950", "1951", "1952",
    "1953", "1954", "1955", "1956", "1957", "1958", "1959", "1960",
    "1961", "1962", "1963", "1964", "1965", "1966", "1967", "1968",
    "1969", "1970", "1971", "1972", "1973", "1974", "1975", "1976",
    "1977", "1978", "1979", "1980", "1981", "1982", "1983", "1984",
    "1985", "1986", "1987", "1988", "1989", "1990", "1991", "1992",
    "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000",
    "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008",
    "2009",
]

CDX_API = "https://web.archive.org/cdx/search/cdx"
WAYBACK_URL = "https://web.archive.org/web/{ts}/http://www.ufoinfo.com/humanoid/humanoid{page}.shtml"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

REQUEST_DELAY = 2.0  # seconds between requests
MAX_RETRIES = 3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(BASE_DIR / "scrape.log"),
    ],
)
log = logging.getLogger(__name__)

# Type code descriptions
TYPE_CODES = {
    "A": "entity inside/on object",
    "B": "entity entering/exiting",
    "C": "entity near object",
    "D": "entity near landing trace",
    "E": "entity without UFO",
    "F": "trace only",
    "G": "contact/abduction",
    "H": "crash recovery",
    "X": "extreme strangeness",
}

session = requests.Session()
session.headers.update(HEADERS)


def get_cdx_timestamp(page: str) -> str | None:
    """Use the CDX API to find a valid Wayback Machine timestamp for a page.

    Prefer 2008-2013 era snapshots since later ones hit Cloudflare challenges.
    """
    url = f"ufoinfo.com/humanoid/humanoid{page}.shtml"

    # Try several date ranges in order of preference (older = more likely to have real content)
    ranges = [
        ("20080101", "20130101"),  # primary: 2008-2012 era
        ("20060101", "20080101"),  # fallback: 2006-2008
        ("20130101", "20160101"),  # fallback: 2013-2015
    ]

    for from_date, to_date in ranges:
        params = {
            "url": url,
            "output": "json",
            "fl": "timestamp,original,statuscode",
            "filter": "statuscode:200",
            "limit": "1",
            "from": from_date,
            "to": to_date,
        }
        try:
            resp = session.get(CDX_API, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            if len(data) > 1:  # first row is headers
                ts = data[1][0]
                log.info(f"CDX found timestamp {ts} for {page}")
                return ts
        except Exception as e:
            log.warning(f"CDX lookup failed for {page} ({from_date}-{to_date}): {e}")

    # Last resort: any snapshot
    params = {
        "url": url,
        "output": "json",
        "fl": "timestamp,original,statuscode",
        "filter": "statuscode:200",
        "limit": "1",
    }
    try:
        resp = session.get(CDX_API, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if len(data) > 1:
            ts = data[1][0]
            log.info(f"CDX found fallback timestamp {ts} for {page}")
            return ts
    except Exception as e:
        log.warning(f"CDX fallback lookup failed for {page}: {e}")

    return None


def is_valid_content(html: str) -> bool:
    """Check if the HTML is real content, not a Cloudflare challenge page."""
    if "Please wait while your request is being verified" in html:
        return False
    if "One moment, please..." in html and len(html) < 5000:
        return False
    if "wsidchk" in html and len(html) < 5000:
        return False
    return True


def fetch_page(page: str) -> str | None:
    """Fetch a humanoid encounters page from the Wayback Machine."""
    raw_file = RAW_DIR / f"humanoid{page}.html"

    # Use cached file if it exists, is non-empty, and has real content
    if raw_file.exists() and raw_file.stat().st_size > 500:
        cached = raw_file.read_text(encoding="utf-8", errors="replace")
        if is_valid_content(cached):
            log.info(f"Using cached file for {page}")
            return cached
        else:
            log.info(f"Cached file for {page} is a challenge page, re-fetching")
            raw_file.unlink()

    # Get timestamp from CDX
    ts = get_cdx_timestamp(page)
    if not ts:
        log.warning(f"No Wayback snapshot found for page: {page}")
        return None

    url = WAYBACK_URL.format(ts=ts, page=page)
    log.info(f"Fetching {page} from {url}")

    for attempt in range(MAX_RETRIES):
        try:
            resp = session.get(url, timeout=60)
            if resp.status_code == 429:
                wait = 30 * (attempt + 1)
                log.warning(f"Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            html = resp.text
            if not is_valid_content(html):
                log.warning(f"Got challenge page for {page} (attempt {attempt+1})")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(5)
                continue
            raw_file.write_text(html, encoding="utf-8")
            log.info(f"Saved raw HTML for {page} ({len(html)} bytes)")
            return html
        except requests.RequestException as e:
            log.warning(f"Fetch attempt {attempt+1} failed for {page}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(5 * (attempt + 1))

    return None


def parse_entries(html: str, page_label: str) -> list[dict]:
    """Parse humanoid encounter entries from an HTML page."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove script/style
    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text()

    # Normalize whitespace but preserve line breaks
    lines = text.split("\n")
    lines = [line.rstrip() for line in lines]
    text = "\n".join(lines)

    entries = []

    # Split on entry numbers: look for patterns like "1." or "123." at start of line
    # Entry pattern: number followed by period at start of line (or after blank lines)
    # We look for the entry number pattern followed by Location line

    # Strategy: find all entry start positions using the numbered pattern
    # An entry starts with a number+period on its own line or beginning of content block
    entry_pattern = re.compile(
        r'(?:^|\n)\s*(\d{1,4})\.\s*\n'  # entry number on its own line
        r'Location[.\s]*[:.]?\s*(.+?)(?:\n|$)',  # Location line
        re.MULTILINE
    )

    # More flexible: try to find entry boundaries
    # Entries are separated by entry numbers. Let's find all positions.
    boundary_re = re.compile(r'(?:^|\n)\s*(\d{1,4})\.\s*\n', re.MULTILINE)
    boundaries = list(boundary_re.finditer(text))

    if not boundaries:
        # Try alternate format where number and Location are closer together
        boundary_re = re.compile(r'(?:^|\n)\s*(\d{1,4})\.\s*\n\s*Location', re.MULTILINE)
        boundaries = list(boundary_re.finditer(text))

    if not boundaries:
        log.warning(f"No entry boundaries found in page {page_label}")
        # Try even more relaxed pattern
        boundary_re = re.compile(r'(?:^|\n)(\d{1,4})\.\s*$', re.MULTILINE)
        boundaries = list(boundary_re.finditer(text))

    log.info(f"Found {len(boundaries)} entry boundaries in page {page_label}")

    for i, match in enumerate(boundaries):
        entry_num = match.group(1)
        start = match.start()
        end = boundaries[i + 1].start() if i + 1 < len(boundaries) else len(text)

        chunk = text[start:end].strip()
        entry = parse_single_entry(chunk, entry_num, page_label)
        if entry:
            entries.append(entry)

    return entries


def parse_single_entry(chunk: str, entry_num: str, page_label: str) -> dict | None:
    """Parse a single entry chunk into a structured dict."""
    result = {
        "entry_number": entry_num,
        "year_page": page_label,
        "location": "",
        "date": "",
        "time": "",
        "description": "",
        "hc_number": "",
        "source": "",
        "type_code": "",
        "strangeness_index": "",
        "reliability": "",
        "comments": "",
    }

    # Extract Location
    loc_match = re.search(r'Location[.\s]*[:.]?\s*(.+?)(?:\n|$)', chunk)
    if loc_match:
        result["location"] = loc_match.group(1).strip().strip(".")

    # Extract Date and Time
    dt_match = re.search(r'Date:\s*(.+?)\s+Time:\s*(.+?)(?:\n|$)', chunk, re.IGNORECASE)
    if dt_match:
        result["date"] = dt_match.group(1).strip()
        result["time"] = dt_match.group(2).strip()
    else:
        # Sometimes just Date:
        dt_match = re.search(r'Date:\s*(.+?)(?:\n|$)', chunk, re.IGNORECASE)
        if dt_match:
            result["date"] = dt_match.group(1).strip()
            # Check for Time on same or separate line
            time_match = re.search(r'Time:\s*(.+?)(?:\n|$)', chunk, re.IGNORECASE)
            if time_match:
                result["time"] = time_match.group(1).strip()

    # Extract HC addition number (handles "HC addition # 1234", "HC addendum", "HC addition # 3113")
    hc_match = re.search(r'HC\s+addition\s*#?\s*[:.]?\s*(\S+)', chunk, re.IGNORECASE)
    if hc_match:
        result["hc_number"] = hc_match.group(1).strip()
    elif re.search(r'HC\s+addendum', chunk, re.IGNORECASE):
        result["hc_number"] = "addendum"

    # Extract Source - handles multi-line sources before Type:
    # The source can span multiple lines with tabs before Type:
    src_match = re.search(r'Source:\s*(.+?)(?:\s*Type:)', chunk, re.IGNORECASE | re.DOTALL)
    if src_match:
        result["source"] = " ".join(src_match.group(1).split())
    else:
        src_match = re.search(r'Source:\s*(.+?)(?:\n|$)', chunk, re.IGNORECASE)
        if src_match:
            result["source"] = src_match.group(1).strip()

    # Extract Type - the letter right after "Type:"
    type_match = re.search(r'Type:\s*([A-HXa-hx])\b', chunk)
    if type_match:
        result["type_code"] = type_match.group(1).upper()

    # Extract High Strangeness Index
    hsi_match = re.search(r'High\s+Strangeness\s+Index:\s*(\d+)', chunk, re.IGNORECASE)
    if hsi_match:
        result["strangeness_index"] = hsi_match.group(1)

    # Extract Reliability - handles both "Reliability of Source:" and "ROS:"
    rel_match = re.search(r'(?:Reliability\s+of\s+Source|ROS):\s*(\d+)', chunk, re.IGNORECASE)
    if rel_match:
        result["reliability"] = rel_match.group(1)

    # Extract Comments
    comm_match = re.search(r'Comments:\s*(.+?)(?:\n\s*\n|\Z)', chunk, re.IGNORECASE | re.DOTALL)
    if comm_match:
        result["comments"] = " ".join(comm_match.group(1).split())

    # Extract Description: text between Time: line and HC addition line
    # Find the end of the Date/Time header
    desc_start_match = re.search(r'Time:\s*.+?\n', chunk, re.IGNORECASE)
    if not desc_start_match:
        desc_start_match = re.search(r'Date:\s*.+?\n', chunk, re.IGNORECASE)

    # Find the start of the footer (HC addition or Source)
    desc_end_match = re.search(r'\n\s*HC\s+addition|Source:', chunk, re.IGNORECASE)

    if desc_start_match and desc_end_match:
        desc = chunk[desc_start_match.end():desc_end_match.start()]
        desc = " ".join(desc.split())
        result["description"] = desc

    # Only return if we got at least a location or description
    if result["location"] or result["description"]:
        return result

    return None


def main():
    log.info("=" * 60)
    log.info("Starting Rosales Humanoid Encounters scraper")
    log.info("=" * 60)

    all_entries = []
    page_stats = {}

    for idx, page in enumerate(KNOWN_PAGES):
        log.info(f"\n--- Processing page {idx+1}/{len(KNOWN_PAGES)}: humanoid{page} ---")

        html = fetch_page(page)
        if not html:
            page_stats[page] = 0
            continue

        entries = parse_entries(html, page)
        page_stats[page] = len(entries)
        all_entries.extend(entries)

        log.info(f"Parsed {len(entries)} entries from page {page}")

        # Polite delay between fetches (skip if cached)
        if not (RAW_DIR / f"humanoid{page}.html").exists():
            pass  # already fetched
        if idx < len(KNOWN_PAGES) - 1:
            time.sleep(REQUEST_DELAY)

    # Write CSV
    if all_entries:
        fieldnames = [
            "entry_number", "year_page", "location", "date", "time",
            "description", "hc_number", "source", "type_code",
            "strangeness_index", "reliability", "comments",
        ]

        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_entries)

        log.info(f"\nSaved {len(all_entries)} entries to {OUTPUT_CSV}")

    # Summary stats
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total pages processed: {len(page_stats)}")
    print(f"Pages with data: {sum(1 for v in page_stats.values() if v > 0)}")
    print(f"Total entries parsed: {len(all_entries)}")
    print()

    # Entries per page
    print("Entries per page:")
    for page, count in sorted(page_stats.items(), key=lambda x: (x[0] != 'ancient', x[0])):
        if count > 0:
            print(f"  {page:>8s}: {count:>4d} entries")

    # Type code distribution
    if all_entries:
        type_counts = {}
        for e in all_entries:
            tc = e["type_code"] or "unknown"
            type_counts[tc] = type_counts.get(tc, 0) + 1

        print("\nType code distribution:")
        for code in sorted(type_counts.keys()):
            desc = TYPE_CODES.get(code, "unknown")
            print(f"  {code}: {type_counts[code]:>4d}  ({desc})")

        # Strangeness distribution
        si_counts = {}
        for e in all_entries:
            si = e["strangeness_index"] or "N/A"
            si_counts[si] = si_counts.get(si, 0) + 1

        print("\nHigh Strangeness Index distribution:")
        for si in sorted(si_counts.keys(), key=lambda x: (x == "N/A", x)):
            print(f"  {si:>3s}: {si_counts[si]:>4d}")

        # Entries with descriptions
        with_desc = sum(1 for e in all_entries if e["description"])
        print(f"\nEntries with descriptions: {with_desc}/{len(all_entries)}")

        # CSV file size
        csv_size = OUTPUT_CSV.stat().st_size
        print(f"CSV file size: {csv_size / 1024 / 1024:.1f} MB")

    print("\nDone!")


if __name__ == "__main__":
    main()
