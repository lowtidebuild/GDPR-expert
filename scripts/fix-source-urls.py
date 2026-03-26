#!/usr/bin/env python3
"""
Fix source_url fields in non-GDPR legislation files.

Bug: All non-GDPR article files have source_url pointing to GDPR URLs
     (https://eur-lex.europa.eu/eli/reg/2016/679/art_N/oj/eng)
     instead of the correct legislation URL.

Correct URL patterns:
- EU AI Act:              .../eli/reg/2024/1689/art_N/oj/eng
- Data Act:               .../eli/reg/2023/2854/art_N/oj/eng
- Data Governance Act:    .../eli/reg/2022/868/art_N/oj/eng
- ePrivacy Directive:     .../eli/dir/2002/58/art_N/oj/eng
"""

import os
import re
import sys

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "library", "grade-a")

# Directory name -> correct ELI base URL (without art_N/oj/eng)
DIR_TO_URL = {
    "eu-ai-act":           "https://eur-lex.europa.eu/eli/reg/2024/1689",
    "data-act":            "https://eur-lex.europa.eu/eli/reg/2023/2854",
    "data-governance-act": "https://eur-lex.europa.eu/eli/reg/2022/868",
    "eprivacy-directive":  "https://eur-lex.europa.eu/eli/dir/2002/58",
}

# The buggy URL pattern to match
BUGGY_PATTERN = re.compile(
    r'source_url:\s*"https://eur-lex\.europa\.eu/eli/reg/2016/679/art_\d+/oj/eng"'
)

# Pattern to extract article number from frontmatter
ARTICLE_PATTERN = re.compile(r'^article:\s*(\d+)', re.MULTILINE)


def fix_file(filepath, correct_base_url):
    """Fix the source_url in a single file. Returns True if modified."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if file has the buggy URL
    if not BUGGY_PATTERN.search(content):
        return False, "no buggy URL found"

    # Extract article number from frontmatter
    match = ARTICLE_PATTERN.search(content)
    if not match:
        return False, "no article number found"

    article_num = match.group(1)
    correct_url = f'{correct_base_url}/art_{article_num}/oj/eng'

    # Replace the source_url line
    new_content = BUGGY_PATTERN.sub(
        f'source_url: "{correct_url}"',
        content
    )

    if new_content == content:
        return False, "no change after replacement"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, correct_url


def main():
    total_fixed = 0
    total_skipped = 0
    total_errors = 0

    for dir_name, base_url in DIR_TO_URL.items():
        dir_path = os.path.join(BASE, dir_name)
        if not os.path.isdir(dir_path):
            print(f"WARNING: Directory not found: {dir_path}")
            continue

        dir_fixed = 0
        print(f"\n--- {dir_name} ---")

        for filename in sorted(os.listdir(dir_path)):
            if not filename.endswith('.md'):
                continue

            filepath = os.path.join(dir_path, filename)
            fixed, info = fix_file(filepath, base_url)

            if fixed:
                dir_fixed += 1
                total_fixed += 1
                print(f"  FIXED: {filename} -> {info}")
            else:
                total_skipped += 1
                print(f"  SKIP:  {filename} ({info})")

        print(f"  Subtotal: {dir_fixed} files fixed in {dir_name}")

    print(f"\n=== SUMMARY ===")
    print(f"Total fixed:   {total_fixed}")
    print(f"Total skipped: {total_skipped}")
    print(f"Total errors:  {total_errors}")


if __name__ == "__main__":
    main()
