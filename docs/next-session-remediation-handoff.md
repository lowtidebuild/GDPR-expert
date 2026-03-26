# Next Session Remediation Handoff

Last updated: 2026-03-27

## Current State

The highest-risk remediation pass is complete.

- `null` list fields were normalized to explicit `[]`
- `scripts/build-indexes.py` now uses real YAML parsing
- `case-index.json` was rebuilt from current source files
- `enforcement-index.json` now carries `decision_date`
- `source_url` is now included in case and enforcement indexes
- all CJEU case records now point to record-level EUR-Lex URLs
- all enforcement records no longer point to the GDPRhub homepage
- `scripts/validate-kb.py` passes

Validation command:

```bash
python3 scripts/validate-kb.py
```

Expected result:

```text
KB validation passed.
```

## Important Constraint

Do not run remediation and index rebuilding in parallel.

Bad:

```bash
python3 scripts/remediate-kb.py --task all
python3 scripts/build-indexes.py --type all
```

in separate concurrent processes.

Good:

```bash
python3 scripts/remediate-kb.py --task all
python3 scripts/build-indexes.py --type all
python3 scripts/validate-kb.py
```

## What Was Added

- `scripts/remediate-kb.py`
- `scripts/validate-kb.py`
- `docs/quality-remediation-checklist.md`

## Remaining High-Value Work

### 1. Canonicalize enforcement source URLs

Current status:

- 1 enforcement record has a direct GDPRhub URL
- 34 enforcement records still use record-targeted GDPRhub search fallback URLs

This is better than homepage links, but still not ideal for MCP exposure.

Target state:

- direct GDPRhub decision URL where available, or
- official DPA decision / press-release / PDF URL where more authoritative

Recommended order:

1. DPC Ireland decisions
2. CNIL decisions
3. AP Netherlands decisions
4. Garante decisions
5. ICO / German DPAs / IMY / multi-DPA records

Files to focus on first:

- `library/grade-b/enforcement-decisions/dpc-whatsapp-225m-transparency.md`
- `library/grade-b/enforcement-decisions/dpc-meta-whatsapp-1200m-transfers.md`
- `library/grade-b/enforcement-decisions/dpc-tiktok-530m-china-transfers.md`
- `library/grade-b/enforcement-decisions/dpc-linkedin-310m-advertising.md`
- `library/grade-b/enforcement-decisions/cnpd-amazon-746m-advertising.md`
- `library/grade-b/enforcement-decisions/cnil-google-150m-cookies-2022.md`
- `library/grade-b/enforcement-decisions/cnil-google-50m-transparency-consent-2019.md`
- `library/grade-b/enforcement-decisions/garante-openai-15m-chatgpt-ai.md`

### 2. Remove taxonomy pollution

This file is still wrong by category:

- `library/grade-b/enforcement-decisions/cjeu-schufa-art22-automated-scoring.md`

Problem:

- it is a CJEU preliminary ruling, not an enforcement decision
- the underlying ruling already exists as a Grade A CJEU case

Recommended action:

1. decide whether to delete it, archive it, or convert it into a cross-reference stub
2. ensure there is only one canonical record for the judgment
3. rebuild indexes after cleanup

### 3. Deduplicate keywords

This was not touched yet.

Still open:

- many legislation files contain repeated keywords
- many case and enforcement files also duplicate keywords

Recommended strategy:

1. preserve order
2. lowercase only for comparison, not output rewriting
3. keep original display values
4. run after provenance work, not before

### 4. Consider recital provenance

GDPR recital files still do not have `source_url`.

This is not as urgent as the fixed items above, but it is worth deciding whether:

- recital-level `source_url` should be added, or
- recital provenance should be represented through law-level metadata only

## Suggested Next Session Workflow

### Step 1. Inspect current fallback enforcement URLs

```bash
python3 - <<'PY'
from pathlib import Path
import yaml
base = Path("library/grade-b/enforcement-decisions")
for p in sorted(base.glob("*.md")):
    text = p.read_text(encoding="utf-8")
    end = text.find("\n---\n", 4)
    fm = yaml.safe_load(text[4:end])
    url = fm.get("source_url", "")
    if "Special%3ASearch" in url:
        print(p.name, url)
PY
```

### Step 2. Replace fallback URLs with canonical URLs

Update `scripts/remediate-kb.py` so the direct URL map grows over time.

### Step 3. Rebuild indexes

```bash
python3 scripts/build-indexes.py --type all
```

### Step 4. Validate

```bash
python3 scripts/validate-kb.py
```

## Files That Matter Most

- `scripts/build-indexes.py`
- `scripts/remediate-kb.py`
- `scripts/validate-kb.py`
- `docs/quality-remediation-checklist.md`
- `index/case-index.json`
- `index/enforcement-index.json`
- `library/grade-b/enforcement-decisions/`
- `library/grade-a/cjeu-cases/`

## Known Good Checks

These should remain true after further work:

- no generic `https://curia.europa.eu` CJEU homepage URLs remain
- no generic `https://gdprhub.eu` enforcement homepage URLs remain
- no `null` list fields remain in the previously remediated directories
- case/enforcement indexes must stay in sync with source markdown
- `python3 scripts/validate-kb.py` must pass before stopping
