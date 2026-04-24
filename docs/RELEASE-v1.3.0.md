# GDPR Expert v1.3.0 — Citation Audit + DOCX Appendix (2026-04-24)

> Recommended: pull this release before producing formal opinions or memoranda. It adds a post-hoc citation audit layer and makes the public legal-writing style guide part of the normal drafting workflow.

## What Changed

- **citation-auditor added** — `/audit <file.md>` can audit existing Markdown deliverables by extracting citation-bearing factual claims, routing them to verifier skills, aggregating verdicts, and rendering annotated Markdown.
- **Conditional memo/opinion final pass** — formal opinions, memoranda, DOCX documents, and comprehensive analyses now have a documented citation-audit final pass after the built-in fact-checker.
- **DOCX adapter** — `scripts/docx_citation_appendix.py` lets DOCX renderers consume aggregated audit JSON, inject `[Unverified]` / `[Partially Unverified]` tags, and append a styled Citation Audit Log appendix.
- **Legal-writing guide published** — `legal-writing-formatting-guide.md` is now the public EN/KO drafting reference for formal legal opinions and memoranda.
- **Runtime dependencies** — `requirements.txt` now declares `pydantic>=2.0` and `marko>=2.0`.

## Vendor Boundary

The vendored auditor remains isolated:

- `citation_auditor/`
- `.claude/skills/citation-auditor/`
- `.claude/skills/verifiers/`
- `.claude/commands/audit.md`

Project-specific DOCX integration lives under `scripts/` so future vendor updates can be reapplied cleanly.

## Format Coverage

| Format | Citation audit behavior |
|--------|--------------------------|
| `.md` | Native append-mode audit log |
| `.docx` | Adapter-based tag injection + audit appendix |
| `.html`, `.txt` | Use audited Markdown as the source or sidecar |
| `.pdf`, `.pptx` | Sidecar audited Markdown fallback until native wiring exists |

## Verification

- Vendor copy cleaned of `__pycache__`, `.DS_Store`, and empty helper directories.
- `python -m citation_auditor --help` exposes `chunk`, `aggregate`, `render`, and `korean_law`.
- DOCX smoke test validates tag injection and appendix table generation.

---

# GDPR Expert v1.3.0 — Citation Audit + DOCX 부록 (2026-04-24)

> 권장: 정식 의견서나 메모를 작성하기 전에 이 릴리스를 pull 하세요. 사후 인용 감사 레이어가 추가되고, 공개 legal-writing style guide가 일반 작성 워크플로우에 연결됩니다.

## 변경 사항

- **citation-auditor 추가** — `/audit <file.md>`로 기존 Markdown 산출물을 감사할 수 있습니다. 사실·인용 기반 클레임을 추출하고, verifier skill로 라우팅한 뒤, 판정을 집계하여 주석 달린 Markdown을 렌더링합니다.
- **memo/opinion 조건부 최종 패스** — 정식 의견서, 메모, DOCX 문서, 종합 분석에는 기본 fact-check 이후 citation audit 최종 패스를 문서화했습니다.
- **DOCX 어댑터** — `scripts/docx_citation_appendix.py`가 aggregated audit JSON을 소비하여 `[Unverified]` / `[Partially Unverified]` 태그를 주입하고, 스타일된 Citation Audit Log 부록을 DOCX에 붙입니다.
- **Legal-writing guide 공개** — `legal-writing-formatting-guide.md`가 정식 법률의견서와 메모를 위한 EN/KO 공개 작성 기준으로 연결되었습니다.
- **런타임 의존성** — `requirements.txt`에 `pydantic>=2.0`, `marko>=2.0`를 선언했습니다.

## Vendor 경계

vendored auditor는 분리된 상태로 유지됩니다:

- `citation_auditor/`
- `.claude/skills/citation-auditor/`
- `.claude/skills/verifiers/`
- `.claude/commands/audit.md`

프로젝트별 DOCX 통합은 `scripts/` 아래에 두어, 향후 vendor update를 깨끗하게 재적용할 수 있습니다.

## 포맷 커버리지

| 포맷 | Citation audit 동작 |
|------|---------------------|
| `.md` | 네이티브 append-mode 감사 로그 |
| `.docx` | 어댑터 기반 태그 주입 + 감사 부록 |
| `.html`, `.txt` | 감사된 Markdown을 source 또는 sidecar로 사용 |
| `.pdf`, `.pptx` | native wiring 전까지 감사된 Markdown sidecar fallback |

## 검증

- vendor copy에서 `__pycache__`, `.DS_Store`, 빈 helper directory 제거.
- `python -m citation_auditor --help`에서 `chunk`, `aggregate`, `render`, `korean_law` 노출 확인.
- DOCX smoke test로 태그 주입과 부록 표 생성을 확인.
