#!/usr/bin/env python3
"""
remediate-kb.py — Normalize high-risk metadata issues in the KB.

Usage:
    python3 scripts/remediate-kb.py --task all
    python3 scripts/remediate-kb.py --task empty-lists
    python3 scripts/remediate-kb.py --task dedupe-lists
    python3 scripts/remediate-kb.py --task case-urls
    python3 scripts/remediate-kb.py --task enforcement-urls
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
LIBRARY_DIR = BASE_DIR / "library"

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

ENFORCEMENT_DIRECT_URLS = {
    "aepd-caixabank-6m-consent-transparency.md": "https://www.aepd.es/es/documento/ps-00477-2019.pdf",
    "ap-clearview-ai-30m-biometric-netherlands.md": "https://autoriteitpersoonsgegevens.nl/actueel/ap-legt-clearview-boete-op-voor-illegale-dataverzameling-voor-gezichtsherkenning",
    "ap-netflix-5m-transparency.md": "https://autoriteitpersoonsgegevens.nl/en/current/netflix-fined-for-not-properly-informing-customers",
    "ap-uber-290m-us-transfers.md": "https://www.autoriteitpersoonsgegevens.nl/actueel/ap-legt-uber-boete-op-van-290-miljoen-euro-om-doorgifte-data-chauffeurs-naar-vs",
    "bfdi-vodafone-45m-third-party-security.md": "https://www.bfdi.bund.de/SharedDocs/Pressemitteilungen/EN/2025/06_Geldbu%C3%9Fe-Vodafone.html",
    "cnil-amazon-france-32m-employee-monitoring.md": "https://www.cnil.fr/fr/node/164840",
    "cnil-criteo-40m-advertising.md": "https://www.cnil.fr/en/personalised-advertising-criteo-fined-eur-40-million",
    "cnil-facebook-60m-cookies-2022.md": "https://www.cnil.fr/sites/default/files/atoms/files/deliberation_of_the_restricted_committee_no._san-2021-024_of_31_december_2021_concerning_facebook_ireland_limited.pdf",
    "cnil-google-150m-cookies-2022.md": "https://www.cnil.fr/sites/cnil/files/atoms/files/deliberation_of_the_restricted_committee_no._san-2021-023_of_31_december_2021_concerning_google_llc_and_google_ireland_limited.pdf",
    "cnil-google-325m-cookies-gmail-ads.md": "https://www.cnil.fr/en/cookies-and-advertisements-inserted-between-emails-google-fined-325-million-euros-cnil",
    "cnil-google-50m-transparency-consent-2019.md": "https://www.cnil.fr/sites/cnil/files/atoms/files/san-2019-001.pdf",
    "cnil-orange-50m-email-ads-cookies.md": "https://www.cnil.fr/en/advertisements-inserted-among-emails-orange-fined-eu50-million",
    "cnil-shein-150m-cookies-consent.md": "https://www.cnil.fr/en/cookies-placed-without-consent-shein-fined-150-million-euros-cnil",
    "cnpd-amazon-746m-advertising.md": "https://cnpd.public.lu/en/actualites/international/2021/08/decision-amazon-2.html",
    "datatilsynet-grindr-6m-consent-special-categories.md": "https://www.datatilsynet.no/en/regulations-and-tools/regulations/avgjorelser-fra-datatilsynet/2021/gebyr-til-grindr/",
    "dpc-linkedin-310m-advertising.md": "https://www.dataprotection.ie/en/news-media/press-releases/irish-data-protection-commission-fines-linkedin-ireland-eu310-million",
    "dpc-meta-265m-data-scraping.md": "https://dataprotection.ie/index.php/en/news-media/press-releases/data-protection-commission-announces-decision-in-facebook-data-scraping-inquiry",
    "dpc-meta-91m-password-plaintext.md": "https://www.dataprotection.ie/en/news-media/press-releases/DPC-announces-91-million-fine-of-Meta",
    "dpc-meta-1200m-eu-us-transfers.md": "https://www.dataprotection.ie/en/news-media/press-releases/Data-Protection-Commission-announces-conclusion-of-inquiry-into-Meta-Ireland",
    "dpc-meta-facebook-instagram-390m-legal-basis.md": "https://www.dataprotection.ie/en/news-media/data-protection-commission-announces-conclusion-two-inquiries-meta-ireland",
    "dpc-meta-instagram-405m-children.md": "https://www.dataprotection.ie/en/resources/law/decisions/Meta-Platforms-Ireland-Limited-formerly-Facebook-Ireland-Limited-and-the-Instagram-social-media-network-September-2022",
    "dpc-tiktok-530m-china-transfers.md": "https://www.dataprotection.ie/en/news-media/latest-news/irish-data-protection-commission-fines-tiktok-eu530-million-and-orders-corrective-measures-following",
    "dpc-whatsapp-225m-transparency.md": "https://www.dataprotection.ie/en/news-media/press-releases/data-protection-commission-announces-decision-whatsapp-inquiry",
    "garante-clearview-20m-biometric.md": "https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/9751323",
    "garante-enel-energia-79m-telemarketing.md": "https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/9988921",
    "garante-openai-15m-chatgpt-ai.md": "https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10085432",
    "garante-tim-28m-telemarketing.md": "https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/9256409",
    "garante-wind-tre-17m-telemarketing.md": "https://www.garanteprivacy.it/home/docweb/-/docweb-display/print/9435901",
    "hmbfdi-hm-35m-employee-surveillance.md": "https://datenschutz-hamburg.de/fileadmin/user_upload/HmbBfDI/Pressemitteilungen/2020/2020-10-01-H_M.pdf",
    "ico-british-airways-20m-breach.md": "https://ico.org.uk/media/action-weve-taken/mpns/2618546/british-airways-plc-mpn-20201016.pdf",
    "ico-marriott-18m-data-breach.md": "https://ico.org.uk/media/action-weve-taken/mpns/2618524/marriott-international-inc-mpn-20201030.pdf",
    "imy-spotify-5m-subject-access-rights.md": "https://www.imy.se/en/news/administrative-fee-against-spotify/",
    "lfd-notebooksbilliger-10m-video-surveillance.md": "https://www.lfd.niedersachsen.de/startseite/infothek/presseinformationen/lfd-niedersachsen-verhangt-bussgeld-uber-10-4-millionen-euro-gegen-notebooksbilliger-de-196019.html",
}


def extract_frontmatter(text: str) -> tuple[str, str, str]:
    """Return frontmatter text plus the prefix/suffix delimiters."""
    if not text.startswith("---\n"):
        raise ValueError("missing starting frontmatter delimiter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("missing closing frontmatter delimiter")
    return text[:4], text[4:end], text[end:]


def load_frontmatter(path: Path) -> tuple[dict, str]:
    """Load YAML frontmatter and return the parsed dict plus original text."""
    text = path.read_text(encoding="utf-8")
    _, fm_text, _ = extract_frontmatter(text)
    data = yaml.safe_load(fm_text)
    if not isinstance(data, dict):
        raise ValueError(f"frontmatter is not a mapping in {path}")
    return data, text


def write_frontmatter(path: Path, data: dict, original_text: str) -> bool:
    """Write updated frontmatter while preserving the markdown body."""
    prefix, _, suffix = extract_frontmatter(original_text)
    new_fm = yaml.safe_dump(
        data,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=1000,
    ).strip()
    new_text = f"{prefix}{new_fm}{suffix}"
    if new_text == original_text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def normalize_empty_lists() -> int:
    """Convert null list fields to explicit empty lists."""
    updated = 0
    for rel_dir, fields in LIST_FIELDS_BY_DIR.items():
        dir_path = LIBRARY_DIR / rel_dir
        if not dir_path.exists():
            continue
        for path in sorted(dir_path.glob("*.md")):
            data, original_text = load_frontmatter(path)
            changed = False
            for field in fields:
                if field in data and data[field] is None:
                    data[field] = []
                    changed = True
            if changed and write_frontmatter(path, data, original_text):
                updated += 1
    return updated


def normalize_list_values() -> int:
    """Strip blank values and deduplicate list fields while preserving order."""
    updated = 0
    for rel_dir, fields in LIST_FIELDS_BY_DIR.items():
        dir_path = LIBRARY_DIR / rel_dir
        if not dir_path.exists():
            continue
        for path in sorted(dir_path.glob("*.md")):
            data, original_text = load_frontmatter(path)
            changed = False
            for field in fields:
                values = data.get(field)
                if not isinstance(values, list):
                    continue

                deduped = []
                seen = set()
                for value in values:
                    if value is None:
                        changed = True
                        continue
                    if isinstance(value, str):
                        cleaned = value.strip()
                        if not cleaned:
                            changed = True
                            continue
                        key = cleaned.casefold()
                        value = cleaned
                    else:
                        key = value
                    if key in seen:
                        changed = True
                        continue
                    seen.add(key)
                    deduped.append(value)

                if values != deduped:
                    data[field] = deduped
                    changed = True

            if changed and write_frontmatter(path, data, original_text):
                updated += 1
    return updated


def derive_cjeu_source_url(case_number: str) -> str | None:
    """
    Convert a case number like C-311/18 to an official EUR-Lex CELEX URL.
    Formula:
      C-311/18 -> 62018CJ0311
    """
    match = re.fullmatch(r"([A-Z])-(\d+)/(\d{2})", case_number.strip())
    if not match:
        return None

    court_code_map = {
        "C": "CJ",
        "T": "TJ",
        "F": "FJ",
    }
    court_letter, raw_number, raw_year = match.groups()
    court_code = court_code_map.get(court_letter)
    if not court_code:
        return None

    year_suffix = int(raw_year)
    year = 2000 + year_suffix if year_suffix < 50 else 1900 + year_suffix
    case_num = int(raw_number)
    celex = f"6{year}{court_code}{case_num:04d}"
    return f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{celex}"


def fix_case_source_urls() -> int:
    """Replace generic CJEU source URLs with record-level official EUR-Lex links."""
    updated = 0
    case_dir = LIBRARY_DIR / "grade-a" / "cjeu-cases"
    for path in sorted(case_dir.glob("*.md")):
        data, original_text = load_frontmatter(path)
        case_number = data.get("case_number", "")
        derived = derive_cjeu_source_url(case_number)
        if not derived or data.get("source_url") == derived:
            continue
        data["source_url"] = derived
        if write_frontmatter(path, data, original_text):
            updated += 1
    return updated

def fix_enforcement_source_urls() -> int:
    """Replace enforcement source URLs with curated record-level URLs."""
    updated = 0
    enf_dir = LIBRARY_DIR / "grade-b" / "enforcement-decisions"
    today = datetime.now(timezone.utc).date().isoformat()
    for path in sorted(enf_dir.glob("*.md")):
        data, original_text = load_frontmatter(path)
        new_url = ENFORCEMENT_DIRECT_URLS.get(path.name)
        if not new_url:
            continue
        if data.get("source_url") == new_url:
            continue
        data["source_url"] = new_url
        data["retrieved_at"] = today
        if write_frontmatter(path, data, original_text):
            updated += 1
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(description="Remediate high-risk KB metadata issues")
    parser.add_argument(
        "--task",
        choices=["all", "empty-lists", "dedupe-lists", "case-urls", "enforcement-urls"],
        default="all",
    )
    args = parser.parse_args()

    started = datetime.now(timezone.utc).isoformat()
    print(f"KB remediation started at {started}")

    if args.task in ("all", "empty-lists"):
        count = normalize_empty_lists()
        print(f"  empty lists normalized: {count}")

    if args.task in ("all", "dedupe-lists"):
        count = normalize_list_values()
        print(f"  list values deduplicated: {count}")

    if args.task in ("all", "case-urls"):
        count = fix_case_source_urls()
        print(f"  case source URLs fixed: {count}")

    if args.task in ("all", "enforcement-urls"):
        count = fix_enforcement_source_urls()
        print(f"  enforcement source URLs fixed: {count}")


if __name__ == "__main__":
    main()
