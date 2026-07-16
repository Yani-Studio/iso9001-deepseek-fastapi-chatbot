import os
import json

# Kill current pipeline
os.system('tmux kill-session -t batch_bench 2>/dev/null')
os.system('pkill -9 -f run_pipeline 2>/dev/null')
os.system('pkill -9 -f test_batch_benchmark 2>/dev/null')

# Modify test_batch_benchmark.py to include the logic rules in the system prompt
with open('/home/yani_studio/Desktop/iso/test_batch_benchmark.py', 'r') as f:
    code = f.read()

old_prompt = '{"role": "system", "content": f"You are a helpful and professional ISO 9001 expert assistant. Answer in Korean. Context:\\n{context}"}'
new_prompt = '{"role": "system", "content": f"You are a professional ISO 9001 expert. Answer in Korean. MUST follow these rules: 1. Keep each sentence concise (around 15 words). 2. Use logical connectives (e.g. 첫째, 둘째, 따라서). Context:\\n{context}"}'

if old_prompt in code:
    code = code.replace(old_prompt, new_prompt)
    with open('/home/yani_studio/Desktop/iso/test_batch_benchmark.py', 'w') as f:
        f.write(code)

# Reset ONLY gemma, phi, llama, deepseek in benchmark_data.json
with open('/home/yani_studio/Desktop/iso/benchmark_data.json', 'r') as f:
    data = json.load(f)

for model in ['gemma4', 'phi4', 'llama4', 'deepseek_v4']:
    if model in data:
        data[model]['done'] = 0
        data[model]['status'] = 'pending'
        if 'score_rag' in data[model]: data[model]['score_rag'] = 0.0
        if 'score_acc' in data[model]: data[model]['score_acc'] = 0.0
        if 'score_logic' in data[model]: data[model]['score_logic'] = 0.0

with open('/home/yani_studio/Desktop/iso/benchmark_data.json', 'w') as f:
    json.dump(data, f, indent=2)

# Create a new run script that starts from gemma4
pipeline_script = '''#!/bin/bash
python3 /home/yani_studio/Desktop/iso/test_batch_benchmark.py gemma4
python3 /home/yani_studio/Desktop/iso/test_batch_benchmark.py phi4
python3 /home/yani_studio/Desktop/iso/test_batch_benchmark.py llama4
python3 /home/yani_studio/Desktop/iso/test_batch_benchmark.py deepseek_v4
'''
with open('/home/yani_studio/Desktop/iso/run_pipeline.sh', 'w') as f:
    f.write(pipeline_script)

# Restart pipeline
os.system('tmux new-session -d -s batch_bench "bash /home/yani_studio/Desktop/iso/run_pipeline.sh >> /home/yani_studio/Desktop/iso/massive.log 2>&1"')
