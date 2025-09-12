#!/usr/bin/env python3
"""
Retrieve all public DOIs from an ORCID iD, fetch their BibTeX records
from Crossref, and write the combined bibliography to output.bib.
"""

import sys
import json
import time
from pathlib import Path

import requests

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
ORCID_ID = "0000-0002-7205-7554"          # ← replace with the target ORCID iD
OUTPUT_FILE = Path("output.bib")
CROSSREF_RATE_LIMIT = 1.0                # seconds between Crossref calls
# ------------------------------------------------------------


def get_orcid_works(orcid_id: str) -> list[dict]:
    """
    Call the public ORCID API and return the list of work summaries.
    Each summary contains (among other fields) a list of external identifiers,
    from which we extract DOIs.
    """
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
    headers = {"Accept": "application/json"}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    # The works are under `group` → each work summary
    works = []
    for group in data.get("group", []):
        # A group may contain multiple versions of the same work; take the first
        work_summary = group.get("work-summary", [{}])[0]
        works.append(work_summary)
    return works


def extract_dois(work_summaries: list[dict]) -> list[str]:
    """
    Pull DOI strings from the external identifiers of each work.
    Returns a deduplicated list of DOIs (lower‑cased, without the URL prefix).
    """
    dois = set()
    for w in work_summaries:
        ext_ids = w.get("external-ids", {}).get("external-id", [])
        for eid in ext_ids:
            if eid.get("external-id-type", "").lower() == "doi":
                doi = eid.get("external-id-value", "").strip()
                # Normalise: remove possible URL prefix and lower‑case
                if doi.lower().startswith("doi:"):
                    doi = doi[4:]
                doi = doi.lower()
                dois.add(doi)
    return sorted(dois)


def fetch_bibtex_from_crossref(doi: str) -> str:
    """
    Query Crossref for a single DOI‑identified work and return its BibTeX entry.
    """
    # url = f"https://api.crossref.org/works/{doi}"
    url = f"https://api.crossref.org/works/{doi}/transform"
    headers = {"Accept": "application/x-bibtex"}
    resp = requests.get(url, headers=headers, timeout=10)
    # resp = requests.get(url, timeout=10)
    # Crossref returns 404 for unknown DOIs – we simply skip those.
    if resp.status_code == 200:
        return resp.text.strip()
    else:
        sys.stderr.write(f"⚠️ Error on Crossref: {doi} (status: {resp.status_code})\n")
        return ""


def main():
    # 1️ Get works from ORCID
    try:
        works = get_orcid_works(ORCID_ID)
    except Exception as e:
        sys.stderr.write(f"❌ Failed to fetch ORCID data: {e}\n")
        sys.exit(1)

    # 2️ Extract DOIs
    dois = extract_dois(works)
    if not dois:
        sys.stderr.write("⚠️ No DOIs found for this ORCID iD.\n")
        sys.exit(0)

    # 3️ Retrieve BibTeX from Crossref
    bib_entries = []
    for doi in dois:
        bib = fetch = fetch_bibtex_from_crossref(doi)
        if bib:
            bib_entries.append(bib)
        time.sleep(CROSSREF_RATE_LIMIT)   # respect rate limit

    # 4️ Write to output file
    if bib_entries:
        OUTPUT_FILE.write_text("\n\n".join(bib_entries) + "\n", encoding="utf-8")
        print(f"✅ Wrote {len(bib_entries)} entries to {OUTPUT_FILE}")
    else:
        sys.stderr.write("⚠️ No BibTeX entries retrieved.\n")


if __name__ == "__main__":
    main()
