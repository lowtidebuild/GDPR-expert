# GDPR-expert — EU Data Protection Agent-Native RAG System

## Overview

AI agent for EU data protection law — GDPR, ePrivacy Directive, EU AI Act, Data Act, and Data Governance Act. Built on the same architecture as PIPA-expert (Korean privacy law agent).

## Architecture

**Agent-Native RAG**: The agent uses Claude's native Read/Grep/Glob tools to search structured markdown files with YAML frontmatter. No external vector database needed (v1.0).

## Directory Structure

```
library/
  grade-a/                    — Official primary sources (665 files)
    gdpr/                      99 articles
    gdpr-recitals/            173 recitals
    eprivacy-directive/        21 articles
    eu-ai-act/                113 articles + recitals
    data-act/                  50 articles + recitals
    data-governance-act/       38 articles + recitals
    edpb-guidelines/           52 guidelines
    edpb-opinions/             31 opinions
    edpb-binding-decisions/    10 Art. 65 binding decisions
    edpb-recommendations/       7 recommendations
    edpb-statements/           19 statements
    edpb-reports/               1 report
    cjeu-cases/                51 judgments
  grade-b/                    — Verified secondary sources (37 files)
    enforcement-decisions/     35 DPA enforcement decisions
    legislative-proposals/      2 Digital Omnibus Package
  grade-c/                    — Academic/reference
index/                        — JSON search indexes (5 indexes, 700+ items)
config/                       — Configuration files
scripts/                      — Data collection/processing scripts
.claude/agents/               — Agent definitions
.claude/skills/               — Skill definitions
```

## Source Grade System

- **Grade A**: Legislation text, EDPB guidelines, CJEU judgments — authoritative, can be sole basis
- **Grade B**: DPA enforcement decisions, law firm analyses — verified, cross-verification recommended
- **Grade C**: Academic papers — reference only, [EDITORIAL] tag required
- **Grade D**: News, AI summaries — excluded from RAG

## Key Files

- **Agent**: `.claude/agents/gdpr-agent.md` — Main GDPR expert agent
- **Fact-Checker**: `.claude/agents/fact-checker/AGENT.md` — Citation verification sub-agent
- **Source Registry**: `index/source-registry.json` — Collection status for all sources
- **Fetch Script**: `scripts/fetch-eu-legislation.py` — CELLAR REST API collector

## Data Collection

Legislation is collected from the EU Publications Office CELLAR REST API:
```bash
python3 scripts/fetch-eu-legislation.py --law gdpr    # Fetch specific law
python3 scripts/fetch-eu-legislation.py                # Fetch all 5 laws
```

API: `https://publications.europa.eu/resource/celex/{CELEX}` with `Accept: application/xhtml+xml`
No authentication required.

## Dependencies

- Python 3.10+ (lxml, requests for future scripts)
- markitdown CLI (EDPB PDF conversion)
- Claude Code (agent execution)

## Current Status

- Phase 0-5 complete
- 702 KB files: 665 Grade A + 37 Grade B
- 5 legislation (321 articles + 536 recitals), 120 EDPB documents, 51 CJEU cases, 35 enforcement decisions, 2 Digital Omnibus proposals
- 5 JSON indexes (700+ indexed items)
- Phase 6 pending: Agent refinement (ingest skill, legal opinion formatter)
