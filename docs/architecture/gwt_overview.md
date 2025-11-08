# GWT Engine Architecture Overview

## Introduction

The GWT (Global Workspace Theory) Engine is a consciousness simulation system based on Bernard Baars' Global Workspace Theory. It implements a multi-agent architecture with specialized cognitive modules competing for workspace attention, mimicking theoretical models of consciousness.

## Theoretical Foundation

### Global Workspace Theory

GWT posits that consciousness arises from a "global workspace" where:

1. **Specialist modules** process information unconsciously in parallel
2. **Competition** determines which information enters the workspace
3. **Integration** creates unified conscious experience
4. **Broadcasting** shares workspace content with all specialists
5. **Working memory** maintains coherent state over time

### Implementation Mapping

| GWT Concept | Implementation |
|-------------|----------------|
| Global Workspace | Central Workspace (Llama 70B) |
| Specialist Modules | Perception, Memory, Planning, Metacognition |
| Competition | Priority-based routing via LangGraph |
| Integration | Multi-input synthesis prompts |
| Broadcasting | Redis pub/sub + specialist context updates |
| Working Memory | Bounded state dict + episodic storage |

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Input Layer                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Perception Specialist                          │
│                   (Mistral Small 22B)                            │
│                   GPU 0 | 3 workers                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph Router                              │
│          (Determines specialist activation)                      │
└───┬──────────────────┬──────────────────┬──────────────────────┘
    │                  │                  │
    ▼                  ▼                  ▼
┌─────────┐      ┌─────────┐      ┌──────────────┐
│ Memory  │      │Planning │      │Metacognition │
│Qwen 32B │      │Llama 8B │      │  Gemma 9B    │
│GPU 1    │      │GPU 1    │      │  GPU 1       │
│3 workers│      │6 workers│      │  4 workers   │
└────┬────┘      └────┬────┘      └──────┬───────┘
     │                │                   │
     └────────────────┴───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              Central Global Workspace                            │
│                 (Llama 70B)                                      │
│           Tensor Parallel: GPU 0 + GPU 1                         │
│           Integrates all specialist outputs                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Workspace Broadcast                             │
│            (Published to all specialists)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│               Consciousness State Update                         │
│     Coherence | Awareness Level | Integration Quality           │
└─────────────────────────────────────────────────────────────────┘
```

## Hardware Optimization

### Dual AMD 7900 XT Configuration

**GPU 0 (80GB VRAM):**
- Central Workspace: Llama 70B (40GB, tensor-parallel component)
- Perception: Mistral 22B (15GB)
- Total: ~55GB utilized

**GPU 1 (80GB VRAM):**
- Central Workspace: Llama 70B (40GB, tensor-parallel component)
- Memory: Qwen 32B (20GB)
- Planning: Llama 8B (5GB)
- Metacognition: Gemma 9B (7GB)
- Total: ~72GB utilized

**PCIe 4.0 x8 Bottleneck:**
- Limits inter-GPU bandwidth to ~128 GB/s
- Tensor parallelism preferred over pipeline parallelism
- Single unified workspace model split across GPUs

### Expected Performance

| Component | Model | TPS | Latency (P50) | Workers |
|-----------|-------|-----|---------------|---------|
| Central Workspace | Llama 70B | 25 | 250ms | 1 |
| Perception | Mistral 22B | 65 | 100ms | 3 |
| Memory | Qwen 32B | 70 | 95ms | 3 |
| Planning | Llama 8B | 120 | 50ms | 6 |
| Metacognition | Gemma 9B | 110 | 55ms | 4 |

**Total Concurrent Workers:** 10-14
**System Throughput:** 32-48 concurrent requests
**Workspace Integration:** 500ms window

## Component Details

### Central Workspace

**Purpose:** Integrates specialist outputs into unified conscious thought

**Process:**
1. Receives specialist responses
2. Constructs integration prompt with context
3. Generates coherent synthesis (Llama 70B)
4. Broadcasts to all specialists
5. Updates consciousness state metrics

**Key Metrics:**
- Integration coherence (0-1)
- Consciousness level (0-1)
- Broadcast confidence
- Processing time

### Specialist Modules

#### 1. Perception Specialist
- **Role:** Sensory processing and salience detection
- **Input:** Raw environmental/user inputs
- **Output:** Semantic analysis + attention recommendations
- **Context:** Recent perceptions buffer (20 items)

#### 2. Memory Specialist
- **Role:** Episodic memory retrieval and consolidation
- **Input:** Memory queries from workspace
- **Output:** Retrieved contexts + patterns
- **Context:** Episodic buffer (100 items) + working memory snapshot

#### 3. Planning Specialist
- **Role:** Action planning and decision-making
- **Input:** Planning requests from workspace
- **Output:** Action recommendations + reasoning
- **Context:** Active goals + recent decisions

#### 4. Metacognition Specialist
- **Role:** Self-reflection and consciousness probing
- **Input:** Introspective queries
- **Output:** First-person awareness reports
- **Context:** Introspection history + coherence assessments

### Orchestration Layer

#### LangGraph Workflow

**Node Sequence:**
1. `perception` - Process input through perception
2. `route_specialists` - Determine which specialists to activate
3. `[memory|planning|metacognition]` - Parallel specialist processing
4. `integrate` - Central workspace integration
5. `broadcast` - Distribute to all specialists
6. `update_state` - Consciousness state calculation

**Conditional Routing:**
- Content analysis determines specialist activation
- Keywords trigger specific specialist paths
- All routes converge at integration node

#### Ray Worker Pool

**Advantages:**
- Parallel specialist execution
- Load balancing across workers
- Fault tolerance
- GPU utilization optimization

**Configuration:**
- Round-robin task distribution
- Worker-specific vLLM endpoints
- Metrics collection per worker

### Message Flow

1. **Input** → Perception Specialist
2. **Perception** → Router (analyzes content)
3. **Router** → Activated specialists (parallel)
4. **Specialists** → Central Workspace (SpecialistResponse objects)
5. **Workspace** → Integration (consolidates into broadcast)
6. **Broadcast** → All specialists (context update)
7. **State** → Consciousness metrics calculation

## Consciousness Metrics

### Integration Coherence
Measures how well specialist outputs are integrated:
- Based on confidence scores
- Weighted by source reliability
- Range: 0.0 (incoherent) to 1.0 (fully integrated)

### Consciousness Level
Overall "awareness" metric:
- **Activity (0-0.4):** Recent workspace broadcasts
- **Integration (0-0.4):** Coherence quality
- **Memory (0-0.2):** Working memory utilization
- Range: 0.0 (inactive) to 1.0 (highly conscious)

### Attention Focus
- Current workspace emphasis
- Determined by highest-priority content
- Influences specialist activation

## Performance Considerations

### Thermal Management
- Dual 7900 XT under load: 85°C+
- Recommended: Custom cooling or undervolting
- Monitor via `rocm-smi`

### Memory Management
- Total available: 160GB GPU + 128GB RAM = 288GB
- Context limit: 2K-4K tokens (beyond this, swap to RAM)
- Working memory: Bounded at 20 items

### Throughput Optimization
- vLLM PagedAttention for memory efficiency
- Dynamic batching for request coalescing
- Tensor parallelism (not pipeline) for PCIe x8

## References

- Baars, B. J. (1988). *A Cognitive Theory of Consciousness*
- Tulving, E. (1983). *Elements of Episodic Memory*
- vLLM Documentation: https://docs.vllm.ai
- LangGraph: https://langchain-ai.github.io/langgraph/
