# GitHub Metadata (for manual entry)

## Repository "About" Section

### Description (max 350 chars)
```
AI-powered EU data protection law advisor. 5 EU laws (GDPR, ePrivacy, AI Act, Data Act, DGA) · 1063 indexed legal sources · 120 EDPB documents · 51 CJEU cases. Structured RAG with fact-checking. Built for Claude Code.
```

### Website
```
https://lowtidebuild.github.io/github-folio/
```

### Topics (tags)
```
gdpr, eu-law, data-protection, ai-agent, rag, legal-tech, edpb, cjeu, eprivacy, ai-act, data-act, claude-code, legal-research, compliance, privacy
```

---

## Release: v1.0.0

### Title
```
v1.0.0 — Initial Release
```

### Release Notes (Markdown)

```markdown
# GDPR Expert v1.0.0

AI-powered EU data protection law advisor with structured RAG and built-in fact-checking.

## What's Inside

### Knowledge Base — 1063 Indexed Legal Sources

| Category | Count | Source |
|----------|-------|--------|
| Legislation (5 EU laws) | 321 articles + 536 recitals | CELLAR REST API |
| EDPB Documents | 120 (guidelines, opinions, binding decisions) | edpb.europa.eu |
| CJEU Case Law | 51 landmark judgments | curia.europa.eu |
| Enforcement Decisions | 35 major DPA fines | gdprhub.eu |
| Digital Omnibus Package | 2 legislative proposals | EU Commission |

### Laws Covered

- **GDPR** (Regulation 2016/679) — 99 articles + 173 recitals
- **ePrivacy Directive** (2002/58/EC) — 21 articles
- **EU AI Act** (Regulation 2024/1689) — 113 articles + 180 recitals
- **Data Act** (Regulation 2023/2854) — 50 articles + 120 recitals
- **Data Governance Act** (Regulation 2022/868) — 38 articles + 63 recitals

### Key Features

- **Structured RAG** — Every article is a standalone Markdown file with YAML frontmatter, cross-references, and keywords. Not flat-text search.
- **Mandatory 9-source search** — Agent must search all source categories before drafting opinions. Prevents narrow citation.
- **Fact-check sub-agent** — Every citation verified against KB originals before output.
- **Source grade system** — Grade A (legislation, EDPB, CJEU) through Grade D (excluded). Every citation tagged.
- **Multilingual** — Responds in English, Korean, German, French, Dutch, and other EU languages.
- **DOCX legal opinions** — Professional documents with verified citations and risk matrices.
- **Ingest system** — Add your own sources (national DPA decisions, internal policies, academic papers).
- **Digital Omnibus awareness** — Includes COM(2025) 836 + 837 proposals for forward-looking analysis.

### Data Collection

All legislation collected from the EU Publications Office **CELLAR REST API** (no authentication required). EDPB documents batch-downloaded and converted from PDF via markitdown. No web scraping.

### Getting Started

```bash
git clone https://github.com/lowtidebuild/GDPR-expert.git
cd GDPR-expert
pip install python-docx markitdown
claude --agent .claude/agents/gdpr-agent.md
```

See the [How to Use Guide](docs/en/HOW-TO-USE.md) for a non-developer walkthrough.

### What's Next (Phase 6)

- Ingest skill implementation (automated source ingestion workflow)
- Legal opinion formatter skill (standardized DOCX templates)
- Output format selection (md, docx, html)
- Additional CJEU cases and enforcement decisions
```
