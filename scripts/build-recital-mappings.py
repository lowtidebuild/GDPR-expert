#!/usr/bin/env python3
"""
build-recital-mappings.py — Build GDPR Recital-Article mappings from gdpr-info.eu

Fetches "Suitable Recitals" data from each article page, then updates:
1. Recital files: related_articles field
2. Article files: adds related_recitals field
3. _cross-refs.json: updates recital_to_article and article_to_recital sections
"""

import json
import re
import time
import urllib.request
import urllib.error
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
GDPR_DIR = BASE_DIR / "library" / "grade-a" / "gdpr"
RECITAL_DIR = BASE_DIR / "library" / "grade-a" / "gdpr-recitals"

# ─── Step 1: Fetch article→recital mappings from gdpr-info.eu ────────────────

def fetch_recitals_for_article(art_num):
    """Fetch suitable recitals for a given GDPR article from gdpr-info.eu"""
    url = f"https://gdpr-info.eu/art-{art_num}-gdpr/"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        # Look for recital links in the "Suitable Recitals" section
        # Pattern: /recitals/no-N/ links
        recital_nums = set()

        # Find the suitable recitals section
        # These appear as links like href="/recitals/no-47/"
        pattern = r'href="[^"]*?/recitals/no-(\d+)/?["\s]'
        matches = re.findall(pattern, html)
        for m in matches:
            recital_nums.add(int(m))

        return sorted(recital_nums)
    except Exception as e:
        print(f"  ERROR fetching Art. {art_num}: {e}")
        return []


def build_article_to_recital_map():
    """Build the complete article→recital mapping"""
    mapping = {}

    print("Fetching article→recital mappings from gdpr-info.eu...")
    for art_num in range(1, 100):
        recitals = fetch_recitals_for_article(art_num)
        if recitals:
            mapping[art_num] = recitals
            print(f"  Art. {art_num} → Recitals {recitals}")
        else:
            print(f"  Art. {art_num} → (none found)")
        time.sleep(0.3)  # Be polite

    return mapping


def invert_mapping(art_to_rec):
    """Build recital→article mapping from article→recital mapping"""
    rec_to_art = {}
    for art, recitals in art_to_rec.items():
        for rec in recitals:
            if rec not in rec_to_art:
                rec_to_art[rec] = []
            rec_to_art[rec].append(art)
    # Sort article lists
    for rec in rec_to_art:
        rec_to_art[rec] = sorted(rec_to_art[rec])
    return rec_to_art


# ─── Step 2: Update recital files ────────────────────────────────────────────

def update_recital_file(recital_num, articles):
    """Update related_articles in a recital file"""
    filepath = RECITAL_DIR / f"recital{recital_num}.md"
    if not filepath.exists():
        print(f"  WARNING: {filepath.name} not found")
        return False

    content = filepath.read_text(encoding="utf-8")

    # Build the new related_articles block
    if articles:
        lines = "\n".join(f'  - "Art. {a}"' for a in articles)
        new_block = f"related_articles:\n{lines}"
    else:
        new_block = "related_articles:"

    # Replace the existing related_articles field
    # Handle both empty and populated cases
    # Pattern: related_articles: followed by optional list items until next field or ---
    pattern = r"related_articles:.*?(?=\n(?:# ===|---))"
    replacement = new_block

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content != content:
        filepath.write_text(new_content, encoding="utf-8")
        return True
    return False


# ─── Step 3: Update article files ────────────────────────────────────────────

def update_article_file(art_num, recitals):
    """Add or update related_recitals in an article file"""
    filepath = GDPR_DIR / f"art{art_num}.md"
    if not filepath.exists():
        print(f"  WARNING: {filepath.name} not found")
        return False

    content = filepath.read_text(encoding="utf-8")

    # Build the new related_recitals block
    if recitals:
        lines = "\n".join(f'  - "Recital {r}"' for r in recitals)
        new_block = f"related_recitals:\n{lines}"
    else:
        new_block = "related_recitals:"

    # Check if related_recitals already exists
    if "related_recitals:" in content:
        # Replace existing
        pattern = r"related_recitals:.*?(?=\n(?:# ===|---))"
        new_content = re.sub(pattern, new_block, content, flags=re.DOTALL)
    else:
        # Insert after cross_references block (before # === Search Metadata ===)
        # Find the end of cross_references section
        pattern = r"(\n# === Search Metadata ===)"
        new_content = re.sub(pattern, f"\n{new_block}\n\\1", content)

        # If no Search Metadata section, insert before closing ---
        if new_content == content:
            # Insert after cross_references entries
            # Find cross_references and its items, then insert after
            cr_pattern = r"(cross_references:(?:\n  - [^\n]+)*)"
            match = re.search(cr_pattern, content)
            if match:
                insert_pos = match.end()
                new_content = content[:insert_pos] + "\n" + new_block + content[insert_pos:]

    if new_content != content:
        filepath.write_text(new_content, encoding="utf-8")
        return True
    return False


# ─── Step 4: Update _cross-refs.json ─────────────────────────────────────────

def update_cross_refs_json(art_to_rec, rec_to_art):
    """Update the _cross-refs.json file with recital mappings"""
    json_path = GDPR_DIR / "_cross-refs.json"

    if json_path.exists():
        data = json.loads(json_path.read_text(encoding="utf-8"))
    else:
        data = {}

    # Update article_to_recital
    data["article_to_recital"] = {
        f"Art. {art}": [f"Recital {r}" for r in recs]
        for art, recs in sorted(art_to_rec.items())
    }

    # Update recital_to_article
    data["recital_to_article"] = {
        f"Recital {rec}": [f"Art. {a}" for a in arts]
        for rec, arts in sorted(rec_to_art.items())
    }

    json_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print(f"  Updated {json_path.name}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    # Step 1: Fetch mappings
    art_to_rec = build_article_to_recital_map()
    rec_to_art = invert_mapping(art_to_rec)

    # Save raw mapping for reference
    mapping_path = BASE_DIR / "scripts" / "recital-article-mapping.json"
    mapping_data = {
        "article_to_recital": {str(k): v for k, v in sorted(art_to_rec.items())},
        "recital_to_article": {str(k): v for k, v in sorted(rec_to_art.items())}
    }
    mapping_path.write_text(json.dumps(mapping_data, indent=2) + "\n")
    print(f"\nSaved raw mapping to {mapping_path.name}")

    # Stats
    total_articles_with_recitals = len(art_to_rec)
    total_recitals_with_articles = len(rec_to_art)
    print(f"\nArticles with recitals: {total_articles_with_recitals}/99")
    print(f"Recitals with articles: {total_recitals_with_articles}/173")

    # Step 2: Update recital files
    print("\nUpdating recital files...")
    updated_recitals = 0
    for rec_num in range(1, 174):
        articles = rec_to_art.get(rec_num, [])
        if update_recital_file(rec_num, articles):
            updated_recitals += 1
    print(f"  Updated {updated_recitals} recital files")

    # Step 3: Update article files
    print("\nUpdating article files...")
    updated_articles = 0
    for art_num in range(1, 100):
        recitals = art_to_rec.get(art_num, [])
        if update_article_file(art_num, recitals):
            updated_articles += 1
    print(f"  Updated {updated_articles} article files")

    # Step 4: Update _cross-refs.json
    print("\nUpdating _cross-refs.json...")
    update_cross_refs_json(art_to_rec, rec_to_art)

    # Verification
    print("\n=== Verification ===")
    checks = {
        "Recital 47 → Art. 6": 6 in rec_to_art.get(47, []),
        "Recital 32 → Art. 7": 7 in rec_to_art.get(32, []),
        "Recital 71 → Art. 22": 22 in rec_to_art.get(71, []),
        "Recital 39 → Art. 5": 5 in rec_to_art.get(39, []),
        "Art. 6 → Recital 47": 47 in art_to_rec.get(6, []),
        "Art. 22 → Recital 71": 71 in art_to_rec.get(22, []),
    }
    for check, result in checks.items():
        status = "PASS" if result else "FAIL"
        print(f"  {status}: {check}")


if __name__ == "__main__":
    main()
