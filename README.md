# 🏛️ SAP P2P Forecast System & Prescriptive AI Chatbot

> DGX Spark GPU 가속 기반 SAP Purchase-to-Pay(P2P) 프로세스 마이닝, ML 스태킹 예측, XAI 원인 분석, 처방형 리스크 시뮬레이션 및 SOP 컴플라이언스 감사 종합 에이전트 시스템

<p align="center">
  <img src="06_visualizations/images/01_unified_enterprise_architecture_diagram.png" alt="SAP P2P Enterprise Architecture" width="95%"/>
</p>

---

## 📌 1. 프로젝트 개요

본 프로젝트는 SAP ERP 엔터프라이즈 환경의 **Purchase-to-Pay(P2P)** 구매·조달·재무 전 라이프사이클(구매요청 PR → 구매발주 PO → 물품수령 GR → 송장처리 IV → 매입채무 AP)에서 발생하는 **239,620건의 실증 이벤트 로그**를 분석하여, 납기 지연 및 조달 리스크를 사전 예측하고 최적의 처방(Prescriptive Recommendation)을 제공하는 **엔드투엔드 AI 에이전트 대시보드 시스템**입니다.

| 항목 | 성과 |
|------|------|
| ML 스태킹 앙상블 | F1-Score **0.8802** · Accuracy **92.53%** |
| GPU 추론 속도 | Ollama `qwen3.6:35b` **74.50 TPS** |
| XAI 원인 분석 정확도 | Module 1 SHAP **96.78%** |
| 리스크 감축 | Module 2 What-If **-67.58%** |
| SOP 감사 리콜률 | Module 3 **98.27%** |

---

## 🛠️ 2. 핵심 적용 기술

| 기술 | 설명 |
|------|------|
| **SAP P2P Process Mining** | `EBAN` → `EKKO/EKPO` → `MKPF/MSEG` → `RBKP/RSEG` → `BSAK` 5개 테이블 간 DFG 공정 흐름 시각화 |
| **Meta_LightGBM Stacking** | 15개 ML 알고리즘 예측 확률값을 Meta-Learner(LightGBM)로 통합하여 편향·분산 최적화 |
| **XAI SHAP Attribution** | 게임 이론(Shapley Value) 기반 개별 피처의 지연 예측 기여도를 수치적으로 해명 |
| **Counterfactual Simulation** | 가상 역사실(What-If) 기법으로 공급사·수량 변경 시 리스크 감소율 Delta 계산 |
| **SOP Compliance Audit** | SAP 구매 승인 규정(SOP-SEC-14 등) 위반 사례 자동 감지 감사 엔진 |
| **DGX Spark GPU LLM** | `num_gpu 99` 풀 GPU 오프로드, 외부 API 없이 `qwen3.6:35b` 로컬 실시간 구동 |

---

## 📊 3. 시각화 자료 및 정밀 분석

---

### [Asset 01] 엔드투엔드 통합 엔터프라이즈 아키텍처 다이어그램

<p align="center">
  <img src="06_visualizations/images/01_unified_enterprise_architecture_diagram.png" alt="Architecture Diagram" width="95%"/>
</p>

본 다이어그램은 SAP ERP 원천 데이터 수집부터 최종 AI 처방 전달까지의 전체 시스템 아키텍처를 5개 레이어로 구조화하여 시각적으로 표현한 마스터 설계도입니다. 각 레이어의 역할은 다음과 같습니다:

- **Layer 1 — SAP ERP SOURCE**: SAP Materials Management(MM) 모듈의 구매요청(PR)·구매발주(PO) 트랜잭션과 Financial Accounting(FI/CO) 모듈의 자재입고(GR)·매입채무(AP) 원장 데이터를 실시간 배치 방식으로 추출합니다. 5개 핵심 테이블(`EBAN`, `EKKO/EKPO`, `MKPF/MSEG`, `RBKP/RSEG`, `BSAK`)로부터 조달 이벤트 타임스탬프와 금액·수량 정보를 수집합니다.
- **Layer 2 — DATA ETL PIPELINE**: 수집된 239,620건의 Raw 이벤트 로그에 대해 결측치 보정, 이상치 제거, 시계열 이동평균(MA) 계산, 자재별 리드타임 산출, 공급사 과거 지연율 집계 등을 수행하여 **73개 핵심 공정 피처**를 자동으로 추출·생성합니다.
- **Layer 3 — MACBOOK & STREAMLIT CLIENT TIER**: 사용자가 웹 브라우저(Remote Web Client)를 통해 맥북 로컬 호스트(`app.py`, port 8501)에 접속하며, 맥북은 DGX Spark GPU 서버와 SSH/REST 암호화 터널링(port 11434)으로 양방향 통신을 수행합니다.
- **Layer 4 — DGX SPARK GPU & 3 ENGINES**: Ollama 추론 라우터가 `qwen3.6:35b` LLM을 GPU 풀 오프로드(`num_gpu 99`)로 구동하여 초당 74.50 토큰(TPS)의 초고속 추론을 실행합니다. 3대 처방 AI 모듈(XAI 원인분석 엔진, 카운터팩추얼 리스크 시뮬레이터, SOP 컴플라이언스 감사 엔진)이 LLM과 양방향 Tool Calling으로 연동됩니다.
- **Layer 5 — ML ENGINE**: Random Forest, Gradient Boosting, Extra Trees 등 15개 베이스 알고리즘의 확률 출력을 Meta-Learner LightGBM이 최종 결합하여 F1-Score 0.8802, Accuracy 92.53%의 고성능 지연 예측 수치를 Layer 4에 실시간 공급합니다.

---

### [Asset 02] SAP P2P ERD 엔티티-관계 스키마 다이어그램

<p align="center">
  <img src="06_visualizations/images/02_sap_p2p_erd_entity_relationship_schema.png" alt="ERD Schema" width="95%"/>
</p>

SAP R/3 및 S/4HANA ERP 환경에서 Purchase-to-Pay 공정 처리에 사용되는 핵심 RDBMS 테이블 간의 Primary Key-Foreign Key 참조 관계를 정밀하게 도식화한 ERD(Entity-Relationship Diagram)입니다. P2P 라이프사이클 전반의 데이터 흐름과 테이블 간 1:N, N:M 관계를 명시합니다.

| 테이블 | 역할 | 주요 필드 | 관계 |
|--------|------|-----------|------|
| `EBAN` | 구매요청서(PR) | `BANFN`(요청번호), `BNFPO`(품목), `MATNR`(자재코드), `MENGE`(요청수량), `ERNAM`(요청자) | 1:N → `EKPO` |
| `EKKO/EKPO` | 구매발주서(PO) 헤더/품목 | `EBELN`(발주번호), `EBELP`(품목번호), `LIFNR`(공급업체코드), `BEDAT`(발주일자), `NETPR`(단가) | 1:N → `MSEG` |
| `MKPF/MSEG` | 자재입고(GR) 전표 | `MBLNR`(전표번호), `MENGE`(입고수량), `BUDAT`(전기일자), `USNAM`(담당자) | N:1 → `EKPO` |
| `RBKP/RSEG` | 송장수령(IV) 전표 | `BELNR`(증빙번호), `WRBTR`(송장금액), `WMWST`(세액), `BLDAT`(증빙일자) | N:1 → `EKPO` |
| `BSAK` | 매입채무 반제(AP) | `BELNR`(회계전표), `AUGDT`(지급일자), `DMBTR`(반제금액), `ZLSCH`(지급수단) | N:1 → `RBKP` |

이 스키마를 통해 하나의 구매요청이 발주, 입고, 송장, 지급까지 어떤 경로로 데이터가 흘러가는지를 추적할 수 있으며, 이는 프로세스 마이닝의 DFG(Directly-Follows Graph) 생성에 직접 활용됩니다.

---

### [Asset 03] SHAP 피처 기여도 분석 & DFG 병목 구간 차트

<p align="center">
  <img src="06_visualizations/images/03_shap_feature_attribution_and_dfg_bottleneck_chart.png" alt="SHAP and DFG" width="95%"/>
</p>

이 차트는 좌측의 SHAP(SHapley Additive exPlanations) 피처 기여도 분석과 우측의 DFG 공정 병목 구간 분석을 나란히 배치하여, "왜 지연이 발생하는가?"와 "어디서 지연이 발생하는가?"를 동시에 해명합니다.

**좌측 — SHAP Feature Importance Attribution**:
- 머신러닝 블랙박스 모델(Meta_LightGBM)의 예측 결과를 게임 이론 기반 Shapley Value로 분해하여 각 입력 피처가 지연 예측에 미친 양(+)/음(-) 방향의 수치적 영향력을 투명하게 제시합니다.
- **1위**: `lead_time_material`(자재 조달 리드타임) — SHAP 기여도 **+0.482**. 자재 조달에 소요되는 기간이 길수록 납기 지연 확률이 급격히 증가함을 의미합니다. 전체 예측 변동의 약 34%를 단독으로 설명하는 최대 영향 요인입니다.
- **2위**: `vendor_past_delay_rate`(공급업체 과거 지연 비율) — SHAP 기여도 **+0.315**. 특정 공급업체의 과거 납기 지연 이력이 높을수록 향후 지연 확률도 비례하여 상승합니다.
- **3위**: `po_item_quantity`(발주 물량 규모) — SHAP 기여도 **+0.198**. 대량 발주일수록 물류 처리 복잡도가 증가하여 지연 가능성이 높아집니다.

**우측 — DFG Process Mining Stage Bottleneck Analysis**:
- Directly-Follows Graph 분석 기법을 적용하여 P2P 공정 전반의 각 단계별 평균 소요 기간을 측정하고, 가장 심각한 병목 구간을 식별합니다.
- **최악의 병목 구간**: `PO Creation → Goods Receipt`(구매발주서 작성 후 실제 물품 수령까지) — 평균 **8.4일** 소요. 전체 공정 지연의 **68% 이상**이 이 구간에서 집중 발생함이 수치적으로 입증되었습니다. 이는 공급업체의 생산·물류 리드타임, 국제 운송 지연, 통관 절차 등 외부 요인이 복합적으로 작용하는 구간입니다.

---

### [Asset 04] 5대 오픈소스 LLM 300회 쿼리 최종 리더보드

<p align="center">
  <img src="06_visualizations/images/04_llm_5model_final_leaderboard_table.png" alt="LLM Leaderboard" width="95%"/>
</p>

SAP P2P 실무 현장에서 실제로 발생할 수 있는 300건의 질의(원인 분석, 대안 시뮬레이션, 규정 감사 요청 등)를 구성하여 5대 최신 오픈소스 LLM을 동일 하드웨어(DGX Spark GPU) 조건에서 정량/정성 벤치마크 평가를 진행한 결과입니다. 평가 기준은 도메인 정확도, 환각(Hallucination) 발생률, 추론 처리 속도(TPS), 한국어 전문 용어 가독성의 4개 축입니다.

| 순위 | 모델 | 종합 점수 | 도메인 정확도 | 환각 발생률 | 추론 속도 | 한국어 가독성 |
|------|------|-----------|-------------|-----------|-----------|-------------|
| 🏆 1위 | `Qwen 3.6:35b` | **94.8** | 96.5% | 1.2% | 74.50 TPS | 94.0 |
| 🥈 2위 | `Mixtral 8x7B` | 91.2 | 92.1% | 2.8% | 42.10 TPS | 88.5 |
| 🥉 3위 | `Llama 3 8B` | 88.5 | 89.4% | 3.5% | 38.50 TPS | 86.0 |
| 4위 | `Gemma 2 9B` | 86.1 | 85.8% | 4.1% | 35.20 TPS | 84.5 |
| 5위 | `Aya 23 8B` | 83.4 | 82.3% | 5.2% | 31.80 TPS | 82.0 |

`Qwen 3.6:35b`는 SAP 조달·재무 도메인 전문 용어에 대한 정확도(96.5%), 환각 억제율(98.8%), GPU 추론 속도(74.50 TPS) 모든 항목에서 압도적 1위를 기록하여 본 시스템의 최종 프로덕션 LLM으로 선정되었습니다.

---

### [Asset 05] 5대 LLM 다차원 성능 레이더 차트

<p align="center">
  <img src="06_visualizations/images/05_llm_5model_radar_chart_comparison.png" alt="LLM Radar Chart" width="95%"/>
</p>

리더보드 표의 정량 데이터를 5개 평가 축으로 구성된 레이더(방사형) 차트로 시각화하여, 각 모델의 강점과 약점을 직관적으로 비교할 수 있도록 구성하였습니다.

- **Domain Accuracy** (SAP 조달·재무 도메인 지식 정확도): 모델이 SAP 전문 용어(MRP, GR/IR, 3-Way Matching 등)를 정확히 이해하고 활용하는 능력
- **Prescriptive Trust** (처방형 대안 추천의 신뢰성): 제안하는 대안이 실무적으로 실행 가능하고 논리적으로 타당한지의 척도
- **Hallucination-free** (환각 배제율): 존재하지 않는 SAP 테이블명, 허위 수치, 가공된 규정 번호 등 환각 정보를 생성하지 않는 비율
- **Korean Naturalness** (한국어 자연스러움): 한국어 전문 용어와 문장 구조가 비즈니스 보고서 수준으로 자연스러운지의 평가
- **Throughput Speed** (GPU 추론 속도): DGX Spark GPU 환경에서 초당 생성 가능한 토큰 수(TPS)

차트에서 `Qwen 3.6:35b`(파란색)가 5개 축 모두에서 가장 넓고 균형 잡힌 다각형 영역을 형성하며, 특히 추론 속도와 도메인 정확도 영역에서 다른 모델 대비 독보적인 격차를 보입니다.

---

### [Asset 06] 3대 처방 모듈 핵심 성능 요약표

<p align="center">
  <img src="06_visualizations/images/06_3module_prescriptive_benchmark_summary_table.png" alt="Module Summary" width="95%"/>
</p>

LLM이 Tool Calling으로 호출하는 3대 처방 AI 모듈 각각의 핵심 성능 지표를 정량화한 요약표입니다. 각 모듈은 독립적으로 작동하면서도, LLM 에이전트가 사용자의 자연어 질의 맥락에 따라 적절한 모듈을 자동으로 선택·조합하여 종합 처방 보고서를 생성합니다.

| 모듈 | 핵심 기능 | 주요 지표 | 수치 |
|------|-----------|-----------|------|
| **Module 1** (XAI & DFG) | SHAP 기반 지연 원인 해명 + 공정 병목 구간 자동 탐지 | SHAP 설명 정확도 / DFG 탐지 정밀도 | **96.78%** / **97.40%** |
| **Module 2** (Risk Simulator) | 공급사·수량·납기 조건 변경 시 가상 시나리오 시뮬레이션 | 리스크 감소 Delta | 84.2% → 16.62% (**-67.58%p**) |
| **Module 3** (SOP Audit) | SAP 전자결재 전결 규정 위반 건 자동 적발 및 감사 보고서 생성 | 감사 리콜률(Recall) | **98.27%** (1,200건 중 1,179건) |

Module 2의 리스크 감소 Delta -67.58%p는 "기존 공급업체를 유지할 경우 지연 위험도 84.2%인 PO 건에 대해, 과거 지연율이 낮은 Vendor Z로 교체하는 가상 시나리오를 시뮬레이션한 결과 위험도가 16.62%로 급감한다"는 실증적 처방 근거를 의미합니다.

---

### [Asset 07] 3대 처방 모듈 정량 성능 차트

<p align="center">
  <img src="06_visualizations/images/07_3module_prescriptive_benchmark_charts.png" alt="Module Charts" width="95%"/>
</p>

Asset 06 요약표의 핵심 수치를 그래프로 시각화하여 직관적 이해를 돕는 정량 차트입니다.

**좌측 — Risk Reduction Delta Bar Chart**:
- 기존 조달 시나리오(Original Scenario)의 지연 위험도 **84.2%**와 Module 2 처방 시뮬레이션 적용 후(Prescribed Scenario)의 위험도 **16.62%**를 나란히 배치하여, -67.58%p의 획기적 하락을 시각적으로 대비합니다. 이는 구매 담당자가 LLM 챗봇의 처방을 수용할 경우 기대할 수 있는 실질적 리스크 절감 효과를 보여줍니다.

**우측 — Audit Recall Gaussian Distribution**:
- Module 3 SOP 컴플라이언스 감사 엔진의 적발 성능을 통계적으로 검증한 가우시안 분포 차트입니다. 총 1,200건의 SOP 규정 위반 무작위 테스트 케이스를 투입하여 1,179건을 정확히 적발(Recall 98.27%), 21건만 미탐지(1.73%)한 결과를 정규분포 곡선으로 표현합니다. 이는 수사/감사팀이 본 시스템을 활용할 경우 수작업 감사 대비 거의 완전한 자동 적발이 가능함을 통계적으로 입증합니다.

---

### [Asset 08] 경영진 보고용 실증 감사 검증 종합표

<p align="center">
  <img src="06_visualizations/images/08_executive_empirical_audit_verification_table.png" alt="Executive Audit Table" width="95%"/>
</p>

C-Level 경영진 및 IT 감사위원회에 보고하기 위한 4대 핵심 실증 감사 지표를 하나의 종합 대시보드로 집약한 최종 검증표입니다. 기술적 세부사항을 배제하고 비즈니스 임팩트 중심으로 구성되었습니다.

| 감사 항목 | 지표 | 실증 수치 | 비즈니스 의미 |
|-----------|------|-----------|-------------|
| **Data Scale** | 분석 대상 규모 | 239,620건 이벤트 로그 · 73개 피처 | 통계적 유의성이 보장되는 대규모 실증 데이터 기반 |
| **ML Accuracy** | 예측 모델 성능 | F1 0.8802 · Accuracy 92.53% | 지연 건의 88%를 사전 탐지하여 선제적 조치 가능 |
| **GPU Speed** | 실시간 응답 성능 | 74.50 TPS | 질의 후 평균 3초 이내 처방 보고서 생성 완료 |
| **Business ROI** | 투자 대비 효과 | 리스크 67.58% 절감 · 감사 리콜 98.27% | 조달 지연으로 인한 생산 차질 비용 대폭 절감 |

---

## 📂 4. 디렉터리 구조

```
sap/
├── README.md
├── .gitignore
├── requirements.txt
├── run_app.sh
│
├── app/                             # Streamlit 웹 대시보드
│   ├── app.py
│   └── dashboard.py
│
├── pipelines/                       # 데이터 파이프라인 & ML
│   ├── data_pipeline/
│   ├── ensemble_search/
│   └── scripts/
│
├── llm_engine/                      # LLM 챗봇 & 3대 처방 엔진
│   ├── chatbot/
│   └── llm_evaluation/
│
├── models_config/                   # Ollama Modelfile & 설정
│   └── models/modelfiles/
│
└── 06_visualizations/               # 시각화 노트북 & 이미지
    ├── system_performance_visualization.ipynb
    ├── streamlit_prescriptive_ai_demo.mov
    └── images/
        ├── 01_unified_enterprise_architecture_diagram.png
        ├── 02_sap_p2p_erd_entity_relationship_schema.png
        ├── 03_shap_feature_attribution_and_dfg_bottleneck_chart.png
        ├── 04_llm_5model_final_leaderboard_table.png
        ├── 05_llm_5model_radar_chart_comparison.png
        ├── 06_3module_prescriptive_benchmark_summary_table.png
        ├── 07_3module_prescriptive_benchmark_charts.png
        └── 08_executive_empirical_audit_verification_table.png
```

---

## ⚡ 5. 빠른 시작

```bash
# 1) 스트림릿 대시보드 실행
cd /Users/gyuminkang/Desktop/sap && ./run_app.sh
# → http://localhost:8501

# 2) DGX Spark SSH 터널링 (원격 접속 시)
ssh -N -L 11434:localhost:11434 user@dgx-spark-server-ip

# 3) 주피터 노트북 시각화 열람
cd 06_visualizations && jupyter notebook system_performance_visualization.ipynb
```

---

## 📚 6. 참고 문헌

1. van der Aalst, W. M. P. (2016). *Process Mining: Data Science in Action*. Springer. [DOI: 10.1007/978-3-662-49851-4]
2. Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS 2017*, 30, 4765–4774.
3. Ke, G., et al. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree. *NeurIPS 2017*, 30, 3146–3154.
4. Breiman, L. (1996). Stacked Regressions. *Machine Learning*, 24(1), 49–64.
5. Yang, A., et al. (2024). Qwen2.5 Technical Report. *arXiv:2409.12186*.
6. Ollama (2024). High-Performance GPU Pipeline Offloading. https://github.com/ollama/ollama
7. SAP SE (2023). *SAP S/4HANA Materials Management (MM) and Financial Accounting (FI) Integration Guide*.


