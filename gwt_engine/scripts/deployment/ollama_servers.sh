#!/bin/bash
# Multi-Instance Ollama Server Deployment
# Optimized for Dual AMD 7900 XT

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Multi-Instance Ollama Deployment ===${NC}"
echo ""

# Check Ollama installation
if ! command -v ollama &> /dev/null; then
    echo "ERROR: Ollama not found. Install with: curl -fsSL https://ollama.ai/install.sh | sh"
    exit 1
fi

echo -e "${GREEN}✓ Ollama detected${NC}"
echo ""

# Function to start Ollama instance
start_ollama_instance() {
    local NAME=$1
    local GPU=$2
    local PORT=$3
    local NUM_PARALLEL=$4

    echo -e "${YELLOW}Starting $NAME on GPU $GPU (port $PORT, parallel=$NUM_PARALLEL)...${NC}"

    CUDA_VISIBLE_DEVICES=$GPU \
    OLLAMA_HOST=0.0.0.0:$PORT \
    OLLAMA_NUM_PARALLEL=$NUM_PARALLEL \
    ollama serve > logs/ollama_${NAME}.log 2>&1 &

    echo $! > /tmp/ollama_${NAME}.pid
    echo -e "${GREEN}✓ $NAME started (PID: $(cat /tmp/ollama_${NAME}.pid))${NC}"
}

# Create logs directory
mkdir -p logs

echo -e "${YELLOW}=== Phase 1: Central Workspace (GPU 0+1 tensor parallel) ===${NC}"
# Note: Ollama doesn't support tensor parallelism like vLLM
# So we run on single GPU with high parallelism
start_ollama_instance "central" 0 11434 4

sleep 3

echo ""
echo -e "${YELLOW}=== Phase 2: GPU 0 Specialists (Perception) ===${NC}"
start_ollama_instance "gpu0_specialists" 0 11435 6

sleep 3

echo ""
echo -e "${YELLOW}=== Phase 3: GPU 1 Specialists (Memory, Planning, Metacognition) ===${NC}"
start_ollama_instance "gpu1_specialists" 1 11436 8

sleep 3

echo ""
echo -e "${GREEN}=== All Ollama Instances Started ===${NC}"
echo ""
echo "Instance URLs:"
echo "  - Central Workspace: http://localhost:11434"
echo "  - GPU 0 Specialists: http://localhost:11435"
echo "  - GPU 1 Specialists: http://localhost:11436"
echo ""
echo "Logs: logs/ollama_*.log"
echo "PIDs: /tmp/ollama_*.pid"
echo ""
echo -e "${YELLOW}Waiting 10 seconds for servers to initialize...${NC}"
sleep 10

# Pull models if not already present
echo ""
echo -e "${YELLOW}Ensuring models are pulled...${NC}"

# Central Workspace (Llama 70B)
ollama pull llama3.1:70b-q4_K_M

# Perception (Mistral 22B)
OLLAMA_HOST=http://localhost:11435 ollama pull mistral-small:22b-q5_K_M

# Memory (Qwen 32B)
OLLAMA_HOST=http://localhost:11436 ollama pull qwen2.5-coder:32b-q4_K_M

# Planning (Llama 8B)
OLLAMA_HOST=http://localhost:11436 ollama pull llama3.1:8b-q5_K_M

# Metacognition (Gemma 9B)
OLLAMA_HOST=http://localhost:11436 ollama pull gemma2:9b-q6_K_M

echo ""
echo -e "${GREEN}=== Deployment Complete ===${NC}"
echo ""
echo "To stop servers: ./gwt_engine/scripts/deployment/stop_ollama_servers.sh"
echo "To test: curl http://localhost:11434/api/tags"
