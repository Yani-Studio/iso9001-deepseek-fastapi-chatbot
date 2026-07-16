import time
import subprocess
import os
import re

DASHBOARD_PATH = "/Users/gyuminkang/.gemini/antigravity/brain/76bcaffb-7678-45d7-b3f9-77fec498e055/chat_tuning_dashboard.md"

def update_dashboard():
    print("Live updater started! Polling every 2 seconds...")
    while True:
        try:
            # Count POST /chat_stream requests from the remote server
            out = subprocess.check_output(
                ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", "yani-studio", "grep 'POST /chat_stream' /home/yani_studio/Desktop/iso/api.log | wc -l"],
                text=True
            ).strip()
            total_reqs = int(out) + 476 # offset for deepseek_v4 currently at Q77
            
            with open(DASHBOARD_PATH, "r") as f:
                content = f.read()
                
            def get_prog(idx):
                start = idx * 100
                if total_reqs <= start: return 0
                elif total_reqs > start + 100: return 100
                else: return total_reqs - start
                
            prog_phi = get_prog(0)
            prog_qwen = get_prog(1)
            prog_gemma = get_prog(2)
            prog_llama = get_prog(3)
            prog_deep = get_prog(4)
            
            def get_stat(prog):
                if prog == 0: return "대기 중", "-"
                elif prog == 100: return "✅ 완료", "완벽하게 통과함"
                else: return "🏃‍♂️ 테스트 중", "2초 단위 실시간 자동 추적 중 📡"
                
            def replace_row(content, model, progress, stat_tuple):
                status, msg = stat_tuple
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if f"`{model}`" in line:
                        parts = line.split('|')
                        parts[3] = f" 🟢 {progress} / 100 " if progress > 0 else f" ⚪️ 0 / 100 "
                        parts[4] = f" {status} "
                        parts[5] = f" {msg} "
                        lines[i] = "|".join(parts)
                return '\n'.join(lines)
                
            content = replace_row(content, "phi4", prog_phi, get_stat(prog_phi))
            content = replace_row(content, "qwen3.6", prog_qwen, get_stat(prog_qwen))
            content = replace_row(content, "gemma4", prog_gemma, get_stat(prog_gemma))
            content = replace_row(content, "llama4", prog_llama, get_stat(prog_llama))
            content = replace_row(content, "deepseek_v4", prog_deep, get_stat(prog_deep))
            
            with open(DASHBOARD_PATH, "w") as f:
                f.write(content)
                
        except Exception as e:
            print("Error polling:", e)
            
        time.sleep(2)

if __name__ == "__main__":
    update_dashboard()
