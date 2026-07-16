import requests
import json
import time
import subprocess
import os

SERVER_URL = "http://192.168.0.34:8000"
MODELS = ["qwen3.6", "gemma4", "phi4", "llama4", "deepseek_v4"]

# Pilot Test Questions (will be expanded to 1000 later)
QUESTIONS = [
    "품질 목표를 수립할 때 ISO 9001에서 요구하는 필수 포함 사항은 무엇인가요?",
    "부적합 제품이 발견되었을 때 조직이 취해야 하는 조치 절차를 설명해 주세요.",
    "내부 심사의 목적과 주기에 대해 ISO 9001은 어떻게 규정하고 있나요?",
    "경영검토 시 최고경영자가 반드시 검토해야 하는 입력 사항은 무엇인가요?",
    "리스크 기반 사고란 무엇이며, 품질경영시스템에 어떻게 적용해야 하나요?"
]

OUTPUT_FILE = "benchmark_results.json"

def restart_server():
    print("[시스템] 서버를 강제 재부팅합니다 (OOM 방지)...")
    subprocess.run([
        "ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", "yani-studio",
        "pkill -9 -f server_api.py; sleep 3; nohup python3 /home/yani_studio/Desktop/iso/server_api.py < /dev/null > /home/yani_studio/Desktop/iso/server.log 2>&1 &"
    ], check=False)
    time.sleep(15) # Wait for uvicorn to start

def run_pilot():
    results = {m: [] for m in MODELS}
    
    for model_id in MODELS:
        restart_server()
        print(f"[{model_id}] 평가 시작...")
        
        # Load Model
        try:
            res = requests.post(f"{SERVER_URL}/load", json={"model_id": model_id}, timeout=1200)
            if res.status_code != 200:
                print(f"[{model_id}] 로드 실패: {res.text}")
                continue
        except Exception as e:
            print(f"[{model_id}] 로드 중 예외 발생: {e}")
            continue
            
        # Run inference on all questions
        for idx, q in enumerate(QUESTIONS):
            print(f"  -> Q{idx+1} 추론 중...")
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
                
                # <think> 태그 제거
                if "</think>" in answer:
                    answer = answer.split("</think>")[-1].strip()
                    
                results[model_id].append({
                    "question": q,
                    "answer": answer,
                    "time_seconds": round(end_t - start_t, 2)
                })
                print(f"  -> 완료! ({round(end_t - start_t, 2)}초)")
                
            except Exception as e:
                print(f"  -> 에러: {e}")
                
        # 중간 저장
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    print("🚀 파이프라인 파일럿 테스트 (5문제) 시작!")
    run_pilot()
    print("✅ 파일럿 테스트 완료! 결과가 benchmark_results.json에 저장되었습니다.")
