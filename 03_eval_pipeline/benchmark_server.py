import requests
import json
import time
import subprocess
import os

SERVER_URL = "http://localhost:8000"
MODELS = ["qwen3.6", "gemma4", "phi4", "llama4", "deepseek_v4"]

QUESTIONS = [
    "품질 목표를 수립할 때 ISO 9001에서 요구하는 필수 포함 사항은 무엇인가요?",
    "부적합 제품이 발견되었을 때 조직이 취해야 하는 조치 절차를 설명해 주세요.",
    "내부 심사의 목적과 주기에 대해 ISO 9001은 어떻게 규정하고 있나요?",
    "경영검토 시 최고경영자가 반드시 검토해야 하는 입력 사항은 무엇인가요?",
    "리스크 기반 사고란 무엇이며, 품질경영시스템에 어떻게 적용해야 하나요?"
]

OUTPUT_FILE = "/home/yani_studio/Desktop/iso/benchmark_results.json"

def restart_server():
    print("[시스템] 서버를 강제 재부팅합니다 (OOM 방지)...")
    subprocess.run(["pkill", "-9", "-f", "server_api.py"], check=False)
    time.sleep(3)
    subprocess.Popen("nohup python3 /home/yani_studio/Desktop/iso/server_api.py > /home/yani_studio/Desktop/iso/server.log 2>&1 &", shell=True)
    time.sleep(15)

def run_pilot():
    results = {m: [] for m in MODELS}
    
    for model_id in MODELS:
        restart_server()
        print(f"[{model_id}] 평가 시작...")
        
        try:
            res = requests.post(f"{SERVER_URL}/load", json={"model_id": model_id}, timeout=1200)
            if res.status_code != 200:
                print(f"[{model_id}] 로드 실패")
                continue
        except Exception as e:
            print(f"[{model_id}] 로드 에러: {e}")
            continue
            
        for idx, q in enumerate(QUESTIONS):
            start_t = time.time()
            try:
                chat_res = requests.post(
                    f"{SERVER_URL}/chat_stream", 
                    json={"model_id": model_id, "message": q},
                    stream=True,
                    timeout=1200
                )
                answer = ""
                for line in chat_res.iter_lines():
                    if line:
                        decoded = line.decode('utf-8')
                        if decoded.startswith("data: "):
                            data_str = decoded[6:]
                            if data_str == "[DONE]": break
                            try:
                                data = json.loads(data_str)
                                if "token" in data: answer += data["token"]
                            except: pass
                end_t = time.time()
                if "</think>" in answer:
                    answer = answer.split("</think>")[-1].strip()
                results[model_id].append({"question": q, "answer": answer, "time": round(end_t - start_t, 2)})
            except Exception as e:
                pass
                
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run_pilot()
