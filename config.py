"""ISO 9001 AI 챗봇 파이프라인 — 공통 설정"""
import os
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/yani_studio/Desktop/iso")
PDF_PATH = BASE_DIR / "품질경영매뉴얼.pdf"
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"
LOG_DIR = BASE_DIR / "logs"
DB_DIR = BASE_DIR / "chromadb"
STATUS_FILE = BASE_DIR / "pipeline_status.json"

for d in [DATA_DIR, MODEL_DIR, LOG_DIR, DB_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# 5개 독립 트랙을 위한 모델 명세
MODELS = [
    {"id": "qwen3.6", "name": "Qwen3.6-27B", "repo": "Qwen/Qwen3.6-27B", "ollama_tag": "qwen3.6:27b-q8_0"},
    {"id": "gemma4", "name": "Gemma 4 31B", "repo": "google/gemma-4-31b", "ollama_tag": "gemma4:31b"},
    {"id": "phi4", "name": "Phi-4-Medium", "repo": "microsoft/phi-4", "ollama_tag": "phi4"},
    {"id": "llama4", "name": "Llama 4 Scout", "repo": "NousResearch/Meta-Llama-3-8B-Instruct", "ollama_tag": "llama4:scout"},
    {"id": "deepseek_v4", "name": "DeepSeek V4 Pro", "repo": "deepseek-ai/deepseek-coder-6.7b-instruct", "ollama_tag": "deepseek-coder:6.7b"},
]

def get_status():
    if STATUS_FILE.exists():
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    
    # 초기 상태 구성
    init_status = {
        "common": {"step1_extract": "pending", "step4_vectordb": "pending"},
        "tracks": {}
    }
    for m in MODELS:
        init_status["tracks"][m["id"]] = {
            "name": m["name"],
            "step2_generate": "pending",
            "step3_finetune": "pending",
            "message": ""
        }
    return init_status

def save_status(status):
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)

def update_common_status(step, state, progress=0, message=""):
    status = get_status()
    if step not in status["common"] or isinstance(status["common"][step], str):
        status["common"][step] = {"status": state, "progress": progress, "message": message}
    else:
        status["common"][step]["status"] = state
        if progress > 0 or state == "done": status["common"][step]["progress"] = progress
        if message: status["common"][step]["message"] = message
    save_status(status)

def update_track_status(model_id, step, state, progress=0, message=""):
    status = get_status()
    if model_id in status["tracks"]:
        if step:
            if step not in status["tracks"][model_id] or isinstance(status["tracks"][model_id][step], str):
                status["tracks"][model_id][step] = {"status": state, "progress": progress}
            else:
                status["tracks"][model_id][step]["status"] = state
                if progress > 0 or state == "done": status["tracks"][model_id][step]["progress"] = progress
        if message: status["tracks"][model_id]["message"] = message
    save_status(status)
