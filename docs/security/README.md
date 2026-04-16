# Security Docs

This directory holds follow-up security artifacts that sit next to the code hardening work.

## Files

- `2026-04-kb-prompt-injection-audit.md` — baseline retroactive audit of `library/` using the same patterns as `scripts/sanitize.py`
- `2026-04-kb-prompt-injection-audit.json` — machine-readable version of the same audit
- `secret-rotation-checklist.md` — operator checklist for rotating repo-related secrets without exposing `.env`
- `threat-model-lite.md` — lightweight security model for the repo's current trust boundaries and remaining gaps

## Recommended cadence

1. Re-run `python3 scripts/audit_prompt_injection.py --root library --report-json <path>.json --report-md <path>.md` after any large ingestion batch.
2. Review `threat-model-lite.md` whenever a new ingestion path, agent, or external tool surface is added.
3. Use `secret-rotation-checklist.md` whenever provider credentials are rotated or copied into a new environment.
