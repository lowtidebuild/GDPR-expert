#!/usr/bin/env python3
"""
fetch-eu-legislation.py — Fetch EU legislation from CELLAR REST API (Publications Office)

Parses XHTML output into per-article markdown files with YAML frontmatter.
Primary path: CELLAR REST API with Accept: application/xhtml+xml (no auth required)

Usage:
    python3 scripts/fetch-eu-legislation.py                    # Fetch all configured laws
    python3 scripts/fetch-eu-legislation.py --law gdpr         # Fetch specific law
    python3 scripts/fetch-eu-legislation.py --law gdpr --dry   # Dry run (parse only, no write)
"""

import argparse
import json
import logging
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from textwrap import dedent

# ─── Configuration ───────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent
LIBRARY_DIR = BASE_DIR / "library" / "grade-a"
INDEX_DIR = BASE_DIR / "index"
LOG_DIR = BASE_DIR / "scripts" / "logs"

CELLAR_BASE = "https://publications.europa.eu/resource/celex"

LAWS = {
    "gdpr": {
        "celex": "32016R0679",
        "name": "General Data Protection Regulation",
        "short": "GDPR",
        "type": "regulation",
        "effective_date": "20180525",
        "dir": "gdpr",
        "recitals_dir": "gdpr-recitals",
        "has_recitals": True,
    },
    "eprivacy": {
        "celex": "02002L0058-20091219",
        "name": "Directive on Privacy and Electronic Communications",
        "short": "ePrivacy Directive",
        "type": "directive",
        "effective_date": "20020731",
        "dir": "eprivacy-directive",
        "recitals_dir": None,
        "has_recitals": False,  # Consolidated version may not have recitals in XHTML
    },
    "ai-act": {
        "celex": "32024R1689",
        "name": "Artificial Intelligence Act",
        "short": "EU AI Act",
        "type": "regulation",
        "effective_date": "20240801",
        "dir": "eu-ai-act",
        "recitals_dir": "eu-ai-act-recitals",
        "has_recitals": True,
    },
    "data-act": {
        "celex": "32023R2854",
        "name": "Data Act",
        "short": "Data Act",
        "type": "regulation",
        "effective_date": "20240111",
        "dir": "data-act",
        "recitals_dir": "data-act-recitals",
        "has_recitals": True,
    },
    "dga": {
        "celex": "32022R0868",
        "name": "Data Governance Act",
        "short": "DGA",
        "type": "regulation",
        "effective_date": "20220623",
        "dir": "data-governance-act",
        "recitals_dir": "data-governance-act-recitals",
        "has_recitals": True,
    },
}

# ─── XHTML Fetcher ───────────────────────────────────────────────────────────


def fetch_xhtml(celex: str, max_retries: int = 3) -> str:
    """Fetch XHTML from CELLAR REST API with exponential backoff."""
    url = f"{CELLAR_BASE}/{celex}"
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url)
            req.add_header("Accept", "application/xhtml+xml")
            req.add_header("Accept-Language", "eng")
            req.add_header("User-Agent", "GDPR-Expert/1.0")
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            logging.warning(f"HTTP {e.code} for {celex} (attempt {attempt + 1})")
            if e.code == 404:
                raise
        except Exception as e:
            logging.warning(f"Error fetching {celex} (attempt {attempt + 1}): {e}")
        if attempt < max_retries - 1:
            wait = 2 ** attempt
            logging.info(f"Retrying in {wait}s...")
            time.sleep(wait)
    raise RuntimeError(f"Failed to fetch {celex} after {max_retries} attempts")


# ─── XHTML Parser ────────────────────────────────────────────────────────────


def strip_tags(html: str) -> str:
    """Remove HTML tags, decode entities, clean whitespace."""
    text = re.sub(r"<[^>]+>", "", html)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&")
    text = text.replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&#160;", " ")
    # Normalize whitespace but preserve newlines
    lines = []
    for line in text.split("\n"):
        cleaned = " ".join(line.split())
        if cleaned:
            lines.append(cleaned)
    return "\n".join(lines)


def parse_articles(xhtml: str, law_config: dict) -> list[dict]:
    """Parse XHTML to extract articles with metadata."""
    articles = []
    chapter_map = {}  # article_num -> (chapter, chapter_title)

    # Extract chapter structure
    # Chapters appear as "CHAPTER I" / "CHAPTER II" etc.
    chapter_sections = re.finditer(
        r'>CHAPTER\s+([IVX]+)<.*?class="oj-sti-art">(.*?)</p>',
        xhtml,
        re.DOTALL,
    )
    current_chapter = None
    current_chapter_title = None
    chapter_ranges = []

    for match in chapter_sections:
        chapter_num = match.group(1).strip()
        chapter_title = strip_tags(match.group(2)).strip()
        chapter_ranges.append((match.start(), chapter_num, chapter_title))

    # Find each article by its ID
    art_pattern = re.compile(r'id="art_(\d+)">')
    art_positions = [(m.group(1), m.start()) for m in art_pattern.finditer(xhtml)]

    for i, (art_num, art_start) in enumerate(art_positions):
        # Determine end position (start of next article or end of doc)
        if i + 1 < len(art_positions):
            art_end = art_positions[i + 1][1]
        else:
            art_end = len(xhtml)

        art_html = xhtml[art_start:art_end]

        # Extract title
        title_match = re.search(
            r'class="oj-sti-art">(.*?)</p>', art_html, re.DOTALL
        )
        title = strip_tags(title_match.group(1)).strip() if title_match else ""

        # Determine chapter
        chapter = ""
        chapter_title = ""
        for ch_start, ch_num, ch_title in reversed(chapter_ranges):
            if ch_start < art_start:
                chapter = ch_num
                chapter_title = ch_title
                break

        # Extract body text with paragraph structure
        body_lines = []
        # Find paragraphs with numbering
        paragraphs = re.finditer(
            r'<p\s+class="oj-normal">(.*?)</p>', art_html, re.DOTALL
        )
        for p in paragraphs:
            text = strip_tags(p.group(1)).strip()
            if text:
                body_lines.append(text)

        # Also get table-based sub-items (a), (b), etc.
        table_items = re.finditer(
            r'<td[^>]*>\s*<p\s+class="oj-normal">(.*?)</p>\s*</td>',
            art_html,
            re.DOTALL,
        )
        # These are already captured in paragraphs above via nested structure

        body_text = "\n\n".join(body_lines) if body_lines else strip_tags(art_html)

        # Extract cross-references
        cross_refs = set()
        # Article references within same law
        for ref in re.finditer(r"Article\s+(\d+)(?:\((\d+)\))?", body_text):
            ref_art = ref.group(1)
            ref_para = ref.group(2)
            if ref_para:
                cross_refs.add(f"Art. {ref_art}({ref_para})")
            else:
                cross_refs.add(f"Art. {ref_art}")
        # Recital references
        for ref in re.finditer(r"[Rr]ecital(?:s)?\s+(\d+)", body_text):
            cross_refs.add(f"Recital {ref.group(1)}")
        # Inter-legislation references
        for ref in re.finditer(
            r"Directive\s+(\d{4}/\d+/\w+)", body_text
        ):
            cross_refs.add(f"Directive {ref.group(1)}")
        for ref in re.finditer(
            r"Regulation\s+\(EU\)\s+(\d{4}/\d+)", body_text
        ):
            cross_refs.add(f"Regulation (EU) {ref.group(1)}")

        # Extract keywords from title and first paragraph
        keywords = extract_keywords(title, body_text[:500])

        articles.append({
            "num": int(art_num),
            "title": title,
            "chapter": chapter,
            "chapter_title": chapter_title,
            "body": body_text,
            "cross_references": sorted(cross_refs),
            "keywords": keywords,
        })

    return articles


def parse_recitals(xhtml: str) -> list[dict]:
    """Parse XHTML to extract recitals."""
    recitals = []

    # Recitals have IDs like rct_1, rct_2, etc.
    rct_pattern = re.compile(r'id="rct_(\d+)"')
    rct_positions = [(m.group(1), m.start()) for m in rct_pattern.finditer(xhtml)]

    for i, (rct_num, rct_start) in enumerate(rct_positions):
        if i + 1 < len(rct_positions):
            rct_end = rct_positions[i + 1][1]
        else:
            # End at first article
            art1_pos = xhtml.find('id="art_1">')
            rct_end = art1_pos if art1_pos > rct_start else rct_start + 5000

        rct_html = xhtml[rct_start:rct_end]
        body = strip_tags(rct_html).strip()

        # Remove leading ID reference and numbering artifacts
        body = re.sub(r'^id="rct_\d+">\s*', "", body)
        body = re.sub(r"^\(\d+\)\s*", "", body)
        # Remove any trailing HTML fragments
        body = re.sub(r'<[^>]+$', "", body).strip()

        # Find article references in recital text
        related_articles = set()
        for ref in re.finditer(r"Article\s+(\d+)", body):
            related_articles.add(f"Art. {ref.group(1)}")

        recitals.append({
            "num": int(rct_num),
            "body": body,
            "related_articles": sorted(related_articles),
        })

    return recitals


def extract_keywords(title: str, text: str) -> list[str]:
    """Extract relevant keywords from article title and text."""
    # Common GDPR/data protection terms
    keyword_patterns = [
        "consent", "lawful", "processing", "controller", "processor",
        "data subject", "personal data", "special categor", "transfer",
        "supervisory authority", "data protection officer", "DPO",
        "impact assessment", "DPIA", "breach", "notification",
        "right of access", "rectification", "erasure", "portability",
        "restriction", "objection", "profiling", "automated",
        "transparency", "information", "legitimate interest",
        "public interest", "vital interest", "legal obligation",
        "international", "adequacy", "safeguard", "binding corporate",
        "certification", "code of conduct", "penalty", "fine",
        "child", "minor", "genetic", "biometric", "health",
    ]
    combined = f"{title} {text}".lower()
    return [kw for kw in keyword_patterns if kw in combined]


# ─── Markdown Writer ─────────────────────────────────────────────────────────


def write_article_md(article: dict, law_config: dict, output_dir: Path) -> Path:
    """Write a single article as markdown with YAML frontmatter."""
    num = article["num"]
    filepath = output_dir / f"art{num}.md"

    frontmatter = {
        "law": law_config["name"],
        "law_id": law_config["celex"],
        "article": num,
        "article_sub": 0,
        "article_title": article["title"],
        "chapter": article["chapter"],
        "chapter_title": article["chapter_title"],
        "source_grade": "A",
        "source_url": f"https://eur-lex.europa.eu/eli/reg/2016/679/art_{num}/oj/eng",
        "effective_date": law_config["effective_date"],
        "last_amended": None,
        "retrieved_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "cross_references": article["cross_references"],
        "keywords": article["keywords"],
    }

    # Build YAML manually for clean output
    yaml_lines = ["---"]
    yaml_lines.append(f'# === Identification ===')
    yaml_lines.append(f'law: "{frontmatter["law"]}"')
    yaml_lines.append(f'law_id: "{frontmatter["law_id"]}"')
    yaml_lines.append(f'article: {frontmatter["article"]}')
    yaml_lines.append(f'article_sub: 0')
    yaml_lines.append(f'article_title: "{frontmatter["article_title"]}"')
    yaml_lines.append(f'chapter: "{frontmatter["chapter"]}"')
    yaml_lines.append(f'chapter_title: "{frontmatter["chapter_title"]}"')
    yaml_lines.append(f"")
    yaml_lines.append(f'# === Source ===')
    yaml_lines.append(f'source_grade: "A"')
    yaml_lines.append(f'source_url: "{frontmatter["source_url"]}"')
    yaml_lines.append(f'effective_date: "{frontmatter["effective_date"]}"')
    yaml_lines.append(f"last_amended: null")
    yaml_lines.append(f'retrieved_at: "{frontmatter["retrieved_at"]}"')
    yaml_lines.append(f"")
    yaml_lines.append(f'# === Relationships ===')
    yaml_lines.append(f"cross_references:")
    for ref in frontmatter["cross_references"]:
        yaml_lines.append(f'  - "{ref}"')
    yaml_lines.append(f"")
    yaml_lines.append(f'# === Search Metadata ===')
    yaml_lines.append(f"keywords:")
    for kw in frontmatter["keywords"]:
        yaml_lines.append(f'  - "{kw}"')
    yaml_lines.append("---")

    content = "\n".join(yaml_lines)
    content += f"\n\n## Article {num} — {article['title']}\n\n"
    content += article["body"] + "\n"

    filepath.write_text(content, encoding="utf-8")
    return filepath


def write_recital_md(recital: dict, law_config: dict, output_dir: Path) -> Path:
    """Write a single recital as markdown with YAML frontmatter."""
    num = recital["num"]
    filepath = output_dir / f"recital{num}.md"

    yaml_lines = ["---"]
    yaml_lines.append(f'# === Identification ===')
    yaml_lines.append(f'law: "{law_config["name"]}"')
    yaml_lines.append(f'law_id: "{law_config["celex"]}"')
    yaml_lines.append(f'recital: {num}')
    yaml_lines.append(f'document_type: "recital"')
    yaml_lines.append(f"")
    yaml_lines.append(f'# === Source ===')
    yaml_lines.append(f'source_grade: "A"')
    yaml_lines.append(f'effective_date: "{law_config["effective_date"]}"')
    yaml_lines.append(f'retrieved_at: "{datetime.now(timezone.utc).strftime("%Y-%m-%d")}"')
    yaml_lines.append(f"")
    yaml_lines.append(f'# === Relationships ===')
    yaml_lines.append(f"related_articles:")
    for ref in recital["related_articles"]:
        yaml_lines.append(f'  - "{ref}"')
    yaml_lines.append("---")

    content = "\n".join(yaml_lines)
    content += f"\n\n## Recital {num}\n\n"
    content += recital["body"] + "\n"

    filepath.write_text(content, encoding="utf-8")
    return filepath


# ─── Metadata Writers ────────────────────────────────────────────────────────


def write_meta_json(articles: list, law_config: dict, output_dir: Path):
    """Write _meta.json for the law directory."""
    meta = {
        "law": law_config["name"],
        "law_id": law_config["celex"],
        "type": law_config["type"],
        "short_name": law_config["short"],
        "effective_date": law_config["effective_date"],
        "article_count": len(articles),
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
    }
    (output_dir / "_meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def write_hierarchy_json(articles: list, output_dir: Path):
    """Write _hierarchy.json with Chapter → Article tree."""
    hierarchy = {}
    for art in articles:
        ch = art["chapter"] or "NONE"
        if ch not in hierarchy:
            hierarchy[ch] = {
                "chapter": ch,
                "chapter_title": art["chapter_title"],
                "articles": [],
            }
        hierarchy[ch]["articles"].append({
            "article": art["num"],
            "title": art["title"],
        })
    (output_dir / "_hierarchy.json").write_text(
        json.dumps(list(hierarchy.values()), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_cross_refs_json(articles: list, recitals: list, output_dir: Path):
    """Write _cross-refs.json with bidirectional Article↔Recital mappings."""
    refs = {
        "article_to_recital": {},
        "recital_to_article": {},
        "article_to_article": {},
    }

    for art in articles:
        art_key = f"Art. {art['num']}"
        art_refs = []
        art_recitals = []
        for ref in art["cross_references"]:
            if ref.startswith("Recital"):
                art_recitals.append(ref)
            elif ref.startswith("Art."):
                art_refs.append(ref)
        if art_recitals:
            refs["article_to_recital"][art_key] = art_recitals
        if art_refs:
            refs["article_to_article"][art_key] = art_refs

    for rct in recitals:
        rct_key = f"Recital {rct['num']}"
        if rct["related_articles"]:
            refs["recital_to_article"][rct_key] = rct["related_articles"]

    (output_dir / "_cross-refs.json").write_text(
        json.dumps(refs, indent=2, ensure_ascii=False), encoding="utf-8"
    )


# ─── Source Registry Updater ─────────────────────────────────────────────────


def update_source_registry(law_key: str, count: int, recital_count: int = 0):
    """Update index/source-registry.json with collection status."""
    reg_path = INDEX_DIR / "source-registry.json"
    if reg_path.exists():
        registry = json.loads(reg_path.read_text())
    else:
        registry = {"type": "source_registry", "sources": {"grade-a": {}, "grade-b": {}, "grade-c": {}}}

    law_config = LAWS[law_key]
    dir_name = law_config["dir"]

    registry["generated_at"] = datetime.now(timezone.utc).isoformat()
    registry["sources"]["grade-a"][dir_name] = {
        "status": "complete",
        "count": count,
        "target": count,
    }

    if recital_count > 0 and law_config.get("recitals_dir"):
        registry["sources"]["grade-a"][law_config["recitals_dir"]] = {
            "status": "complete",
            "count": recital_count,
            "target": recital_count,
        }

    reg_path.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8"
    )


# ─── Main ────────────────────────────────────────────────────────────────────


def process_law(law_key: str, dry_run: bool = False) -> dict:
    """Fetch and process a single law. Returns stats dict."""
    law = LAWS[law_key]
    logging.info(f"Processing {law['short']} (CELEX: {law['celex']})")

    # Fetch XHTML
    xhtml = fetch_xhtml(law["celex"])
    logging.info(f"Fetched {len(xhtml)} chars of XHTML")

    # Save raw XHTML for debugging
    raw_path = LOG_DIR / f"{law_key}-raw.html"
    raw_path.write_text(xhtml, encoding="utf-8")

    # Parse articles
    articles = parse_articles(xhtml, law)
    logging.info(f"Parsed {len(articles)} articles")

    # Parse recitals
    recitals = []
    if law["has_recitals"]:
        recitals = parse_recitals(xhtml)
        logging.info(f"Parsed {len(recitals)} recitals")

    if dry_run:
        logging.info("DRY RUN — not writing files")
        for art in articles[:3]:
            logging.info(f"  Art. {art['num']}: {art['title']} ({len(art['body'])} chars)")
        return {"articles": len(articles), "recitals": len(recitals), "errors": []}

    # Write article files
    art_dir = LIBRARY_DIR / law["dir"]
    art_dir.mkdir(parents=True, exist_ok=True)
    errors = []

    for art in articles:
        try:
            write_article_md(art, law, art_dir)
        except Exception as e:
            errors.append(f"Art. {art['num']}: {e}")
            logging.error(f"Failed to write Art. {art['num']}: {e}")

    # Write recital files
    if recitals and law.get("recitals_dir"):
        rct_dir = LIBRARY_DIR / law["recitals_dir"]
        rct_dir.mkdir(parents=True, exist_ok=True)
        for rct in recitals:
            try:
                write_recital_md(rct, law, rct_dir)
            except Exception as e:
                errors.append(f"Recital {rct['num']}: {e}")
                logging.error(f"Failed to write Recital {rct['num']}: {e}")

    # Write metadata
    write_meta_json(articles, law, art_dir)
    write_hierarchy_json(articles, art_dir)
    write_cross_refs_json(articles, recitals, art_dir)

    # Update source registry
    update_source_registry(law_key, len(articles), len(recitals))

    stats = {
        "articles": len(articles),
        "recitals": len(recitals),
        "errors": errors,
    }
    logging.info(f"Done: {stats['articles']} articles, {stats['recitals']} recitals, {len(errors)} errors")
    return stats


def main():
    parser = argparse.ArgumentParser(description="Fetch EU legislation from CELLAR")
    parser.add_argument("--law", choices=list(LAWS.keys()), help="Specific law to fetch")
    parser.add_argument("--dry", action="store_true", help="Dry run (parse only)")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    # Setup logging
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"fetch-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file),
        ],
    )

    laws_to_process = [args.law] if args.law else list(LAWS.keys())
    all_stats = {}

    for law_key in laws_to_process:
        try:
            stats = process_law(law_key, dry_run=args.dry)
            all_stats[law_key] = stats
        except Exception as e:
            logging.error(f"FAILED to process {law_key}: {e}")
            all_stats[law_key] = {"articles": 0, "recitals": 0, "errors": [str(e)]}

    # Print summary
    print("\n" + "=" * 60)
    print("COLLECTION SUMMARY")
    print("=" * 60)
    total_articles = 0
    total_recitals = 0
    total_errors = 0
    for key, stats in all_stats.items():
        status = "OK" if not stats["errors"] else f"ERRORS: {len(stats['errors'])}"
        print(f"  {LAWS[key]['short']:20s} | {stats['articles']:3d} articles | {stats['recitals']:3d} recitals | {status}")
        total_articles += stats["articles"]
        total_recitals += stats["recitals"]
        total_errors += len(stats["errors"])
    print("-" * 60)
    print(f"  {'TOTAL':20s} | {total_articles:3d} articles | {total_recitals:3d} recitals | {total_errors} errors")
    print(f"\nLog: {log_file}")


if __name__ == "__main__":
    main()
