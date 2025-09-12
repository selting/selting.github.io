import pandas as pd
from datetime import datetime
from pathlib import Path
import sys
import os
import re

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
TALKS_CSV = Path('talks.csv')
MD_DIR = Path('../_talks')
# ------------------------------------------------------------


def slugify(text: str) -> str:
    """Create a URL‑friendly slug (lowercase, hyphens, alphanum only)."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)          # drop punctuation
    text = re.sub(r"\s+", "-", text)              # spaces → hyphens
    return text.strip("-")

def format_date(year: str, month: str | None = None, day: str | None = None) -> str:
    """Return ISO date string; missing month/day default to 01."""
    month = month or "01"
    day   = day   or "01"
    try:
        dt = datetime(int(year), int(month), int(day))
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return f"{year}-01-01"

def build_front_matter(entry: dict) -> str:
    """
    Build the front‑matter block for a single BibTeX entry.
    ``idx`` is a 1‑based counter used to generate placeholder URLs.
    """
    title   = entry.get("Title", "Untitled").strip("{}")
    date    = entry.get('Date')
    year    = date.year
    month   = date.month
    day     = date.day
    date    = format_date(year, month, day)

    place = entry.get('Place', '')
    conference = entry.get('Meeting Name', '')

    # Build a simple citation string – you can adapt the format later
    authors = entry.get("Author", "Anonymous")
    citation = f'{authors}. ({year}). &quot;{title}.&quot; <i>{conference}, {place}</i>.'

    # Permalink uses the date + slugified title
    slug = slugify(title)
    permalink = f"/talks/{date}-{slug}"

    # Example excerpt – you may replace with a real abstract if present
    excerpt = entry.get("Abstract", f"").replace("\n  ", " ")

    url= entry.get("Url", "#")    

    front = f"""---
title: "{title}"
collection: talks
type: "Talk"
permalink: "{permalink}"
venue: "{conference}"
date: "{date}"
location: "{place}"
---"""
    return front

def get_file_name(entry: dict) -> str:
    """
    build the file name for a single bibtex entry
    """
    title   = entry.get("Title", "Untitled").strip("{}")
    date    = entry.get('Date')
    year    = date.year
    month   = date.month
    day     = date.day
    date    = format_date(year, month, day)

    slug = slugify(title)
    file_name = f"{date}-{slug}.md"
    return file_name

def main() -> None:
    if not TALKS_CSV.is_file():
        sys.stderror.write(f'file not found {TALKS_CSV}')
        sys.exit(1)

    MD_DIR.mkdir(parents=True, exist_ok=True)

    talks_df = pd.read_csv('talks.csv', parse_dates=['Date', 'Publication Year', 'Date Added', 'Date Modified', 'Access Date', 'Filing Date'])

    for i, row in talks_df.iterrows():
        row = dict(row)
        md_content = build_front_matter(row)
        file_name = get_file_name(row)
        out_path = MD_DIR / file_name

        out_path.write_text(md_content + '\n', encoding='utf-8')
        print(f'✅ {out_path}')

    print(f"\nAll markdown files written to: {MD_DIR}")

if __name__ == "__main__":
    main()
