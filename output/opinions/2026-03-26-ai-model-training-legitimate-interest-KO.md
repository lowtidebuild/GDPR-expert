# 법률 분석 메모

## 건: GDPR상 AI 기반 지출 분석 기능을 위한 고객 조달 데이터의 LLM 미세조정(Fine-Tuning) 적법성 검토 — 정당한 이익(Art. 6(1)(f)) 근거 분석

**일자:** 2026년 3월 26일

**생성 주체:** Jinju Legal Orchestrator — EU 데이터 보호 스페셜리스트 Kim De Bruyne (김덕배)

**요청 맥락:** [의뢰인] — B2B SaaS 조달 플랫폼

**분류:** 기밀 — 검토 초안

---

## I. 요약 (Executive Summary)

**귀사는 현재 GDPR 제28조상 개인정보 수탁처리자(processor) 자격으로 고객 조달 데이터를 사용하여 LLM을 미세조정하는 데 정당한 이익(Art. 6(1)(f))을 법적 근거로 원용할 수 없습니다.** 수탁처리자가 고객 데이터를 자사의 AI 학습 목적으로 사용하는 것은 수탁처리 관계의 근본적 위반에 해당하며, 해당 처리에 대해 사실상 개인정보처리자(controller)로 간주됩니다 — 이는 최대 1,000만 유로 또는 전 세계 연간 매출의 2%에 해당하는 과징금(Art. 83(4)(a))을 수반할 수 있습니다.

AI 모델 학습이 이루어지기 전에 고객과의 법률관계 재구성이 필수적입니다. 법률관계가 재구성되더라도 현행법상 정당한 이익 분석은 상당한 과제를 수반하며, 신중한 완화 조치가 필요합니다. 다만, 제안된 디지털 옴니버스 패키지(COM(2025) 837)가 채택될 경우 AI 개발을 명시적 정당한 이익으로 인정하여 분석이 다소 용이해질 수 있습니다 — 그러나 완전히 면제되는 것은 아닙니다.

**위험 평가: 높음 — 법률관계 재구성 없이는 해당 처리는 위법합니다.**

---

## II. 사실관계

귀사는 B2B SaaS 플랫폼을 운영하며 기업 고객을 대리하여 조달 데이터(인보이스, 구매주문서, 벤더 계약)를 처리합니다. 귀사는 GDPR 제28조에 따른 개인정보 수탁처리자로 활동합니다. 해당 데이터에는 고객사 직원의 업무 연락처(성명, 이메일, 직함, 전화번호)가 포함되어 있습니다.

귀사의 CTO는 이 데이터를 사용하여 "AI 기반 지출 분석" 기능 — 지출 패턴 예측 및 비용 최적화 제안 — 을 위한 대규모 언어모델(LLM)을 미세조정할 것을 제안합니다.

---

## III. 분석

### A. 선결 쟁점: 개인정보처리자(Controller) vs. 수탁처리자(Processor) 지위 (Art. 28 GDPR)

#### 1. 법적 기본 틀

이것은 정당한 이익 분석에 앞서 반드시 해결해야 할 결정적 쟁점입니다.

[VERIFIED] [Grade A] **GDPR 제28조 제3항 (a)호**는 수탁처리자가 다음과 같이 해야 한다고 규정합니다:

> *"processes the personal data only on documented instructions from the controller, including with regard to transfers of personal data to a third country or an international organisation"*

[VERIFIED] [Grade A] **GDPR 제29조**는 이를 강화합니다:

> *"The processor and any person acting under the authority of the controller or of the processor, who has access to personal data, shall not process those data except on instructions from the controller, unless required to do so by Union or Member State law."*

[VERIFIED] [Grade A] **GDPR 제28조 제10항**은 위반의 결과를 명시합니다:

> *"if a processor infringes this Regulation by determining the purposes and means of processing, the processor shall be considered to be a controller in respect of that processing."*

#### 2. 전문(Recital) 맥락

[VERIFIED] [Grade A] **전문(Recital) 81**은 제28조의 입법 취지를 제공합니다:

> *"The carrying-out of processing by a processor should be governed by a contract or other legal act under Union or Member State law, binding the processor to the controller, setting out the subject-matter and duration of the processing, the nature and purposes of the processing, the type of personal data and categories of data subjects, taking into account the specific tasks and responsibilities of the processor in the context of the processing to be carried out and the risk to the rights and freedoms of the data subject."*

이는 수탁처리자의 역할이 **개인정보처리자와의 계약에 의해 한정**됨을 확인합니다 — 수탁처리자는 계약에서 정의된 개인정보처리자의 목적을 위해 데이터를 처리하는 것이지, 자체 목적을 위해 처리하는 것이 아닙니다.

#### 3. EDPB의 Controller/Processor 구분 가이드라인

[VERIFIED] [Grade A] **EDPB Guidelines 07/2020 (개인정보처리자 및 수탁처리자 개념에 관한 가이드라인)**이 권위 있는 기준을 제시합니다:

- 개인정보처리자 개념은 **기능적 개념(functional concept)**으로, 형식적 지정이 아닌 실제 역할에 따라 책임을 배분합니다.
- **개인정보처리자**는 처리의 **목적과 수단** — "왜(why)"와 "어떻게(how)" — 를 결정합니다.
- 수탁처리자가 지시를 넘어 자체적으로 목적과 수단을 결정하기 시작하면, **해당 처리에 대해 개인정보처리자로 간주됩니다.**

#### 4. 귀사 상황에의 적용

고객 데이터를 사용하여 자사의 LLM을 미세조정하는 것은 처리에 대한 **새로운 목적을 결정하는 것**에 해당합니다. 원래의 목적(조달 플랫폼 서비스 제공)은 개인정보처리자인 고객사가 정한 것입니다. 자사 제품 개발을 위한 AI 모델 학습은 **귀사가** 결정하는 완전히 별개의 목적입니다.

GDPR 제28조 제10항에 따라, **귀사는 AI 학습 처리에 대해 개인정보처리자로 간주됩니다.** 이는 이론적 위험이 아니라 GDPR이 규정한 직접적 법률효과입니다.

[VERIFIED] [Grade A] **Garante v OpenAI** 집행 결정(1,500만 유로, 2024년 12월 20일)은 DPA가 적절한 법적 근거 없이 모델 학습을 위해 개인정보를 처리하는 AI 기업에 대해 적극적으로 집행하고 있음을 보여줍니다.

#### 5. 수탁처리자에서 개인정보처리자로의 재분류 결과

법률관계 재구성 없이 고객 데이터를 AI 학습에 사용할 경우:

**(a) 처리 계약 위반** — 제28조 제3항 (a)호 위반(지시 범위를 초과한 처리), 계약상 책임 및 해지 사유 발생 가능.

**(b) 행정 과징금** — 제83조 제4항 (a)호: 제28조 수탁처리자 의무 위반 시 최대 1,000만 유로 또는 전 세계 연간 매출의 2%.

**(c) 개인정보처리자의 전체 의무 부담** — AI 학습의 간주 개인정보처리자로서 모든 GDPR 개인정보처리자 의무(법적 근거, 투명성, 정보주체 권리, DPIA 등) 부담 — 이에 대한 준비가 되어 있지 않을 가능성이 높습니다.

**(d) 유효한 법적 근거 부재** — 귀사는 고객의 법적 근거(제6조 제1항 (b)호 — 계약상 필요성)에 따라 수탁처리자로서 데이터를 수집했습니다. 자체 목적으로 사용하려면 **독자적인 법적 근거**가 필요하나, 현재 이를 갖추고 있지 않습니다.

**(e) 민사 책임** — 제82조: 정보주체는 물질적 및 비물질적 손해에 대한 배상을 청구할 수 있습니다.

---

### B. 목적 제한 원칙 (Art. 5(1)(b) GDPR)

#### 1. 원칙

[VERIFIED] [Grade A] **GDPR 제5조 제1항 (b)호:**

> *"[Personal data shall be] collected for specified, explicit and legitimate purposes and not further processed in a manner that is incompatible with those purposes"*

[VERIFIED] [Grade A] **전문(Recital) 50:**

> *"The processing of personal data for purposes other than those for which the personal data were initially collected should be allowed only where the processing is compatible with the purposes for which the personal data were initially collected."*

#### 2. 전문(Recital) 맥락 — Recital 39

[VERIFIED] [Grade A] **전문(Recital) 39**는 목적 제한 및 데이터 최소화에 관한 핵심 해석 맥락을 제공합니다:

> *"In particular, the specific purposes for which personal data are processed should be explicit and legitimate and determined at the time of the collection of the personal data. The personal data should be adequate, relevant and limited to what is necessary for the purposes for which they are processed. [...] Personal data should be processed only if the purpose of the processing could not reasonably be fulfilled by other means."*

마지막 문장 — *"처리 목적이 다른 수단으로 합리적으로 달성될 수 없는 경우에만 개인정보를 처리해야 한다"* — 는 AI 모델 학습에 특히 중요합니다: 이는 목적 제한과 필요성 평가 간의 직접적 연결을 생성하여, 개인정보 없이(예: 익명화 또는 합성 데이터를 통해) 동일한 목적을 달성할 수 있는지 개인정보처리자가 검토할 것을 요구합니다.

#### 3. Art. 6(4)에 따른 호환성 평가

[VERIFIED] [Grade A] **GDPR 제6조 제4항**은 호환성 테스트를 규정합니다. 원래 수집 목적과 다른 목적으로의 처리 시 고려해야 할 요소:

> *(a) 수집 목적과 추가 처리 목적 간의 연관성*
>
> *(b) 특히 정보주체와 개인정보처리자 간의 관계를 고려한 수집 맥락*
>
> *(c) 개인정보의 성격*
>
> *(d) 추가 처리가 정보주체에게 미칠 수 있는 결과*
>
> *(e) 암호화 또는 가명처리를 포함한 적절한 보호조치의 존재*

#### 4. AI 모델 학습에의 적용

**(a) 목적 간 연관성:** 약함. 원래 목적은 조달 SaaS 플랫폼 제공(운영)이고, LLM 미세조정은 제품 개발 활동입니다.

**(b) 수집 맥락:** 불리함. 데이터는 B2B 맥락에서 수집되었으며, 정보주체는 자신의 데이터가 AI 모델 학습에 사용될 것을 합리적으로 기대하지 않습니다.

**(c) 데이터 성격:** 중간 위험. 업무 연락처는 민감정보(Art. 9)는 아니지만, 조달 데이터는 상업적으로 민감한 정보를 포함할 수 있습니다.

**(d) 결과:** 중간. 데이터가 모델 가중치에 내재될 수 있어 추출 또는 재출력 위험이 존재합니다.

**(e) 보호조치:** 유리(구현 시). 가명처리, 차등 프라이버시 등의 기술적 조치로 위험을 완화할 수 있습니다.

**목적 제한에 대한 결론:** AI 모델 학습은 조달 플랫폼 제공이라는 원래 목적과 **명백히 호환되지 않습니다.** 이는 별도의 법적 근거를 요하는 독립적 목적입니다.

---

### C. 정당한 이익 균형 테스트 (Art. 6(1)(f) GDPR)

**전제 참고:** 이 분석은 상기 섹션 III.A의 개인정보처리자/수탁처리자 쟁점이 적절히 재구성되어, 귀사가 AI 학습 목적에 대해 개인정보처리자(또는 공동 개인정보처리자)로 활동하는 경우를 가정합니다.

#### 1. 법적 기본 틀

[VERIFIED] [Grade A] **GDPR 제6조 제1항 (f)호:**

> *"processing is necessary for the purposes of the legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject which require protection of personal data, in particular where the data subject is a child."*

[VERIFIED] [Grade A] **EDPB Guidelines 1/2024 (정당한 이익에 관한 가이드라인, 2024년 10월 8일)**이 3단계 테스트를 제시합니다:

1. 개인정보처리자 또는 제3자의 **정당한 이익** 추구
2. 해당 정당한 이익 목적을 위한 처리의 **필요성**
3. 정보주체의 이익 또는 기본권과 자유가 **우선하지 않을 것**

[VERIFIED] [Grade A] **EDPB Opinion 28/2024** (2024년 12월 17일)가 이 기본 틀을 AI 모델 개발 및 배포에 구체적으로 적용합니다.

#### 2. 제1단계: 정당한 이익 식별

이익은 (a) **적법**하고, (b) **명확하고 정밀하게 표현**되었으며, (c) **현실적이고 현재의**(추측적이지 않은) 것이어야 합니다.

[VERIFIED] [Grade A] EDPB Opinion 28/2024 (para. 69)는 AI 맥락에서의 정당한 이익의 예시를 제시합니다:

> *(i) 사용자를 지원하는 대화형 에이전트 서비스 개발; (ii) 사기성 콘텐츠 또는 행위를 탐지하는 AI 시스템 개발; (iii) 정보 시스템의 위협 탐지 개선*

**귀사의 이익 — "고객을 위한 지출 패턴 예측 및 비용 최적화 제안을 위한 AI 기반 지출 분석 개발"** — 은:

- **적법:** 제품 개선 및 혁신은 인정된 상업적 이익입니다.
- **명확히 표현:** 예 — 기업 고객을 위한 지출 패턴 예측 및 비용 최적화.
- **현실적이고 현재의:** 예 — CTO가 구체적인 개발 계획을 가지고 있다는 전제하에.

**평가: 해당 이익은 정당한 이익으로 인정될 가능성이 높습니다.**

#### 3. 제2단계: 처리의 필요성

[VERIFIED] [Grade A] EDPB Opinion 28/2024 (paras. 70-75):

- 처리가 정당한 이익 추구를 **허용하는지**; 그리고
- **덜 침해적인 방법**이 없는지.

**귀사 시나리오의 핵심 질문:**

**(a) 개인정보가 필요한가?** 지출 분석 기능은 다음을 사용하여 개발할 수 있을 가능성이 있습니다:
- 완전히 익명화된 데이터
- 합성 데이터
- 개인 식별정보 없는 집계 통계 데이터

[VERIFIED] [Grade A] EDPB Opinion 28/2024 (para. 73):

> *"If the pursuit of the purpose is also possible through an AI model that does not entail processing of personal data, then processing personal data should be considered as not necessary."*

**평가: 필요성이 가장 취약한 부분입니다.** 지출 분석(지출 패턴 예측, 비용 최적화 제안)의 핵심 가치는 거래 데이터(금액, 카테고리, 시기, 벤더 유형)에 있으며, 개인 식별정보에 있지 않습니다. 가명처리 또는 익명화된 조달 데이터로 모델을 효과적으로 학습할 수 있을 가능성이 높습니다.

**권고:** 개인정보가 모델 성능에 진정으로 필요한지, 또는 익명화/가명처리된 데이터로 동등한 결과를 달성할 수 있는지에 대한 기술적 평가를 수행하십시오.

#### 4. 제3단계: 균형 테스트

필요성이 확립된 경우를 가정하여:

##### (a) 정보주체의 이익, 기본권 및 자유

[VERIFIED] [Grade A] EDPB Opinion 28/2024 (paras. 77-80)가 식별하는 관련 정보주체 이익:

- 개인정보에 대한 **자기결정 및 통제**
- AI 모델이 직업 활동에 영향을 미치는 경우의 **경제적 이익**
- EU 기본권헌장 제7조(사생활)와 제8조(개인정보보호)에 따른 **기본권**
- 학습된 모델로부터의 개인정보 **추출 또는 재출력 위험**

여기서 정보주체는 **고객사의 직원** — 소비자나 취약한 개인이 아닌 직업적(B2B) 맥락의 개인입니다. 이는 개인정보처리자의 이익에 다소 유리하게 작용합니다.

##### (b) 합리적 기대

[VERIFIED] [Grade A] **전문(Recital) 47**:

> *"At any rate the existence of a legitimate interest would need careful assessment including whether a data subject can reasonably expect at the time and in the context of the collection of the personal data that processing for that purpose may take place."*

**평가: 정보주체는 자신의 조달 데이터가 AI 모델 학습에 사용될 것을 합리적으로 기대하지 않을 것입니다.** 이는 정당한 이익 원용에 상당히 불리하게 작용합니다.

##### (c) 완화 조치

[VERIFIED] [Grade A] EDPB Opinion 28/2024 (paras. 95-105)가 제시하는 완화 조치의 비제한적 목록:

1. 학습 전 모든 개인 식별정보의 **가명처리**
2. 모델 학습 시 **차등 프라이버시(Differential Privacy)** 기술 적용
3. **데이터 최소화** — 업무 연락처 제거, 거래 패턴만 유지
4. **접근 통제** — 모델 접근 제한, 기반 모델의 공개 배포 금지
5. 멤버십 추론 및 추출 공격에 대한 **테스트**
6. **이의제기권(Right to Object)** — 정보주체의 옵트아웃을 가능하게 하는 제21조 메커니즘 구현
7. **투명성** — 개인정보 처리방침을 업데이트하여 AI 학습에 대해 고지
8. **DPIA** — 고위험 AI 처리에 대해 제35조에 따라 의무적

**전반적 균형 평가:**

| 요소 | 비중 | 방향 |
|------|------|------|
| AI 혁신에 대한 상업적 이익 | 중간 | 개인정보처리자에 유리 |
| B2B 직업적 맥락 (소비자 아님) | 중간 | 개인정보처리자에 유리 |
| 고객에 대한 혜택 (비용 최적화) | 중간 | 개인정보처리자에 유리 |
| 합리적 기대의 부재 | 강함 | 정보주체에 유리 |
| 정보주체와의 간접적 관계 | 중간 | 정보주체에 유리 |
| 모델로부터의 데이터 추출 위험 | 중간 | 정보주체에 유리 |
| 상업적으로 민감한 데이터 | 중간 | 정보주체에 유리 |
| 이용 가능한 완화 조치 | 중간 | 개인정보처리자에 유리 (구현 시) |

**균형 테스트 결론:** 강력한 완화 조치 없이는 균형 테스트가 **개인정보처리자에게 불리하게** 기웁니다. 포괄적 완화(가명처리, 차등 프라이버시, 투명성, 옵트아웃) 시 균형이 이동할 수 있으나, 철저한 문서화와 DPIA가 필요한 근접한 판단(close call)으로 남습니다.

---

### D. EDPB의 AI 및 개인정보에 관한 입장

#### 1. EDPB Opinion 28/2024 (2024년 12월 17일)

[VERIFIED] [Grade A] AI 모델 학습과 개인정보에 관한 **EDPB의 확정적 입장**입니다. 핵심 판단:

**(a) 개인정보로 학습된 AI 모델이 자동으로 익명이 되는 것은 아닙니다:**

> *"AI models trained on personal data cannot, in all cases, be considered anonymous. Instead, the determination of whether an AI model is anonymous should be assessed, based on specific criteria, on a case-by-case basis."* (para. 34)

**(b) 개인정보가 모델 파라미터에 "흡수"되어 잔존할 수 있습니다:**

> *"even when an AI model has not been intentionally designed to produce information relating to an identified or identifiable natural person from the training data, information from the training dataset, including personal data, may still remain 'absorbed' in the parameters of the model"* (para. 31)

**(c) 정당한 이익은 가능하나 엄격한 평가가 필요합니다:**

3단계 테스트가 다음 사항에 특별히 주의하며 적용됩니다:
- 처리되는 개인정보의 양과 비례성
- 익명화 또는 합성 대안의 존재 여부
- 정보주체의 합리적 기대
- 프라이버시 보존 기술 (차등 프라이버시, 가명처리)
- 제21조에 따른 이의제기권

**(d) 위법한 처리의 결과 — 3가지 시나리오:**

- **시나리오 1** (동일 개인정보처리자, 데이터 잔존): 후속 처리의 적법성은 사안별로 평가.
- **시나리오 2** (다른 개인정보처리자가 배포): 배포하는 개인정보처리자는 개발이 적법했는지 실사를 수행해야 함.
- **시나리오 3** (위법한 학습 후 모델 익명화): 모델이 진정으로 익명인 경우, GDPR이 후속 운영에 적용되지 않음.

#### 2. Garante v OpenAI 집행 결정 (1,500만 유로, 2024년 12월)

[VERIFIED] [Grade B] 이탈리아 DPA가 OpenAI에 대해 다음 위반으로 1,500만 유로 과징금을 부과했습니다:

- 유효한 법적 근거 없이 ChatGPT를 개인정보로 학습 (Art. 6)
- AI 학습을 위한 데이터 사용에 대한 투명성 미흡 (Art. 13)
- 13세 미만 사용자에 대한 연령 확인 부재 (Art. 8)
- 데이터 유출 통지 미이행 (Art. 33)

---

### E. 디지털 옴니버스 패키지 (COM(2025) 837)의 영향

#### 1. 개요

[VERIFIED] [Grade B] **디지털 법률 옴니버스** (COM(2025) 837, 2025년 11월 19일 공개)는 AI 개발과 관련된 중요한 GDPR 개정안을 제안합니다. 입법 제안으로서 **아직 법률이 아니며**, 입법 과정에서 상당한 변경이 있을 수 있습니다.

#### 2. 본 분석에 영향을 미치는 주요 제안 변경사항

##### (a) AI 개발을 명시적 정당한 이익으로 인정

[VERIFIED] [Grade B] **제안 전문(Recital) 30:**

> *"The development and use of AI systems and the underlying models such as large language models and generative video models rely on data, including personal data... The processing of personal data in this context may therefore be carried out for purposes of a legitimate interest within the meaning of Article 6 of Regulation (EU) 2016/679, where appropriate."*

이는 자동적 법적 근거를 생성하는 것이 **아닙니다** — AI 개발이 정당한 이익이 될 수 있음을 **확인**할 뿐입니다. 전체 3단계 테스트는 여전히 적용됩니다.

##### (b) AI 처리에 대한 균형 요소

[VERIFIED] [Grade B] **제안 전문(Recital) 31**은 균형 테스트에 대한 지침을 제공합니다:

- 이익이 **정보주체와 사회에 유익**한지 (예: 편향 탐지, 접근성)
- 정보주체의 **합리적 기대**
- 향상된 투명성 제공, 무조건적 이의제기권, 제3자의 AI 개발을 위한 데이터 사용을 제한하는 기술적 표시 존중, AI 학습을 위한 최신 프라이버시 보존 기술, 재출력 및 데이터 유출 위험을 효과적으로 최소화하는 적절한 기술적 조치를 포함한 **보호조치**

##### (c) 특수범주 데이터에 대한 AI 예외

[VERIFIED] [Grade B] **제안 Art. 9(2)(k):**

> *"processing in the context of the development and operation of an AI system... or an AI model, subject to the conditions referred to in paragraph 5."*

새로운 Art. 9(5)는 다음을 요구합니다:
- 특수범주 데이터 처리를 방지하기 위한 기술적 및 조직적 조치
- 식별된 특수범주 데이터의 삭제 (가능한 경우)
- 삭제에 비례하지 않는 노력이 필요한 경우: 데이터가 출력에 사용되거나 공개되지 않도록 효과적 보호

##### (d) 개인정보 정의 — 상대적 접근법

제안된 개정안은 가명처리된 데이터에 대한 **상대적/주관적 접근법**을 채택합니다: 해당 주체가 자연인을 식별할 *"합리적으로 사용될 가능성이 있는 수단"*을 갖추지 않은 경우, 해당 정보는 개인정보가 아닙니다. 이는 적절히 가명처리된 데이터를 처리하는 AI 개발자에게 유리할 수 있습니다.

#### 3. 영향 평가: 현행법 vs. 제안된 옴니버스

| 쟁점 | 현행 GDPR | COM(2025) 837 채택 시 |
|------|-----------|----------------------|
| AI 학습의 정당한 이익 | 명시적 열거 없음; 논증 가능 | 전문에서 명시적 확인 |
| 균형 테스트 요건 | 전체 3단계 테스트 | 동일, 그러나 AI 특화 지침 추가 |
| 연구 목적의 목적 제한 | 좁은 "과학적 연구" | 넓은 정의, 상업적 목적도 포함 가능 |
| AI에서의 특수범주 데이터 | 매우 제한적 예외 | 잔여 처리를 위한 새로운 Art. 9(2)(k) 예외 |
| 가명처리된 데이터 | 모든 주체에게 개인정보 | 상대적 접근법 — 수신자에게 비개인정보일 수 있음 |

#### 4. 유의사항

디지털 옴니버스는 **제안 단계**에 있습니다. 유럽의회와 이사회가 아직 3자 협상(trilogue)을 시작하지 않았습니다. 최종 조문은 상당히 달라질 수 있습니다. 입법 제안은 **Grade B** 출처로 분류됩니다 — 현재 준수 결정에 의존할 수 없습니다.

---

## IV. 권고사항

### 즉시 조치 (현행법)

1. **현재의 수탁처리자 자격으로 AI 모델 학습을 진행하지 마십시오.** 이는 제28조 제10항에 따른 위법한 목적 결정에 해당합니다.

2. **고객과의 법률관계를 재구성하십시오:**
   - **방안 A:** 각 고객에게 AI 모델 학습을 위한 데이터 사용에 대한 **명시적 계약상 허가**를 받을 것 (이 목적에 대한 공동 개인정보처리자 또는 독립적 개인정보처리자 관계를 반영하도록 DPA 수정).
   - **방안 B:** 고객을 통한 **정보주체 동의 확보** — B2B 맥락에서 기술적으로 복잡하고 운영상 부담이 큼.
   - **방안 C:** **데이터의 사전 익명화** — 학습 전에 조달 데이터를 완전히 익명화(모든 개인 식별정보 제거, 데이터 집계)할 수 있다면 GDPR이 적용되지 않음.

3. **데이터 최소화 평가를 수행하십시오:** 개인정보가 모델 학습에 진정으로 필요한지, 또는 익명화/가명처리된 거래 데이터로 충분한지 판단하십시오.

4. **개인정보가 필요한 경우, 처리 개시 전에 전체 DPIA**를 수행하십시오 (Art. 35).

5. **강력한 완화 조치를 구현하십시오:**
   - 학습 전 모든 개인 식별정보 가명처리
   - 차등 프라이버시 기술 적용
   - 추출 및 멤버십 추론 공격에 대한 모델 테스트
   - 제21조 이의제기권 메커니즘 구현
   - 개인정보 처리방침 업데이트

6. **정당한 이익 평가를 철저히 문서화하십시오** — 이는 책임성 원칙(Art. 5(2))에 따라 요구됩니다.

### 중기 조치 (디지털 옴니버스 대비)

7. **COM(2025) 837의 입법 진행 상황을 모니터링하십시오.** 제안대로 채택되면 법적 근거 분석이 용이해지나 면제되지는 않습니다.

8. **익명화 우선 아키텍처를 고려하십시오:** 기본적으로 데이터를 익명화하는 AI 학습 파이프라인을 설계하고, 명백히 필요한 경우에만 개인정보를 사용하십시오. 이 접근법은 현행법과 제안된 법 모두에서 견고합니다.

9. **DPO와 협의**하고, 제안된 AI 학습 활동에 대해 주관 감독기관(lead supervisory authority)으로부터 지침을 구하는 것을 고려하십시오.

---

## V. 관련 법조문 상호참조

| 조항 | 관련성 |
|------|--------|
| GDPR Art. 4(1) | 개인정보의 정의 |
| GDPR Art. 4(7) | 개인정보처리자의 정의 |
| GDPR Art. 5(1)(a) | 적법성, 공정성, 투명성 |
| GDPR Art. 5(1)(b) | 목적 제한 |
| GDPR Art. 5(1)(c) | 데이터 최소화 |
| GDPR Art. 5(2) | 책임성 |
| GDPR Art. 6(1)(f) | 정당한 이익 |
| GDPR Art. 6(4) | 호환 목적 테스트 |
| GDPR Art. 9 | 특수범주 데이터 |
| GDPR Art. 21 | 이의제기권 |
| GDPR Art. 22 | 자동화된 의사결정 |
| GDPR Art. 25 | 설계에 의한 데이터 보호 |
| GDPR Art. 28 | 수탁처리자 의무 |
| GDPR Art. 29 | 개인정보처리자 권한 하의 처리 |
| GDPR Art. 35 | DPIA |
| GDPR Art. 82 | 손해배상 청구권 |
| GDPR Art. 83(4)(a) | 수탁처리자 의무 위반 과징금 |
| GDPR Art. 89 | 연구/통계 목적의 보호조치 |
| GDPR Recital 47 | 정당한 이익 / 합리적 기대 |
| GDPR Recital 50 | 호환 목적 |
| GDPR Recital 81 | 수탁처리자 의무 |
| EU AI Act Art. 10 | 고위험 AI의 데이터 거버넌스 |
| COM(2025) 837 | 디지털 옴니버스 GDPR 개정안 (제안) |

## VI. 인용 주요 출처

### EDPB 문서 (Grade A)
- EDPB Opinion 28/2024 — AI 모델 및 개인정보 (2024년 12월 17일)
- EDPB Guidelines 1/2024 — Art. 6(1)(f) 정당한 이익 (2024년 10월 8일)
- EDPB Guidelines 07/2020 — 개인정보처리자 및 수탁처리자 개념
- EDPB ChatGPT Taskforce Report (2024년 5월 23일)

### CJEU 판례 (Grade A)
- C-621/22 — KNLTB (정당한 이익, 상업적 목적)
- C-252/21 — Meta v Bundeskartellamt (정당한 이익, 추적)
- C-683/21 — Nacionalinis visuomenės sveikatos centras (공동 개인정보처리자, 수탁처리자 책임)
- C-40/17 — Fashion ID (데이터 접근 없는 공동 개인정보처리자)
- C-210/16 — Wirtschaftsakademie (공동 개인정보처리자, Facebook 팬 페이지)
- C-634/21 — SCHUFA Scoring (Art. 22에 따른 자동화된 신용평가)
- C-413/23 — EDPS v SRB (개인정보/가명처리에 대한 상대적 접근법)
- C-582/14 — Breyer (동적 IP 주소, 정당한 이익)

### 집행 결정 (Grade B)
- Garante v OpenAI — 1,500만 유로 (2024년 12월 20일)

### 입법 제안 (Grade B)
- COM(2025) 837 — 디지털 법률 옴니버스

---

## VII. 면책사항

본 분석 메모는 정보 제공 목적으로 작성되었으며, 법률 자문에 해당하지 않습니다. 본 분석은 2026년 3월 현재 시행 중인 GDPR과 공개된 EDPB 지침에 기초합니다. 디지털 옴니버스 패키지(COM(2025) 837)는 채택 전 상당한 변경이 있을 수 있는 입법 제안입니다. 구체적 사안, 이행 결정 또는 개별 DPA와의 소통에 대해서는 관련 관할권의 자격 있는 법률 자문을 받으시기 바랍니다.

---

*생성 주체: Jinju Legal Orchestrator*
*EU 데이터 보호 스페셜리스트 Kim De Bruyne (김덕배)*
*2026년 3월 26일*
