#!/usr/bin/env python3
"""
fill-keywords.py — Fill empty keywords arrays in legislation files.
Extracts keywords from article_title and body text.
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LIBRARY_DIR = BASE_DIR / "library"

# Common legal stop words to exclude
STOP_WORDS = {
    "the", "of", "and", "or", "to", "in", "for", "a", "an", "by", "on",
    "with", "as", "at", "from", "is", "that", "this", "it", "be", "are",
    "was", "were", "been", "being", "have", "has", "had", "do", "does",
    "did", "will", "shall", "may", "can", "could", "would", "should",
    "must", "not", "no", "nor", "so", "if", "but", "than", "such",
    "which", "who", "whom", "whose", "where", "when", "how", "what",
    "its", "his", "her", "their", "our", "your", "any", "all", "each",
    "every", "both", "more", "most", "other", "some", "only", "own",
    "same", "into", "through", "about", "between", "after", "before",
    "during", "without", "under", "above", "below", "up", "down",
    "out", "off", "over", "again", "further", "then", "once", "also",
    "very", "just", "because", "against", "upon", "within", "whether",
    "while", "although", "since", "until", "unless", "however",
    "therefore", "thus", "hence", "accordingly", "moreover", "furthermore",
    "including", "accordance", "pursuant", "herein", "thereof", "whereas",
    "inter", "alia", "referred", "regard", "respect", "particular",
    "provided", "ensure", "necessary", "appropriate", "relevant",
    "set", "laid", "provide", "apply", "applies", "applicable",
    "paragraph", "article", "point", "section", "chapter", "regulation",
    "directive", "member", "state", "states", "union", "european",
    "commission", "council", "parliament",
}

# Legal domain terms worth keeping as keywords
LEGAL_TERMS = {
    "personal data", "data subject", "controller", "processor",
    "consent", "legitimate interest", "data protection",
    "supervisory authority", "privacy", "transparency",
    "data breach", "notification", "security", "encryption",
    "pseudonymisation", "anonymisation", "profiling",
    "automated decision", "data portability", "right to erasure",
    "right of access", "rectification", "restriction",
    "cross-border", "transfer", "adequacy", "safeguards",
    "binding corporate rules", "standard contractual clauses",
    "impact assessment", "prior consultation",
    "codes of conduct", "certification", "penalties", "fines",
    "artificial intelligence", "high-risk", "ai system",
    "provider", "deployer", "general-purpose",
    "connected product", "data holder", "data recipient",
    "interoperability", "smart contract", "cloud",
    "switching", "data sharing", "data access",
    "public sector", "altruism", "intermediation",
    "biometric", "health data", "genetic data",
    "employment", "children", "minor",
    "cookie", "electronic communications", "traffic data",
    "direct marketing", "spam", "confidentiality",
    "judicial remedy", "compensation", "liability",
    "representative", "record of processing",
    "data protection officer", "dpo",
    "fundamental rights", "charter",
}


def extract_keywords_from_title(title):
    """Extract meaningful words from article title."""
    if not title:
        return []
    # Clean and split
    words = re.findall(r"[a-zA-Z'-]+", title.lower())
    return [w for w in words if w not in STOP_WORDS and len(w) > 2]


def extract_keywords_from_body(body, max_keywords=6):
    """Extract key legal terms from body text."""
    body_lower = body.lower()
    found = []

    # Check for multi-word legal terms first
    for term in LEGAL_TERMS:
        if term in body_lower:
            found.append(term)

    # Also extract single important nouns from first 800 chars
    first_part = body_lower[:800]
    words = re.findall(r"[a-zA-Z'-]+", first_part)
    word_freq = {}
    for w in words:
        if w not in STOP_WORDS and len(w) > 3:
            word_freq[w] = word_freq.get(w, 0) + 1

    # Add high-frequency single words not already covered
    for w, count in sorted(word_freq.items(), key=lambda x: -x[1]):
        if count >= 2 and w not in " ".join(found):
            found.append(w)
        if len(found) >= max_keywords:
            break

    return found[:max_keywords]


def process_file(filepath):
    """Process a single markdown file to fill empty keywords."""
    content = filepath.read_text(encoding="utf-8")

    # Check if file has frontmatter
    if not content.startswith("---"):
        return False

    # Split frontmatter and body
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False

    frontmatter = parts[1]
    body = parts[2]

    # Check if keywords field exists and is empty
    # Match: keywords:\n (followed by non-list-item or end of frontmatter)
    has_empty_keywords = bool(re.search(r"keywords:\s*$", frontmatter, re.MULTILINE))
    if not has_empty_keywords:
        return False

    # Extract article_title
    title_match = re.search(r'article_title:\s*"([^"]*)"', frontmatter)
    title = title_match.group(1) if title_match else ""

    # Also try title_en for non-legislation files
    if not title:
        title_match = re.search(r'title_en:\s*"([^"]*)"', frontmatter)
        title = title_match.group(1) if title_match else ""

    # Extract keywords
    title_keywords = extract_keywords_from_title(title)
    body_keywords = extract_keywords_from_body(body)

    # Combine and deduplicate
    all_keywords = []
    seen = set()
    for kw in title_keywords + body_keywords:
        kw_lower = kw.lower()
        if kw_lower not in seen:
            seen.add(kw_lower)
            all_keywords.append(kw_lower)

    if not all_keywords:
        return False

    # Limit to 8 keywords
    all_keywords = all_keywords[:8]

    # Build replacement
    kw_lines = "\n".join(f'  - "{kw}"' for kw in all_keywords)
    new_keywords = f"keywords:\n{kw_lines}"

    # Replace empty keywords field
    new_content = re.sub(r"keywords:\s*$", new_keywords, content, count=1, flags=re.MULTILINE)

    if new_content != content:
        filepath.write_text(new_content, encoding="utf-8")
        return True
    return False


def main():
    updated = 0
    checked = 0

    for grade_dir in ["grade-a", "grade-b"]:
        lib_path = LIBRARY_DIR / grade_dir
        if not lib_path.exists():
            continue

        for md_file in sorted(lib_path.rglob("*.md")):
            checked += 1
            if process_file(md_file):
                updated += 1
                print(f"  Updated: {md_file.relative_to(LIBRARY_DIR)}")

    print(f"\nChecked {checked} files, updated {updated} with keywords")


if __name__ == "__main__":
    main()
