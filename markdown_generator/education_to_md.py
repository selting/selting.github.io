import pandas as pd
from pathlib import Path
from bib_to_md_selting import slugify, format_date 
import sys
import os
import numpy as np

# ============
MD_DIR = Path().home() / 'Code/selting.github.io/_education'
EDU_CSV = Path().home() / 'Documents/Bewerbungen/CV/education.csv'

# =========


def build_front_matter(row: dict):
    start_date = row.get('start_date', '')
    end_date = row.get('end_date', '')
    if not end_date or end_date is np.nan:
        end_date = row.get('expected_end_date')

    qualification = row.get('qualification', '')
    institution = row.get('institution', '')
    city = row.get('city', '')

    front = f"""---
start : {start_date}
end : {end_date}
qualification: {qualification}
institution: {institution}
city: {city}
---
"""
    return front

def build_file_name(row):
    start_date = row.get('start_date', '')
    end_date = row.get('end_date', '')
    if not end_date or end_date is np.nan:
        end_date = row.get('expected_end_date')
    
    qualification = row.get('qualification', '')
    institution = row.get('institution', '')
    city = row.get('city', '')
    slug = slugify(qualification)
    file_name = f"{end_date}-{slug}.md"
    return file_name

def main():
    # if not EDU_CSV.is_file():
    #     sys.stderr.write(f"education file not found: {EDU_CSV}\n")
    #     sys.exit(1)
    MD_DIR.mkdir(parents=True, exist_ok=True)

    edu_df = pd.read_csv(EDU_CSV) 
    for idx, row in edu_df.iterrows():
        row = dict(row)
        front = build_front_matter(row)
        file_name = build_file_name(row)
        out_path = MD_DIR / file_name
        out_path.write_text(front + "\n", encoding="utf-8")
        print(f"✅ {out_path}")

if __name__ == "__main__":
    main()
