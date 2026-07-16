# 🚀 ISO 9001 AI RAG 파이프라인 및 챗봇 성능 평가 프로젝트

![System Architecture](06_visualizations/images/00_architecture.svg)

## 📌 프로젝트 개요 (Overview)
본 프로젝트는 **ISO 9001:2015 품질경영시스템** 도메인에 특화된 프로덕션 레벨의 **검색 증강 생성(RAG) 파이프라인**을 구축하고, 5가지 최신 오픈소스 로컬 대형 언어 모델(LLM)을 엄격하게 벤치마킹한 프로젝트입니다. 
로컬 맥북(프론트엔드)과 원격 Ubuntu DGX 서버(백엔드)를 분리한 분산 아키텍처를 채택하여, 무거운 벡터 검색과 LLM 추론은 서버에 위임하고 유저 인터페이스는 가볍게 유지했습니다.

## 🚶‍♂️ 전체 개발 과정 및 파이프라인 (The Journey)

### 1. 분산 처리 아키텍처 설계 (Architecture Design)
로컬 장비의 하드웨어 한계를 극복하기 위해 물리적 분산 환경을 구축했습니다.
* **Local MacBook:** 사용자와 상호작용하는 Streamlit Chat UI 구동 및 초기 PDF 문서 인덱싱 요청
* **Ubuntu DGX Server:** FastAPI 기반 API 서버, 문서 임베딩을 위한 Chroma DB, 그리고 최신 오픈소스 로컬 LLM(DeepSeek, Llama 등) 호스팅 및 추론 연산 처리

### 2. 평가용 데이터셋 구축 (Dataset Generation)
단순한 질의응답을 넘어 AI 모델의 안정성을 한계까지 테스트하기 위해 `04_dataset_tools`를 활용하여 **100-Question Gauntlet(건틀릿) 데이터셋**을 구축했습니다.
* **85%** - ISO 9001 핵심 규정 및 지식 (Core Knowledge)
* **10%** - 엣지 케이스 및 엉뚱한 질문 (Edge Cases / Nonsense)
* **5%** - 도메인 외 일반 인사말 (Out of Domain)

![Dataset Composition](06_visualizations/images/06_dataset_composition.png)

### 3. 자동화된 벤치마크 파이프라인 (Automated Eval Pipeline)
`03_eval_pipeline` 폴더 내의 스크립트를 통해 5개의 오픈소스 모델(DeepSeek v4, Llama 4, Qwen 3.6, Phi 4, Gemma 4)을 대상으로 자동화된 평가를 수행했습니다.

**[핵심 평가 지표]**
![RAG Performance](06_visualizations/images/02_performance_barchart.png)
* **DeepSeek v4** 모델이 RAG Score 99.9점을 기록하며 가장 압도적인 품질을 보여주었습니다.

**[추론 속도 vs 답변 품질 (Speed vs Quality)]**
![Speed vs Quality](06_visualizations/images/04_speed_vs_quality.png)
* DeepSeek v4는 품질뿐만 아니라 **질문당 평균 10.9초**의 매우 효율적인 추론 속도를 달성하여 최종 프로덕션 모델로 낙점되었습니다.

### 4. 챗봇 안정성 튜닝 (Hallucination & Stability Tuning)
기업용 챗봇에서 가장 치명적인 '할루시네이션(환각)'을 잡기 위해 파라미터 최적화를 진행했습니다.

![Tuning Process](06_visualizations/images/05_tuning_process.png)
* **튜닝 과정:** Temperature와 Repetition Penalty 값을 조절해가며 에러율을 추적했습니다.
* **결과:** 최종 'Golden Iteration' (Temp 0.7, Rep. Penalty 1.15) 셋업을 통해 **할루시네이션 에러를 0건으로 완벽히 제거**했습니다. 
* 결과적으로 5개 모델 모두 엄격한 안정성 건틀릿 테스트를 **100% Pass** 하도록 튜닝을 완료했습니다.

### 5. 데이터 시각화 및 문서화 (Visualization)
평가된 모든 벤치마크 데이터는 `06_visualizations` 폴더의 파이썬 스크립트를 통해 깃허브 프로페셔널 테마(연보라색 톤 + 고정폭 폰트 + 그리드 디자인)가 적용된 아름다운 고화질 SVG 및 PNG 차트로 일괄 자동 추출되도록 시스템화했습니다.

---

## 📁 디렉토리 구조 (Repository Structure)
```text
📦 Project Root
 ┣ 📂 01_backend/          # FastAPI 서버 구현체 및 API 라우팅
 ┣ 📂 02_frontend/         # Streamlit 기반 사용자 챗봇 UI (mac_chat_app.py)
 ┣ 📂 03_eval_pipeline/    # 모델 자동 벤치마킹 및 안정성 평가 스크립트 모음
 ┣ 📂 04_dataset_tools/    # ISO 9001 평가 데이터셋 생성 및 정제 스크립트
 ┣ 📂 05_deployment/       # 원격 서버 배포 및 프로세스 관리용 Shell 스크립트
 ┗ 📂 06_visualizations/   # 분석 결과 시각화용 Jupyter Notebook 및 SVG/PNG 추출 코드
```

> ⚠️ **참고사항:** 깃허브 레포지토리의 용량 최적화 및 보안을 위해 로컬 LLM의 무거운 가중치 파일(`.bin`, `.safetensors`)과 원본 대용량 평가 데이터(`.json`)는 제외되었습니다.
