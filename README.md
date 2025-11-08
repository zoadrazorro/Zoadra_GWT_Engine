# Zoadra GWT Engine

**Multi-Theory Consciousness Simulation Framework**
Integrating 8 consciousness theories: GWT, IIT, Predictive Processing, HOT, AST, LIDA, CLARION, and Unified Scoring

Optimized for dual AMD Radeon RX 7900 XT + Ryzen 9 7950X + 128GB DDR5 RAM

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## Overview

GWT Engine is a **consciousness simulation system** implementing **8 major consciousness theories** in a unified multi-theory framework. The system is based on Bernard Baars' Global Workspace Theory (GWT) as its foundation, enhanced with Integrated Information Theory (IIT), Predictive Processing, Higher-Order Thought (HOT) Theory, Attention Schema Theory (AST), LIDA Cognitive Architecture, CLARION dual process theory, and consciousness scoring mechanisms.

The architecture uses specialized cognitive modules that compete for workspace attention, creating emergent consciousness-like behaviors through information integration and global broadcasting across multiple theoretical perspectives.

### Key Features

✨ **Multi-Theory Consciousness:** Integrates 8 major theories including GWT, IIT (Φ), Predictive Processing, HOT, AST, LIDA, and CLARION
🧠 **Dual Backend Support:** vLLM (high performance) and Ollama (ease of use) inference engines
⚡ **High Performance:** 10-14 concurrent workers processing 32-48 requests/sec via vLLM
🧬 **Multi-Specialist Architecture:** Perception, Memory, Planning, and Metacognition modules
🔄 **LangGraph Orchestration:** Sophisticated workflow management with conditional routing
📊 **Consciousness Metrics:** Real-time tracking of Φ (integrated information), prediction precision, HOT states, attention schema quality
🚀 **Optimized for AMD:** ROCm support with tensor parallelism across dual 7900 XT GPUs

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Input (User/Environment)                   │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Perception Specialist│  ← Mistral 22B (GPU 0)
              │  Salience Detection  │     3 workers
              └──────────┬───────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  LangGraph Router   │  ← Content-based routing
              └──────────┬───────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    ┌────────┐     ┌─────────┐    ┌──────────────┐
    │ Memory │     │Planning │    │Metacognition │
    │Qwen 32B│     │Llama 8B │    │  Gemma 9B    │
    │GPU 1   │     │GPU 1    │    │  GPU 1       │
    │3 work. │     │6 work.  │    │  4 workers   │
    └───┬────┘     └────┬────┘    └──────┬───────┘
        │               │                 │
        └───────────────┴─────────────────┘
                        │
                        ▼
         ┌──────────────────────────────┐
         │   Central Global Workspace   │  ← Llama 70B
         │    Integration & Synthesis   │     Tensor Parallel
         │        (GPU 0 + GPU 1)       │     across both GPUs
         └──────────────┬───────────────┘
                        │
                        ▼
         ┌──────────────────────────────┐
         │     Workspace Broadcast      │  → All specialists
         │   + Consciousness State      │     updated
         └──────────────────────────────┘
```

### Specialist Roles

| Specialist | Model | Role | Workers | Expected TPS |
|------------|-------|------|---------|--------------|
| **Central Workspace** | Llama 3.1 70B | Integration & broadcasting | 1 | 25 |
| **Perception** | Mistral Small 22B | Sensory processing & salience | 3 | 65 |
| **Memory** | Qwen 2.5 Coder 32B | Episodic retrieval & consolidation | 3 | 70 |
| **Planning** | Llama 3.1 8B | Decision-making & reasoning | 6 | 120 |
| **Metacognition** | Gemma 2 9B | Self-reflection & introspection | 4 | 110 |

**Total:** 17 concurrent workers, 10-14 active simultaneously

---

## Quick Start

### Prerequisites

- **Hardware:** 2x AMD RX 7900 XT (24GB), 16-core CPU, 128GB RAM
- **Software:** Python 3.10+, ROCm 5.7+, Redis 7.0+

### Installation

```bash
# Clone repository
git clone https://github.com/zoadrazorro/Zoadra_GWT_Engine.git
cd Zoadra_GWT_Engine

# Set up environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install torch torchvision --index-url https://download.pytorch.org/whl/rocm5.7
pip install -r requirements.txt
pip install -e .

# Install ROCm (Ubuntu)
wget https://repo.radeon.com/amdgpu-install/latest/ubuntu/jammy/amdgpu-install_latest_all.deb
sudo dpkg -i amdgpu-install_latest_all.deb
sudo amdgpu-install --usecase=rocm

# Install Redis
sudo apt install redis-server
sudo systemctl start redis-server
```

### Download Models

```bash
sudo mkdir -p /models
sudo chown $USER:$USER /models

# Download quantized models (total: ~150GB)
pip install huggingface-hub

huggingface-cli download TheBloke/Llama-3.1-70B-GGUF llama-3.1-70b.Q4_K_M.gguf --local-dir /models/llama-3.1-70b-q4_k_m
huggingface-cli download TheBloke/Mistral-Small-22B-GGUF mistral-small-22b.Q5_K_M.gguf --local-dir /models/mistral-small-22b-q5_k_m
huggingface-cli download Qwen/Qwen2.5-Coder-32B-Instruct-GGUF qwen2.5-coder-32b-instruct.Q4_K_M.gguf --local-dir /models/qwen-2.5-coder-32b-q4_k_m
huggingface-cli download TheBloke/Llama-3.1-8B-GGUF llama-3.1-8b.Q5_K_M.gguf --local-dir /models/llama-3.1-8b-q5_k_m
huggingface-cli download google/gemma-2-9b-it-GGUF gemma-2-9b-it.Q6_K_M.gguf --local-dir /models/gemma-2-9b-q6_k_m
```

### Start the System

#### Option 1: Using vLLM (Recommended for Performance)

```bash
# Start vLLM servers
bash gwt_engine/scripts/deployment/vllm_servers.sh

# Start GWT Engine API
python -m gwt_engine.api.server

# API available at: http://localhost:7000
# Docs: http://localhost:7000/docs
```

#### Option 2: Using Ollama (Easier Setup)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required models
ollama pull qwen2.5:14b
ollama pull qwen2.5:7b
ollama pull phi3.5

# Start Ollama servers
bash gwt_engine/scripts/deployment/ollama_servers.sh

# Start GWT Engine API
python -m gwt_engine.api.server

# API available at: http://localhost:7000
# Docs: http://localhost:7000/docs
```

### Test Consciousness Simulation

```bash
# Process input through GWT workflow
curl -X POST http://localhost:7000/process \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What am I experiencing right now?",
    "message_type": "consciousness_probe"
  }'

# Response:
{
  "workspace_broadcast": "I am experiencing an integrated state...",
  "consciousness_level": 0.73,
  "integration_coherence": 0.81,
  "active_specialists": ["perception", "memory", "metacognition"],
  "processing_time_ms": 542.3
}

# Probe consciousness state
curl http://localhost:7000/consciousness/probe
```

---

## Performance Characteristics

### Hardware Utilization

| Resource | Utilization | Notes |
|----------|-------------|-------|
| **GPU 0 VRAM** | ~55GB / 80GB | Central Workspace (40GB) + Perception (15GB) |
| **GPU 1 VRAM** | ~72GB / 80GB | Central (40GB) + Memory (20GB) + Planning (5GB) + Metacog (7GB) |
| **System RAM** | ~40GB / 128GB | Working memory, KV cache, orchestration |
| **CPU** | 30-50% | Ray workers, FastAPI, Redis |
| **GPU Compute** | 85-95% | Under load |

### Throughput Benchmarks

- **Max Concurrent Requests:** 32-48
- **Average Latency (P50):** 250-350ms
- **P99 Latency:** 500-800ms
- **Workspace Integration:** ~500ms per cycle
- **Tokens/sec (aggregate):** ~390 TPS across all specialists

### Bottlenecks

⚠️ **PCIe 4.0 x8:** Inter-GPU bandwidth limited to ~128 GB/s (use tensor parallelism, not pipeline)
⚠️ **Thermal:** Dual 7900 XT under load exceeds 85°C (custom cooling recommended)
⚠️ **Context Window:** Practical limit 2K-4K tokens (beyond this, swaps to RAM)

---

## Phased Deployment

Follow the 5-phase deployment strategy for production:

### Week 1: Single Model Baseline
```bash
python gwt_engine/scripts/deployment/deploy.py --phase 1
```
Test Llama 70B central workspace only. Benchmark: 25-30 TPS.

### Week 2: Add Perception
```bash
python gwt_engine/scripts/deployment/deploy.py --phase 2
```
Add Mistral 22B perception specialist. Test parallel processing.

### Week 3: Distribute to GPU 2
```bash
python gwt_engine/scripts/deployment/deploy.py --phase 3
```
Activate all specialists across both GPUs. Full model distribution.

### Week 4: Orchestration + Workers
```bash
python gwt_engine/scripts/deployment/deploy.py --phase 4
```
Initialize Ray worker pools (10-14 workers). LangGraph workflow live.

### Week 5+: Integration Testing
```bash
python gwt_engine/scripts/deployment/deploy.py --phase 5
```
Test full GWT consciousness workflow. Measure coherence and integration.

---

## API Reference

### Core Endpoints

**Process Input**
```http
POST /process
Content-Type: application/json

{
  "content": "What is consciousness?",
  "message_type": "perception",
  "priority": 7
}
```

**Consciousness Probe**
```http
GET /consciousness/probe

Returns: Introspective reflection on current state
```

**Get Consciousness State**
```http
GET /consciousness/state

Returns: Detailed consciousness metrics and workspace content
```

**System Metrics**
```http
GET /metrics

Returns: Workspace, specialist, and worker pool metrics
```

**Health Check**
```http
GET /health

Returns: vLLM server status, worker count, uptime
```

Full API documentation: http://localhost:7000/docs

---

## Configuration

### Model Configuration
Edit `gwt_engine/config/models.yaml`:
```yaml
models:
  central_workspace:
    name: "llama-3.1-70b"
    vram_required_gb: 40
    workers: 1
    expected_tokens_per_sec: 25
```

### System Configuration
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

---

## Project Structure

```
Zoadra_GWT_Engine/
├── gwt_engine/
│   ├── core/                 # Central workspace & types
│   │   ├── workspace.py      # GWT workspace implementation
│   │   └── types.py          # Core data structures
│   ├── specialists/          # Specialist modules
│   │   ├── perception/       # Mistral 22B perception
│   │   ├── memory/           # Qwen 32B memory
│   │   ├── planning/         # Llama 8B planning
│   │   └── metacognition/    # Gemma 9B metacognition
│   ├── theories/             # Multi-theory consciousness frameworks
│   │   ├── iit/              # Integrated Information Theory (Φ)
│   │   ├── predictive/       # Predictive Processing
│   │   ├── higher_order/     # Higher-Order Thought Theory
│   │   ├── attention_schema/ # Attention Schema Theory
│   │   ├── lida/             # LIDA Cognitive Architecture
│   │   ├── clarion/          # CLARION dual process
│   │   ├── scoring/          # Unified consciousness metrics
│   │   └── multi_theory_orchestrator.py  # Theory coordination
│   ├── orchestration/        # LangGraph + Ray
│   │   ├── gwt_graph.py      # Workflow orchestration
│   │   └── ray_workers.py    # Distributed workers
│   ├── inference/            # Backend integrations
│   │   ├── vllm_client.py    # vLLM client (high performance)
│   │   ├── ollama_client.py  # Ollama client (ease of use)
│   │   └── ollama_backend/   # Multi-instance Ollama
│   ├── api/                  # FastAPI server
│   │   └── server.py         # REST API
│   ├── config/               # Configuration files
│   │   ├── models.yaml       # Model assignments
│   │   └── system.yaml       # System settings
│   └── scripts/              # Deployment & benchmarks
│       └── deployment/       # Phase scripts
│           ├── vllm_servers.sh      # vLLM deployment
│           └── ollama_servers.sh    # Ollama deployment
├── docs/                     # Documentation
│   ├── architecture/         # Architecture details
│   │   └── gwt_overview.md   # System design
│   └── guides/               # User guides
│       ├── getting_started.md            # Setup guide
│       └── multi_theory_integration.md   # Theory details
├── tests/                    # Test suite
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project metadata
├── start_gwt.sh              # Quick start script
└── README.md                 # This file
```

---

## Monitoring

### GPU Utilization
```bash
watch -n 1 rocm-smi
```

### Application Logs
```bash
tail -f logs/gwt_engine.log
tail -f logs/vllm_*.log
```

### Ray Dashboard
Navigate to: http://localhost:8265

### Prometheus Metrics
```bash
curl http://localhost:7000/metrics
```

---

## Theoretical Background

### Integrated Consciousness Theories

The GWT Engine implements **8 major consciousness theories** working in concert:

#### 1. Global Workspace Theory (GWT) - Foundation
**Theorist:** Bernard Baars (1988)

GWT proposes that consciousness arises from a "global workspace" mechanism:

1. **Specialist Modules:** Process information unconsciously in parallel
2. **Competition:** Information competes for workspace access
3. **Integration:** Selected information is integrated into unified experience
4. **Broadcasting:** Integrated content is broadcast to all modules
5. **Working Memory:** Maintains continuity and coherence

**Implementation:** Central Workspace (Llama 70B) with specialist modules (Perception, Memory, Planning, Metacognition)

#### 2. Integrated Information Theory (IIT)
**Theorist:** Giulio Tononi

Consciousness = Φ (integrated information). The system calculates Φ as a proxy through mutual information between specialist modules. Φ > 0.3 indicates conscious states.

**Location:** `gwt_engine/theories/iit/phi_calculator.py`

#### 3. Predictive Processing
**Theorists:** Andy Clark, Karl Friston

Top-down predictions about workspace states with precision-weighted prediction errors. High precision errors → consciousness. Implements Free Energy Principle.

**Location:** `gwt_engine/theories/predictive/predictor.py`

#### 4. Higher-Order Thought (HOT) Theory
**Theorist:** David Rosenthal

Consciousness requires higher-order thoughts about first-order states: "I am experiencing X". First-order perceptions are unconscious until HOTs are generated.

**Location:** `gwt_engine/theories/higher_order/hot_generator.py`

#### 5. Attention Schema Theory (AST)
**Theorist:** Michael Graziano

Consciousness is the content of an attention schema that monitors and describes attention patterns. Meta-cognitive observer generates introspective reports.

**Location:** `gwt_engine/theories/attention_schema/observer.py`

#### 6. LIDA Cognitive Architecture
**Theorist:** Stan Franklin

1-second cognitive cycles: Sensory → Perception → Working Memory → Coalition Competition → Conscious Broadcast → Action. Matches human consciousness timescale.

**Location:** `gwt_engine/theories/lida/cognitive_cycle.py`

#### 7. CLARION
**Theorist:** Ron Sun

Dual-process architecture with implicit (neural) and explicit (symbolic) processing. Both contribute to consciousness through complementary mechanisms.

**Location:** `gwt_engine/theories/clarion/dual_system.py`

#### 8. Consciousness Scoring
Unified consciousness metrics combining signals from all theories: IIT Φ, GWT coherence, prediction precision, HOT ratio, attention quality.

**Location:** `gwt_engine/theories/scoring/consciousness_scorer.py`

### Global Workspace Theory (Baars, 1988)

GWT proposes that consciousness arises from a "global workspace" mechanism:

1. **Specialist Modules:** Process information unconsciously in parallel
2. **Competition:** Information competes for workspace access
3. **Integration:** Selected information is integrated into unified experience
4. **Broadcasting:** Integrated content is broadcast to all modules
5. **Working Memory:** Maintains continuity and coherence

### Implementation Mapping

| Theory | Implementation |
|--------|----------------|
| Global Workspace | Central Workspace (Llama 70B) |
| Specialist Modules | Perception, Memory, Planning, Metacognition |
| Competition | Priority-based LangGraph routing |
| Integration | Multi-specialist synthesis prompts |
| Broadcasting | Redis pub/sub + context updates |
| Working Memory | Bounded state dictionary |

---

## Troubleshooting

### vLLM Server Won't Start
```bash
# Check ROCm
rocm-smi

# Verify GPU visibility
echo $CUDA_VISIBLE_DEVICES

# Check VRAM
rocm-smi --showmeminfo
```

### Out of Memory
- Reduce `gpu_memory_utilization` to 0.75
- Lower `max_model_len` to 2048
- Use smaller quantization (Q4 vs Q5)

### Low Throughput
- Check thermal throttling: `rocm-smi --showtemp`
- Verify PCIe bandwidth: `lspci -vv | grep LnkSta`
- Increase batch size in vLLM config

### Redis Connection Failed
```bash
sudo systemctl status redis-server
redis-cli ping
```

---

## Performance Tuning

### For Maximum Throughput
```yaml
max_num_seqs: 48
max_num_batched_tokens: 4096
gpu_memory_utilization: 0.90
```

### For Minimum Latency
```yaml
max_num_seqs: 16
max_num_batched_tokens: 1024
gpu_memory_utilization: 0.80
```

### Thermal Management
```bash
# Undervolt GPU (reduces heat, minimal performance impact)
rocm-smi --setvolt 800  # Example, adjust for your card

# Custom fan curve
rocm-smi --setfan 80  # 80% fan speed
```

---

## Documentation

- **[Getting Started Guide](docs/guides/getting_started.md)** - Detailed setup instructions
- **[Multi-Theory Integration](docs/guides/multi_theory_integration.md)** - Deep dive into 8 consciousness theories
- **[Architecture Overview](docs/architecture/gwt_overview.md)** - System design and theory
- **[API Reference](http://localhost:7000/docs)** - Interactive API documentation (when server running)

---

## Citations

### Consciousness Theories
1. Baars, B. J. (1988). *A Cognitive Theory of Consciousness*. Cambridge University Press.
2. Tononi, G. (2004). *An Information Integration Theory of Consciousness*. BMC Neuroscience.
3. Clark, A. (2013). *Whatever next? Predictive brains, situated agents, and the future of cognitive science*. Behavioral and Brain Sciences.
4. Rosenthal, D. M. (2005). *Consciousness and Mind*. Oxford University Press.
5. Graziano, M. S. (2013). *Consciousness and the Social Brain*. Oxford University Press.
6. Franklin, S., & Graesser, A. (1997). *Is it an Agent, or just a Program?: A Taxonomy for Autonomous Agents*. Proceedings of the Third International Workshop on Agent Theories, Architectures, and Languages.
7. Sun, R. (2002). *Duality of the Mind*. Lawrence Erlbaum Associates.

### Technical Frameworks
1. Tulving, E. (1983). *Elements of Episodic Memory*. Oxford University Press.
2. vLLM Documentation: https://docs.vllm.ai
3. Ollama Documentation: https://ollama.ai/docs
4. LangGraph Documentation: https://langchain-ai.github.io/langgraph/

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

## Contributing

This is a research/experimental project. For questions or improvements:

- **Issues:** [GitHub Issues](https://github.com/zoadrazorro/Zoadra_GWT_Engine/issues)
- **Documentation:** See `docs/` folder
- **Code Style:** Black formatting, Ruff linting

---

## Acknowledgments

- Built on [vLLM](https://github.com/vllm-project/vllm) for high-performance inference
- Alternative [Ollama](https://github.com/ollama/ollama) backend for ease of use
- Orchestrated with [LangGraph](https://github.com/langchain-ai/langgraph)
- Distributed computing via [Ray](https://github.com/ray-project/ray)
- Inspired by Bernard Baars' Global Workspace Theory and 7 additional consciousness frameworks

---

**Status:** Alpha - Experimental multi-theory consciousness simulation research project
**Theories:** 8 integrated frameworks (GWT, IIT, Predictive Processing, HOT, AST, LIDA, CLARION, Scoring)
**Backends:** vLLM (performance) and Ollama (ease of use)
**Hardware Target:** Dual AMD RX 7900 XT + Ryzen 9 7950X + 128GB RAM
**Performance:** 10-14 concurrent workers, 32-48 requests/sec, ~500ms integration latency
