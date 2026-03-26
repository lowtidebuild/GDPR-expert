#!/usr/bin/env python3
"""
populate-phase5.py — Create markdown KB files from Phase 5 research data.

Processes:
1. Additional CJEU cases (34)
2. Art. 65 binding decisions (10)
3. Additional EDPB Opinions (25)
4. Additional enforcement decisions (25)
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def make_slug(text: str) -> str:
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")[:80]


def yaml_list(items: list) -> str:
    if not items:
        return ""
    return "\n".join(f'  - "{item}"' for item in items)


def write_cjeu_cases():
    """Create markdown files for additional CJEU cases."""
    catalog_path = BASE_DIR / "library" / "grade-a" / "cjeu-cases" / "additional-cases-catalog.json"
    if not catalog_path.exists():
        print("CJEU catalog not found")
        return 0

    cases = json.loads(catalog_path.read_text())
    output_dir = BASE_DIR / "library" / "grade-a" / "cjeu-cases"
    count = 0

    for case in cases:
        case_num = case.get("case_number", "")
        slug = make_slug(case_num)
        filepath = output_dir / f"{slug}.md"

        if filepath.exists():
            continue

        gdpr_arts = case.get("gdpr_articles", [])
        keywords = case.get("keywords", [])
        summary = case.get("summary", "")
        parties = case.get("parties", case.get("title", ""))

        content = f"""---
# === Identification ===
source_id: "a-precedent-{slug}"
slug: "{slug}"
title_en: "{parties.replace('"', "'")}"
case_number: "{case_num}"
ecli: "{case.get('ecli', '')}"
document_type: precedent
source_grade: A
publisher: "Court of Justice of the European Union (CJEU)"
judgment_date: "{case.get('judgment_date', '')}"
source_url: "https://curia.europa.eu"
jurisdiction: EU
significance: "{case.get('significance', 'important')}"
retrieved_at: "{NOW}"

# === Related GDPR Articles ===
gdpr_articles:
{yaml_list(gdpr_arts)}

# === Search Metadata ===
keywords:
{yaml_list(keywords)}
---

## {case_num} — {case.get('title', '')}

**Parties:** {parties}

**Judgment Date:** {case.get('judgment_date', 'Unknown')}

**ECLI:** {case.get('ecli', 'Unknown')}

**Significance:** {case.get('significance', 'important')}

### Key Holding

{summary}

### Related GDPR Articles

{', '.join(gdpr_arts) if gdpr_arts else 'N/A'}
"""
        filepath.write_text(content, encoding="utf-8")
        count += 1

    print(f"  CJEU cases: {count} new files created")
    return count


def write_art65_decisions():
    """Create markdown files for Art. 65 binding decisions."""
    research_path = BASE_DIR / "scripts" / "logs" / "art65-and-opinions-research.json"
    if not research_path.exists():
        print("Art. 65 research not found")
        return 0

    data = json.loads(research_path.read_text())
    decisions = data.get("part1_art65_binding_decisions", [])
    output_dir = BASE_DIR / "library" / "grade-a" / "edpb-binding-decisions"
    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0

    for dec in decisions:
        dec_num = dec.get("decision_number", dec.get("number", f"bd-{count}"))
        slug = make_slug(dec_num)
        filepath = output_dir / f"{slug}.md"

        if filepath.exists():
            continue

        title = dec.get("title", dec_num)
        target = dec.get("target_company", dec.get("target", ""))
        fine = dec.get("fine_amount", dec.get("fine", ""))
        date = dec.get("date", dec.get("decision_date", ""))
        issue = dec.get("key_issue", dec.get("issue", ""))
        summary = dec.get("summary", "")
        gdpr_arts = dec.get("gdpr_articles", dec.get("gdpr_articles_at_stake", []))
        pdf_url = dec.get("pdf_url", "")
        dpas = dec.get("dpas_involved", dec.get("parties", ""))

        content = f"""---
# === Identification ===
source_id: "a-binding-decision-{slug}"
slug: "{slug}"
title_en: "{str(title).replace('"', "'")}"
decision_number: "{dec_num}"
document_type: binding_decision
source_grade: A
publisher: "European Data Protection Board (EDPB)"
decision_date: "{date}"
source_url: "{pdf_url}"
jurisdiction: EU
target_entity: "{str(target).replace('"', "'")}"
fine_amount: "{fine}"
retrieved_at: "{NOW}"

# === Related GDPR Articles ===
gdpr_articles:
{yaml_list(gdpr_arts if isinstance(gdpr_arts, list) else [str(gdpr_arts)])}

# === Search Metadata ===
keywords:
  - "binding decision"
  - "Article 65"
  - "dispute resolution"
{yaml_list(dec.get('keywords', []))}
---

## {dec_num} — {title}

**Target Entity:** {target}

**Fine Amount:** {fine}

**Decision Date:** {date}

**DPAs Involved:** {dpas}

**Key Issue:** {issue}

### Summary

{summary}

### Related GDPR Articles

{', '.join(gdpr_arts) if isinstance(gdpr_arts, list) else str(gdpr_arts)}
"""
        filepath.write_text(content, encoding="utf-8")
        count += 1

    print(f"  Art. 65 binding decisions: {count} new files created")
    return count


def write_edpb_opinions():
    """Create markdown files for additional EDPB opinions."""
    research_path = BASE_DIR / "scripts" / "logs" / "art65-and-opinions-research.json"
    if not research_path.exists():
        print("EDPB opinions research not found")
        return 0

    data = json.loads(research_path.read_text())
    opinions = data.get("part2_edpb_opinions_impactful", [])
    output_dir = BASE_DIR / "library" / "grade-a" / "edpb-opinions"
    count = 0

    for op in opinions:
        op_num = op.get("opinion_number", op.get("number", f"opinion-{count}"))
        slug = make_slug(op_num)
        filepath = output_dir / f"{slug}.md"

        if filepath.exists():
            continue

        title = op.get("title", "")
        date = op.get("publication_date", op.get("date", ""))
        pdf_url = op.get("pdf_url", "")
        gdpr_arts = op.get("related_gdpr_articles", op.get("gdpr_articles", []))
        keywords = op.get("keywords", [])
        summary = op.get("summary", op.get("one_sentence_summary", ""))

        content = f"""---
# === Identification ===
source_id: "a-opinion-{slug}"
slug: "{slug}"
title_en: "{str(title).replace('"', "'")}"
document_number: "{op_num}"
document_type: opinion
source_grade: A
publisher: "European Data Protection Board (EDPB)"
published_date: "{date}"
source_url: "{pdf_url}"
jurisdiction: EU
retrieved_at: "{NOW}"

# === Related GDPR Articles ===
gdpr_articles:
{yaml_list(gdpr_arts if isinstance(gdpr_arts, list) else [str(gdpr_arts)])}

# === Search Metadata ===
keywords:
{yaml_list(keywords if isinstance(keywords, list) else [str(keywords)])}
---

## {op_num} — {title}

**Published:** {date}

### Summary

{summary}

### Related GDPR Articles

{', '.join(gdpr_arts) if isinstance(gdpr_arts, list) else str(gdpr_arts)}
"""
        filepath.write_text(content, encoding="utf-8")
        count += 1

    print(f"  EDPB Opinions: {count} new files created")
    return count


def write_enforcement_decisions():
    """Create markdown files for additional enforcement decisions."""
    research_path = BASE_DIR / "scripts" / "logs" / "enforcement-research.json"
    if not research_path.exists():
        print("Enforcement research not found")
        return 0

    data = json.loads(research_path.read_text())
    decisions = data.get("decisions", [])
    output_dir = BASE_DIR / "library" / "grade-b" / "enforcement-decisions"
    count = 0

    for dec in decisions:
        slug = dec.get("slug", make_slug(dec.get("title", f"decision-{count}")))
        filepath = output_dir / f"{slug}.md"

        if filepath.exists():
            continue

        title = dec.get("title", "")
        dpa = dec.get("dpa", "")
        target = dec.get("target_entity", "")
        fine = dec.get("fine_amount", "")
        date = dec.get("decision_date", "")
        violated = dec.get("violated_articles", [])
        keywords = dec.get("keywords", [])
        significance = dec.get("significance", "important")
        summary = dec.get("summary", "")

        content = f"""---
# === Identification ===
source_id: "b-decision-{slug}"
slug: "{slug}"
title_en: "{str(title).replace('"', "'")}"
document_type: decision
source_grade: B
publisher: "{str(dpa).replace('"', "'")}"
target_entity: "{str(target).replace('"', "'")}"
fine_amount: "{fine}"
decision_date: "{date}"
source_url: "https://gdprhub.eu"
jurisdiction: EU
significance: "{significance}"
retrieved_at: "{NOW}"

# === Violated Articles ===
violated_articles:
{yaml_list(violated if isinstance(violated, list) else [str(violated)])}

# === Search Metadata ===
keywords:
{yaml_list(keywords if isinstance(keywords, list) else [str(keywords)])}
---

## {title}

**DPA:** {dpa}

**Target Entity:** {target}

**Fine Amount:** {fine}

**Decision Date:** {date}

**Significance:** {significance}

### Summary

{summary}

### Violated Articles

{', '.join(violated) if isinstance(violated, list) else str(violated)}
"""
        filepath.write_text(content, encoding="utf-8")
        count += 1

    print(f"  Enforcement decisions: {count} new files created")
    return count


def main():
    print("Phase 5: Populating KB with research data...")
    total = 0
    total += write_cjeu_cases()
    total += write_art65_decisions()
    total += write_edpb_opinions()
    total += write_enforcement_decisions()
    print(f"\nTotal new files: {total}")


if __name__ == "__main__":
    main()
