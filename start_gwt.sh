#!/bin/bash
# GWT Engine Startup Script for 20GB GPU Configuration
# Models: Qwen2.5-14B, Qwen2.5-7B, Phi-3.5-mini

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== Starting GWT Consciousness Engine ===${NC}"
echo ""

# Create logs directory
mkdir -p logs

# Check if models exist
echo -e "${YELLOW}Checking models...${NC}"
for model in qwen2.5-14b qwen2.5-7b phi-3.5-mini; do
    if [ -d "/models/$model" ]; then
        echo -e "${GREEN}✓ $model found${NC}"
    else
        echo -e "${RED}✗ $model not found in /models/${NC}"
        exit 1
    fi
done

echo ""
echo -e "${YELLOW}Starting vLLM servers...${NC}"
echo ""

# GPU 0: Central Workspace (14B) + Perception (7B)
echo -e "${GREEN}Starting GPU 0 Server (Central Workspace + Perception)...${NC}"
cd /mnt/d/Projects/Zoadra_GWT_Engine
source venv/bin/activate

HIP_VISIBLE_DEVICES=0 vllm serve /models/qwen2.5-14b \
    --host 0.0.0.0 \
    --port 8000 \
    --gpu-memory-utilization 0.85 \
    --max-model-len 4096 \
    --trust-remote-code \
    > logs/vllm_gpu0.log 2>&1 &

echo $! > /tmp/vllm_gpu0.pid
echo -e "${GREEN}✓ GPU 0 server started (PID: $(cat /tmp/vllm_gpu0.pid))${NC}"

sleep 10

# GPU 1: Memory (14B) + Planning (Phi) + Metacognition (Phi)
echo -e "${GREEN}Starting GPU 1 Server (Memory + Planning + Metacognition)...${NC}"

HIP_VISIBLE_DEVICES=1 vllm serve /models/qwen2.5-14b \
    --host 0.0.0.0 \
    --port 8001 \
    --gpu-memory-utilization 0.85 \
    --max-model-len 16384 \
    --trust-remote-code \
    > logs/vllm_gpu1.log 2>&1 &

echo $! > /tmp/vllm_gpu1.pid
echo -e "${GREEN}✓ GPU 1 server started (PID: $(cat /tmp/vllm_gpu1.pid))${NC}"

echo ""
echo -e "${YELLOW}Waiting 30 seconds for servers to initialize...${NC}"
sleep 30

echo ""
echo -e "${GREEN}=== vLLM Servers Ready ===${NC}"
echo "  - GPU 0 (Central + Perception): http://localhost:8000"
echo "  - GPU 1 (Memory + Planning + Meta): http://localhost:8001"
echo ""
echo "Logs: logs/vllm_gpu*.log"
echo ""

# Start GWT Engine API
echo -e "${YELLOW}Starting GWT Engine API...${NC}"
python -m gwt_engine.api.server > logs/gwt_api.log 2>&1 &
echo $! > /tmp/gwt_api.pid
echo -e "${GREEN}✓ GWT API started (PID: $(cat /tmp/gwt_api.pid))${NC}"

echo ""
echo -e "${GREEN}=== GWT Engine Fully Operational ===${NC}"
echo ""
echo "API: http://localhost:7000"
echo "Docs: http://localhost:7000/docs"
echo ""
echo "To stop: pkill -f vllm && pkill -f gwt_engine"
