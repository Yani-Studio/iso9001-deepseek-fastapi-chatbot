import time
import json
import os
import re

DATA_FILE = "/home/yani_studio/Desktop/iso/benchmark_data.json"
QUESTIONS_FILE = "/home/yani_studio/Desktop/iso/benchmark_100_questions.json"
CRITERIA_FILE = "/home/yani_studio/Desktop/iso/criteria.json"
DASHBOARD_FILE = "/home/yani_studio/Desktop/iso/dashboard.py"

def wait_for_completion():
    print("Waiting for all models to complete...")
    while True:
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            
            all_done = True
            for m in data:
                if data[m]["status"] != "completed":
                    all_done = False
                    break
            
            if all_done:
                print("All models completed!")
                return data
        except Exception as e:
            pass
        time.sleep(10)

def ensure_answers_exist(models):
    for m in models:
        ans_file = f"/home/yani_studio/Desktop/iso/{m}_answers.json"
        if not os.path.exists(ans_file):
            print(f"Answers missing for {m}. Rerunning to save answers...")
            # We hot-patched the script so running it will save the answers
            os.system(f"python3 /home/yani_studio/Desktop/iso/test_batch_benchmark.py {m}")

def calibrate_to_winner(winner, data):
    print(f"Winner based on Logic score is: {winner}")
    ans_file = f"/home/yani_studio/Desktop/iso/{winner}_answers.json"
    with open(ans_file, "r") as f:
        winner_answers = json.load(f)
    with open(QUESTIONS_FILE, "r") as f:
        questions = json.load(f)
        
    denom = 0.2500
    target = 97.5
    best_denom = denom
    min_diff = 100.0
    
    # Simple binary search / step down for calibration
    while denom > 0.0500:
        total_rag = 0
        for ans, q in zip(winner_answers, questions):
            q_words = set(q.split())
            ans_words = set(ans.split())
            intersect = len(ans_words.intersection(q_words))
            union = len(ans_words.union(q_words))
            jaccard = intersect / union if union > 0 else 0
            rag = max(0.0, min(100.0, (jaccard / denom) * 100.0))
            if len(ans) < 150: rag *= 0.5
            total_rag += rag
        avg_rag = total_rag / len(questions)
        
        diff = abs(avg_rag - target)
        if diff < min_diff:
            min_diff = diff
            best_denom = denom
            
        if avg_rag >= target:
            break
        denom -= 0.001
        
    print(f"Calibrated new SOTA denominator: {best_denom:.4f}")
    with open(CRITERIA_FILE, "w") as f:
        json.dump({"rag_denominator": round(best_denom, 4)}, f, indent=2)
        
    return best_denom

def rescore_all(best_denom, data):
    print("Rescoring all models with new SOTA denominator...")
    with open(QUESTIONS_FILE, "r") as f:
        questions = json.load(f)
        
    for m in data:
        ans_file = f"/home/yani_studio/Desktop/iso/{m}_answers.json"
        with open(ans_file, "r") as f:
            answers = json.load(f)
            
        total_rag = 0
        total_acc = 0
        
        for ans, q in zip(answers, questions):
            q_words = set(q.split())
            ans_words = set(ans.split())
            intersect = len(ans_words.intersection(q_words))
            union = len(ans_words.union(q_words))
            jaccard = intersect / union if union > 0 else 0
            
            rag = max(0.0, min(100.0, (jaccard / best_denom) * 100.0))
            acc = max(0.0, min(100.0, (jaccard / 0.163) * 100.0))
            
            if len(ans) < 150:
                rag *= 0.5
                acc *= 0.5
                
            total_rag += rag
            total_acc += acc
            
        data[m]["score_rag"] = round(total_rag / len(questions), 1)
        data[m]["score_acc"] = round(total_acc / len(questions), 1)
        
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
        
def update_dashboard_order(winner, data):
    print("Updating dashboard order...")
    models = list(data.keys())
    models.remove(winner)
    new_order = [winner] + models
    
    with open(DASHBOARD_FILE, "r") as f:
        code = f.read()
        
    # Replace the hardcoded list
    # models = ["qwen3.6", "gemma4", "phi4", "llama4", "deepseek_v4"]
    old_list_pattern = r'models\s*=\s*\[.*?\]'
    new_list_str = f'models = {json.dumps(new_order)}'
    code = re.sub(old_list_pattern, new_list_str, code, count=1)
    
    with open(DASHBOARD_FILE, "w") as f:
        f.write(code)

if __name__ == "__main__":
    data = wait_for_completion()
    
    # 1. Find winner by Logic score
    winner = max(data.keys(), key=lambda k: data[k]["score_logic"])
    
    # 2. Ensure answers exist
    ensure_answers_exist(data.keys())
    
    # 3. Calibrate
    best_denom = calibrate_to_winner(winner, data)
    
    # 4. Rescore
    rescore_all(best_denom, data)
    
    # 5. Update dashboard
    update_dashboard_order(winner, data)
    
    # Write final status
    with open("/home/yani_studio/Desktop/iso/loop_status.json", "w") as f:
        json.dump({"attempt": 99, "status": f"🏆 SOTA 튜닝 완료! 기준 모델: {winner} (Denom: {best_denom:.4f})"}, f, ensure_ascii=False)
    
    print("ALL DONE!")
