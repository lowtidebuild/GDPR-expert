#!/usr/bin/env python3
"""
fetch-edpb-guidelines.py — Download EDPB PDFs and convert to markdown

Reads the catalog at library/edpb_documents_catalog.json,
downloads PDFs, converts via markitdown, adds frontmatter.
"""

import json
import logging
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sanitize import sanitize_text

BASE_DIR = Path(__file__).resolve().parent.parent
CATALOG_PATH = BASE_DIR / "library" / "edpb_documents_catalog.json"
PDF_DIR = BASE_DIR / "library" / "inbox" / "edpb-pdfs"
LOG_DIR = BASE_DIR / "scripts" / "logs"

# Output directories by type
OUTPUT_DIRS = {
    "guideline": BASE_DIR / "library" / "grade-a" / "edpb-guidelines",
    "recommendation": BASE_DIR / "library" / "grade-a" / "edpb-recommendations",
    "opinion": BASE_DIR / "library" / "grade-a" / "edpb-opinions",
    "statement": BASE_DIR / "library" / "grade-a" / "edpb-statements",
    "report": BASE_DIR / "library" / "grade-a" / "edpb-reports",
    "endorsement": BASE_DIR / "library" / "grade-a" / "edpb-guidelines",  # endorsed WP29 → guidelines
}

EDPB_BASE = "https://www.edpb.europa.eu"


def download_pdf(url: str, dest: Path, max_retries: int = 3) -> bool:
    """Download a PDF file with retries."""
    if dest.exists() and dest.stat().st_size > 1000:
        return True  # Already downloaded

    # Fix relative URLs
    if url.startswith("/"):
        url = EDPB_BASE + url

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "GDPR-Expert/1.0 (legal research)")
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
                if len(data) < 1000:
                    logging.warning(f"Suspiciously small PDF ({len(data)} bytes): {url}")
                    return False
                dest.write_bytes(data)
                return True
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            logging.warning(f"Download failed (attempt {attempt+1}): {url} — {e}")
        except Exception as e:
            logging.warning(f"Download error (attempt {attempt+1}): {url} — {e}")
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)
    return False


def convert_pdf_to_md(pdf_path: Path) -> str:
    """Convert PDF to markdown using markitdown."""
    try:
        result = subprocess.run(
            ["markitdown", str(pdf_path)],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
        else:
            logging.warning(f"markitdown failed for {pdf_path.name}: {result.stderr[:200]}")
            return ""
    except subprocess.TimeoutExpired:
        logging.warning(f"markitdown timeout for {pdf_path.name}")
        return ""
    except Exception as e:
        logging.warning(f"markitdown error for {pdf_path.name}: {e}")
        return ""


def make_slug(doc: dict) -> str:
    """Create a filename slug from document metadata."""
    doc_num = doc.get("document_number", "")
    # Clean up document number for filename
    slug = doc_num.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    if not slug:
        slug = f"edpb-doc-{doc.get('id', 'unknown')}"
    return slug


def assess_quality(md_content: str) -> str:
    """Assess conversion quality."""
    if not md_content:
        return "failed"
    char_count = len(md_content)
    line_count = md_content.count("\n")
    heading_count = len(re.findall(r"^#{1,3}\s", md_content, re.MULTILINE))

    if char_count < 2000:
        return "needs-review"
    if heading_count < 2:
        return "needs-review"
    if line_count < 50:
        return "needs-review"
    return "good"


def generate_frontmatter(doc: dict, md_content: str, quality: str) -> str:
    """Generate YAML frontmatter for an EDPB document."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    doc_type = doc.get("type", "guideline")
    slug = make_slug(doc)

    grade_prefix = "a" if doc_type in ("guideline", "recommendation", "opinion") else "b"

    lines = ["---"]
    lines.append(f'# === Identification ===')
    lines.append(f'source_id: "{grade_prefix}-{doc_type}-{slug}"')
    lines.append(f'slug: "{slug}"')
    lines.append(f'title_en: "{doc.get("title", "").replace(chr(34), chr(39))}"')
    lines.append(f'document_number: "{doc.get("document_number", "")}"')
    lines.append(f'document_type: "{doc_type}"')
    lines.append(f'status: "{doc.get("status", "adopted")}"')
    lines.append(f'')
    lines.append(f'# === Source ===')
    lines.append(f'source_grade: "A"')
    lines.append(f'publisher: "European Data Protection Board (EDPB)"')
    lines.append(f'published_date: "{doc.get("publication_date", "")}"')
    lines.append(f'source_url: "{doc.get("pdf_url", "")}"')
    lines.append(f'original_format: pdf')
    lines.append(f'jurisdiction: EU')
    lines.append(f'retrieved_at: "{now}"')
    lines.append(f'conversion_quality: "{quality}"')
    lines.append(f'char_count: {len(md_content)}')
    lines.append(f'')
    lines.append(f'# === Related GDPR Articles ===')
    lines.append(f'gdpr_articles:')
    for art in doc.get("gdpr_articles", []):
        lines.append(f'  - "{art}"')
    lines.append(f'')
    lines.append(f'# === Search Metadata ===')
    lines.append(f'keywords:')
    for kw in doc.get("keywords", []):
        lines.append(f'  - "{kw}"')
    lines.append("---")
    return "\n".join(lines)


def process_document(doc: dict, stats: dict):
    """Download, convert, and save one EDPB document."""
    doc_id = doc.get("id", "?")
    title = doc.get("title", "Unknown")[:60]
    pdf_url = doc.get("pdf_url", "")
    doc_type = doc.get("type", "guideline")

    if not pdf_url:
        logging.warning(f"[{doc_id}] No PDF URL — skipping: {title}")
        stats["skipped"] += 1
        return

    slug = make_slug(doc)
    pdf_path = PDF_DIR / f"{slug}.pdf"
    output_dir = OUTPUT_DIRS.get(doc_type, OUTPUT_DIRS["guideline"])
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / f"{slug}.md"

    # Skip if already processed
    if md_path.exists() and md_path.stat().st_size > 500:
        logging.info(f"[{doc_id}] Already exists — skipping: {title}")
        stats["existing"] += 1
        return

    # Download
    logging.info(f"[{doc_id}] Downloading: {title}")
    if not download_pdf(pdf_url, pdf_path):
        logging.error(f"[{doc_id}] Download FAILED: {title}")
        stats["download_failed"] += 1
        stats["errors"].append(f"[{doc_id}] Download failed: {title}")
        return

    # Convert
    logging.info(f"[{doc_id}] Converting: {pdf_path.name}")
    md_content = convert_pdf_to_md(pdf_path)
    if not md_content:
        logging.error(f"[{doc_id}] Conversion FAILED: {title}")
        stats["convert_failed"] += 1
        stats["errors"].append(f"[{doc_id}] Conversion failed: {title}")
        return

    # Assess quality
    quality = assess_quality(md_content)

    # Sanitize markitdown output before it touches the KB.
    md_content, audit = sanitize_text(md_content)

    # Generate frontmatter + write
    frontmatter = generate_frontmatter(doc, md_content, quality)
    full_content = frontmatter + "\n\n" + md_content
    md_path.write_text(full_content, encoding="utf-8")

    if audit:
        audit_path = md_path.with_suffix(md_path.suffix + ".audit.json")
        audit_path.write_text(
            json.dumps({"source": str(pdf_path), "matches": audit}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        logging.warning(f"[{doc_id}] Injection patterns sanitized: {len(audit)} match(es) -> {audit_path.name}")

    stats["success"] += 1
    stats["by_quality"][quality] = stats["by_quality"].get(quality, 0) + 1
    logging.info(f"[{doc_id}] OK ({quality}): {title} → {md_path.name}")


def main():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    log_file = LOG_DIR / f"edpb-fetch-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file),
        ],
    )

    # Load catalog
    catalog = json.loads(CATALOG_PATH.read_text())
    docs = catalog.get("documents", [])
    logging.info(f"Loaded catalog: {len(docs)} documents")

    stats = {
        "total": len(docs),
        "success": 0,
        "existing": 0,
        "skipped": 0,
        "download_failed": 0,
        "convert_failed": 0,
        "by_quality": {},
        "errors": [],
    }

    for i, doc in enumerate(docs):
        logging.info(f"--- [{i+1}/{len(docs)}] ---")
        process_document(doc, stats)
        # Be polite to EDPB servers
        if i > 0 and i % 5 == 0:
            time.sleep(1)

    # Summary
    print("\n" + "=" * 60)
    print("EDPB COLLECTION SUMMARY")
    print("=" * 60)
    print(f"  Total in catalog:    {stats['total']}")
    print(f"  Successfully saved:  {stats['success']}")
    print(f"  Already existed:     {stats['existing']}")
    print(f"  Skipped (no URL):    {stats['skipped']}")
    print(f"  Download failed:     {stats['download_failed']}")
    print(f"  Conversion failed:   {stats['convert_failed']}")
    print(f"  Quality breakdown:   {stats['by_quality']}")
    if stats["errors"]:
        print(f"\n  ERRORS ({len(stats['errors'])}):")
        for err in stats["errors"]:
            print(f"    {err}")
    print(f"\nLog: {log_file}")


if __name__ == "__main__":
    main()
