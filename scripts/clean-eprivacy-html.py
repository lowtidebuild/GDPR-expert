#!/usr/bin/env python3
"""
Clean HTML artifacts from ePrivacy Directive markdown files.

Removes:
- HTML tags (e.g., <div class="eli-subdivision", </div>)
- EUR-Lex amendment markers (▼M1, ▼M2, ▼B, ►M2, ◄, etc.)
- Standalone id="..." attribute lines
- Blank lines left behind after removal (collapses multiple blanks to max 1)

Preserves:
- YAML frontmatter (everything between the two --- delimiters)
- Actual article text content
- Markdown formatting (## headers, etc.)
- Paragraph numbering and structure
"""

import os
import re
import glob


EPRIVACY_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "library", "grade-a", "eprivacy-directive"
)


def split_frontmatter(content: str) -> tuple[str, str]:
    """Split file into frontmatter and body. Returns (frontmatter, body)."""
    # Match the pattern: starts with ---, then content, then ---
    match = re.match(r'^(---\n.*?\n---)\n(.*)', content, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return "", content


def clean_body(body: str) -> tuple[str, list[str]]:
    """Clean HTML artifacts from body text. Returns (cleaned_body, changes)."""
    changes = []
    original = body

    # 1. Remove lines that are just id="art_N"> (standalone id attributes)
    pattern = r'^id="[^"]*">\s*$'
    matches = re.findall(pattern, body, re.MULTILINE)
    if matches:
        body = re.sub(pattern, '', body, flags=re.MULTILINE)
        changes.append(f"Removed {len(matches)} standalone id attribute line(s)")

    # 2. Remove HTML tags (opening and closing, including partial/unclosed tags)
    # Matches <tag ...> and <tag ... (unclosed, as seen in the files)
    html_tag_pattern = r'</?[a-zA-Z][^>]*>?'
    html_matches = re.findall(html_tag_pattern, body)
    if html_matches:
        # Only remove lines that are ENTIRELY an HTML tag (possibly with whitespace)
        # This avoids accidentally removing HTML-like content in article text
        full_line_html = r'^\s*</?[a-zA-Z][^>]*>?\s*$'
        line_matches = re.findall(full_line_html, body, re.MULTILINE)
        if line_matches:
            body = re.sub(full_line_html, '', body, flags=re.MULTILINE)
            changes.append(f"Removed {len(line_matches)} HTML tag line(s)")

    # 3. Remove EUR-Lex amendment markers
    # Lines that are just ▼M1, ▼M2, ▼B, ►M2, etc. (possibly with trailing dashes)
    amendment_pattern = r'^\s*[▼►◄][A-Z0-9]+[\s—]*$'
    amendment_matches = re.findall(amendment_pattern, body, re.MULTILINE)
    if amendment_matches:
        body = re.sub(amendment_pattern, '', body, flags=re.MULTILINE)
        changes.append(f"Removed {len(amendment_matches)} amendment marker line(s)")

    # 4. Remove inline ►M2 / ◄ markers (e.g., "►M2\nSecurity of processing ◄")
    # Handle ►XX at start of line followed by text on next line with ◄
    inline_open = r'►[A-Z0-9]+'
    inline_close = r'\s*◄'
    inline_open_matches = re.findall(inline_open, body)
    inline_close_matches = re.findall(inline_close, body)
    if inline_open_matches:
        body = re.sub(inline_open, '', body)
        changes.append(f"Removed {len(inline_open_matches)} inline ► marker(s)")
    if inline_close_matches:
        body = re.sub(inline_close, '', body)
        changes.append(f"Removed {len(inline_close_matches)} inline ◄ marker(s)")

    # 5. Remove duplicate "Article N" line after the ## header
    # Pattern: "## Article N — \n\nArticle N\n" -> keep only the ## header
    # The standalone "Article N" line is redundant with the ## header
    art_dup_pattern = r'(## Article \d+[a-z]? — [^\n]*\n)\n+Article \d+[a-z]?\n'
    art_dup_matches = re.findall(art_dup_pattern, body)
    if art_dup_matches:
        body = re.sub(art_dup_pattern, r'\1', body)
        changes.append(f"Removed {len(art_dup_matches)} duplicate Article title line(s)")

    # 6. Collapse multiple blank lines into at most one
    body = re.sub(r'\n{3,}', '\n\n', body)

    # 7. Remove trailing whitespace on each line
    body = re.sub(r'[ \t]+$', '', body, flags=re.MULTILINE)

    # 8. Ensure file ends with exactly one newline
    body = body.rstrip('\n') + '\n'

    if body != original:
        if not changes:
            changes.append("Whitespace normalization only")

    return body, changes


def process_file(filepath: str) -> list[str]:
    """Process a single markdown file. Returns list of changes made."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter, body = split_frontmatter(content)
    if not frontmatter:
        return [f"WARNING: No frontmatter found, skipping"]

    cleaned_body, changes = clean_body(body)

    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter + '\n' + cleaned_body)

    return changes


def main():
    md_files = sorted(glob.glob(os.path.join(EPRIVACY_DIR, "art*.md")))
    print(f"Found {len(md_files)} article files in {EPRIVACY_DIR}\n")

    total_changes = 0
    for filepath in md_files:
        filename = os.path.basename(filepath)
        changes = process_file(filepath)
        if changes:
            total_changes += len(changes)
            print(f"  {filename}:")
            for c in changes:
                print(f"    - {c}")
        else:
            print(f"  {filename}: no changes needed")

    print(f"\nDone. {total_changes} change(s) across {len(md_files)} files.")


if __name__ == "__main__":
    main()
