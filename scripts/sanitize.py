#!/usr/bin/env python3
"""
sanitize.py — Prompt-injection sanitizer for ingested / fetched content.

Contract:
    sanitize_text(raw: str) -> tuple[str, list[dict]]

    - `clean` wraps each match in <escape>MATCH</escape>.
    - `audit` is a list of {pattern: str, match: str, line: int, col: int}.
    - Idempotent: sanitize_text(sanitize_text(x)[0])[0] == sanitize_text(x)[0].
    - Non-matches are preserved byte-for-byte.

CLI:
    python3 scripts/sanitize.py --in raw.md --out clean.md --audit clean.audit.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("xml_system_open", re.compile(r"<system>", re.IGNORECASE)),
    ("xml_system_close", re.compile(r"</system>", re.IGNORECASE)),
    ("xml_user_open", re.compile(r"<user>", re.IGNORECASE)),
    ("xml_assistant_open", re.compile(r"<assistant>", re.IGNORECASE)),
    ("forged_untrusted_close", re.compile(r"</untrusted_content>", re.IGNORECASE)),
    ("forged_escape_open", re.compile(r"<escape>(?!\w)", re.IGNORECASE)),
    ("chatml_start", re.compile(r"<\|im_start\|>")),
    ("chatml_end", re.compile(r"<\|im_end\|>")),
    ("role_system", re.compile(r"\[SYSTEM\]")),
    ("role_user", re.compile(r"\[USER\]")),
    ("role_assistant", re.compile(r"\[ASSISTANT\]")),
    ("role_instruction", re.compile(r"\[INSTRUCTION\]")),
    ("md_instruction_header", re.compile(r"^###\s+Instruction:", re.MULTILINE)),
    ("jb_ignore_previous", re.compile(r"Ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions?", re.IGNORECASE)),
    ("jb_disregard_above", re.compile(r"Disregard\s+(?:everything\s+|all\s+)?the\s+above", re.IGNORECASE)),
    ("jb_forget_above", re.compile(r"Forget\s+(?:everything|all)\s+above", re.IGNORECASE)),
    ("jb_you_are_now", re.compile(r"You\s+are\s+now\s+DAN\b", re.IGNORECASE)),
    ("ko_ignore_prev", re.compile(r"이전\s*지시\s*무시")),
    ("ko_ignore_above", re.compile(r"위의?\s*지시를?\s*무시")),
    ("ko_leak_prompt", re.compile(r"시스템\s*프롬프트를?\s*(?:출력|공개|보여)")),
    ("ko_from_now_you", re.compile(r"지금부터\s*너는")),
]


@dataclass(frozen=True)
class Match:
    pattern: str
    match: str
    start: int
    end: int


def _find_all_matches(raw: str) -> list[Match]:
    hits: list[Match] = []
    for name, rx in PATTERNS:
        for found in rx.finditer(raw):
            hits.append(
                Match(
                    pattern=name,
                    match=found.group(0),
                    start=found.start(),
                    end=found.end(),
                )
            )
    hits.sort(key=lambda hit: (hit.start, -(hit.end - hit.start)))

    deduped: list[Match] = []
    cursor = -1
    for hit in hits:
        if hit.start >= cursor:
            deduped.append(hit)
            cursor = hit.end
    return deduped


def _to_line_col(raw: str, offset: int) -> tuple[int, int]:
    line_start = raw.rfind("\n", 0, offset) + 1
    line = raw.count("\n", 0, offset) + 1
    col = offset - line_start + 1
    return line, col


def sanitize_text(raw: str) -> tuple[str, list[dict]]:
    """Return sanitized text plus an audit trail of escaped matches."""
    hits = _find_all_matches(raw)
    escape_windows = [
        (match.start(), match.end())
        for match in re.finditer(r"<escape>.*?</escape>", raw, re.DOTALL)
    ]

    def already_escaped(hit: Match) -> bool:
        return any(start <= hit.start and hit.end <= end for start, end in escape_windows)

    hits = [hit for hit in hits if not already_escaped(hit)]

    if not hits:
        return raw, []

    output: list[str] = []
    audit: list[dict] = []
    cursor = 0
    for hit in hits:
        output.append(raw[cursor:hit.start])
        output.append("<escape>")
        output.append(hit.match)
        output.append("</escape>")
        line, col = _to_line_col(raw, hit.start)
        audit.append({
            "pattern": hit.pattern,
            "match": hit.match,
            "line": line,
            "col": col,
        })
        cursor = hit.end
    output.append(raw[cursor:])
    return "".join(output), audit


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prompt-injection sanitizer for ingested content."
    )
    parser.add_argument("--in", dest="inp", required=True, type=Path, help="Input file.")
    parser.add_argument("--out", dest="out", required=True, type=Path, help="Sanitized output.")
    parser.add_argument("--audit", dest="audit", required=True, type=Path, help="Audit JSON sidecar.")
    parser.add_argument(
        "--fail-on-match",
        action="store_true",
        help="Exit 2 if any injection was found.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    raw = args.inp.read_text(encoding="utf-8")
    clean, audit = sanitize_text(raw)
    args.out.write_text(clean, encoding="utf-8")
    args.audit.write_text(
        json.dumps({"source": str(args.inp), "matches": audit}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    plural = "es" if len(audit) != 1 else ""
    print(f"{args.inp} -> {args.out} ({len(audit)} match{plural})")
    if audit and args.fail_on_match:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
