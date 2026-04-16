#!/usr/bin/env python3
"""
audit_prompt_injection.py — Read-only retroactive scan for prompt-injection markers.

Scans existing markdown files under a root directory (default: library/) using the
same pattern set as scripts/sanitize.py, but does not modify the source files.

Usage:
    python3 scripts/audit_prompt_injection.py
    python3 scripts/audit_prompt_injection.py --root library \
        --report-json docs/security/2026-04-kb-prompt-injection-audit.json \
        --report-md docs/security/2026-04-kb-prompt-injection-audit.md
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from sanitize import sanitize_text

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = BASE_DIR / "library"


def display_path(path: Path, base: Path) -> str:
    """Return a stable display path, relative when possible."""
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def split_frontmatter(text: str) -> tuple[int, str]:
    """Return (body_line_offset, body_text), preserving line numbers for audit entries."""
    if not text.startswith("---\n"):
        return 0, text

    closing = text.find("\n---\n", 4)
    if closing == -1:
        return 0, text

    body_start = closing + len("\n---\n")
    body_offset = text[:body_start].count("\n")
    return body_offset, text[body_start:]


def audit_markdown_file(path: Path, root: Path) -> dict | None:
    """Return a file-level audit record when matches are present, otherwise None."""
    text = path.read_text(encoding="utf-8")
    line_offset, body = split_frontmatter(text)
    _, matches = sanitize_text(body)
    if not matches:
        return None

    adjusted = []
    for match in matches:
        adjusted.append({
            "pattern": match["pattern"],
            "match": match["match"],
            "line": match["line"] + line_offset,
            "col": match["col"],
        })

    return {
        "path": display_path(path, root.parent if root != BASE_DIR else BASE_DIR),
        "match_count": len(adjusted),
        "matches": adjusted,
    }


def audit_tree(root: Path) -> dict:
    """Scan markdown files under root and return a summary report."""
    files = sorted(path for path in root.rglob("*.md") if path.is_file())
    findings = []
    pattern_counter: Counter[str] = Counter()

    for path in files:
        result = audit_markdown_file(path, root)
        if not result:
            continue
        findings.append(result)
        pattern_counter.update(match["pattern"] for match in result["matches"])

    findings.sort(key=lambda item: (-item["match_count"], item["path"]))
    generated_at = datetime.now(timezone.utc).isoformat()
    return {
        "generated_at": generated_at,
        "root": display_path(root, BASE_DIR),
        "scanned_files": len(files),
        "files_with_matches": len(findings),
        "total_matches": sum(item["match_count"] for item in findings),
        "pattern_counts": dict(sorted(pattern_counter.items())),
        "findings": findings,
    }


def render_markdown(report: dict) -> str:
    """Render a human-friendly markdown report."""
    lines = [
        "# KB Prompt-Injection Audit",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Root: `{report['root']}`",
        f"- Scanned markdown files: `{report['scanned_files']}`",
        f"- Files with matches: `{report['files_with_matches']}`",
        f"- Total matches: `{report['total_matches']}`",
        "",
    ]

    if report["pattern_counts"]:
        lines.extend([
            "## Pattern Counts",
            "",
            "| Pattern | Count |",
            "|---|---:|",
        ])
        for pattern, count in report["pattern_counts"].items():
            lines.append(f"| `{pattern}` | {count} |")
        lines.append("")

    lines.extend([
        "## Findings",
        "",
    ])

    if not report["findings"]:
        lines.append("No matches detected in the scanned markdown corpus.")
        lines.append("")
        return "\n".join(lines)

    for finding in report["findings"]:
        lines.append(f"### `{finding['path']}`")
        lines.append("")
        lines.append(f"- Match count: `{finding['match_count']}`")
        for match in finding["matches"]:
            excerpt = match["match"].replace("\n", "\\n")
            lines.append(
                f"- `{match['pattern']}` at line {match['line']}, col {match['col']}: `{excerpt}`"
            )
        lines.append("")

    return "\n".join(lines)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only audit for prompt-injection markers in existing markdown files."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="Root directory to scan. Defaults to library/.",
    )
    parser.add_argument("--report-json", type=Path, help="Optional JSON report output path.")
    parser.add_argument("--report-md", type=Path, help="Optional Markdown report output path.")
    parser.add_argument(
        "--fail-on-match",
        action="store_true",
        help="Exit 1 if any matches are found.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    root = args.root if args.root.is_absolute() else (BASE_DIR / args.root)
    report = audit_tree(root)

    if args.report_json:
        json_path = args.report_json if args.report_json.is_absolute() else BASE_DIR / args.report_json
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.report_md:
        md_path = args.report_md if args.report_md.is_absolute() else BASE_DIR / args.report_md
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(render_markdown(report), encoding="utf-8")

    print(
        f"Scanned {report['scanned_files']} markdown files under {root}. "
        f"Matches: {report['total_matches']} across {report['files_with_matches']} files."
    )
    if args.fail_on_match and report["total_matches"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
