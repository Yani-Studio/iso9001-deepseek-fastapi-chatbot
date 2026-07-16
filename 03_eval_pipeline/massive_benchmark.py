import requests
import json
import time
import subprocess
import os

SERVER_URL = "http://localhost:8000"
MODELS = ["qwen3.6", "gemma4", "phi4", "llama4", "deepseek_v4"]
OUTPUT_FILE = "/home/yani_studio/Desktop/iso/massive_results.json"

base_topics = ["품질방침", "내부심사", "부적합", "시정조치", "경영검토", "문서화된 정보", "리스크 관리", "고객 만족", "공급망 관리", "품질목표"]

questions = []
for i in range(1000):
    topic = base_topics[i % len(base_topics)]
    scenario = ["제조업", "IT 소프트웨어", "건설업", "서비스업", "의료기기"][i % 5]
    questions.append(f"[{scenario} 환경] ISO 9001:2015 규격 중 '{topic}'과 관련된 요구사항을 설명하고, 실제 심사에서 자주 지적되는 부적합 사례를 1가지 제시하세요. (Q-{i+1})")

def restart_server():
    print("[시스템] 서버를 강제 재부팅합니다 (OOM 방지)...", flush=True)
    subprocess.run(["pkill", "-9", "-f", "server_api.py"], check=False)
    time.sleep(3)
    subprocess.Popen("nohup python3 /home/yani_studio/Desktop/iso/server_api.py < /dev/null > /home/yani_studio/Desktop/iso/server.log 2>&1 &", shell=True)
    time.sleep(15)

def run_benchmark():
    results = {m: [] for m in MODELS}
    
    for model_id in MODELS:
        restart_server()
        print(f"\n======================================", flush=True)
        print(f"[{model_id}] 1,000제 대규모 평가 시작...", flush=True)
        print(f"======================================\n", flush=True)
        
        try:
            res = requests.post(f"{SERVER_URL}/load", json={"model_id": model_id}, timeout=1200)
            if res.status_code != 200:
                print(f"[{model_id}] 로드 실패", flush=True)
                continue
        except Exception as e:
            print(f"[{model_id}] 로드 에러: {e}", flush=True)
            continue
            
        for idx, q in enumerate(questions):
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
                
                results[model_id].append({"q_id": idx+1, "question": q, "time": round(end_t - start_t, 2), "answer_length": len(answer)})
                
                if (idx + 1) % 10 == 0:
                    print(f"[{model_id}] {idx+1}/1000 완료 (최근 문항 소요시간: {round(end_t - start_t, 2)}초)", flush=True)
                    
            except Exception as e:
                print(f"[{model_id}] {idx+1}번 문항 에러: {e}", flush=True)
                
            # 중간 저장 (50문항 마다)
            if (idx + 1) % 50 == 0:
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run_benchmark()
    print("ALL DONE!", flush=True)
