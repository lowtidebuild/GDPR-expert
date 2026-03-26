# How to Use GDPR Expert

[English](./HOW-TO-USE.md) | [한국어](../ko/HOW-TO-USE.md)

> This guide is written for **non-developers**. You don't need to understand Python, Git, or APIs. If you can type a question, you can use this tool.

---

## What You Need (One-Time Setup)

| What | Why | How to Get It |
|------|-----|---------------|
| **Claude Code** | This is the app that runs the agent | [Download here](https://claude.ai/claude-code) — available as CLI, desktop app, or VS Code extension |
| **This repository** | Contains the legal knowledge base + agent | Your team lead or IT will provide access |

That's it. No databases, no servers, no API keys to configure (unless you want to refresh the legal data yourself).

---

## Starting the Agent

### Option A: Desktop App / VS Code

1. Open Claude Code
2. Open the `GDPR-expert` folder
3. The agent activates automatically — you'll see it has access to the legal knowledge base

### Option B: Terminal (CLI)

```bash
cd GDPR-expert
claude --agent .claude/agents/gdpr-agent.md
```

---

## Asking Questions

Just type your question in natural language. The agent understands both **English** and **Korean**, and can also respond in major EU languages upon request.

### Simple Lookups

> "Show me GDPR Article 6"

> "What does Article 17 say about the right to erasure?"

> "What are the EDPB's guidelines on consent?"

### Legal Analysis

> "Can we rely on legitimate interest to send marketing emails to our existing B2B customers?"

> "What are the legal requirements for appointing a DPO under Articles 37-39?"

> "Compare the data breach notification requirements under GDPR and the NIS2 Directive"

### Cross-Referencing

> "Which Recitals explain the legitimate interest balancing test under Article 6(1)(f)?"

> "What CJEU cases have interpreted the right to erasure under Article 17?"

> "How does the ePrivacy Directive interact with GDPR for cookie consent?"

### Forward-Looking Analysis

> "How would the Digital Omnibus Package change the breach notification rules if adopted?"

> "What changes does the Digital Omnibus propose for AI training under legitimate interest?"

---

## Requesting a Legal Opinion (DOCX)

When you need a formal document — not just a chat answer — ask for a legal opinion:

> "Draft a legal opinion on whether our company can transfer employee data to the US after Schrems II. DOCX format."

> "Write a compliance assessment for our AI-powered recruitment tool under GDPR and the AI Act. English and Korean versions."

> "Prepare a DPIA analysis for our new customer profiling feature. DOCX."

The agent will:
1. Research across the full knowledge base (legislation, guidelines, case law)
2. Draft a structured opinion with verified citations
3. Run the fact-checker to verify every legal reference
4. Generate a professional DOCX file saved to `output/opinions/`

### Bilingual Opinions

Add "English and Korean" to your request:

> "Legal opinion on international data transfers — DOCX, English and Korean versions"

The agent will produce two separate DOCX files. In the Korean version, **legal citations remain in the original English** (EU law is authoritative in English) while the analysis and commentary are in Korean.

---

## Understanding the Output

### Citation Tags

Every legal reference in the agent's output is tagged so you know how reliable it is:

| Tag | What It Means | Should You Trust It? |
|-----|--------------|---------------------|
| `[VERIFIED] [Grade A]` | Matched exactly against the legislation text in the knowledge base | High confidence — but always double-check critical points |
| `[VERIFIED] [Grade B]` | From a DPA enforcement decision or court ruling in the KB | Good confidence — these are authoritative but secondary |
| `[UNVERIFIED]` | Found via web search, not in the local knowledge base | Verify independently before relying on it |
| `[INSUFFICIENT]` | The agent couldn't find enough evidence | The agent is being honest — don't guess, consult a lawyer |
| `[CONTRADICTED]` | Different sources say different things | Both sides are shown — you decide which applies |

### Source Grades

| Grade | What's In It | Can You Rely On It Alone? |
|-------|-------------|--------------------------|
| **A** | EU legislation text, EDPB guidelines, CJEU judgments | Yes |
| **B** | DPA enforcement decisions, national court rulings | Yes, but cross-check with Grade A recommended |
| **C** | Law firm analyses, academic papers | No — use as commentary only |
| **D** | News articles, AI summaries | Excluded from the system entirely |

---

## Adding Your Own Sources

Got a national DPA decision, an internal policy, or an academic paper you want the agent to know about?

### Step 1: Drop the file

Place any file (PDF, DOCX, HTML) into the `library/inbox/` folder.

### Step 2: Tell the agent

> "I added a file to the inbox, please ingest it"

or simply:

> "/ingest"

### Step 3: Done

The agent will:
- Convert the file to Markdown
- Automatically classify its trust level (Grade A, B, or C)
- Extract metadata (title, date, keywords, related GDPR articles)
- Place it in the correct folder
- Update the search indexes

Your new source is now searchable and citable in future opinions.

### What to Add (Examples)

| You Have | What Happens |
|----------|-------------|
| German TTDSG (national ePrivacy law) | Classified as Grade A, filed under legislation |
| French CNIL decision PDF | Classified as Grade B, filed under enforcement |
| Freshfields client alert on AI Act | Classified as Grade C, filed under reference |
| TechCrunch article about GDPR fine | Rejected as Grade D with a warning |

---

## Tips for Best Results

### Be Specific

| Instead of | Try |
|-----------|-----|
| "Tell me about GDPR" | "What are the six legal bases for processing under GDPR Article 6?" |
| "Is this legal?" | "Can a processor use controller's data for AI training without explicit authorization under Article 28?" |
| "What about data transfers?" | "What safeguards are required for transferring personal data to the US after the Schrems II judgment?" |

### Ask for Counterarguments

> "What are the arguments AGAINST relying on legitimate interest for this processing?"

The agent has a built-in adversarial mode — it will look for exceptions, contrary case law, and alternative interpretations. But it helps to ask explicitly.

### Request the Fact-Check Report

For important opinions, ask to see the verification results:

> "Show me the fact-check report for this opinion"

This shows you exactly which citations were verified, which had issues, and the overall confidence score.

---

## What This Tool Does NOT Do

- **It does not provide legal advice.** It's a research assistant that helps you find and organize legal sources faster. A qualified lawyer must review the output.
- **It does not know about your specific contracts or internal policies** — unless you add them via the ingest system.
- **It does not automatically update.** The legal data is a snapshot. Run the refresh scripts periodically or add new sources via ingest.
- **It does not cover national implementations of EU Directives** by default. The ePrivacy Directive, for example, is transposed differently in each EU Member State. Add your country's implementation via ingest.

---

## Getting Help

- **Something looks wrong?** Ask the agent: "Verify your last citation for Article X"
- **Need a different format?** Just ask: "Give me this as a markdown summary" or "Make it a DOCX"
- **Agent seems stuck?** Try rephrasing your question or breaking it into smaller parts
- **Technical issues?** Contact your team lead or check the [GitHub repository](https://github.com/lowtidebuild/GDPR-expert)

---

> **Remember:** This is a power tool, not an autopilot. It makes legal research dramatically faster and more thorough, but the final judgment always belongs to a qualified human.
