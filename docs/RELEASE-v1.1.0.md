# GDPR Expert v1.1.0 — Knowledge Base Quality Hardening

Full-stack quality audit and remediation pass across all 1,060 files, driven by a dual-model review process (Claude Opus + OpenAI Codex). This release makes the knowledge base reliable enough for external consumption — including a future MCP server.

## What Changed

### GDPR Recital-Article Bidirectional Mappings (new)

Every GDPR article now knows its Recitals, and every Recital knows its Articles. Sourced from [gdpr-info.eu](https://gdpr-info.eu/) authoritative mappings, not text extraction.

- 83/99 articles linked to their Recitals
- 172/173 Recitals linked to their Articles
- `_cross-refs.json` updated with `article_to_recital` and `recital_to_article` sections

Example: query Article 6 and you automatically get Recitals 39-50, 171 — the full legislative intent behind lawfulness of processing.

### Metadata Integrity Fixes (713 files)

| Fix | Scope |
|-----|-------|
| `source_url` pointed to wrong legislation | 222 files (AI Act, ePrivacy, Data Act, DGA all pointed to GDPR) |
| Schema migration (old → new format) | 27 files (17 CJEU cases + 10 enforcement decisions) |
| `source_grade` / `source_id` mismatches | 48 files |
| HTML artifacts in ePrivacy files | 21 files |
| Empty `keywords` populated | 529 files |
| YAML `null` → explicit `[]` for list fields | ~71 files |
| Keyword deduplication | 169 files |

### Source Provenance Hardening

- All 51 CJEU cases now have record-level EUR-Lex CELEX URLs (was: generic `curia.europa.eu`)
- All 33 enforcement decisions now have regulator-specific decision URLs (was: generic `gdprhub.eu`)
- ePrivacy `article_title` and `chapter` fields filled for all 21 articles

### Data Cleanup

- Removed SCHUFA duplicate (existed in both CJEU cases and enforcement decisions)
- Removed Meta legal-basis duplicate record
- Renamed 3 enforcement decisions for accuracy (WhatsApp → Meta, Clearview multi-DPA → Garante)
- Enforcement decisions: 35 → 33

### Index & Tooling

- New: `legislative-proposal-index.json` (2 Digital Omnibus proposals)
- Rebuilt all indexes with corrected field mappings (`decision_date`, not `published_date`)
- `build-indexes.py` upgraded to real YAML parser
- New: `remediate-kb.py` (null normalization, keyword dedup)
- New: `validate-kb.py` (automated KB integrity checks)
- `source-registry.json` status semantics fixed (count < target → "partial")

### Documentation

- New: [Quality Audit Playbook](docs/quality-audit-playbook.md) — reusable 4-phase audit process
- README (EN/KO): Claude Code & Codex attribution, updated counts
- All file counts synchronized across README, CLAUDE.md, agent definition, release notes

## Knowledge Base (v1.1.0)

| | Count |
|---|---|
| **Legislation** | 5 EU laws — 321 articles + 535 recitals |
| **EDPB** | 120 documents (guidelines, opinions, Art. 65 binding decisions) |
| **CJEU** | 51 landmark judgments |
| **Enforcement** | 33 major DPA decisions |
| **Digital Omnibus** | COM(2025) 836 + 837 proposals |
| **Total indexed** | **1,060 sources** |

## Audit Process

This release was produced by a three-layer review:

1. **Claude Opus** — 4 parallel agents audited all 1,064 files, found 17 issues across 4 severity levels
2. **Claude Opus** — 3 batches of parallel agents + scripts fixed all 17 issues (713 files changed)
3. **OpenAI Codex 5.4** — independent blind audit found 7 additional issues, then remediated them

The [Quality Audit Playbook](docs/quality-audit-playbook.md) documents this process for reuse.

## Quick Start

```bash
git clone https://github.com/lowtidebuild/GDPR-expert.git
cd GDPR-expert
pip install python-docx markitdown
claude --agent .claude/agents/gdpr-agent.md
```

> [How to Use Guide](docs/en/HOW-TO-USE.md) · [사용 가이드](docs/ko/HOW-TO-USE.md)
