<div align="center">
  <h1>🚀 ISO 9001 Expert Chatbot</h1>
  <p><em>Powered by DeepSeek, FastAPI, and ChromaDB</em></p>

  <!-- Badges -->
  <p>
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/FastAPI-005571?logo=fastapi" alt="FastAPI">
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
    <img src="https://img.shields.io/badge/Chroma-DB-FF6F00" alt="Chroma DB">
    <img src="https://img.shields.io/badge/LLM-DeepSeek_v4-0d1117" alt="DeepSeek">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT">
  </p>

  <p>
    <b>ISO 9001:2015 규격에 완벽히 대응하는 프로덕션 레벨 RAG(검색 증강 생성) 파이프라인 및 엔터프라이즈 AI 챗봇 벤치마킹 프로젝트입니다.</b>
  </p>
  <br/>
</div>

## 📑 목차 (Table of Contents)
- [📌 프로젝트 개요 (Overview)](#-프로젝트-개요-overview)
- [🏗️ 시스템 아키텍처 (Architecture)](#️-시스템-아키텍처-architecture)
- [📊 벤치마크 및 성능 (Performance)](#-벤치마크-및-성능-performance)
- [⚡ 추론 속도 및 효율성 (Efficiency)](#-추론-속도-및-효율성-efficiency)
- [📉 안정성 및 파라미터 튜닝 (Stability Tuning)](#-안정성-및-파라미터-튜닝-stability-tuning)
- [🚀 퀵 스타트 (Quick Start)](#-퀵-스타트-quick-start)
- [📁 디렉토리 구조 (Repository Structure)](#-디렉토리-구조-repository-structure)

<hr>

## 📌 프로젝트 개요 (Overview)

본 레포지토리(`iso9001-deepseek-fastapi-chatbot`)는 **ISO 9001:2015 품질경영시스템**에 특화된 AI 컨설턴트를 구축하는 프로젝트입니다. 단순히 튜토리얼 수준을 넘어, **실제 프로덕션 환경에서 사용할 수 있는 로컬 오픈소스 LLM 5종**의 성능을 극한의 건틀릿(Gauntlet) 데이터셋으로 엄격하게 평가하고 튜닝한 결과를 포함합니다.

---

## 🏗️ 시스템 아키텍처 (Architecture)

하드웨어 리소스를 최적화하고 실제 서비스 배포 환경을 모사하기 위해, 프론트엔드와 백엔드를 철저히 분리한 **분산 처리 아키텍처**를 채택했습니다.

<div align="center">
  <img src="06_visualizations/images/00_architecture.svg" alt="System Architecture" width="80%">
</div>

| 환경 | 역할 및 기술 스택 |
|---|---|
| **💻 Local MacBook** | 사용자가 체감하는 지연 시간을 최소화하기 위한 가벼운 **Streamlit** Chat UI 구동. 사용자 질의 및 초기 PDF 문서 업로드 담당. |
| **🖥️ Ubuntu DGX Server** | 무거운 연산 전담. **FastAPI** 서버가 REST API로 통신하며, 문서 파싱/임베딩, **Chroma DB** 벡터 검색, **DeepSeek** 등 로컬 LLM 추론 연산 수행. |

---

## 📊 벤치마크 및 성능 (Performance)

단순 요약 능력을 넘어 실무 환경의 엣지 케이스에서도 안정적으로 동작하는지 평가하기 위해 **100-Question Gauntlet 데이터셋**을 직접 구축했습니다.

<details>
<summary><b>💡 건틀릿 데이터셋 구성 보기 (클릭하여 펼치기)</b></summary>
<br>
<img src="06_visualizations/images/06_dataset_composition.png" width="60%">

* **ISO 9001 Core Knowledge (85%):** 규격서의 핵심 지식에 대한 심층 질문 (예: "내부 심사 주기는?")
* **Edge Cases / Nonsense (10%):** 환각을 유도하는 함정 질문 (예: "규격서에 마블 영화 내용이 있나요?")
* **General Greeting / Out of Domain (5%):** 도메인 외 일상 대화 처리 능력 평가
</details>

### 모델별 종합 성능 평가 지표

총 5개의 최신 오픈소스 로컬 LLM (`DeepSeek v4`, `Phi-4`, `Llama 4`, `Gemma 4`, `Qwen 3.6`)을 벤치마킹했습니다.

<div align="center">
  <img src="06_visualizations/images/01_performance_metrics.png" width="70%">
  <img src="06_visualizations/images/02_performance_barchart.png" width="80%">
</div>

> 🏆 **Winner: DeepSeek v4**  
> 평가 결과, DeepSeek v4 모델이 **RAG Score 99.9점, Accuracy 99.7점**이라는 경이로운 수치를 기록하며 경쟁 모델들을 완벽하게 압도했습니다. (반면 특정 모델들은 도메인 내에서 정확도가 50점대까지 떨어지는 불안정성을 보였습니다.)

---

## ⚡ 추론 속도 및 효율성 (Efficiency)

엔터프라이즈 환경에서는 답변의 품질만큼이나 **빠른 응답 속도(Low Latency)**가 생명입니다.

<div align="center">
  <img src="06_visualizations/images/03_inference_time.png" width="70%">
  <img src="06_visualizations/images/04_speed_vs_quality.png" width="80%">
</div>

* Llama 4와 Phi-4는 추론 속도가 매우 빨랐으나, RAG 품질 측면에서 1등을 달성하지는 못했습니다.
* **DeepSeek v4**는 **평균 10.9초라는 훌륭하고 실용적인 추론 속도를 유지하면서도 99.9점이라는 독보적인 품질**을 달성해, 가장 완벽한 트레이드오프(Trade-off) 밸런스를 입증했습니다.

---

## 📉 안정성 및 파라미터 튜닝 (Stability Tuning)

LLM의 치명적 한계인 **'할루시네이션(거짓말)'** 현상을 원천 차단하기 위해, 극한의 하이퍼파라미터 튜닝을 진행했습니다.

<div align="center">
  <img src="06_visualizations/images/05_tuning_process.png" width="70%">
</div>

* 챗봇이 오직 사실(Fact)에 기반해 답변하도록 `Temperature`(창의성)와 `Repetition Penalty`(반복 페널티)를 미세 조정했습니다.
* 그 결과, 초기 5건씩 발생하던 환각 에러가 최적의 **Golden Iteration (Temp 0.7, Rep. Penalty 1.15)** 셋업을 찾은 후 **0건으로 완벽히 소멸**되었습니다.

<details>
<summary><b>🛡️ 최종 챗봇 안정성 테스트 결과 (클릭하여 펼치기)</b></summary>
<br>
<img src="06_visualizations/images/07_gauntlet_results.png" width="60%">
튜닝을 마친 후 진행된 최종 건틀릿 테스트에서 주력 모델 모두가 실패율 0을 기록하며 <b>100% Pass Rate</b>의 엔터프라이즈급 안정성을 확보했습니다.
</details>

---

## 🚀 퀵 스타트 (Quick Start)

로컬 환경에서 프론트엔드를 실행하고, 원격 서버에서 백엔드를 구동하는 방법입니다.

```bash
# 1. 원격 서버(Ubuntu)에서 백엔드 및 LLM 구동
cd 01_backend
pip install -r requirements.txt
uvicorn server_api:app --host 0.0.0.0 --port 8000

# 2. 로컬 장비(MacBook)에서 프론트엔드 구동
cd 02_frontend
pip install streamlit requests
streamlit run mac_chat_app.py
```

---

## 📁 디렉토리 구조 (Repository Structure)

```text
📦 iso9001-deepseek-fastapi-chatbot
 ┣ 📂 01_backend/          # FastAPI 서버 구현체 및 RAG API 라우팅
 ┣ 📂 02_frontend/         # Streamlit 기반 사용자 챗봇 UI (mac_chat_app.py)
 ┣ 📂 03_eval_pipeline/    # 모델 자동 벤치마킹 및 안정성 평가 툴킷
 ┣ 📂 04_dataset_tools/    # ISO 9001 평가 데이터셋(Gauntlet) 생성 스크립트
 ┣ 📂 05_deployment/       # 원격 서버 배포 및 프로세스 관리 Shell 스크립트
 ┗ 📂 06_visualizations/   # 분석 결과 시각화용 Jupyter Notebook 및 이미지 모음
```

> ⚠️ **Notice:** 원활한 소스코드 리뷰 및 경량화를 위해 로컬 LLM의 무거운 가중치 파일(`.bin`, `.safetensors`)과 원본 대용량 평가 데이터 파일은 본 레포지토리에서 제외되었습니다.

---

## 📚 출처 및 참고문헌 (References & Acknowledgements)

본 프로젝트는 다음의 규격서와 이전의 머신러닝 대회 경험, 그리고 훌륭한 오픈소스 생태계를 참고하여 제작되었습니다.

* **ISO 9001:2015 규격 원문:**
  * [ISO 9001:2015 Quality management systems — Requirements](https://www.iso.org/standard/62085.html)
* **Kaggle Gemma LoRA Fine-Tuning 경험:**
  * 본 프로젝트의 파라미터 튜닝 및 모델 안정성 평가 방법론은 과거 **Kaggle 대회에 참여하여 Gemma 모델을 LoRA로 파인튜닝했던 경험**에서 큰 영감을 받았습니다. 당시 작성했던 노트북 코드는 아래 링크에서 확인하실 수 있습니다.
  * 🔗 [Kaggle: Aims to Teach Fine-Tuning Python (Gemma LoRA)](https://www.kaggle.com/code/chldlsel/aims-to-teach-fine-tuning-python)
* **Open Source Frameworks & Models:**
  * [DeepSeek AI](https://github.com/deepseek-ai) - 경량화된 고성능 추론을 가능하게 한 핵심 로컬 LLM
  * [FastAPI](https://fastapi.tiangolo.com/) - 고성능 RAG 백엔드 서버 구축
  * [Streamlit](https://streamlit.io/) - 직관적인 Python 기반 챗봇 프론트엔드 UI 구축
  * [ChromaDB](https://docs.trychroma.com/) - 효율적인 로컬 벡터 임베딩 저장소
  * [Mermaid JS](https://mermaid.js.org/) - 시스템 아키텍처 다이어그램 시각화
