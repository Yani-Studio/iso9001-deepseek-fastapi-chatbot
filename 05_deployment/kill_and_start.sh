#!/bin/bash
pkill -9 -f run_batch_seq || true
pkill -9 -f test_batch_benchmark || true
tmux kill-session -t batch_bench || true
tmux new-session -d -s batch_bench "python3 /home/yani_studio/Desktop/iso/run_batch_seq.py >> /home/yani_studio/Desktop/iso/massive.log 2>&1"
echo "Restarted successfully."
