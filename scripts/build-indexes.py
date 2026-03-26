#!/usr/bin/env python3
"""
build-indexes.py — Build JSON search indexes for the GDPR-expert KB

Usage:
    python3 scripts/build-indexes.py --type all
    python3 scripts/build-indexes.py --type article
    python3 scripts/build-indexes.py --type edpb
    python3 scripts/build-indexes.py --type case
    python3 scripts/build-indexes.py --type enforcement
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LIBRARY_DIR = BASE_DIR / "library"
INDEX_DIR = BASE_DIR / "index"


def parse_frontmatter(filepath: Path) -> dict:
    """Parse YAML frontmatter from a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    fm_text = text[3:end]
    result = {}
    current_key = None
    current_list = None

    for line in fm_text.split("\n"):
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        # List item
        if line.startswith("  - "):
            val = line.strip("  - ").strip().strip('"').strip("'")
            if current_list is not None:
                current_list.append(val)
            continue
        # Key: value
        match = re.match(r'^(\w[\w_]*)\s*:\s*(.*)', line)
        if match:
            key = match.group(1)
            val = match.group(2).strip().strip('"').strip("'")
            if val == "":
                # Might be start of a list
                result[key] = []
                current_key = key
                current_list = result[key]
            elif val == "null":
                result[key] = None
                current_list = None
            else:
                # Try numeric
                try:
                    result[key] = int(val)
                except ValueError:
                    result[key] = val
                current_list = None
    return result


def build_article_index():
    """Build article-index.json from all legislation directories."""
    articles = []
    law_dirs = [
        "grade-a/gdpr", "grade-a/eprivacy-directive", "grade-a/eu-ai-act",
        "grade-a/data-act", "grade-a/data-governance-act",
    ]
    for law_dir in law_dirs:
        dir_path = LIBRARY_DIR / law_dir
        if not dir_path.exists():
            continue
        for md in sorted(dir_path.glob("art*.md")):
            fm = parse_frontmatter(md)
            if not fm.get("article"):
                continue
            articles.append({
                "id": f"{dir_path.name}-art{fm['article']}",
                "law": fm.get("law", ""),
                "law_id": fm.get("law_id", ""),
                "article": str(fm["article"]),
                "chapter": fm.get("chapter", ""),
                "title": fm.get("article_title", ""),
                "path": str(md.relative_to(BASE_DIR)),
                "source_grade": fm.get("source_grade", "A"),
                "effective_date": fm.get("effective_date", ""),
                "keywords": fm.get("keywords", []) if isinstance(fm.get("keywords"), list) else [],
            })

    index = {
        "type": "article_index",
        "count": len(articles),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "articles": articles,
    }
    out = INDEX_DIR / "article-index.json"
    out.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  article-index.json: {len(articles)} articles")
    return len(articles)


def build_recital_index():
    """Build recital-index.json from all recital directories."""
    recitals = []
    recital_dirs = ["grade-a/gdpr-recitals"]
    # Also check for other law recitals that might have been saved in the law dir
    for law_dir in ["grade-a/eu-ai-act", "grade-a/data-act", "grade-a/data-governance-act"]:
        dir_path = LIBRARY_DIR / law_dir
        if dir_path.exists() and list(dir_path.glob("recital*.md")):
            recital_dirs.append(law_dir)

    for rdir in recital_dirs:
        dir_path = LIBRARY_DIR / rdir
        if not dir_path.exists():
            continue
        for md in sorted(dir_path.glob("recital*.md")):
            fm = parse_frontmatter(md)
            recital_num = fm.get("recital", "")
            if not recital_num:
                # Try to extract from filename
                m = re.search(r"recital(\d+)", md.name)
                recital_num = int(m.group(1)) if m else 0
            recitals.append({
                "id": f"{dir_path.name}-recital{recital_num}",
                "law": fm.get("law", ""),
                "law_id": fm.get("law_id", ""),
                "recital": str(recital_num),
                "path": str(md.relative_to(BASE_DIR)),
                "related_articles": fm.get("related_articles", []) if isinstance(fm.get("related_articles"), list) else [],
            })

    index = {
        "type": "recital_index",
        "count": len(recitals),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "recitals": recitals,
    }
    out = INDEX_DIR / "recital-index.json"
    out.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  recital-index.json: {len(recitals)} recitals")
    return len(recitals)


def build_edpb_document_index():
    """Build edpb-document-index.json from all EDPB directories."""
    docs = []
    edpb_dirs = [
        "grade-a/edpb-guidelines", "grade-a/edpb-opinions",
        "grade-a/edpb-recommendations", "grade-a/edpb-statements",
        "grade-a/edpb-reports", "grade-a/edpb-binding-decisions",
    ]
    for edir in edpb_dirs:
        dir_path = LIBRARY_DIR / edir
        if not dir_path.exists():
            continue
        for md in sorted(dir_path.glob("*.md")):
            fm = parse_frontmatter(md)
            docs.append({
                "id": fm.get("source_id", md.stem),
                "slug": fm.get("slug", md.stem),
                "title": fm.get("title_en", md.stem),
                "document_number": fm.get("document_number", ""),
                "document_type": fm.get("document_type", "guideline"),
                "published_date": fm.get("published_date", ""),
                "path": str(md.relative_to(BASE_DIR)),
                "source_grade": fm.get("source_grade", "A"),
                "gdpr_articles": fm.get("gdpr_articles", []) if isinstance(fm.get("gdpr_articles"), list) else [],
                "keywords": fm.get("keywords", []) if isinstance(fm.get("keywords"), list) else [],
                "conversion_quality": fm.get("conversion_quality", "unknown"),
                "char_count": fm.get("char_count", 0),
            })

    index = {
        "type": "edpb_document_index",
        "count": len(docs),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "documents": docs,
    }
    out = INDEX_DIR / "edpb-document-index.json"
    out.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  edpb-document-index.json: {len(docs)} documents")
    return len(docs)


def build_case_index():
    """Build case-index.json from CJEU cases."""
    cases = []
    case_dirs = ["grade-a/cjeu-cases"]
    # Also check old location
    old_dir = BASE_DIR / "gdpr-agent-kb" / "cjeu-cases"

    for cdir in case_dirs:
        dir_path = LIBRARY_DIR / cdir
        if not dir_path.exists():
            continue
        for md in sorted(dir_path.glob("*.md")):
            fm = parse_frontmatter(md)
            cases.append({
                "id": fm.get("source_id", md.stem),
                "slug": fm.get("slug", md.stem),
                "title": fm.get("title_en", md.stem),
                "case_number": fm.get("case_number", ""),
                "ecli": fm.get("ecli", ""),
                "judgment_date": fm.get("published_date", fm.get("judgment_date", "")),
                "path": str(md.relative_to(BASE_DIR)),
                "source_grade": "A",
                "gdpr_articles": fm.get("gdpr_articles", []) if isinstance(fm.get("gdpr_articles"), list) else [],
                "keywords": fm.get("keywords", []) if isinstance(fm.get("keywords"), list) else [],
                "significance": fm.get("significance", ""),
            })

    index = {
        "type": "case_index",
        "count": len(cases),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cases": cases,
    }
    out = INDEX_DIR / "case-index.json"
    out.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  case-index.json: {len(cases)} cases")
    return len(cases)


def build_enforcement_index():
    """Build enforcement-index.json from enforcement decisions."""
    decisions = []
    enf_dir = LIBRARY_DIR / "grade-b" / "enforcement-decisions"
    if not enf_dir.exists():
        print("  enforcement-index.json: 0 decisions (directory not found)")
        return 0

    for md in sorted(enf_dir.glob("*.md")):
        fm = parse_frontmatter(md)
        decisions.append({
            "id": fm.get("source_id", md.stem),
            "slug": fm.get("slug", md.stem),
            "title": fm.get("title_en", md.stem),
            "publisher": fm.get("publisher", ""),
            "target_entity": fm.get("target_entity", ""),
            "fine_amount": fm.get("fine_amount", ""),
            "published_date": fm.get("published_date", ""),
            "path": str(md.relative_to(BASE_DIR)),
            "source_grade": "B",
            "violated_articles": fm.get("violated_articles", []) if isinstance(fm.get("violated_articles"), list) else [],
            "keywords": fm.get("keywords", []) if isinstance(fm.get("keywords"), list) else [],
        })

    index = {
        "type": "enforcement_index",
        "count": len(decisions),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "decisions": decisions,
    }
    out = INDEX_DIR / "enforcement-index.json"
    out.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  enforcement-index.json: {len(decisions)} decisions")
    return len(decisions)


def update_source_registry():
    """Update source-registry.json with current counts."""
    reg_path = INDEX_DIR / "source-registry.json"
    registry = json.loads(reg_path.read_text()) if reg_path.exists() else {
        "type": "source_registry", "sources": {"grade-a": {}, "grade-b": {}}
    }
    registry["generated_at"] = datetime.now(timezone.utc).isoformat()

    # Count files in each directory
    dir_counts = {
        "gdpr": ("grade-a/gdpr", "art*.md"),
        "gdpr-recitals": ("grade-a/gdpr-recitals", "recital*.md"),
        "eprivacy-directive": ("grade-a/eprivacy-directive", "art*.md"),
        "eu-ai-act": ("grade-a/eu-ai-act", "art*.md"),
        "data-act": ("grade-a/data-act", "art*.md"),
        "data-governance-act": ("grade-a/data-governance-act", "art*.md"),
        "edpb-guidelines": ("grade-a/edpb-guidelines", "*.md"),
        "edpb-opinions": ("grade-a/edpb-opinions", "*.md"),
        "edpb-recommendations": ("grade-a/edpb-recommendations", "*.md"),
        "edpb-statements": ("grade-a/edpb-statements", "*.md"),
        "edpb-binding-decisions": ("grade-a/edpb-binding-decisions", "*.md"),
        "edpb-reports": ("grade-a/edpb-reports", "*.md"),
        "cjeu-cases": ("grade-a/cjeu-cases", "*.md"),
    }

    for key, (subdir, pattern) in dir_counts.items():
        dir_path = LIBRARY_DIR / subdir
        count = len(list(dir_path.glob(pattern))) if dir_path.exists() else 0
        if key not in registry["sources"].get("grade-a", {}):
            registry["sources"]["grade-a"][key] = {}
        registry["sources"]["grade-a"][key]["status"] = "complete" if count > 0 else "pending"
        registry["sources"]["grade-a"][key]["count"] = count

    # Enforcement
    enf_dir = LIBRARY_DIR / "grade-b" / "enforcement-decisions"
    enf_count = len(list(enf_dir.glob("*.md"))) if enf_dir.exists() else 0
    registry["sources"]["grade-b"]["enforcement-decisions"] = {
        "status": "complete" if enf_count > 0 else "pending",
        "count": enf_count,
    }

    # Legislative proposals
    prop_dir = LIBRARY_DIR / "grade-b" / "legislative-proposals"
    prop_count = len(list(prop_dir.glob("*.md"))) if prop_dir.exists() else 0
    registry["sources"]["grade-b"]["legislative-proposals"] = {
        "status": "complete" if prop_count > 0 else "pending",
        "count": prop_count,
    }

    reg_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  source-registry.json: updated")


def main():
    parser = argparse.ArgumentParser(description="Build search indexes")
    parser.add_argument("--type", choices=["all", "article", "recital", "edpb", "case", "enforcement"],
                       default="all")
    args = parser.parse_args()

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    print("Building indexes...")

    totals = {}
    if args.type in ("all", "article"):
        totals["articles"] = build_article_index()
    if args.type in ("all", "recital"):
        totals["recitals"] = build_recital_index()
    if args.type in ("all", "edpb"):
        totals["edpb_docs"] = build_edpb_document_index()
    if args.type in ("all", "case"):
        totals["cases"] = build_case_index()
    if args.type in ("all", "enforcement"):
        totals["enforcement"] = build_enforcement_index()

    update_source_registry()

    print(f"\nTotal indexed: {sum(totals.values())} items across {len(totals)} indexes")


if __name__ == "__main__":
    main()
