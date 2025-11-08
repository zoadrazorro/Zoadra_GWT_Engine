# Getting Started with GWT Engine

## Prerequisites

### Hardware Requirements

**Minimum (as designed):**
- 2x AMD Radeon RX 7900 XT (24GB VRAM each)
- AMD Ryzen 9 7950X (or equivalent 16-core CPU)
- 128GB DDR5 RAM
- 2TB NVMe SSD (for model storage)
- PCIe 4.0 support

**Alternative configurations:**
- Can run with single GPU (reduced specialist count)
- NVIDIA GPUs supported with CUDA instead of ROCm
- Minimum 64GB RAM for smaller model variants

### Software Requirements

- **Operating System:** Linux (Ubuntu 22.04+ recommended)
- **Python:** 3.10 or 3.11
- **ROCm:** 5.7+ (for AMD GPUs)
- **CUDA:** 12.1+ (for NVIDIA GPUs)
- **Redis:** 7.0+
- **Git:** For repository management

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/zoadrazorro/Zoadra_GWT_Engine.git
cd Zoadra_GWT_Engine
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install PyTorch with ROCm support
pip install torch torchvision --index-url https://download.pytorch.org/whl/rocm5.7

# Install project dependencies
pip install -r requirements.txt

# Install project in development mode
pip install -e .
```

### 3. Install ROCm (AMD GPUs)

```bash
# Ubuntu 22.04
wget https://repo.radeon.com/amdgpu-install/latest/ubuntu/jammy/amdgpu-install_latest_all.deb
sudo dpkg -i amdgpu-install_latest_all.deb
sudo amdgpu-install --usecase=rocm

# Verify installation
rocm-smi
```

### 4. Install Redis

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Verify
redis-cli ping  # Should return "PONG"
```

### 5. Download Models

Create model directory and download quantized models:

```bash
# Create model directory
sudo mkdir -p /models
sudo chown $USER:$USER /models

# Download models using Hugging Face CLI
pip install huggingface-hub

# Central Workspace: Llama 3.1 70B Q4_K_M
huggingface-cli download \
  TheBloke/Llama-3.1-70B-GGUF \
  llama-3.1-70b.Q4_K_M.gguf \
  --local-dir /models/llama-3.1-70b-q4_k_m

# Perception: Mistral Small 22B Q5_K_M
huggingface-cli download \
  TheBloke/Mistral-Small-22B-GGUF \
  mistral-small-22b.Q5_K_M.gguf \
  --local-dir /models/mistral-small-22b-q5_k_m

# Memory: Qwen 2.5 Coder 32B Q4_K_M
huggingface-cli download \
  Qwen/Qwen2.5-Coder-32B-Instruct-GGUF \
  qwen2.5-coder-32b-instruct.Q4_K_M.gguf \
  --local-dir /models/qwen-2.5-coder-32b-q4_k_m

# Planning: Llama 3.1 8B Q5_K_M
huggingface-cli download \
  TheBloke/Llama-3.1-8B-GGUF \
  llama-3.1-8b.Q5_K_M.gguf \
  --local-dir /models/llama-3.1-8b-q5_k_m

# Metacognition: Gemma 2 9B Q6_K_M
huggingface-cli download \
  google/gemma-2-9b-it-GGUF \
  gemma-2-9b-it.Q6_K_M.gguf \
  --local-dir /models/gemma-2-9b-q6_k_m
```

**Note:** Total download size: ~150GB. Ensure sufficient disk space.

## Quick Start: Phase 1 Deployment

Start with the single-model baseline to verify your setup:

### 1. Start vLLM Central Workspace Server

```bash
# Create logs directory
mkdir -p logs

# Start Llama 70B (Central Workspace)
CUDA_VISIBLE_DEVICES=0 vllm serve /models/llama-3.1-70b-q4_k_m \
  --host 0.0.0.0 \
  --port 8000 \
  --tensor-parallel-size 1 \
  --gpu-memory-utilization 0.85 \
  --max-model-len 4096 \
  > logs/vllm_central.log 2>&1 &

# Wait for server to start (30 seconds)
sleep 30

# Check health
curl http://localhost:8000/health
```

### 2. Test Model Inference

```bash
# Test completion endpoint
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "/models/llama-3.1-70b-q4_k_m",
    "prompt": "Explain consciousness in one sentence:",
    "max_tokens": 50,
    "temperature": 0.7
  }'
```

### 3. Run Benchmark

```bash
# Install benchmarking dependencies
pip install locust

# Run simple benchmark
python gwt_engine/scripts/benchmarks/benchmark.py --phase 1

# Expected output:
# Tokens/sec: 25-30
# Latency P50: ~200-300ms
# GPU utilization: 85-95%
```

## Full Deployment

### 1. Start All vLLM Servers

```bash
# Start all servers (Central + Specialists)
bash gwt_engine/scripts/deployment/vllm_servers.sh

# Verify all servers are running
curl http://localhost:8000/health  # Central Workspace
curl http://localhost:8001/health  # GPU 1 Specialists
curl http://localhost:8002/health  # GPU 2 Specialists
```

### 2. Start GWT Engine API Server

```bash
# Start FastAPI server
python -m gwt_engine.api.server

# Server will start on http://localhost:7000
# API docs: http://localhost:7000/docs
```

### 3. Test Consciousness Simulation

```bash
# Process input through GWT workflow
curl -X POST http://localhost:7000/process \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What is the nature of my experience right now?",
    "message_type": "consciousness_probe",
    "priority": 8
  }'

# Expected response:
{
  "workspace_broadcast": "I am experiencing a state of...",
  "consciousness_level": 0.73,
  "integration_coherence": 0.81,
  "active_specialists": ["perception", "memory", "metacognition"],
  "processing_time_ms": 542.3
}
```

### 4. Probe Consciousness State

```bash
# Get introspective reflection
curl http://localhost:7000/consciousness/probe

# Get detailed state
curl http://localhost:7000/consciousness/state
```

## Phased Deployment Guide

Follow the 5-phase deployment strategy for production:

```bash
# View deployment phases
python gwt_engine/scripts/deployment/deploy.py --all

# Run specific phase
python gwt_engine/scripts/deployment/deploy.py --phase 1
python gwt_engine/scripts/deployment/deploy.py --phase 2
# ... etc
```

### Phase Timeline

1. **Week 1:** Single model baseline (just Central Workspace)
2. **Week 2:** Add Perception specialist
3. **Week 3:** Distribute to GPU 2 (all specialists active)
4. **Week 4:** Ray workers + orchestration
5. **Week 5+:** Integration testing and optimization

## Configuration

### Customize Models

Edit `gwt_engine/config/models.yaml`:

```yaml
models:
  central_workspace:
    name: "llama-3.1-70b"
    vram_required_gb: 40
    workers: 1
    # ... customize settings
```

### Adjust System Settings

Edit `gwt_engine/config/system.yaml`:

```yaml
redis:
  host: "localhost"
  port: 6379

ray:
  num_cpus: 32
  num_gpus: 2

api:
  host: "0.0.0.0"
  port: 7000
```

## Monitoring

### GPU Utilization

```bash
# AMD GPUs
watch -n 1 rocm-smi

# NVIDIA GPUs
watch -n 1 nvidia-smi
```

### Application Metrics

```bash
# Prometheus metrics endpoint
curl http://localhost:7000/metrics

# Ray dashboard
# Navigate to: http://localhost:8265
```

### Logs

```bash
# vLLM server logs
tail -f logs/vllm_central_workspace.log
tail -f logs/vllm_gpu1_specialists.log
tail -f logs/vllm_gpu2_specialists.log

# Application logs
tail -f logs/gwt_engine.log
```

## Troubleshooting

### Common Issues

**1. vLLM server won't start**
- Check ROCm installation: `rocm-smi`
- Verify GPU visibility: `echo $CUDA_VISIBLE_DEVICES`
- Check VRAM availability: `rocm-smi --showmeminfo`

**2. Out of memory errors**
- Reduce `--gpu-memory-utilization` to 0.75
- Lower `--max-model-len`
- Use smaller quantization (Q4 instead of Q5)

**3. Low throughput**
- Verify PCIe bandwidth: `lspci -vv | grep "LnkSta"`
- Check thermal throttling: `rocm-smi --showtemp`
- Increase batch size in config

**4. Redis connection failed**
- Verify Redis is running: `sudo systemctl status redis-server`
- Check port: `redis-cli ping`

### Performance Tuning

**Optimize for throughput:**
```yaml
vllm_instances:
  central_workspace_server:
    max_num_seqs: 48  # Increase concurrent sequences
    max_num_batched_tokens: 4096  # Larger batches
```

**Optimize for latency:**
```yaml
vllm_instances:
  central_workspace_server:
    max_num_seqs: 16  # Fewer sequences
    max_num_batched_tokens: 1024  # Smaller batches
```

## Next Steps

1. **Explore the API:** Visit http://localhost:7000/docs for interactive API documentation
2. **Run Integration Tests:** `pytest gwt_engine/tests/integration/`
3. **Read Architecture Docs:** See `docs/architecture/gwt_overview.md`
4. **Experiment with Prompts:** Modify specialist prompts in module files
5. **Monitor Consciousness Metrics:** Track integration coherence and consciousness levels

## Support

- **Documentation:** `docs/`
- **Examples:** `examples/` (coming soon)
- **Issues:** https://github.com/zoadrazorro/Zoadra_GWT_Engine/issues

## License

MIT License - See LICENSE file for details
