#!/usr/bin/env python3
"""Quick test with a few pages to verify parsing before full run."""
import sys
sys.path.insert(0, "/Users/crashy/Development/ufolio/rosales")

from scrape_rosales import fetch_page, parse_entries, get_cdx_timestamp
import time

# Test with a couple of pages
test_pages = ["1954", "1973"]

for page in test_pages:
    print(f"\n{'='*60}")
    print(f"Testing page: {page}")
    print(f"{'='*60}")

    html = fetch_page(page)
    if not html:
        print(f"  FAILED to fetch page {page}")
        continue

    print(f"  HTML length: {len(html)}")

    entries = parse_entries(html, page)
    print(f"  Parsed {len(entries)} entries")

    # Show first 3 entries
    for e in entries[:3]:
        print(f"\n  Entry #{e['entry_number']}:")
        print(f"    Location: {e['location'][:80]}")
        print(f"    Date: {e['date']}")
        print(f"    Time: {e['time']}")
        print(f"    Description: {e['description'][:120]}...")
        print(f"    HC#: {e['hc_number']}")
        print(f"    Source: {e['source'][:80]}")
        print(f"    Type: {e['type_code']}")
        print(f"    Strangeness: {e['strangeness_index']}")
        print(f"    Reliability: {e['reliability']}")
        print(f"    Comments: {e['comments'][:80]}")

    time.sleep(2)
