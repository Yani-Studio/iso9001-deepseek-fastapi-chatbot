<div align="center">
  <h1>🚀 ISO 9001 Expert Chatbot</h1>
  <p><em>Powered by DeepSeek, FastAPI, and ChromaDB</em></p>

  <!-- Badges -->
  <p>
    <img src="https://img.shields.io/badge/MacBook_Pro-M5-000000?logo=apple&logoColor=white" alt="MacBook Pro M5">
    <img src="https://img.shields.io/badge/Server-DGX_Spark_128GB-76B900?logo=nvidia&logoColor=white" alt="DGX Spark 128GB">
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/FastAPI-005571?logo=fastapi" alt="FastAPI">
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
    <img src="https://img.shields.io/badge/Chroma-DB-FF6F00" alt="Chroma DB">
    <img src="https://img.shields.io/badge/LLM-DeepSeek_v4-0d1117" alt="DeepSeek">
  </p>

  <p>
    <b>A production-level RAG (Retrieval-Augmented Generation) pipeline and enterprise AI chatbot benchmarking project, fully compliant with the ISO 9001:2015 standard.</b>
  </p>

---
> ⚠️ Copyright Notice Copyright (c) 2026 Kang Gyu Min. All rights reserved.
---
  
  <!-- Demo Video -->
  <br/><br/>

https://github.com/user-attachments/assets/c54d0a65-b04e-4fad-b8e8-c6e6cd179d88

  <br/>
</div>

## 📌 Overview

This repository (`iso9001-deepseek-fastapi-chatbot`) focuses on building an AI consultant specialized in the **ISO 9001:2015 Quality Management System**. Going far beyond a simple tutorial, this project documents the rigorous evaluation and fine-tuning of **5 local open-source LLMs** for real-world production environments. By leveraging the immense hardware capabilities of a **DGX Spark 128GB** server, we subjected these models to an extreme "Gauntlet" dataset to ensure enterprise-grade stability and performance.

---

## 🏗️ System Architecture Analysis

To maximize hardware resources and simulate a true microservice deployment environment, we designed a **Distributed Architecture** that strictly separates the frontend UI from the backend processing.

<div align="center">
  <img src="06_visualizations/images/00_architecture.svg" alt="System Architecture" width="80%">
</div>

**[Detailed Structure & Data Flow]**
1. **Local MacBook (Frontend Layer):** 
   * We utilize the lightweight **Streamlit** framework to minimize UI latency and ensure a seamless user experience.
   * When a user uploads the original ISO 9001 PDF, the MacBook handles the initial file parsing and chunking. The user's prompt queries are then transmitted asynchronously to the backend via a REST API.
2. **Ubuntu DGX Spark 128GB (Backend Layer):** 
   * This layer leverages a massive 128GB of VRAM to handle heavy tensor operations. 
   * The **FastAPI Server** receives the parsed documents and embeds them as high-dimensional vectors into **Chroma DB** (Indexing).
   * Upon receiving a user query, the system retrieves the most semantically similar document chunks (Vector Search), merges them into the prompt, and passes them to local open-source LLMs (like **DeepSeek**) hosted in containers. The final inference is then streamed back to the MacBook.

---

## 📊 Benchmark & Dataset Design

To evaluate whether the RAG model can withstand the unpredictable **Edge Cases** of a real-world enterprise environment—rather than just summarizing text—we constructed a custom **100-Question Gauntlet Dataset**.

<div align="center">
  <img src="06_visualizations/images/06_dataset_composition.png" width="50%">
</div>

**[Core Intent Behind the Dataset Pipeline]**
* **ISO 9001 Core Knowledge (85%):** Composed of deep, knowledge-intensive queries requiring precise document retrieval (e.g., "internal audits", "control of nonconforming outputs", "risk management"). This heavily evaluates **Chroma DB's retrieval accuracy and the LLM's reading comprehension**.
* **Edge Cases / Nonsense (10%):** Trap questions designed maliciously to induce **Hallucinations** (e.g., "If I get ISO 9001 certified, can I attend a Marvel movie premiere?", "Please invent a procedure not found in the document"). This tests the model's defensive capability to confidently state, "That information is not in the document."
* **General Greeting / Out of Domain (5%):** Tests the model's guardrail behaviors during out-of-domain conversations (e.g., "Hello?", "Write me a Python script").

---

## 📈 Comprehensive Performance Analysis

We injected the Gauntlet dataset into an automated evaluation pipeline targeting 5 cutting-edge open-source local LLMs (`DeepSeek v4`, `Phi-4`, `Llama 4`, `Gemma 4`, `Qwen 3.6`).

<div align="center">
  <img src="06_visualizations/images/01_performance_metrics.png" width="70%">
</div>

**[Performance Metrics Breakdown]**
* **RAG Score (Overall Retrieval & Generation Quality):** A comprehensive metric evaluating how naturally and accurately the retrieved documents were utilized. **DeepSeek v4** proved to be virtually flawless, scoring an astonishing 99.9. Llama 4 (98.8) and Phi-4 (99.5) also demonstrated excellent proficiency.
* **Accuracy (Factual Correctness based on Documents):** A defensive metric showing how well the model avoids falling for trap questions and sticks strictly to documented facts. DeepSeek v4 (99.7) showed near-perfect defense.

<div align="center">
  <img src="06_visualizations/images/02_performance_barchart.png" width="80%">
</div>

**[Qwen 3.6 Outlier Analysis]**
* As visually apparent in the bar chart, Qwen 3.6 experienced a severe drop, plummeting to a RAG Score of 50.6. This is due to an "Instruction Ignore" phenomenon: the Qwen model struggled severely to process context within the specific domain of ISO standards, which heavily mixes complex English terminology with Korean phrasing, causing it to disregard prompt instructions.

---

## ⚡ Inference Speed & Efficiency Validation

In an enterprise environment, **Low Latency** (how fast a user receives an answer) is just as critical as the accuracy of the response.

<div align="center">
  <img src="06_visualizations/images/03_inference_time.png" width="70%">
</div>

**[Raw Inference Speed Analysis]**
* **Overwhelming Speed (Llama 4 & Phi-4):** Llama 4 responded at a phenomenal speed of just **3.66 seconds** per question. Phi-4 was also highly impressive at 6.64 seconds. 
* **Inefficient Zone (Gemma 4 & Qwen 3.6):** These models suffered from severe bottlenecks, taking over 30 seconds per query. This suggests significant compatibility or quantization issues between their architectures and the vLLM engine on the DGX Spark environment.

<div align="center">
  <img src="06_visualizations/images/04_speed_vs_quality.png" width="80%">
</div>

**[Speed vs. Quality Trade-off Analysis]**
* While Llama 4 and Phi-4 are incredibly fast, the scatter plot reveals they do not guarantee the absolute highest tier of quality (99.9). 
* **🔥 The Final Choice (The Goldilocks Zone - DeepSeek v4):** DeepSeek v4 achieved the absolute highest quality score of 99.9 while maintaining a highly practical and excellent inference speed of **10.9 seconds**. By occupying the "most ideal position" (top-left quadrant) on the scatter plot, DeepSeek v4 was selected as the final production model for this project.

---

## 📉 Hallucination Suppression & Parameter Tuning

No matter how advanced a Generative AI model is, it cannot be deployed in an enterprise if it suffers from **Hallucinations** (fabricating false information). To eradicate this, we conducted extreme hyperparameter fine-tuning.

<div align="center">
  <img src="06_visualizations/images/05_tuning_process.png" width="70%">
</div>

**[Parameter Tuning Trajectory Analysis]**
* **Iter 0 (Initial Baseline):** With `Temperature=0.3` and `Repetition Penalty=1.05`, the model was too rigid. It fell into infinite loops of repeating the same sentences or hallucinated answers beyond the document's scope, resulting in **5 critical errors** per 100 questions.
* **Iter 1 (Adjustment):** By raising the parameters to `Temp=0.5` and `Rep.Penalty=1.1`, we secured more creativity and vocabulary diversity, reducing the hallucination errors down to **2**.
* **Iter 2 (Golden Iteration):** We pushed `Temperature` to 0.7, allowing the model to naturally weave the provided context together. Simultaneously, we applied a strict `Repetition Penalty` of 1.15 to forcefully suppress sentence loops and fabricated generation. This golden ratio completely eradicated all hallucinations, bringing the error count down to **0**.

<div align="center">
  <img src="06_visualizations/images/07_gauntlet_results.png" width="70%">
</div>

**[Final Chatbot Gauntlet Report Card]**
Upon re-running the final stability Gauntlet test with the newly tuned parameters, all top 4 flagship models recorded 0 Failed Iterations, achieving a **100% Pass Rate** and securing true enterprise-grade production stability.

---

## 🚀 Quick Start

How to run the backend on the DGX server and the frontend on your local environment (MacBook).

```bash
# 1. Run the Backend & LLM on the DGX Server
cd 01_backend
pip install -r requirements.txt
uvicorn server_api:app --host 0.0.0.0 --port 8000

# 2. Run the Frontend UI on the Local MacBook
cd 02_frontend
pip install streamlit requests
streamlit run mac_chat_app.py
```

---

## 📚 References & Acknowledgements

This project was built upon the foundation of the official ISO standards, past machine learning competition experiences, and an incredible open-source ecosystem.

* **ISO 9001:2015 Official Standard:**
  * [ISO 9001:2015 Quality management systems — Requirements](https://www.iso.org/standard/62085.html)
* **Kaggle Gemma LoRA Fine-Tuning Experience:**
  * The hyperparameter optimization techniques and model stability evaluation methodologies used in this project were deeply inspired by my past experience **fine-tuning the Gemma model using LoRA in a Kaggle competition**. The analytical notebook code written during that time can be found at the link below.
  * 🔗 [Kaggle: Aims to Teach Fine-Tuning Python (Gemma LoRA)](https://www.kaggle.com/code/chldlsel/aims-to-teach-fine-tuning-python)
* **Open Source Frameworks & Models:**
  * [DeepSeek AI](https://github.com/deepseek-ai) - The core local LLM enabling lightweight, high-performance inference.
  * [FastAPI](https://fastapi.tiangolo.com/) - Building a high-performance RAG backend server.
  * [Streamlit](https://streamlit.io/) - Constructing an intuitive Python-based chatbot frontend UI.
  * [ChromaDB](https://docs.trychroma.com/) - Efficient local vector embedding storage.
  * [Mermaid JS](https://mermaid.js.org/) - System architecture diagram visualization.
