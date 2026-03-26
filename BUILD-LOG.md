# GDPR-expert Build Log

## 2026-03-25 — Day 1: From Zero to 857 Legal Files in One Session

### The Vision
PIPA-expert(한국 개인정보보호법 AI 에이전트)를 성공적으로 구축한 후, 같은 아키텍처로 EU 데이터 보호 법령 전문 에이전트를 만들기로 결정.

### Design Phase (~30분)
- `/office-hours` 스킬로 디자인 문서 작성
- 핵심 결정: GDPR + ePrivacy + AI Act + Data Act + DGA (5개 법령)
- DSA/DMA는 스코프 아웃 — "GDPR expert"가 "EU digital regulation 백과사전"이 되면 안 됨

### Engineering Review (~20분)
- `/plan-eng-review` 스킬로 10개 이슈 발견 및 해결
- 외부 리뷰어(Claude subagent)의 핵심 지적:
  - "CJEU 판례를 Grade B로 두면 안 된다 — EU법에서 CJEU는 구속력 있는 해석이다" → Grade A로 승격
  - "에이전트를 마지막에 만들지 말고 먼저 만들어라 — 기존 48개 파일로 즉시 작동" → Phase 0.5로 변경
  - "EUR-Lex SOAP API가 Formex XML을 직접 안 줄 수도 있다" → 실제 검증 필수

### Phase 0: Infrastructure (~5분)
- Git init, 디렉토리 구조 생성 (25개 폴더)
- PIPA-expert에서 config 파일 복사 + EU 버전으로 수정
- `.env` (EUR-Lex API credentials), `.gitignore` 설정

### Phase 0: API Verification — The Plot Twist (~10분)
- EUR-Lex SOAP API → **401 Unauthorized** (인증 방식 문제)
- EUR-Lex 웹사이트 → **AWS WAF** 차단 (JavaScript 필요)
- **CELLAR REST API** → 성공! `Accept: application/xhtml+xml`로 804KB GDPR 전문 수신
- XHTML에 `id="art_1"` ~ `id="art_99"`, `id="rct_1"` ~ `id="rct_173"` 완벽한 구조 확인
- **결정: SOAP 대신 CELLAR REST가 primary 경로**

### Phase 1-2: 법령 수집 — 857 Files in 30 Seconds (~15분)
- `fetch-eu-legislation.py` 작성 (CELLAR REST XHTML 파싱)
- GDPR: 99 articles + 173 recitals → **0 errors**
- ePrivacy Directive: 21 articles → 0 errors (통합본 CELEX 발견 필요)
- EU AI Act: 113 articles + 180 recitals → 0 errors
- Data Act: 50 articles + 120 recitals → 0 errors
- DGA: 38 articles + 63 recitals → 0 errors
- **총: 321 articles + 536 recitals = 857개 파일, 0 errors**

### Phase 0.5: MVP Agent (~10분)
- PIPA-expert의 에이전트 구조를 EU 버전으로 적응
- `gdpr-agent.md`: Dr. Elena Richter 페르소나, 4-step 검색 프로토콜, Dual-Pass 검증
- `fact-checker/AGENT.md`: 8개 검증 항목 (조문 존재, 내용 일치, Recital 정합성 등)
- `CLAUDE.md`: 프로젝트 개요

### Digital Omnibus Package 발견 (~중간)
- 유저가 Digital Omnibus Package (2025.11.19 EC 채택) 지적
- COM(2025) 836 (AI Act 개정안) + COM(2025) 837 (GDPR/ePrivacy/Data Act 등 개정안)
- 아직 proposal 단계이므로 Grade B 참고자료로 수집 결정
- GDPR Art. 6(1)(f) legitimate interest에 AI 명시적 인정 등 중요한 변경 포함

### Stats So Far

| Metric | Count |
|--------|-------|
| 법령 수 | 5 |
| Articles | 321 |
| Recitals | 536 |
| 기존 EDPB Guidelines | 20 |
| 기존 CJEU Cases | 17 |
| 기존 Enforcement Decisions | 10 |
| 총 KB 파일 | 904+ |
| Errors | 0 |
| 소요 시간 | ~1.5시간 (디자인 + 리뷰 + 구현) |

### Key Insight
> "EUR-Lex SOAP API가 401을 뱉었을 때 당황하지 않고 CELLAR REST API로 피벗한 것이 결정적이었다. Publications Office의 CELLAR는 인증 없이 구조화된 XHTML을 제공한다 — 이게 진짜 기계 접근용 API다."

### Digital Omnibus Package (~5분)
- COM(2025) 836 (AI Act 개정안) + COM(2025) 837 (GDPR/ePrivacy/Data Act 등 개정안)
- EP와 Council PDF 다운로드 → markitdown → Grade B로 배치
- 아직 proposal 단계이지만, frontmatter `key_changes`에 GDPR Art. 6(1)(f) AI legitimate interest 등 핵심 변경사항 요약

### Phase 3: EDPB 문서 85개 배치 수집 (~4분)
- `edpb_documents_catalog.json` 86개 문서 카탈로그 작성
- `fetch-edpb-guidelines.py`로 PDF 다운로드 + markitdown 변환 자동화
- 85개 성공, 0 실패 (1개는 URL 없어서 스킵)
- Guidelines 52개 + Recommendations 7개 + Opinions 6개 + Statements 19개 + Report 1개

### Phase 4: 마이그레이션 + 인덱스 (~5분)
- 기존 CJEU 17개 → `library/grade-a/cjeu-cases/` (Grade A — EU법에서 CJEU는 구속력 있는 해석)
- 기존 집행결정 10개 → `library/grade-b/enforcement-decisions/`
- 기존 GDPR 원문 → `library/inbox/archive/`
- `build-indexes.py --type all`로 5개 인덱스 빌드:
  - article-index.json (321 articles)
  - recital-index.json (173 recitals)
  - edpb-document-index.json (85 documents)
  - case-index.json (17 cases)
  - enforcement-index.json (10 decisions)

## Final Stats (Day 1)

| Category | Count | Grade |
|----------|-------|-------|
| **Legislation articles** | 321 | A |
| **Recitals** | 536 | A |
| **EDPB Guidelines** | 52 | A |
| **EDPB Opinions** | 6 | A |
| **EDPB Recommendations** | 7 | A |
| **EDPB Statements** | 19 | A |
| **CJEU Cases** | 17 | A |
| **Enforcement Decisions** | 10 | B |
| **Legislative Proposals** | 2 | B |
| **TOTAL** | **970** | |

## Key Decisions Made
1. **CELLAR REST > SOAP API** — EUR-Lex SOAP API는 401 반환. CELLAR XHTML이 인증 없이 구조화된 데이터 제공
2. **CJEU = Grade A** — EU법에서 CJEU 판례는 구속력 있는 해석. 한국법(Grade B) 관행 미적용
3. **에이전트 먼저** — Phase 0.5에서 MVP 에이전트 구축. KB 수집과 병행
4. **Digital Omnibus = Grade B** — 아직 proposal이지만 GDPR 개정 방향 파악에 필수

## Architecture

```
GDPR-expert KB (970 files)
├── library/grade-a/          → 958 files (legislation + EDPB + CJEU)
│   ├── gdpr/                 99 articles
│   ├── gdpr-recitals/       173 recitals
│   ├── eprivacy-directive/   21 articles
│   ├── eu-ai-act/           113 articles (+180 recitals in same dir)
│   ├── data-act/             50 articles (+120 recitals)
│   ├── data-governance-act/  38 articles (+63 recitals)
│   ├── edpb-guidelines/      52 documents
│   ├── edpb-opinions/         6 documents
│   ├── edpb-recommendations/  7 documents
│   ├── edpb-statements/      19 documents
│   └── cjeu-cases/           17 cases
├── library/grade-b/          → 12 files
│   ├── enforcement-decisions/ 10 decisions
│   └── legislative-proposals/  2 (Digital Omnibus)
└── index/                    → 5 JSON indexes + source registry
```

### Phase 5: 고영향 자료 확장 (~25분, 병렬 리서치)

3개 에이전트가 동시에 리서치:
- **CJEU 판례 34건** 추가: Deutsche Wohnen (기업 과징금 책임), SCHUFA Scoring (Art. 22 자동화 결정), IAB Europe TCF (adtech 공동 컨트롤러) 등
- **Art. 65 binding decisions 10건**: Meta/WhatsApp/Instagram/TikTok/Facebook 대상 EDPB 구속력 있는 결정 전수
- **EDPB Opinions 25건** 추가: 적정성 결정 (일본, 한국, 영국), AI Act, SCCs, 건강데이터, 인증 등
- **집행결정 25건** 추가: CNIL v Google EUR 325M, H&M EUR 35M (직원감시), OpenAI EUR 15M (최초 GenAI 과징금) 등

### 레거시 KB 정리
- `gdpr-agent-kb/` → `library/inbox/archive/gdpr-agent-kb-legacy/`로 통합
- 모든 데이터가 `library/` 단일 구조로 통일

## Final Stats

| Category | Count | Grade |
|----------|-------|-------|
| **GDPR Articles** | 99 | A |
| **GDPR Recitals** | 173 | A |
| **ePrivacy Articles** | 21 | A |
| **EU AI Act Articles** | 113 | A |
| **Data Act Articles** | 50 | A |
| **DGA Articles** | 38 | A |
| **EDPB Guidelines** | 52 | A |
| **EDPB Opinions** | 31 | A |
| **EDPB Binding Decisions** | 10 | A |
| **EDPB Recommendations** | 7 | A |
| **EDPB Statements** | 19 | A |
| **EDPB Reports** | 1 | A |
| **CJEU Cases** | 51 | A |
| **Enforcement Decisions** | 35 | B |
| **Legislative Proposals** | 2 | B |
| **TOTAL** | **702** | |

## Architecture (Final)

```
GDPR-expert KB (702 files)
├── library/grade-a/           → 665 files
│   ├── gdpr/                  99 articles
│   ├── gdpr-recitals/        173 recitals
│   ├── eprivacy-directive/    21 articles
│   ├── eu-ai-act/            113 articles
│   ├── data-act/              50 articles
│   ├── data-governance-act/   38 articles
│   ├── edpb-guidelines/       52 guidelines
│   ├── edpb-opinions/         31 opinions
│   ├── edpb-binding-decisions/ 10 Art.65 decisions
│   ├── edpb-recommendations/   7 recommendations
│   ├── edpb-statements/       19 statements
│   ├── edpb-reports/           1 report
│   └── cjeu-cases/            51 judgments
├── library/grade-b/           → 37 files
│   ├── enforcement-decisions/  35 DPA decisions
│   └── legislative-proposals/   2 Digital Omnibus
└── index/                     → 5 JSON indexes (690 indexed items)
```

## Timeline

| Time | What |
|------|------|
| 0:00 | `/office-hours` — 디자인 문서 작성 |
| 0:30 | `/plan-eng-review` — 10개 이슈 발견/해결 |
| 0:50 | Phase 0 — Git init, 디렉토리, configs |
| 0:55 | EUR-Lex API 검증 — SOAP 실패 → CELLAR XHTML 발견 |
| 1:05 | Phase 1-2 — 5개 법령 321 articles + 536 recitals, 0 errors |
| 1:15 | Phase 0.5 — MVP 에이전트 + 팩트체커 |
| 1:20 | Digital Omnibus Package 수집 (Grade B) |
| 1:25 | Phase 3 — EDPB 85개 문서 배치 수집 |
| 1:35 | Phase 4 — 마이그레이션 + 인덱스 빌드 |
| 1:45 | Phase 5 — CJEU 34 + Art.65 10 + Opinions 25 + 집행결정 25 |
| 2:10 | 레거시 KB 정리 + 최종 인덱스 재빌드 |

> **소요 시간: ~2.5시간 (디자인 리뷰 포함). 702개 KB 파일. 0 errors.**
>
> **핵심 인사이트:** "EUR-Lex SOAP API가 401을 뱉었을 때 CELLAR REST로 피벗한 것이 프로젝트를 살렸다. Publications Office의 CELLAR는 인증 없이 구조화된 XHTML을 제공한다 — 이게 진짜 기계 접근용 API다. 그리고 에이전트를 먼저 만든 것이 옳았다 — KB를 확장하면서 에이전트로 검증할 수 있었다."
