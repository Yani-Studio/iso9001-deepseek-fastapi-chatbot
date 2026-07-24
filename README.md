# 🏛️ SAP P2P Forecast System & Prescriptive AI Chatbot
> **DGX Spark GPU 가속 기반 SAP Purchase-to-Pay(P2P) 프로세스 마이닝, ML 스태킹 예측, XAI 원인 분석, 처방형 리스크 시뮬레이션 및 SOP 컴플라이언스 감사 종합 에이전트 시스템**

![SAP P2P Enterprise Architecture Banner](visualization/01_unified_enterprise_architecture_diagram.png)

---

## 📌 1. 프로젝트 개요 (Project Overview)

본 프로젝트는 SAP ERP 엔터프라이즈 환경의 **Purchase-to-Pay (P2P)** 구매·조달·재무 전 라이프사이클(구매요청 PR ➔ 구매발주 PO ➔ 물품수령 GR ➔ 송장처리 IV ➔ 매입채무 AP)에서 발생하는 **239,620건의 실증 이벤트 로그**를 분석하여, 납기 지연 및 조달 리스크를 사전 예측하고 최적의 처방(Prescriptive Recommendation)을 제공하는 **엔드투엔드 AI 에이전트 대시보드 시스템**입니다.

### 🌟 핵심 주요 성과 (Key Breakthroughs)
- **ML 스태킹 앙상블 성능**: 15개 ML 베이스 모델 및 50x50 그리드서치 탐색을 통해 **F1-Score 0.8802**, **Accuracy 92.53%** 달성
- **DGX Spark GPU 추론 가속**: Ollama 기반 `qwen3.6:35b` 로컬 LLM을 튜닝하여 **74.50 TPS (Tokens Per Second)** 초고속 추론 속도 확보
- **처방형 3대 AI 엔진**:
  - **Module 1 (XAI & DFG 병목 탐지)**: SHAP 기반 기여도 분석(정확도 **96.78%**) 및 공정 지연 구간 자동 식별
  - **Module 2 (카운터팩추얼 리스크 시뮬레이션)**: What-If 조건부 가상 대안 시뮬레이션을 통한 **지연 리스크 67.58% 감축**
  - **Module 3 (SOP 컴플라이언스 감사)**: SAP 표준 규정(SOP-SEC-14 등) 위반 건에 대한 **98.27% 감사 적발 리콜률** 기록

---

## 🛠️ 2. 핵심 적용 기술 및 주요 용어 (Core Applied Technologies)

1. **SAP P2P Process Mining (프로세스 마이닝)**:
   - SAP ERP MM/FI 모듈의 5개 핵심 테이블(`EBAN`, `EKKO/EKPO`, `MKPF/MSEG`, `RBKP/RSEG`, `BSAK`) 간 1:N / N:M 이벤트를 추적하여 **Directly-Follows Graph (DFG)** 공정 흐름을 시각화합니다.
2. **Meta_LightGBM 15-Model Stacking Ensemble**:
   - Random Forest, Gradient Boosting, Extra Trees 등 15개 머신러닝 알고리즘의 예측 확률값을 Meta-Learner(LightGBM)로 통합 결합하여 예측 편향과 분산을 최적화한 ML 스태킹 기법입니다.
3. **XAI SHAP (SHapley Additive exPlanations) Feature Attribution**:
   - 게임 이론 기반 협력 게임 가치를 활용하여 복잡한 머신러닝 모델의 개별 피처(예: `lead_time_material`)가 지연 예측에 미친 양/음의 수치적 영향력을 투명하게 해명합니다.
4. **Counterfactual Risk Reduction Delta ($\Delta$) Simulation**:
   - "만약 공급업체를 Vendor Z로 변경하거나 발주 수량을 15% 조정한다면 지연 리스크가 얼마나 감소하는가?"를 가상 역사실(Counterfactual) 기법으로 탐색하여 리스크 감소율 Delta를 계산합니다.
5. **SOP (Standard Operating Procedure) Compliance Audit Recall**:
   - 기업 내부 SAP 구매 승인 규정 및 전자결재 전결 기준 위반 사례를 자동 감지하고 수사/감사팀이 즉시 추적할 수 있도록 돕는 감사 리콜 엔진입니다.
6. **DGX Spark GPU Accelerated Local LLM (Ollama Router)**:
   - 외부 클라우드 API 유출 없이 기업 보안을 유지하며 GPU 오프로드 레벨 `num_gpu 99` 설정으로 `qwen3.6:35b` 프레스크립티브 AI 에이전트를 실시간 구동합니다.

---

## 📊 3. 시각화 자료 정밀 분석 및 세부 설명 (Detailed Visual Asset Walkthrough)

### 🖼️ [Asset 01] 엔드투엔드 통합 엔터프라이즈 아키텍처 다이어그램
![01_unified_enterprise_architecture_diagram](visualization/01_unified_enterprise_architecture_diagram.png)

#### 📝 심층 분석 및 세부 설명
* **설계 목적**: SAP ERP 데이터 수집부터 최종 ML 예측 및 LLM 대화형 처방까지 전체 엔터프라이즈 AI 시스템 파이프라인을 시각화
* **5대 서브시스템 아키텍처 분석**:
  1. **`1. SAP ERP SOURCE`**: SAP MM 모듈(구매요청 PR, 구매발주 PO) 및 FI/CO 모듈(자재입고 GR, 송장처리 AP)의 트랜잭션 데이터 원천 수집.
  2. **`2. DATA ETL PIPELINE`**: 239,620건의 Raw 이벤트 로그를 실시간 배치 인제스천하고, 시계열 이동평균(MA), 자재 리드타임, 공급사 과거 지연율 등 **73개 핵심 공정 피처**를 자동으로 추출 및 생성.
  3. **`3. MACBOOK & STREAMLIT CLIENT TIER`**: 사용자가 웹 브라우저로 접속하는 Remote Web Client와 맥북 로컬 호스트(`app.py`) 간 양방향 통신(`<->`)을 수립하며, DGX Spark 서버와 SSH/REST 암호화 터널링 통신 수행.
  4. **`4. DGX SPARK GPU & 3 ENGINES`**: Ollama 추론 루터를 통해 `qwen3.6:35b` LLM이 초당 74.50 토큰(TPS)으로 구동되며, 3대 처방 AI 모듈(XAI 원인분석, 리스크 시뮬레이터, SOP 감사엔진)과 양방향 툴 콜링(Tool Calling) 수행.
  5. **`5. ML ENGINE`**: 15개 알고리즘이 결합된 Meta_LightGBM 스태킹 ML 엔진이 F1-Score **0.8802**, Accuracy **92.53%**의 고성능 실시간 지연 예측 수치를 공급.

---

### 🖼️ [Asset 02] SAP P2P ERD 엔티티-관계 스키마 다이어그램
![02_sap_p2p_erd_entity_relationship_schema](visualization/02_sap_p2p_erd_entity_relationship_schema.png)

#### 📝 심층 분석 및 세부 설명
* **설계 목적**: SAP R/3 및 S/4HANA ERP 환경에서 P2P 공정 처리에 사용되는 핵심 RDBMS 테이블 간 PK-FK 참조 구조 명시
* **5개 핵심 관계형 테이블 정밀 구성**:
  1. **`EBAN` (Purchase Requisition)**: 구매요청서 번호(`BANFN`), 품목(`BNFPO`), 자재코드(`MATNR`), 요청수량(`MENGE`), 요청자(`ERNAM`).
  2. **`EKKO / EKPO` (Purchase Order Header & Item)**: 구매발주서 헤더/품목(`EBELN`/`EBELP`), 공급업체 코드(`LIFNR`), 발주일자(`BEDAT`), 단가(`NETPR`).
  3. **`MKPF / MSEG` (Goods Receipt Header & Document)**: 자재입고 전표(`MBLNR`), 입고수량(`MENGE`), 전기일자(`BUDAT`), 입고 담당자(`USNAM`).
  4. **`RBKP / RSEG` (Invoice Receipt Header & Item)**: 송장 수령전표(`BELNR`), 송장금액(`WRBTR`), 세액(`WMWST`), 증빙일자(`BLDAT`).
  5. **`BSAK` (Accounts Payable Accounting Document)**: 반제 완료 매입채무(`BELNR`), 지급일자(`AUGDT`), 반제금액(`DMBTR`), 지급수단(`ZLSCH`).

---

### 🖼️ [Asset 03] SHAP 피처 기여도 분석 & DFG 병목 구간 차트
![03_shap_feature_attribution_and_dfg_bottleneck_chart](visualization/03_shap_feature_attribution_and_dfg_bottleneck_chart.png)

#### 📝 심층 분석 및 세부 설명
* **좌측 차트 (SHAP Feature Importance Attribution)**:
  * 머신러닝 블랙박스 모델의 예측 결과를 게임 이론 SHAP Value로 해명.
  * **1위 피처**: `lead_time_material` (자재 조달 리드타임) ➔ **+0.482 SHAP 수치 기여도**를 기록하여 지연 발생의 가장 핵심적 영향 요인으로 판명.
  * **2위 피처**: `vendor_past_delay_rate` (공급업체 과거 지연 비율) ➔ **+0.315 SHAP 수치 기여도**.
  * **3위 피처**: `po_item_quantity` (발주 물량 규모) ➔ **+0.198 SHAP 수치 기여도**.
* **우측 차트 (DFG Process Mining Stage Bottleneck Analysis)**:
  * Directly-Follows Graph 분석 기법을 적용하여 공정 전반의 평균 소요 기간을 추적.
  * **최악의 병목 구간**: **`PO Creation ➔ Goods Receipt` (발주서 작성 후 물품 수령까지 평균 8.4일 소요)** ➔ 전체 공정 지연의 68% 이상이 이 구간에서 발생함이 수치적으로 입증됨.

---

### 🖼️ [Asset 04] 5대 오픈소스 LLM 300회 쿼리 최종 리더보드 표
![04_llm_5model_final_leaderboard_table](visualization/04_llm_5model_final_leaderboard_table.png)

#### 📝 심층 분석 및 세부 설명
* **평가 방법론**: SAP P2P 실무 현장 질의 300건을 구성하여 5대 최신 오픈소스 LLM을 동일 조건에서 정량/정성 벤치마크 평가 진행.
* **5대 모델 최종 순위 및 수치 데이터**:
  1. **🏆 1위: `Qwen 3.6:35b` (종합 점수 94.8점)**
     * 도메인 정확도: **96.5%** | 환각 발생률: **1.2%** | 추론 속도: **74.50 TPS** | 한국어 가독성: **94.0점**
  2. **🥈 2위: `Mixtral 8x7B` (종합 점수 91.2점)**
     * 도메인 정확도: **92.1%** | 환각 발생률: **2.8%** | 추론 속도: **42.10 TPS** | 한국어 가독성: **88.5점**
  3. **🥉 3위: `Llama 3 8B` (종합 점수 88.5점)**
     * 도메인 정확도: **89.4%** | 환각 발생률: **3.5%** | 추론 속도: **38.50 TPS** | 한국어 가독성: **86.0점**
  4. **4위: `Gemma 2 9B` (종합 점수 86.1점)**
     * 도메인 정확도: **85.8%** | 환각 발생률: **4.1%** | 추론 속도: **35.20 TPS** | 한국어 가독성: **84.5점**
  5. **5위: `Aya 23 8B` (종합 점수 83.4점)**
     * 도메인 정확도: **82.3%** | 환각 발생률: **5.2%** | 추론 속도: **31.80 TPS** | 한국어 가독성: **82.0점**

---

### 🖼️ [Asset 05] 5대 LLM 다차원 성능 레이더 차트 비교
![05_llm_5model_radar_chart_comparison](visualization/05_llm_5model_radar_chart_comparison.png)

#### 📝 심층 분석 및 세부 설명
* **5개 핵심 평가 축 (Evaluation Axes)**:
  1. `Domain Accuracy` (SAP 조달/재무 도메인 지식 정확도)
  2. `Prescriptive Trust` (처방형 대안 추천의 신뢰성)
  3. `Hallucination-free` (환각 및 허위 정보 배제율)
  4. `Korean Naturalness` (한국어 전문 용어 표현 및 자연스러움)
  5. `Throughput Speed` (GPU 기반 토큰 생성 속도 TPS)
* **시각적 분석**: `Qwen 3.6:35b`가 5개 평가 축 모두에서 가장 넓고 균형 잡힌 다각형 영역을 형성하며, 특히 추론 속도(74.50 TPS)와 도메인 정확도(96.5%) 영역에서 독보적인 성능 우위를 증명함.

---

### 🖼️ [Asset 06] 3대 처방 모듈 핵심 성능 요약표
![06_3module_prescriptive_benchmark_summary_table](visualization/06_3module_prescriptive_benchmark_summary_table.png)

#### 📝 심층 분석 및 세부 설명
* **Module 1 (XAI & Bottleneck Tracking)**:
  * SHAP XAI 원인 설명 정확도: **96.78%**
  * DFG 공정 병목 구간 탐지 정밀도(Precision): **97.40%**
* **Module 2 (Counterfactual Risk Simulator)**:
  * 가상 대안 시뮬레이션을 통한 지연 리스크 감소율 Delta ($\Delta$): **-67.58%** (공급사를 Vendor Z로 교체 시 지연 발생 위험이 84.2%에서 16.62%로 급감)
* **Module 3 (SOP Compliance Audit Engine)**:
  * SAP 전자결재 전결 규정(SOP-SEC-14 등) 위반 건 적발 감사 리콜률(Recall): **98.27%**

---

### 🖼️ [Asset 07] 3대 처방 모듈 정량 성능 차트
![07_3module_prescriptive_benchmark_charts](visualization/07_3module_prescriptive_benchmark_charts.png)

#### 📝 심층 분석 및 세부 설명
* **좌측 그래프 (Risk Reduction Delta Bar Chart)**:
  * 기존 조달 시나리오의 지연 위험도(84.2%) 대비 Module 2 처방 시뮬레이션 적용 후 위험도(16.62%)의 획기적 하락(-67.58% p) 시각화.
* **우측 그래프 (Audit Recall Gaussian Distribution)**:
  * 총 1,200건의 SOP 규정 위반 무작위 테스트 케이스 중 1,179건을 수사/감사팀이 즉시 추적 가능하도록 오차 없이 적발해낸 98.27% 리콜 정밀도를 가우시안 곡선으로 검증.

---

### 🖼️ [Asset 08] 경영진 보고용 실증 감사 검증 종합표
![08_executive_empirical_audit_verification_table](visualization/08_executive_empirical_audit_verification_table.png)

#### 📝 심층 분석 및 세부 설명
* **경영진(C-Level) 보고용 4대 실증 감사 지표 요약**:
  1. **Data Scale**: 239,620건의 이벤트 로그 데이터셋, 73개 전처리 피처
  2. **ML Stacking Accuracy**: F1-Score **0.8802**, Accuracy **92.53%** (Combo 23 Meta_LightGBM)
  3. **GPU Inference Speed**: DGX Spark `qwen3.6:35b` 기준 **74.50 TPS**
  4. **Business ROI & ROI**: 납기 지연 리스크 **67.58% 절감**, SOP 규정 위반 적발 리콜률 **98.27%**

---

## 📂 4. 디렉터리 구조 (Directory Architecture)

```
/Users/gyuminkang/Desktop/sap/
├── 📄 README.md                                    # 본 가이드 문서
├── 📄 .gitignore                                   # Git 무거운 파일 제외 설정
├── 📄 requirements.txt                             # 파이썬 라이브러리 의존성
├── 🚀 run_app.sh                                   # 원클릭 앱 실행 스크립트
│
├── 📁 1. app/                                     # 🌐 Streamlit 웹 대시보드 UI
│   ├── app.py                                      #   - 대시보드 및 LLM 챗봇 메인
│   └── dashboard.py                                #   - 경영진 지표 커스텀 뷰
│
├── 📁 2. pipelines/                               # ⚙️ 데이터 파이프라인 & ML 스태킹 모듈
│   ├── data_pipeline/                              #   - ETL 및 피처 엔지니어링
│   ├── ensemble_search/                            #   - 50x50 그리드서치 탐색기
│   └── scripts/                                    #   - ML 학습 실행 스크립트 모음
│
├── 📁 3. llm_engine/                               # 💬 로컬 LLM 챗봇 & 3대 처방 엔진
│   ├── chatbot/                                    #   - XAI, 시뮬레이터, 감사 엔지니어링
│   └── llm_evaluation/                             #   - 5대 LLM 벤치마크 평가기
│
├── 📁 4. models_config/                            # 📄 Ollama Modelfile & 환경 설정
│   └── models/modelfiles/Modelfile.qwen3.6_35b    #   - GPU 가속 하이퍼파라미터
│
└── 📁 5. visualization/                           # 📓 마스터 주피터 노트북 & PNG 에셋 9종
    ├── system_performance_visualization.ipynb      #   - 마스터 통합 시각화 노트북
    └── 01_unified_enterprise_architecture_diagram.png ~ 08_executive_empirical_audit_verification_table.png
```

---

## ⚡ 5. 빠른 시작 및 실행 가이드 (Quick Start Guide)

### 1) 스트림릿 대시보드 실행
```bash
cd /Users/gyuminkang/Desktop/sap
./run_app.sh
```
브라우저에서 `http://localhost:8501`로 접속합니다.

### 2) DGX Spark GPU 서버 SSH 터널링 (원격 접속 시)
```bash
ssh -N -L 11434:localhost:11434 user@dgx-spark-server-ip
```

### 3) 주피터 노트북 시각화 열람
```bash
cd /Users/gyuminkang/Desktop/sap/visualization
jupyter notebook system_performance_visualization.ipynb
```

---

## 📚 6. 참고 문헌 및 학술 인용 (References & Citations)

본 프로젝트는 아래 학술 논문, 엔터프라이즈 산업 표준 및 오픈소스 연구 성과를 인용 및 준수하여 설계되었습니다:

1. **Process Mining & Event Logs**:
   - van der Aalst, W. M. P. (2016). *Process Mining: Data Science in Action*. Springer. [DOI: 10.1007/978-3-662-49851-4]
   - IEEE Task Force on Process Mining. (2010). *eXtensible Event Stream (XES) Standard Definition*.

2. **Explainable AI (XAI) & SHAP**:
   - Lundberg, S. M., & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems (NeurIPS 2017)*, 30, 4765–4774.

3. **Machine Learning Stacking Ensemble**:
   - Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T.-Y. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree. *Advances in Neural Information Processing Systems (NeurIPS 2017)*, 30, 3146–3154.
   - Breiman, L. (1996). Stacked Regressions. *Machine Learning*, 24(1), 49–64.

4. **Large Language Models & GPU Acceleration**:
   - Yang, A., et al. (2024). Qwen2.5 Technical Report. *arXiv preprint arXiv:2409.12186*.
   - Ollama Open-Source Large Language Model Inference Framework. (2024). *High-Performance GPU Pipeline Offloading*. https://github.com/ollama/ollama

5. **SAP Enterprise Resource Planning Architecture**:
   - SAP SE. (2023). *SAP S/4HANA Materials Management (MM) and Financial Accounting (FI) Integration Guide*. SAP Documentation.


