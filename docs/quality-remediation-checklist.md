# KB Quality Remediation Checklist

Last updated: 2026-03-27

## Priority 0 — Data Integrity Blockers

- [x] Replace pseudo-empty YAML list fields with explicit `[]`
  - Scope: legislation articles, recital files, CJEU cases, enforcement decisions
  - Tooling: `python3 scripts/remediate-kb.py --task empty-lists`
- [x] Switch index generation to real YAML parsing
  - File: `scripts/build-indexes.py`
- [x] Rebuild `case-index.json` from current source files
  - Result: source IDs, GDPR articles, keywords, significance now match source markdown
- [x] Fix enforcement decision date propagation into `enforcement-index.json`
  - Result: `decision_date` now populated for all enforcement records
- [x] Add `source_url` propagation to `case-index.json` and `enforcement-index.json`

## Priority 1 — Record-Level Provenance

- [x] Replace generic CJEU source URLs with record-level official EUR-Lex URLs
  - Tooling: `python3 scripts/remediate-kb.py --task case-urls`
- [x] Replace enforcement `source_url: https://gdprhub.eu` homepage values
  - Current state:
    - curated direct GDPRhub URLs where confidently known
    - record-targeted GDPRhub search URLs as fallback
  - Tooling: `python3 scripts/remediate-kb.py --task enforcement-urls`
- [ ] Upgrade enforcement fallbacks from GDPRhub search URLs to direct decision pages or official DPA URLs
  - Highest-value targets: Meta, TikTok, Amazon, Google, OpenAI, H&M, Clearview AI

## Priority 2 — Validation Guardrails

- [x] Add high-risk validator
  - File: `scripts/validate-kb.py`
  - Command: `python3 scripts/validate-kb.py`
- [ ] Add validator execution to release workflow / pre-publish checklist
- [ ] Add CI job to fail on index drift or generic homepage source URLs

## Priority 3 — Remaining Quality Debt

- [ ] Deduplicate keyword arrays across legislation, cases, and enforcement decisions
- [ ] Add recital-level `source_url` provenance where technically stable
- [ ] Resolve taxonomy pollution
  - Remove or reclassify `grade-b/enforcement-decisions/cjeu-schufa-art22-automated-scoring.md`
  - Avoid storing the same CJEU ruling as both a Grade A case and a Grade B enforcement decision
- [ ] Tighten `source-registry.json` semantics further
  - `partial` should be used when `count < target`
  - release docs should not claim `complete` when coverage is below target
- [ ] Add canonical schema docs for each source family
  - legislation article
  - recital
  - CJEU case
  - enforcement decision
  - EDPB document

## Standard Recovery Sequence

1. `python3 scripts/remediate-kb.py --task all`
2. `python3 scripts/build-indexes.py --type all`
3. `python3 scripts/validate-kb.py`
