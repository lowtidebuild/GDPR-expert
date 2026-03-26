#!/usr/bin/env python3
"""
validate-kb.py — Validate high-risk KB integrity constraints.

Focuses on:
1. Real YAML frontmatter parsing
2. Explicit list fields (no nulls where lists are expected)
3. Case/enforcement index sync with source markdown
4. CJEU and enforcement source_url quality

Usage:
    python3 scripts/validate-kb.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
LIBRARY_DIR = BASE_DIR / "library"
INDEX_DIR = BASE_DIR / "index"

LIST_FIELDS_BY_DIR = {
    "grade-a/gdpr": ["cross_references", "related_recitals", "keywords"],
    "grade-a/gdpr-recitals": ["related_articles"],
    "grade-a/eprivacy-directive": ["cross_references", "keywords"],
    "grade-a/eu-ai-act": ["cross_references", "keywords"],
    "grade-a/eu-ai-act-recitals": ["related_articles"],
    "grade-a/data-act": ["cross_references", "keywords"],
    "grade-a/data-act-recitals": ["related_articles"],
    "grade-a/data-governance-act": ["cross_references", "keywords"],
    "grade-a/data-governance-act-recitals": ["related_articles"],
    "grade-a/cjeu-cases": ["gdpr_articles", "keywords"],
    "grade-b/enforcement-decisions": ["violated_articles", "keywords"],
}


def load_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing starting frontmatter delimiter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("missing closing frontmatter delimiter")
    data = yaml.safe_load(text[4:end])
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data


def validate_frontmatter_and_list_fields() -> list[str]:
    issues: list[str] = []
    for rel_dir, list_fields in LIST_FIELDS_BY_DIR.items():
        dir_path = LIBRARY_DIR / rel_dir
        if not dir_path.exists():
            issues.append(f"missing directory: {rel_dir}")
            continue
        for path in sorted(dir_path.glob("*.md")):
            try:
                data = load_frontmatter(path)
            except Exception as exc:
                issues.append(f"{path.relative_to(BASE_DIR)}: YAML parse failure: {exc}")
                continue
            for field in list_fields:
                if field in data and not isinstance(data[field], list):
                    issues.append(
                        f"{path.relative_to(BASE_DIR)}: expected list for {field}, got {type(data[field]).__name__}"
                    )
                    continue
                if isinstance(data.get(field), list):
                    normalized: list[str] = []
                    for item in data[field]:
                        if isinstance(item, str):
                            normalized.append(item.strip().casefold())
                        else:
                            normalized.append(str(item))
                    if any(not item for item in normalized):
                        issues.append(f"{path.relative_to(BASE_DIR)}: blank value present in {field}")
                    if len(normalized) != len(set(normalized)):
                        issues.append(f"{path.relative_to(BASE_DIR)}: duplicate values present in {field}")
    return issues


def validate_case_index() -> list[str]:
    issues: list[str] = []
    case_index_path = INDEX_DIR / "case-index.json"
    data = json.loads(case_index_path.read_text(encoding="utf-8"))
    entries = {entry["path"]: entry for entry in data["cases"]}
    case_dir = LIBRARY_DIR / "grade-a" / "cjeu-cases"

    for path in sorted(case_dir.glob("*.md")):
        rel = str(path.relative_to(BASE_DIR))
        entry = entries.get(rel)
        if not entry:
            issues.append(f"{rel}: missing from case-index.json")
            continue
        fm = load_frontmatter(path)
        checks = [
            ("source_id", "id"),
            ("title_en", "title"),
            ("judgment_date", "judgment_date"),
            ("significance", "significance"),
            ("source_url", "source_url"),
            ("gdpr_articles", "gdpr_articles"),
            ("keywords", "keywords"),
        ]
        for fm_key, index_key in checks:
            if (fm.get(fm_key) or "") != (entry.get(index_key) or ""):
                issues.append(f"{rel}: case-index mismatch for {index_key}")
                break
        source_url = fm.get("source_url", "")
        if source_url in {"https://curia.europa.eu", "https://gdprhub.eu"}:
            issues.append(f"{rel}: generic case source_url still present")
    return issues


def validate_enforcement_index() -> list[str]:
    issues: list[str] = []
    index_path = INDEX_DIR / "enforcement-index.json"
    data = json.loads(index_path.read_text(encoding="utf-8"))
    entries = {entry["path"]: entry for entry in data["decisions"]}
    enf_dir = LIBRARY_DIR / "grade-b" / "enforcement-decisions"

    for path in sorted(enf_dir.glob("*.md")):
        rel = str(path.relative_to(BASE_DIR))
        entry = entries.get(rel)
        if not entry:
            issues.append(f"{rel}: missing from enforcement-index.json")
            continue
        fm = load_frontmatter(path)
        checks = [
            ("source_id", "id"),
            ("title_en", "title"),
            ("decision_date", "decision_date"),
            ("source_url", "source_url"),
            ("violated_articles", "violated_articles"),
            ("keywords", "keywords"),
        ]
        for fm_key, index_key in checks:
            if (fm.get(fm_key) or "") != (entry.get(index_key) or ""):
                issues.append(f"{rel}: enforcement-index mismatch for {index_key}")
                break
        if not entry.get("decision_date"):
            issues.append(f"{rel}: missing decision_date in enforcement-index.json")
        if fm.get("source_url") == "https://gdprhub.eu":
            issues.append(f"{rel}: generic enforcement source_url still present")
        if "title=Special%3ASearch" in fm.get("source_url", ""):
            issues.append(f"{rel}: search fallback enforcement source_url still present")
        if str(fm.get("publisher", "")).startswith("CJEU") or str(fm.get("title_en", "")).startswith("CJEU"):
            issues.append(f"{rel}: CJEU case is misclassified as an enforcement decision")
    return issues


def main() -> int:
    issues = []
    issues.extend(validate_frontmatter_and_list_fields())
    issues.extend(validate_case_index())
    issues.extend(validate_enforcement_index())

    if issues:
        print("KB validation failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("KB validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
