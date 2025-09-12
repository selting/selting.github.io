#!/usr/bin/env python3
"""
Convert a BibTeX library (output.bib) into one markdown file per entry.
Each file contains Jekyll‑style front‑matter matching the example you gave.
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

import bibtexparser

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
BIB_FILE      = Path("output.bib")          # input BibTeX file
MD_DIR        = Path("../_publications")     # where markdown files will be written
COLLECTION    = "publications"
CATEGORY      = "manuscripts"
SLIDES_URL    = "http://selting.github.io/files/slides{num}.pdf"
PAPER_URL     = "http://selting.github.io/files/paper{num}.pdf"
BIBTEX_URL    = "http://selting.github.io/files/bibtex{num}.bib"
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


def build_front_matter(entry: dict, idx: int) -> str:
    """
    Build the front‑matter block for a single BibTeX entry.
    ``idx`` is a 1‑based counter used to generate placeholder URLs.
    """
    title   = entry.get("title", "Untitled").strip("{}")
    year    = entry.get("year", "1900")
    month   = entry.get("month")
    day     = entry.get("day")
    date    = format_date(year, month, day)

    # Try to get a venue (journal, booktitle, etc.)
    venue = entry.get("journal") or entry.get("booktitle") or "Unknown venue"

    # Build a simple citation string – you can adapt the format later
    authors = entry.get("author", "Anonymous")
    citation = f'{authors}. ({year}). &quot;{title}.&quot; <i>{venue}</i>.'

    # Permalink uses the date + slugified title
    slug = slugify(title)
    permalink = f"/publications/{date}-{slug}"

    # Example excerpt – you may replace with a real abstract if present
    excerpt = entry.get("abstract", f"").replace("\n  ", " ")

    paperurl= entry.get("url", "#")    

    front = f"""---
title: "{title}"
collection: {COLLECTION}
category: {CATEGORY}
permalink: {permalink}
excerpt: '{excerpt}'
date: {date}
venue: '{venue}'
slidesurl: #'{SLIDES_URL.format(num=idx)}'
paperurl: '{paperurl}'
bibtexurl: #'{BIBTEX_URL.format(num=idx)}'
citation: #'{citation}'
---"""
    return front

def get_file_name(entry: dict, idx:int) -> str:
    """
    build the file name for a single bibtex entry
    """
    title   = entry.get("title", "Untitled").strip("{}")
    year    = entry.get("year", "1900")
    month   = entry.get("month")
    day     = entry.get("day")
    date    = format_date(year, month, day)
    slug = slugify(title)
    file_name = f"{date}-{slug}.md"
    return file_name

def main() -> None:
    if not BIB_FILE.is_file():
        sys.stderr.write(f"❌ BibTeX file not found: {BIB_FILE}\n")
        sys.exit(1)

    MD_DIR.mkdir(parents=True, exist_ok=True)

    with BIB_FILE.open(encoding="utf-8") as bf:
        bib_db = bibtexparser.load(bf)

    for i, entry in enumerate(bib_db.entries, start=1):
        md_content = build_front_matter(entry, i)
        # md_content += build_
        file_name = get_file_name(entry, i)
        out_path = MD_DIR / file_name

        out_path.write_text(md_content + "\n", encoding="utf-8")
        print(f"✅ {out_path}")

    print(f"\nAll markdown files written to: {MD_DIR}")


if __name__ == "__main__":
    main()
