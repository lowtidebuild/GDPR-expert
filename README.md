<div align="center">

**[English](#gdpr-expert)** · **[한국어](README.ko.md)**

> Latest release: **[v1.3.0 — Citation Audit + DOCX Appendix](docs/RELEASE-v1.3.0.md)**

</div>

> [!IMPORTANT]
> **As of 2026-05-08, this repo has been superseded by [`data-protection-agent`](https://github.com/kipeum86/data-protection-agent) — please use that going forward.**
>
> The EU GDPR (`GDPR-expert`) and Korea PIPA (`PIPA-expert`) specialist agents have been folded into one unified cross-jurisdictional privacy research agent, together with a newly added California (CCPA-as-amended-by-CPRA) sub-KB. The unified repo collapses cross-jurisdiction questions into a single dispatch (instead of two parallel single-jurisdiction runs), adds a cross-jurisdictional citation auditor that catches authority-blending across borders, and ships polished DOCX / HTML legal-opinion deliverables.
>
> This repo is preserved for historical reference and continuity of any external links; **all future development — KB updates, auditor checks, output renderers, the answering pipeline — happens on [`data-protection-agent`](https://github.com/kipeum86/data-protection-agent)**. See the [v1.0.0 release notes](https://github.com/kipeum86/data-protection-agent/releases/tag/v1.0.0) for the full launch narrative.

<div align="center">

# GDPR Expert

### KP Legal Orchestrator · AI-Based EU Data Protection Workflow System

**5 EU laws** · **321 articles + 535 recitals** · **120 EDPB documents** · **51 CJEU cases** · **1,060+ indexed items**

Powered by structured RAG · Built with [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) & [Codex](https://openai.com/index/introducing-codex/)

[![Laws](https://img.shields.io/badge/Legislation-5_EU_Laws-blue)](#-knowledge-base)
[![Articles](https://img.shields.io/badge/Articles-321-blue)](#-knowledge-base)
[![EDPB](https://img.shields.io/badge/EDPB_Documents-120-green)](#edpb-documents--120-grade-a-sources)
[![CJEU](https://img.shields.io/badge/CJEU_Cases-51-purple)](#cjeu-case-law--51-grade-a-judgments)
[![Enforcement](https://img.shields.io/badge/Enforcement-33_Decisions-red)](#enforcement-decisions--33-grade-b-sources)
[![License](https://img.shields.io/badge/License-Apache_2.0-yellow)](#license)

<br/>

> *"Data structure is intelligence."*
> — Smarter data beats smarter search. Every time.

</div>

> [!CAUTION]
> **This tool is for legal research assistance only — it does not provide legal advice.** Outputs are AI-generated and may contain errors despite built-in verification. All legal citations should be independently verified before reliance. Consult a qualified attorney for advice on specific legal matters. **[Full Disclaimer](docs/en/DISCLAIMER.md)** · **[면책사항](docs/ko/DISCLAIMER.md)**

> [!TIP]
> **New here?** Read the **[How to Use Guide](docs/en/HOW-TO-USE.md)** — no technical background required. **[사용 가이드 (한국어)](docs/ko/HOW-TO-USE.md)**

---

## The Problem

Existing AI legal assistants (ChatGPT Custom GPTs, Gemini Gems, etc.) treat EU legislation as flat text documents. They upload PDFs, run semantic search, and hope for the best. This approach **fundamentally fails** for EU data protection work because it ignores:

- **Recitals as interpretive authority** — GDPR has 173 Recitals that courts and DPAs rely on to interpret the 99 Articles. Flat-text RAG treats them as disconnected paragraphs
- **Cross-legislation references** — GDPR Article 95 governs the relationship with the ePrivacy Directive; the AI Act (Art. 86, Recital 140) interacts with GDPR Art. 22 on automated decision-making. Five laws form an interconnected web
- **Source authority hierarchy** — an EDPB binding decision (Art. 65) carries legal force; a law firm newsletter does not. Generic RAG treats them identically
- **Citation verifiability** — every legal citation must trace back to an exact provision. "Somewhere in the GDPR" is not a citation

The result? Hallucinated article numbers, fabricated CJEU case holdings, and analysis memos that no privacy professional would rely on.

---

## The Solution

GDPR Expert takes a different approach: **instead of smarter search, build smarter data.**

Every EU legal source is fetched from **official APIs**, parsed into **article-level structured files**, enriched with **cross-references and metadata**, and made searchable through **JSON indexes**. The AI doesn't guess — it reads the actual law.

```mermaid
graph TB
    subgraph agent["<b>GDPR Expert Agent</b>"]
        direction TB

        subgraph core["Core Capabilities"]
            direction LR
            KB["<b>Structured Knowledge Base</b><br/>1,060+ files · 5 laws · 120 EDPB docs<br/>51 CJEU cases · 1,060+ indexed"]
            WS["<b>Multi-Layer Web Search</b><br/>EUR-Lex · EDPB · CURIA<br/>Law Firms · Academic"]
            DX["<b>DOCX Analysis Memo Generator</b><br/>Professional Documents<br/>Multilingual (EN · KR · EU languages)"]
        end

        subgraph pipeline["Research Pipeline"]
            direction LR
            S1["1. KB Search<br/><i>Articles & Recitals</i>"]
            S2["2. EDPB & CJEU<br/><i>Guidelines & case law</i>"]
            S3["3. Cross-Reference<br/><i>Inter-law connections</i>"]
            S4["4. Fact-Check<br/><i>Verify every citation</i>"]
            S1 --> S2 --> S3 --> S4
        end

        subgraph grades["Source Grade System"]
            direction LR
            GA["<b>Grade A</b><br/>Legislation · EDPB · CJEU<br/><i>Sole authority</i>"]
            GB["<b>Grade B</b><br/>DPA Decisions · Court Rulings<br/><i>Cross-verify with A</i>"]
            GC["<b>Grade C</b><br/>Law Firms · Academic<br/><i>Editorial only</i>"]
            GD["<b>Grade D</b><br/>News · AI Summaries<br/><i>Excluded from RAG</i>"]
        end
    end

    Q["User Question"] --> S1
    S4 --> O["Verified Legal Analysis Memo"]

    style agent fill:#f8fafc,stroke:#1B2A4A,stroke-width:2px,color:#1B2A4A
    style core fill:#eef2ff,stroke:#4f46e5,stroke-width:1px
    style pipeline fill:#f0fdf4,stroke:#16a34a,stroke-width:1px
    style grades fill:#fffbeb,stroke:#d97706,stroke-width:1px
    style KB fill:#dbeafe,stroke:#2563eb,color:#1e40af
    style WS fill:#dbeafe,stroke:#2563eb,color:#1e40af
    style DX fill:#dbeafe,stroke:#2563eb,color:#1e40af
    style GA fill:#d1fae5,stroke:#059669,color:#065f46
    style GB fill:#fef3c7,stroke:#d97706,color:#92400e
    style GC fill:#fee2e2,stroke:#dc2626,color:#991b1b
    style GD fill:#f3f4f6,stroke:#6b7280,color:#374151
    style Q fill:#ede9fe,stroke:#7c3aed,color:#5b21b6
    style O fill:#d1fae5,stroke:#059669,color:#065f46
    style S1 fill:#f0fdf4,stroke:#16a34a,color:#166534
    style S2 fill:#f0fdf4,stroke:#16a34a,color:#166534
    style S3 fill:#f0fdf4,stroke:#16a34a,color:#166534
    style S4 fill:#f0fdf4,stroke:#16a34a,color:#166534
```

---

## Knowledge Base

### How the Data Gets In — The Collection Pipeline

Most legal AI tools ask you to "upload a PDF." We built an **automated pipeline** that fetches legislation directly from official EU sources, parses the HTML/XML structure, and generates per-article Markdown files with rich metadata.

```mermaid
flowchart TD
    subgraph leg["Legislation"]
        direction TB
        PO["<b>Publications Office</b><br/>CELLAR REST API<br/><i>no auth required</i>"]
        XHTML["XHTML with structured<br/>article IDs (art_1 … art_99)"]
        FETCH["<b>fetch-eu-legislation.py</b><br/>Parse XHTML → extract articles<br/>Extract Recitals (rct_1 … rct_173)<br/>Build cross-reference maps<br/>Generate YAML frontmatter"]
        ARTS["<code>library/grade-a/gdpr/</code><br/>art1.md … art99.md"]
        RECS["<code>library/grade-a/gdpr-recitals/</code><br/>recital1.md … recital173.md"]
        PO --> XHTML --> FETCH
        FETCH --> ARTS
        FETCH --> RECS
    end

    subgraph edpb["EDPB Documents"]
        direction TB
        EDPB_SRC["<b>edpb.europa.eu</b><br/>PDF download"]
        MARK["<b>markitdown CLI</b><br/>PDF → Markdown"]
        FRONT["<b>Frontmatter Generation</b><br/>keywords · GDPR articles<br/>topics · char_count"]
        EDPB_OUT["<code>library/grade-a/edpb-guidelines/</code><br/><code>library/grade-a/edpb-opinions/</code><br/><code>library/grade-a/edpb-binding-decisions/</code>"]
        EDPB_SRC --> MARK --> FRONT --> EDPB_OUT
    end

    subgraph idx["JSON Indexes"]
        direction TB
        BUILD["<b>build-indexes.py --type all</b>"]
        IDXOUT["article-index.json · 321 articles<br/>recital-index.json · 173 recitals<br/>edpb-document-index.json · 120 docs<br/>case-index.json · 51 cases<br/>enforcement-index.json · 33 decisions"]
        BUILD --> IDXOUT
    end

    ARTS --> BUILD
    RECS --> BUILD
    EDPB_OUT --> BUILD

    style leg fill:#eff6ff,stroke:#2563eb,stroke-width:2px
    style edpb fill:#eff6ff,stroke:#2563eb,stroke-width:2px
    style idx fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
    style PO fill:#dbeafe,stroke:#3b82f6,color:#1e40af
    style EDPB_SRC fill:#dbeafe,stroke:#3b82f6,color:#1e40af
    style XHTML fill:#e0e7ff,stroke:#6366f1,color:#3730a3
    style FETCH fill:#fef9c3,stroke:#ca8a04,color:#713f12
    style MARK fill:#fef9c3,stroke:#ca8a04,color:#713f12
    style FRONT fill:#fef9c3,stroke:#ca8a04,color:#713f12
    style BUILD fill:#fef9c3,stroke:#ca8a04,color:#713f12
    style ARTS fill:#d1fae5,stroke:#059669,color:#065f46
    style RECS fill:#d1fae5,stroke:#059669,color:#065f46
    style EDPB_OUT fill:#d1fae5,stroke:#059669,color:#065f46
    style IDXOUT fill:#d1fae5,stroke:#059669,color:#065f46
```

**Key design choice:** We use the EU Publications Office **CELLAR REST API** — not web scraping. A single HTTP request with `Accept: application/xhtml+xml` returns the full legislation text in structured XHTML with article-level IDs (`art_1`, `art_2`, ... `art_99`). No authentication required. No rate limiting issues for our scale. This is the same infrastructure that powers EUR-Lex itself.

### Legislation — 5 EU Laws via CELLAR API

| Law | CELEX | Articles | Recitals | Directory |
|-----|-------|----------|----------|-----------|
| **GDPR** (Regulation 2016/679) | 32016R0679 | 99 | 173 | `library/grade-a/gdpr/` |
| **ePrivacy Directive** (2002/58/EC) | 02002L0058-20091219 | 21 | *not split* | `library/grade-a/eprivacy-directive/` |
| **EU AI Act** (Regulation 2024/1689) | 32024R1689 | 113 | 180 | `library/grade-a/eu-ai-act/` |
| **Data Act** (Regulation 2023/2854) | 32023R2854 | 50 | 119 | `library/grade-a/data-act/` |
| **Data Governance Act** (Regulation 2022/868) | 32022R0868 | 38 | 63 | `library/grade-a/data-governance-act/` |
| **Total** | | **321** | **535** | |

> **Note on the ePrivacy Directive:** Unlike Regulations (which apply directly across the EU), Directives must be transposed into national law by each Member State. The ePrivacy Directive's cookie consent rules, for example, are implemented differently across the EU-27. This KB contains the EU-level Directive text. For Member State-specific implementations, use the [ingest system](#-source-ingest-system) to add national transposition laws to your knowledge base.

### EDPB Documents — 120 Grade A Sources

Official guidance from the European Data Protection Board, converted from PDF to structured Markdown.

| Type | Count | Examples |
|------|-------|---------|
| **Guidelines** | 52 | Consent (05/2020), Legitimate Interest (01/2024), Territorial Scope (03/2018), DPO (WP243), DPIA (WP248) |
| **Opinions** | 31 | AI Models (28/2024), Consent-or-Pay (08/2024), EU-US DPF (5/2023), SCCs, Adequacy Decisions |
| **Binding Decisions (Art. 65)** | 10 | Meta/WhatsApp EUR 1.2B, Instagram EUR 405M, Facebook EUR 210M, TikTok EUR 345M |
| **Recommendations** | 7 | Supplementary Measures for Transfers (01/2020), European Essential Guarantees (02/2020) |
| **Statements** | 19 | Age Assurance, AI Act, Digital Omnibus, ePrivacy Regulation |
| **Reports** | 1 | EU-US Data Privacy Framework First Review |

### CJEU Case Law — 51 Grade A Judgments

In EU law, CJEU judgments are **binding interpretations** of legislation — not secondary commentary. That's why they're Grade A in this system, not Grade B like court decisions in some other legal traditions.

<details>
<summary><b>Notable cases (click to expand)</b></summary>

| Case | Topic | Why It Matters |
|------|-------|---------------|
| C-131/12 **Google Spain** | Right to be forgotten | Established the right to erasure from search results |
| C-311/18 **Schrems II** | International transfers | Invalidated EU-US Privacy Shield |
| C-252/21 **Meta v Bundeskartellamt** | Legitimate interest | Competition authority can assess GDPR compliance |
| C-807/21 **Deutsche Wohnen** | Corporate fines | Clarified corporate fault requirement for Art. 83 fines |
| C-634/21 **SCHUFA Scoring** | Automated decisions | Credit scoring = automated decision-making under Art. 22 |
| C-604/22 **IAB Europe TCF** | Adtech / consent | TC string is personal data; IAB Europe may be joint controller for the TCF layer |
| C-673/17 **Planet49** | Cookie consent | Pre-ticked boxes are not valid consent |
| C-40/17 **Fashion ID** | Joint controllership | Website operator + Facebook = joint controllers for Like button |
| C-300/21 **Osterreichische Post** | Damages | Mere GDPR infringement does not equal automatic right to compensation |

*...and 42 more cases covering damages, DPO independence, data portability, right of access, legitimate interest balancing, and more.*

</details>

### Enforcement Decisions — 33 Grade B Sources

Major DPA enforcement actions including fines against Meta, Amazon, TikTok, Google, H&M, OpenAI, and Clearview AI.

### Legislative Proposals — Digital Omnibus Package (Grade B)

The EU Commission's November 2025 Digital Omnibus Package (COM(2025) 836 + 837) proposes significant GDPR amendments — clarifying that AI development may qualify as a legitimate interest under Art. 6(1)(f), raising the breach notification threshold, and migrating cookie consent rules from the ePrivacy Directive into GDPR. Stored as Grade B (proposal, not yet law) with key changes summarized in frontmatter.

---

## How the Data is Structured

Every legal source is stored as a standalone `.md` file with rich YAML frontmatter:

```yaml
---
# === Identification ===
law: "General Data Protection Regulation"
law_id: "32016R0679"
article: 6
article_title: "Lawfulness of processing"
chapter: "II"
chapter_title: "Principles"

# === Source ===
source_grade: "A"
effective_date: "20180525"
retrieved_at: "2026-03-25"

# === Relationships ===
cross_references:
  - "Art. 5(1)(a)"
  - "Art. 9"
  - "Recital 40-50"

# === Search Metadata ===
keywords:
  - "consent"
  - "lawful"
  - "legitimate interest"
---

## Article 6 — Lawfulness of processing

1.   Processing shall be lawful only if and to the extent
that at least one of the following applies...
```

This structure enables the AI agent to:

- **Search by keyword** using JSON index files — not brute-force grep across 1,000+ files
- **Follow cross-references** — Art. 6 leads to Recital 47, which leads to Art. 5(1)(b), which leads to Recital 39
- **Verify source authority** — Grade A citations carry more weight than Grade B
- **Read exact provisions** — no hallucination, because the text is right there in the file

---

## How It Works

```mermaid
flowchart TD
    Q["<b>User Question</b>"]

    subgraph kb["KB Search: Mandatory Source Scope"]
        direction TB
        S1["<b>Article Search</b><br/>Grep 5 legislation directories<br/>+ follow cross_references"]
        S2["<b>Recital Mining</b><br/>For each cited Article,<br/>grep Recitals for that Article number"]
        S3["<b>EDPB + CJEU Search</b><br/>Grep guidelines, opinions,<br/>binding decisions, case law"]
        S1 --> S2 --> S3
    end

    subgraph web["Multi-Layer Web Search <i>(if KB insufficient)</i>"]
        direction TB
        L1["<b>Layer 1 Official</b><br/>EUR-Lex · EDPB · CURIA · GDPRhub"]
        L2["<b>Layer 2 Law Firms</b><br/>Major international firms"]
        L3["<b>Layer 3 Academic</b><br/>SSRN · EDPL · IDPL"]
        L1 --> L2 --> L3
    end

    subgraph verify["Adversarial Cross-Verification"]
        direction LR
        PA["<b>Pass A</b><br/>Supporting evidence"]
        PB["<b>Pass B</b><br/>Counterarguments<br/>& exceptions"]
        PA <--> PB
    end

    subgraph fc["Verification Layer"]
        FC["<b>Fact-Check Sub-Agent</b><br/>Verify every citation<br/>against KB originals"]
        CA["<b>Citation Audit</b><br/>Append-mode Markdown<br/>DOCX audit appendix"]
        FC --> CA
    end

    O["<b>Verified Legal Analysis Memo</b><br/>DOCX/Markdown with citations,<br/>risk matrix & audit appendix"]

    Q --> kb
    kb --> web
    web --> verify
    verify --> fc
    fc --> O

    style Q fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#5b21b6
    style kb fill:#eff6ff,stroke:#2563eb,stroke-width:1px
    style web fill:#fefce8,stroke:#ca8a04,stroke-width:1px
    style verify fill:#fef2f2,stroke:#dc2626,stroke-width:1px
    style fc fill:#fff7ed,stroke:#ea580c,stroke-width:1px
    style FC fill:#fed7aa,stroke:#ea580c,color:#9a3412
    style CA fill:#fed7aa,stroke:#ea580c,color:#9a3412
    style O fill:#d1fae5,stroke:#059669,stroke-width:2px,color:#065f46
    style S1 fill:#dbeafe,stroke:#3b82f6,color:#1e40af
    style S2 fill:#dbeafe,stroke:#3b82f6,color:#1e40af
    style S3 fill:#dbeafe,stroke:#3b82f6,color:#1e40af
    style L1 fill:#fef9c3,stroke:#ca8a04,color:#713f12
    style L2 fill:#fef9c3,stroke:#ca8a04,color:#713f12
    style L3 fill:#fef9c3,stroke:#ca8a04,color:#713f12
    style PA fill:#dcfce7,stroke:#16a34a,color:#166534
    style PB fill:#fee2e2,stroke:#ef4444,color:#991b1b
```

### Citation Verification Tags

| Tag | Meaning |
|-----|---------|
| `[VERIFIED]` | Exact match in Grade A source from KB |
| `[UNVERIFIED]` | Grade B only, or partial match |
| `[INSUFFICIENT]` | Not enough evidence — left blank rather than guessed |
| `[CONTRADICTED]` | Sources conflict — both sides presented |

### Legal Writing Style Guide

Formal opinions and memoranda should follow [`legal-writing-formatting-guide.md`](legal-writing-formatting-guide.md). The guide defines EN/KO opinion architecture, tone, certainty language, citation density, AI-generation notices, verification guides, and output-mode formatting rules.

---

## Fact-Check Layer (Hallucination Prevention)

Before any output is finalized, a **dedicated fact-checker sub-agent** verifies every legal citation against the knowledge base:

| Check | Method | On Fail |
|-------|--------|---------|
| Article exists | Glob for `art{N}.md` in KB | Downgrade to `[UNVERIFIED]` |
| Quoted text matches source | Read file, substring match | Replace with correct text |
| Article number is precise | Frontmatter `article` + `article_title` match | Correct the number |
| Recital-Article alignment | Recital's `related_articles` field | Flag weak connection |
| EDPB/CJEU citation exists | Search respective KB directories | Downgrade or remove |
| Cross-reference is valid | Verify target file exists | Flag broken reference |
| Web source is trusted | Match against trusted domain list | Downgrade Grade |

**Confidence threshold:** If below 70%, FAIL items are corrected and re-verified before output. Citations affecting core conclusions are withdrawn rather than left unverified.

---

## Citation Audit

The repository includes `citation-auditor`, a post-hoc audit layer for citation-bearing factual claims.

There are two ways to use it:

- **Automatic memo/opinion pass** — for legal opinions, memoranda, DOCX documents, and comprehensive analyses, the agent runs an additional final-pass audit after fact-checking. Markdown outputs receive an appended `Citation Audit Log`; DOCX outputs consume the same aggregated audit JSON through `scripts/docx_citation_appendix.py` and append a styled audit table.
- **Standalone `/audit` command** — run an audit on any existing Markdown file:

```bash
/audit path/to/opinion.md
```

The auditor chunks Markdown, extracts verifiable factual/citation claims, routes them to verifier skills (`eu-law`, `korean-law`, `us-law`, `uk-law`, `scholarly`, `wikipedia`, `general-web`), and renders verdicts as `verified`, `contradicted`, or `unknown`.

---

## Source Ingest System

### Adding Your Own Sources

The knowledge base is designed to grow. National transposition laws, DPA decisions from your jurisdiction, internal guidance — anything can be added.

```
library/inbox/    <-- drop any file here (PDF, DOCX, HTML, etc.)
     |
     v  Tell the agent: /ingest or "I added files to inbox"
     |
     |-- 1. AUTO-CONVERT to Markdown (via MarkItDown CLI)
     |       Supports: PDF, DOCX, PPTX, HTML, XLSX, images
     |
     |-- 2. AUTO-CLASSIFY Grade (based on content signals)
     |       Grade A: Official sources (eur-lex.europa.eu, edpb.europa.eu, national DPA domains)
     |       Grade B: Court decisions, DPA enforcement decisions
     |       Grade C: Law firm analyses, academic papers (SSRN, journals)
     |       Grade D: News, AI summaries -> REJECTED with warning
     |
     |-- 3. AUTO-GENERATE frontmatter
     |       Extracts: title, publisher, date, keywords, GDPR articles mentioned
     |
     |-- 4. AUTO-PLACE in correct directory
     |       library/grade-a/{category}/ or grade-b/ or grade-c/
     |
     '-- 5. AUTO-UPDATE search indexes
            Rebuilds JSON indexes so new content is immediately searchable
```

### When to Use Ingest

| Scenario | What to Add | Where It Goes |
|----------|------------|-------|
| **National ePrivacy implementation** | Your country's transposition law (e.g., German TTDSG, French CNIL guidance) | Grade A |
| **Recent DPA decision** | PDF from your national DPA's website | Grade B |
| **Internal guidance** | Your organization's data protection policies | Grade B/C |
| **Academic paper** | PDF from SSRN or law journal | Grade C |

> **Note:** Dropping files alone does not trigger processing. You must run `/ingest` or tell the agent (e.g., "I added files to the inbox") to start the pipeline.

---

## Project Structure

```
GDPR-expert/
├── library/
│   ├── inbox/                          # Drop zone for new sources
│   ├── grade-a/                        # Authoritative sources
│   │   ├── gdpr/                       #   GDPR articles (99)
│   │   ├── gdpr-recitals/             #   GDPR Recitals (173)
│   │   ├── eprivacy-directive/        #   ePrivacy articles (21)
│   │   ├── eu-ai-act/                 #   AI Act articles (113)
│   │   ├── eu-ai-act-recitals/       #   AI Act Recitals (180)
│   │   ├── data-act/                  #   Data Act articles (50)
│   │   ├── data-act-recitals/        #   Data Act Recitals (119)
│   │   ├── data-governance-act/       #   DGA articles (38)
│   │   ├── data-governance-act-recitals/ # DGA Recitals (63)
│   │   ├── edpb-guidelines/           #   EDPB Guidelines (52)
│   │   ├── edpb-opinions/            #   EDPB Opinions (31)
│   │   ├── edpb-binding-decisions/   #   Art. 65 Binding Decisions (10)
│   │   ├── edpb-recommendations/     #   EDPB Recommendations (7)
│   │   ├── edpb-statements/          #   EDPB Statements (19)
│   │   ├── edpb-reports/             #   EDPB Reports (1)
│   │   └── cjeu-cases/              #   CJEU Judgments (51)
│   ├── grade-b/                        # Verified secondary
│   │   ├── enforcement-decisions/     #   DPA fines & decisions (33)
│   │   └── legislative-proposals/    #   Digital Omnibus Package (2)
│   └── grade-c/                        # Academic papers
├── index/                              # 5 JSON indexes (1,060+ items)
├── config/                             # Grade definitions + RAG config
├── scripts/                            # Collection & processing scripts
├── .claude/agents/                     # Agent + fact-checker definitions
└── output/opinions/                    # Generator scripts; opinion files live in $GDPR_EXPERT_PRIVATE_DIR
```

---

## Getting Started

> **New here?** Read the **[How to Use Guide](docs/en/HOW-TO-USE.md)** — a step-by-step walkthrough for non-developers.

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) CLI
- Python 3.10+
- Runtime dependencies (`pip install -r requirements.txt`)
- `markitdown` (optional, for PDF ingestion: `pip install markitdown`)

### Setup

```bash
git clone https://github.com/kipeum86/GDPR-expert.git
cd GDPR-expert
pip install -r requirements.txt -r requirements-dev.txt
# Optional, only when ingesting PDFs:
pip install markitdown
```

### Refresh Legislation Data

```bash
# Fetch all 5 EU laws from CELLAR API (no auth required)
python3 scripts/fetch-eu-legislation.py

# Fetch specific law only
python3 scripts/fetch-eu-legislation.py --law gdpr

# Rebuild search indexes after any data change
python3 scripts/build-indexes.py --type all
```

### Run the Agent

```bash
cd GDPR-expert
claude --agent .claude/agents/gdpr-agent.md
```

### Example Queries

```
"Analyze whether we can rely on legitimate interest for AI model training under Art. 6(1)(f)"
"What did the CJEU say about automated decision-making in the SCHUFA case?"
"Compare the breach notification requirements under GDPR vs. the Digital Omnibus proposal"
"Draft a legal analysis memo on cross-border data transfers to the US — DOCX format, English and Korean"
"What are the EDPB's binding decisions on Meta and what fines were imposed?"
```

---

## Part of KP Legal Orchestrator

This agent is part of the **KP Legal Orchestrator** series of specialized legal workflow agents:

| Agent | Public Role | Focus |
|-------|-------------|-------|
| [game-legal-research](https://github.com/kipeum86/game-legal-research) | Game Industry Specialist | Game industry law research |
| [legal-translation-agent](https://github.com/kipeum86/legal-translation-agent) | Legal Translation Specialist | Legal translation workflows |
| [general-legal-research](https://github.com/kipeum86/general-legal-research) | General Legal Research Specialist | Broad legal research |
| [PIPA-expert](https://github.com/kipeum86/PIPA-expert) | Privacy Law Specialist | Korean privacy law |
| **[GDPR-expert](https://github.com/kipeum86/GDPR-expert)** | **EU Data Protection Specialist** | **GDPR, ePrivacy, AI Act, and DGA analysis** |
| [contract-review-agent](https://github.com/kipeum86/contract-review-agent) | Contract Review Specialist | Contract analysis |
| [legal-writing-agent](https://github.com/kipeum86/legal-writing-agent) | Legal Drafting Specialist | Drafting and redline workflows |
| [second-review-agent](https://github.com/kipeum86/second-review-agent) | Senior Review Specialist | Second-pass review and QA |

---

## License

Apache 2.0

---

<div align="center">
<sub>Built with structured data, not blind faith in embeddings.</sub>
<br/>
<sub>Explore the companion repositories above for adjacent legal workflow coverage.</sub>
</div>
