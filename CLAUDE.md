# GDPR-expert — EU Data Protection Agent-Native RAG System

## Overview

AI-based EU data protection workflow agent — GDPR, ePrivacy Directive, EU AI Act, Data Act, and Data Governance Act. Part of Jinju Legal Orchestrator and built on the same architecture as PIPA-expert (Korean privacy law agent).

## Architecture

**Agent-Native RAG**: The agent uses Claude's native Read/Grep/Glob tools to search structured markdown files with YAML frontmatter. No external vector database needed (v1.0).

## Directory Structure

```
library/
  grade-a/                    — Official primary sources (1,027 files)
    gdpr/                      99 articles (with related_recitals mappings)
    gdpr-recitals/            173 recitals (with related_articles mappings)
    eprivacy-directive/        21 articles
    eu-ai-act/                113 articles
    eu-ai-act-recitals/       180 recitals
    data-act/                  50 articles
    data-act-recitals/        119 recitals
    data-governance-act/       38 articles
    data-governance-act-recitals/ 63 recitals
    edpb-guidelines/           52 guidelines
    edpb-opinions/             31 opinions
    edpb-binding-decisions/    10 Art. 65 binding decisions
    edpb-recommendations/       7 recommendations
    edpb-statements/           19 statements
    edpb-reports/               1 report
    cjeu-cases/                51 judgments
  grade-b/                    — Verified secondary sources (37 files)
    enforcement-decisions/     33 DPA enforcement decisions
    legislative-proposals/      2 Digital Omnibus Package
  grade-c/                    — Academic/reference
index/                        — JSON search indexes (7 indexes, 1,062+ items)
config/                       — Configuration files
scripts/                      — Data collection/processing scripts
.claude/agents/               — Agent definitions
.claude/skills/               — Skill definitions
```

## Source Grade System

- **Grade A**: Legislation text, EDPB guidelines, CJEU judgments — authoritative, can be sole basis
- **Grade B**: DPA enforcement decisions, court decisions — verified, cross-verification recommended
- **Grade C**: Law firm analyses, academic papers — reference only, [EDITORIAL] tag required
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

## Local Drafting Addendum

한국어 법률 분석 메모(Memorandum) 생성 시 반드시 `docs/_private/local-drafting-addendum.md`를 읽고 따를 것.

- 문서 구조, 헤더/정보 블록, 법령 인용 형식, 판례 인용 형식, 정의 용어 관례, 문체/어조, 확신도 표현, 번호 매김, 종결부, 타이포그래피 등 전체 규칙 포함
- 전문 문서 작성 품질 기준
- DOCX 생성 시 python-docx CJK 폰트 설정 규칙 포함

## Current Status

- Phase 0-5 complete, Phase 5.5 quality audit complete
- 1,060 KB files: 1,027 Grade A + 33 Grade B
- 5 legislation (321 articles + 535 recitals), 120 EDPB documents, 51 CJEU cases, 33 enforcement decisions, 2 Digital Omnibus proposals
- 7 JSON indexes (1,060 indexed items)
- GDPR articles ↔ recitals bidirectional mappings (sourced from gdpr-info.eu)
- All files have consistent YAML frontmatter schema, keywords, and source grading
- Phase 6 pending: Agent refinement (ingest skill, legal opinion formatter)

## Security

- **NEVER** read, cat, print, or access `.env` files directly
- **NEVER** output API keys, secrets, or credentials in responses
- When debugging environment issues, ask the user to verify env vars are set — do not read them yourself
