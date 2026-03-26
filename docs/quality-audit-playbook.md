# Quality Audit Playbook

법률 KB(Knowledge Base) 프로젝트에 대한 품질 감사 + 수정 재현용 플레이북.
GDPR-expert에서 실전 검증된 프로세스를 정리한 것으로, PIPA-expert 등 동일 아키텍처 프로젝트에 그대로 적용 가능.

---

## Phase 1: 감사 (Audit)

4개 병렬 에이전트로 전수 검사. 각 에이전트에 아래 프롬프트를 줄 것.

### Agent 1: Frontmatter Schema Consistency

**목적:** 모든 .md 파일의 YAML frontmatter가 일관된 스키마를 따르는지 확인

**점검 항목:**
- [ ] 모든 파일에 frontmatter(`---` ... `---`)가 존재하는가
- [ ] 디렉토리별 필수 필드가 빠짐없이 있는가
  - 법령 파일: `law`, `law_id`, `article`, `article_title`, `chapter`, `source_grade`, `source_url`, `effective_date`, `cross_references`, `keywords`
  - EDPB 문서: `title`, `document_type`, `document_number`, `adopted_date`, `source_grade`, `keywords`
  - 판례: `case_number`, `case_name`, `date`, `source_grade`, `keywords`
  - 집행결정: `title`, `authority`, `date`, `source_grade`, `keywords`
- [ ] 필드값 타입이 일관적인가 (따옴표 유무, 배열 문법 등)
- [ ] `source_grade`가 디렉토리 Grade와 일치하는가 (grade-a → "A", grade-b → "B")
- [ ] `source_id` 접두사가 Grade와 일치하는가 (grade-a → `a-`, grade-b → `b-`)
- [ ] 빈 배열 필드(`keywords:`, `cross_references:`)가 YAML 파서에서 `null`이 아닌 `[]`로 읽히는가

**흔한 버그:**
- 2차에 걸친 데이터 수집으로 구형/신형 스키마 혼재
- source_grade가 디렉토리와 불일치 (grade-b인데 `"A"`)
- 빈 값이 YAML `null`로 파싱됨 → MCP/외부 소비자에서 crash

### Agent 2: Cross-Reference Validity

**목적:** frontmatter의 `cross_references`, `related_articles`, `related_recitals`가 실존 파일을 가리키는지 확인

**점검 항목:**
- [ ] 모든 내부 cross-reference가 실존 파일에 매핑되는가 (Art. 6 → art6.md 존재)
- [ ] 외부 법령 참조(TFEU, Charter 등)가 내부 참조와 구분되어 있는가
- [ ] self-reference가 없는가 (Art. 5 → Art. 5)
- [ ] `_cross-refs.json`과 개별 파일 frontmatter가 일치하는가
- [ ] 참조 대상 조문 번호가 해당 법의 범위 내인가 (GDPR Art. 100 같은 유령 참조)

**흔한 버그:**
- Recital에서 "Article 16 of the Treaty"를 GDPR Art. 16으로 잘못 파싱
- `_cross-refs.json`이 frontmatter와 불일치 (한쪽만 업데이트)

### Agent 3: Recital/Article Mapping Completeness

**목적:** 법조문 ↔ Recital 양방향 매핑이 완전한지 확인 (해당되는 법령에 한함)

**점검 항목:**
- [ ] Recital 파일에 `related_articles` 필드가 존재하고 채워져 있는가
- [ ] Article 파일에 `related_recitals` 필드가 존재하고 채워져 있는가
- [ ] 매핑이 양방향으로 일관적인가 (Recital 47 → Art. 6이면, Art. 6 → Recital 47도 있어야)
- [ ] 알려진 핵심 매핑이 정확한가 (프로젝트별 샘플 검증)
- [ ] `_cross-refs.json`의 `recital_to_article`, `article_to_recital` 섹션이 채워져 있는가

**핵심 참고:**
- 텍스트 추출만으로는 부족함. 대부분의 Recital이 "Article N"을 명시적으로 언급하지 않음
- 권위 있는 외부 소스(예: gdpr-info.eu의 "Suitable Recitals")에서 크롤링하는 것이 정확도 면에서 압도적
- PIPA의 경우 법제처 또는 학술 자료에서 조문-이유 매핑을 확인할 것

### Agent 4: Index-Library Sync

**목적:** JSON 인덱스 파일이 실제 library 파일과 정확히 동기화되어 있는지 확인

**점검 항목:**
- [ ] 각 인덱스의 `count`가 실제 디스크 파일 수와 일치하는가
- [ ] 인덱스에 있는데 디스크에 없는 파일이 있는가 (유령 항목)
- [ ] 디스크에 있는데 인덱스에 없는 파일이 있는가 (미인덱싱)
- [ ] 인덱스의 메타데이터(title, date, source_id 등)가 원본 frontmatter와 일치하는가
- [ ] `source-registry.json`의 count/target/status가 현실을 반영하는가
  - count < target인데 "complete"로 표기되면 안 됨
- [ ] 인덱스 빌더가 올바른 필드명을 읽고 있는가 (마이그레이션 후 필드명 변경 반영 여부)

**흔한 버그:**
- 스키마 마이그레이션 후 인덱스 재빌드 안 함 → stale index
- `published_date` → `decision_date`로 바꿨는데 빌더는 여전히 `published_date`를 읽음

### 추가 Agent: 원문 대조 (Content Accuracy)

**목적:** KB의 법 조문 텍스트가 공식 원문과 일치하는지 샘플 검증

**점검 항목:**
- [ ] 핵심 조문 3-5개를 공식 소스(EUR-Lex, 법제처 등)와 word-for-word 대조
- [ ] 다른 법의 텍스트가 섞여 들어간 파일이 없는가 (교차 오염)
- [ ] HTML 잔여물, 특수문자, 파싱 아티팩트가 남아있지 않은가
- [ ] `source_url`이 올바른 법령/조문을 가리키는가 (하드코딩 버그 체크)

---

## Phase 2: 수정 (Remediation)

감사 결과를 severity별로 분류 후, 독립적인 작업을 병렬 에이전트로 처리.

### 수정 우선순위

| Severity | 기준 | 예시 |
|----------|------|------|
| CRITICAL | 데이터 정확성에 직접 영향 | source_url 전부 잘못됨, 매핑 누락/오류 |
| HIGH | 스키마 일관성/무결성 | source_grade 불일치, 구형 스키마 미마이그레이션 |
| MEDIUM | 메타데이터 완성도 | 빈 title, 미인덱싱, 문서 수치 outdated |
| LOW | 검색 품질/미관 | 빈 keywords, 따옴표 불일치, 오타 |

### 수정 패턴

**Bulk fix (스크립트):** source_url, source_grade, 따옴표 통일, keywords 채우기 등 → Python 스크립트
**Schema migration:** 구형→신형 스키마 변환 → 에이전트에게 old/new 샘플 보여주고 변환 지시
**Manual fix:** 개별 오타, 특정 파일 이슈 → Edit 도구로 직접 수정
**External data:** Recital-Article 매핑 등 외부 소스 필요한 작업 → 크롤링 스크립트

### 수정 후 필수 작업

1. **인덱스 재빌드** — 파일 수정 후 반드시 인덱스 재빌드
2. **문서 수치 업데이트** — README, CLAUDE.md, agent 정의, RELEASE 노트 등 모든 곳의 파일 수/인덱스 수 동기화
3. **source-registry.json** — count/target/status 갱신

---

## Phase 3: 독립 2nd Review

수정한 사람과 다른 도구/모델로 독립 감사를 실행. **수정 내용을 알려주지 않는 것**이 핵심.

### 2nd Review 프롬프트 템플릿

```
You are auditing a legal knowledge base for data quality.
Working directory: {PROJECT_PATH}

Do a thorough quality audit. Check the following independently:

1. Frontmatter integrity: Pick 10 random files from each directory
   and verify YAML frontmatter is valid and complete.

2. Cross-reference validity: For 10 articles, check that
   cross_references and related_recitals point to existing files.

3. Source URL correctness: Verify source_url fields point to
   the correct legislation/source.

4. Schema consistency: Are all files in a given directory
   using a uniform schema?

5. Index-library sync: Does source-registry.json match actual
   file counts on disk?

6. Content spot-check: Read 2-3 key articles — does the text
   look like genuine legal text?

Report every issue you find. Be harsh.
This data will be exposed as an MCP server so accuracy is critical.
```

### 2nd Review 도구 옵션

| 도구 | 장점 |
|------|------|
| Codex (OpenAI) | 독립적 관점, 다른 모델의 시각 |
| Claude Code (다른 세션) | 동일 도구이지만 fresh context |
| 수동 검증 | 핵심 파일 3-5개를 직접 열어서 확인 |

---

## Phase 4: 문서 동기화

모든 수정이 끝난 후, 아래 파일들의 수치를 일괄 업데이트:

### 체크리스트

- [ ] `README.md` — badge 숫자, mermaid 다이어그램, 섹션 헤더, 디렉토리 트리
- [ ] `README.ko.md` — 위와 동일 (한국어)
- [ ] `CLAUDE.md` — Current Status 섹션, 디렉토리 구조
- [ ] `.claude/agents/{agent}.md` — KB Scope 섹션
- [ ] `docs/RELEASE-*.md` — 릴리즈 노트 수치
- [ ] `docs/GITHUB-METADATA.md` — GitHub description
- [ ] `index/source-registry.json` — count/target/status

### 검색 팁

수치 변경 후 빠진 곳이 없는지 확인:
```bash
# 예: enforcement 35→33 변경 후
grep -rn "35.*enforcement\|35.*decision\|enforcement.*35" \
  README.md README.ko.md CLAUDE.md docs/ .claude/agents/
```

---

## 실전 타임라인 (GDPR-expert 기준)

| 단계 | 소요 시간 | 비고 |
|------|----------|------|
| Phase 1: 감사 (4 병렬 에이전트) | ~25분 | 1,064 파일 전수 검사 |
| Phase 2: 수정 Batch 1 (4 병렬) | ~5분 | source_url, source_grade 등 bulk fix |
| Phase 2: 수정 Batch 2 (4 병렬) | ~5분 | 스키마 마이그레이션, 메타데이터 |
| Phase 2: 수정 Batch 3 (스크립트) | ~15분 | Recital 매핑, keywords, 인덱스 |
| Phase 3: Codex 2nd review | ~10분 | 독립 감사 |
| Phase 3: Codex remediation | ~15분 | 2nd review 이슈 수정 |
| Phase 4: 문서 동기화 | ~5분 | README, CLAUDE.md 등 |
| **Total** | **~80분** | |
