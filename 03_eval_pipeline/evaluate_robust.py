import requests
import json
import time
import subprocess
import os

SERVER_URL = "http://192.168.0.34:8000"
MODELS = ["gemma4", "phi4", "llama4", "deepseek_v4"]
QUESTION = "품질 목표를 수립할 때 ISO 9001에서 요구하는 필수 포함 사항은 무엇인가요? 측정 가능해야 하나요?"

output_log = "/Users/gyuminkang/.gemini/antigravity/brain/76bcaffb-7678-45d7-b3f9-77fec498e055/scratch/eval_results.txt"

with open(output_log, "w") as f:
    f.write(f"질문: {QUESTION}\n\n")

def restart_server():
    print("서버 재시작 중 (OOM 방지)...")
    subprocess.run([
        "ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", "yani-studio",
        "pkill -9 -f server_api.py; sleep 3; nohup python3 /home/yani_studio/Desktop/iso/server_api.py > /home/yani_studio/Desktop/iso/server.log 2>&1 &"
    ], check=False)
    time.sleep(15) # Wait for uvicorn to start

for model_id in MODELS:
    restart_server()
    print(f"[{model_id}] 로딩 중...")
    
    start_time = time.time()
    try:
        # Load
        res = requests.post(f"{SERVER_URL}/load", json={"model_id": model_id}, timeout=1200) # 20 mins max
        if res.status_code != 200:
            msg = f"[{model_id}] ❌ 로드 실패: {res.text}\n"
            print(msg)
            with open(output_log, "a") as f: f.write(msg + "-"*50 + "\n")
            continue
            
        print(f"[{model_id}] ✅ 로드 완료. 답변 생성 중...")
        
        # Chat
        chat_res = requests.post(
            f"{SERVER_URL}/chat_stream", 
            json={"model_id": model_id, "message": QUESTION},
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
                    
        end_time = time.time()
        
        if "</think>" in answer:
            answer = answer.split("</think>")[-1].strip()
            
        msg = f"[{model_id}] ⏱️ 소요 시간: {end_time - start_time:.2f}초\n💡 답변:\n{answer}\n"
        print(msg)
        with open(output_log, "a") as f: f.write(msg + "-"*50 + "\n")
        
    except Exception as e:
        msg = f"[{model_id}] ❌ 에러 발생: {e}\n"
        print(msg)
        with open(output_log, "a") as f: f.write(msg + "-"*50 + "\n")
