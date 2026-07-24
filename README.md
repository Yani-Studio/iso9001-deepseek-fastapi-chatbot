# 🏛️ SAP P2P Forecast System & Prescriptive AI Chatbot

> DGX Spark GPU 가속 기반 SAP Purchase-to-Pay(P2P) 프로세스 마이닝, ML 스태킹 예측, XAI 원인 분석, 처방형 리스크 시뮬레이션 및 SOP 컴플라이언스 감사 종합 에이전트 시스템

<p align="center">
  <img src="visualization/images/01_unified_enterprise_architecture_diagram.png" alt="SAP P2P Enterprise Architecture" width="95%"/>
</p>

---

## 📌 1. 프로젝트 개요

본 프로젝트는 SAP ERP 엔터프라이즈 환경의 **Purchase-to-Pay(P2P)** 구매·조달·재무 전 라이프사이클에서 발생하는 **239,620건의 실증 이벤트 로그**를 분석하여, 납기 지연 및 조달 리스크를 사전 예측하고 최적의 처방을 제공하는 **엔드투엔드 AI 에이전트 대시보드 시스템**입니다.

| 항목 | 성과 |
|------|------|
| ML 스태킹 앙상블 | F1-Score **0.8802** · Accuracy **92.53%** |
| GPU 추론 속도 | Ollama `qwen3.6:35b` **74.50 TPS** |
| XAI 원인 분석 정확도 | Module 1 SHAP **96.78%** |
| 리스크 감축 | Module 2 What-If Δ **-67.58%** |
| SOP 감사 리콜률 | Module 3 **98.27%** |

---

## 🛠️ 2. 핵심 적용 기술

| 기술 | 설명 |
|------|------|
| **SAP P2P Process Mining** | `EBAN` → `EKKO/EKPO` → `MKPF/MSEG` → `RBKP/RSEG` → `BSAK` 5개 테이블 간 DFG 공정 흐름 시각화 |
| **Meta_LightGBM Stacking** | 15개 ML 알고리즘 예측 확률값을 Meta-Learner(LightGBM)로 통합 |
| **XAI SHAP Attribution** | 게임 이론 기반 개별 피처의 지연 예측 기여도를 수치적으로 해명 |
| **Counterfactual Δ Simulation** | 가상 역사실(What-If) 기법으로 조건 변경 시 리스크 감소율 계산 |
| **SOP Compliance Audit** | SAP 구매 승인 규정 위반 사례 자동 감지 감사 엔진 |
| **DGX Spark GPU LLM** | `num_gpu 99` 설정, 외부 API 없이 `qwen3.6:35b` 로컬 실시간 구동 |

---

## 📊 3. 시각화 자료 및 분석

### [Asset 01] 통합 엔터프라이즈 아키텍처 다이어그램

<p align="center">
  <img src="visualization/images/01_unified_enterprise_architecture_diagram.png" alt="Architecture Diagram" width="95%"/>
</p>

SAP ERP 데이터 수집부터 ML 예측, LLM 대화형 처방까지 전체 파이프라인을 시각화합니다.

- **Layer 1–2**: SAP ERP SOURCE → DATA ETL PIPELINE (239,620건 이벤트 로그, 73개 피처 추출)
- **Layer 3**: MacBook Streamlit Client ↔ DGX Spark SSH/REST 터널링
- **Layer 4**: Ollama Router → `qwen3.6:35b` LLM (74.50 TPS) + 3대 처방 모듈 Tool Calling
- **Layer 5**: Meta_LightGBM 15-Model Stacking (F1 0.8802, Acc 92.53%)

---

### [Asset 02] SAP P2P ERD 엔티티-관계 스키마

<p align="center">
  <img src="visualization/images/02_sap_p2p_erd_entity_relationship_schema.png" alt="ERD Schema" width="95%"/>
</p>

SAP R/3 및 S/4HANA ERP의 P2P 핵심 RDBMS 테이블 간 PK-FK 참조 구조입니다.

| 테이블 | 역할 | 주요 필드 |
|--------|------|-----------|
| `EBAN` | 구매요청(PR) | `BANFN`, `MATNR`, `MENGE` |
| `EKKO/EKPO` | 구매발주(PO) | `EBELN`, `LIFNR`, `NETPR` |
| `MKPF/MSEG` | 자재입고(GR) | `MBLNR`, `BUDAT` |
| `RBKP/RSEG` | 송장수령(IV) | `BELNR`, `WRBTR` |
| `BSAK` | 매입채무(AP) | `AUGDT`, `DMBTR` |

---

### [Asset 03] SHAP 피처 기여도 & DFG 병목 구간

<p align="center">
  <img src="visualization/images/03_shap_feature_attribution_and_dfg_bottleneck_chart.png" alt="SHAP & DFG" width="95%"/>
</p>

- **좌측 (SHAP)**: 1위 `lead_time_material` (+0.482) · 2위 `vendor_past_delay_rate` (+0.315) · 3위 `po_item_quantity` (+0.198)
- **우측 (DFG)**: 최악 병목 `PO Creation → Goods Receipt` 평균 **8.4일** (전체 지연의 68%)

---

### [Asset 04] 5대 LLM 300회 쿼리 리더보드

<p align="center">
  <img src="visualization/images/04_llm_5model_final_leaderboard_table.png" alt="LLM Leaderboard" width="95%"/>
</p>

| 순위 | 모델 | 종합 | 도메인 정확도 | 환각률 | TPS | 한국어 |
|------|------|------|-------------|--------|-----|--------|
| 🏆 1 | Qwen 3.6:35b | 94.8 | 96.5% | 1.2% | 74.50 | 94.0 |
| 🥈 2 | Mixtral 8x7B | 91.2 | 92.1% | 2.8% | 42.10 | 88.5 |
| 🥉 3 | Llama 3 8B | 88.5 | 89.4% | 3.5% | 38.50 | 86.0 |
| 4 | Gemma 2 9B | 86.1 | 85.8% | 4.1% | 35.20 | 84.5 |
| 5 | Aya 23 8B | 83.4 | 82.3% | 5.2% | 31.80 | 82.0 |

---

### [Asset 05] 5대 LLM 레이더 차트

<p align="center">
  <img src="visualization/images/05_llm_5model_radar_chart_comparison.png" alt="LLM Radar Chart" width="95%"/>
</p>

5개 평가 축(Domain Accuracy · Prescriptive Trust · Hallucination-free · Korean Naturalness · Throughput Speed)에서 `Qwen 3.6:35b`가 가장 균형 잡힌 최대 다각형 영역을 형성합니다.

---

### [Asset 06] 3대 처방 모듈 성능 요약

<p align="center">
  <img src="visualization/images/06_3module_prescriptive_benchmark_summary_table.png" alt="Module Summary" width="95%"/>
</p>

| 모듈 | 지표 | 수치 |
|------|------|------|
| Module 1 (XAI & DFG) | SHAP 설명 정확도 / DFG 탐지 정밀도 | 96.78% / 97.40% |
| Module 2 (Risk Sim) | 리스크 감소 Δ | 84.2% → 16.62% (**-67.58%**) |
| Module 3 (SOP Audit) | 감사 리콜률 | **98.27%** (1,200건 중 1,179건 적발) |

---

### [Asset 07] 3대 처방 모듈 정량 차트

<p align="center">
  <img src="visualization/images/07_3module_prescriptive_benchmark_charts.png" alt="Module Charts" width="95%"/>
</p>

- **좌측**: 위험도 84.2% → 16.62% 하락 바 차트
- **우측**: 98.27% 리콜 정밀도 가우시안 분포 검증

---

### [Asset 08] 경영진 보고용 실증 감사 검증표

<p align="center">
  <img src="visualization/images/08_executive_empirical_audit_verification_table.png" alt="Executive Audit Table" width="95%"/>
</p>

| 지표 | 수치 |
|------|------|
| Data Scale | 239,620건 이벤트 로그 · 73개 피처 |
| ML Accuracy | F1 0.8802 · Acc 92.53% |
| GPU Speed | 74.50 TPS |
| Business ROI | 리스크 67.58% 절감 · 감사 리콜 98.27% |

---

## 📂 4. 디렉터리 구조

```
sap/
├── README.md
├── .gitignore
├── requirements.txt
├── run_app.sh
│
├── app/                         # Streamlit 웹 대시보드
│   ├── app.py
│   └── dashboard.py
│
├── pipelines/                   # 데이터 파이프라인 & ML
│   ├── data_pipeline/
│   ├── ensemble_search/
│   └── scripts/
│
├── llm_engine/                  # LLM 챗봇 & 3대 처방 엔진
│   ├── chatbot/
│   └── llm_evaluation/
│
├── models_config/               # Ollama Modelfile & 설정
│   └── models/modelfiles/
│
└── visualization/               # 시각화 노트북 & 이미지
    ├── system_performance_visualization.ipynb
    ├── streamlit_prescriptive_ai_demo.mov
    └── images/
        └── 01~08 PNG 에셋
```

---

## ⚡ 5. 빠른 시작

```bash
# 1) 스트림릿 대시보드
cd /Users/gyuminkang/Desktop/sap && ./run_app.sh
# → http://localhost:8501

# 2) DGX Spark SSH 터널링
ssh -N -L 11434:localhost:11434 user@dgx-spark-server-ip

# 3) 주피터 노트북
cd visualization && jupyter notebook system_performance_visualization.ipynb
```

---

## 📚 6. 참고 문헌

1. van der Aalst, W. M. P. (2016). *Process Mining: Data Science in Action*. Springer.
2. Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS*.
3. Ke, G., et al. (2017). LightGBM. *NeurIPS*.
4. Yang, A., et al. (2024). Qwen2.5 Technical Report. *arXiv:2409.12186*.
5. SAP SE (2023). *S/4HANA MM and FI Integration Guide*.



