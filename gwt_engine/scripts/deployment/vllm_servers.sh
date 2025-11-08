#!/bin/bash
# vLLM Server Startup Scripts for Dual AMD 7900 XT Configuration
# Optimized for ROCm + tensor parallelism

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== GWT Engine vLLM Server Deployment ===${NC}"
echo ""

# Configuration
MODEL_DIR="/models"
CACHE_DIR="/models/cache"

# Check ROCm availability
if ! command -v rocm-smi &> /dev/null; then
    echo -e "${RED}ERROR: ROCm not found. Please install ROCm first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ ROCm detected${NC}"
rocm-smi --showproductname

echo ""
echo -e "${YELLOW}Starting vLLM servers...${NC}"
echo ""

# Function to start vLLM server
start_vllm_server() {
    local NAME=$1
    local MODEL=$2
    local PORT=$3
    local GPU=$4
    local TENSOR_PARALLEL=$5
    local MAX_MODEL_LEN=$6
    local GPU_MEM_UTIL=$7

    echo -e "${GREEN}Starting $NAME on port $PORT (GPU $GPU, tensor_parallel=$TENSOR_PARALLEL)...${NC}"

    CUDA_VISIBLE_DEVICES=$GPU \
    vllm serve $MODEL_DIR/$MODEL \
        --host 0.0.0.0 \
        --port $PORT \
        --tensor-parallel-size $TENSOR_PARALLEL \
        --gpu-memory-utilization $GPU_MEM_UTIL \
        --max-model-len $MAX_MODEL_LEN \
        --max-num-batched-tokens 2048 \
        --max-num-seqs 32 \
        --trust-remote-code \
        --download-dir $CACHE_DIR \
        > logs/vllm_${NAME}.log 2>&1 &

    echo $! > /tmp/vllm_${NAME}.pid
    echo -e "${GREEN}✓ $NAME started (PID: $(cat /tmp/vllm_${NAME}.pid))${NC}"
}

# Create logs directory
mkdir -p logs

# Phase 1: Central Workspace Server (Llama 70B, Tensor Parallel across both GPUs)
echo -e "${YELLOW}=== Phase 1: Central Workspace ===${NC}"
start_vllm_server \
    "central_workspace" \
    "llama-3.1-70b-q4_k_m" \
    8000 \
    "0,1" \
    2 \
    4096 \
    0.90

echo ""
sleep 5

# Phase 2: GPU 1 Specialists Server (Perception on GPU 0)
echo -e "${YELLOW}=== Phase 2: GPU 1 Specialists (Perception) ===${NC}"
start_vllm_server \
    "gpu1_specialists" \
    "mistral-small-22b-q5_k_m" \
    8001 \
    0 \
    1 \
    8192 \
    0.85

echo ""
sleep 5

# Phase 3: GPU 2 Specialists Server (Memory, Planning, Metacognition on GPU 1)
echo -e "${YELLOW}=== Phase 3: GPU 2 Specialists (Memory, Planning, Metacognition) ===${NC}"
# Note: This server will handle multiple models via multi-model serving
# For now, we start with the primary model (Qwen 32B for memory)
start_vllm_server \
    "gpu2_specialists" \
    "qwen-2.5-coder-32b-q4_k_m" \
    8002 \
    1 \
    1 \
    32768 \
    0.85

echo ""
echo -e "${GREEN}=== All vLLM Servers Started ===${NC}"
echo ""
echo "Server URLs:"
echo "  - Central Workspace: http://localhost:8000"
echo "  - GPU 1 Specialists: http://localhost:8001"
echo "  - GPU 2 Specialists: http://localhost:8002"
echo ""
echo "Logs: logs/vllm_*.log"
echo "PIDs: /tmp/vllm_*.pid"
echo ""
echo -e "${YELLOW}Waiting 30 seconds for servers to initialize...${NC}"
sleep 30

# Health check
echo ""
echo -e "${YELLOW}Performing health checks...${NC}"

check_health() {
    local NAME=$1
    local PORT=$2

    if curl -s http://localhost:$PORT/health > /dev/null; then
        echo -e "${GREEN}✓ $NAME is healthy${NC}"
    else
        echo -e "${RED}✗ $NAME is not responding${NC}"
    fi
}

check_health "Central Workspace" 8000
check_health "GPU 1 Specialists" 8001
check_health "GPU 2 Specialists" 8002

echo ""
echo -e "${GREEN}=== Deployment Complete ===${NC}"
echo ""
echo "To stop servers: ./gwt_engine/scripts/deployment/stop_vllm_servers.sh"
