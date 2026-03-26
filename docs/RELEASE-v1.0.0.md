# GDPR Expert v1.0.0

An AI agent that reads EU data protection law the way a lawyer would — article by article, cross-referencing Recitals, EDPB guidance, and CJEU case law — instead of dumping PDFs into a vector database.

## How It Works

All legal sources are collected from **official EU APIs** (not scraped), parsed into article-level Markdown files with structured metadata, and indexed for instant search. The agent reads the actual law, follows cross-references, and fact-checks every citation before output.

## Knowledge Base

| | Count |
|---|---|
| **Legislation** | 5 EU laws — 321 articles + 535 recitals |
| **EDPB** | 120 documents (guidelines, opinions, Art. 65 binding decisions) |
| **CJEU** | 51 landmark judgments |
| **Enforcement** | 35 major DPA decisions |
| **Digital Omnibus** | COM(2025) 836 + 837 proposals |
| **Total indexed** | **1,062 sources** |

**Laws:** GDPR · ePrivacy Directive · EU AI Act · Data Act · Data Governance Act

## What Makes This Different

- **Structured data, not flat text** — each article is a file with YAML frontmatter (cross-references, keywords, source grade, effective date)
- **Source authority grades** — Grade A (legislation, EDPB, CJEU) through D (excluded). Every citation is tagged
- **9-source mandatory search** — the agent must search all source categories before writing an opinion. No cherry-picking
- **Built-in fact-checker** — a sub-agent verifies every legal citation against the knowledge base before output
- **Multilingual** — English, Korean, German, French, Dutch, and other EU languages
- **Expandable** — drop a PDF in `library/inbox/`, run `/ingest`, and it's classified, tagged, and indexed automatically

## Sample Output

A B2B SaaS processor wants to fine-tune an LLM on client data — can they rely on legitimate interest?

→ [English opinion](https://docs.google.com/document/d/1D3jVVQLLaSgXXqvUGWEpoqeMYjOFwBe-/edit?usp=sharing) · [한국어 의견서](https://docs.google.com/document/d/1ImyHxEwdy30mw0N3BFnn9z8qxiK0JK0n/edit?usp=sharing)

## Quick Start

```bash
git clone https://github.com/lowtidebuild/GDPR-expert.git
cd GDPR-expert
pip install python-docx markitdown
claude --agent .claude/agents/gdpr-agent.md
```

→ [How to Use Guide](docs/en/HOW-TO-USE.md) (no technical background needed) · [사용 가이드](docs/ko/HOW-TO-USE.md)

## Disclaimer

AI-generated output — not legal advice. Built-in fact-checker verifies citations but is not infallible. [Full Disclaimer](docs/en/DISCLAIMER.md)
