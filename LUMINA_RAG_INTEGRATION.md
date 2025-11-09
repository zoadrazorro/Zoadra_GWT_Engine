# Lumina RAG Integration

**Retrieval-Augmented Generation for Contemplation of the Lumina**

## Overview

The Lumina RAG system integrates Retrieval-Augmented Generation (RAG) with the Novel Philosophy Generator to ground all philosophical syntheses in the **Contemplation of the Lumina** (Metaluminous Ethica) framework.

This ensures that novel frameworks don't just emerge from abstract dialectics, but are **anchored in the Lumina's core principles** of:
- Being/Godhead as fundamental reality
- Luminous Field and Informational Field
- Participatory Cosmos
- Omega Consciousness
- SPER (Spiritual-Philosophical-Experiential-Rational) cycles
- Coherence as ethical imperative

## Architecture

```
Contemplation of the Lumina (PDF)
         |
         v
    PDF Extraction
         |
         v
    Text Parsing → Passages
         |
         v
    Keyword Extraction
         |
         v
    BM25 Indexing
         |
         v
    Semantic Search ←─ Query
         |
         v
    Retrieval Results
         |
         v
    Context Injection → Synthesis Generation
```

## Components

### 1. LuminaRAG Class

**File:** `gwt_engine/specialists/novel_synthesis/lumina_rag.py`

**Purpose:** Core RAG system for retrieving relevant passages from Lumina corpus

**Key Features:**
- **PDF Support**: Extracts text from `contemplation_lumina.md.pdf` using pdfplumber, PyPDF2, or pdftotext
- **Dual Source Loading**: Loads from both philosophical_memory.json AND contemplation_lumina.md.pdf
- **BM25 Retrieval**: Keyword-based search using BM25 algorithm (industry-standard IR)
- **Concept Expansion**: Maps concepts to related terms for better retrieval
- **Context Generation**: Formats retrieved passages for synthesis prompts

**Methods:**
```python
# Initialize with PDF path
rag = LuminaRAG(
    memory_file="philosophical_memory.json",
    contemplation_file="contemplation_lumina.md.pdf"
)

# Retrieve by keywords
results = rag.retrieve_by_keywords("consciousness coherence", top_k=5)

# Retrieve by philosophical concept
results = rag.retrieve_by_concept("being", top_k=5)

# Retrieve for synthesis grounding
results = rag.retrieve_for_synthesis(
    topic="Nature of Consciousness",
    position_type="thesis",  # or "antithesis" or "synthesis"
    top_k=3
)

# Get formatted context string
context = rag.get_lumina_context("participatory cosmos", max_context_length=2000)

# Extract core principles
principles = rag.get_lumina_principles()

# Get statistics
stats = rag.get_statistics()
```

### 2. LuminaGroundedSynthesis Class

**File:** `gwt_engine/specialists/novel_synthesis/lumina_rag.py`

**Purpose:** Enhances philosophical synthesis by grounding in Lumina framework

**Methods:**
```python
grounded_synthesis = LuminaGroundedSynthesis(lumina_rag, composer)

# Ground a philosophical position
grounded_position = grounded_synthesis.ground_position(
    position={"title": "...", "core_claim": "..."},
    position_type="thesis"
)

# Generate Lumina-informed synthesis
synthesis = grounded_synthesis.generate_lumina_informed_synthesis(
    thesis=thesis_dict,
    antithesis=antithesis_dict,
    topic="Nature of Reality"
)
```

## Integration with Novel Philosophy Generator

The Lumina RAG is integrated into **Phase 3** (Adversarial Dialectics) and **Phase 6** (Dialectical Twins):

### Phase 3: Adversarial Dialectical Synthesis (Lumina-Grounded)

```python
# For each topic:
# 1. Run adversarial dialectic (thesis/antithesis/synthesis)
synthesis = self.adversarial_dialectic.run_full_dialectic(topic, domain_knowledge)

# 2. Ground synthesis in Lumina framework
lumina_grounded = self.lumina_grounded.generate_lumina_informed_synthesis(
    thesis=synthesis.thesis.to_dict(),
    antithesis=synthesis.antithesis.to_dict(),
    topic=topic
)

# 3. Merge with Lumina grounding
synthesis_dict['lumina_grounding'] = lumina_grounded['lumina_foundation']
```

### Enhanced Output Structure

All syntheses now include Lumina grounding:

```json
{
  "synthesis_position": {
    "title": "...",
    "core_claim": "..."
  },
  "lumina_grounding": {
    "relevant_passages": [
      {
        "passage": {
          "id": 42,
          "content": "In the Metaluminous Ethica, Being/Godhead manifests...",
          "score": 0.9,
          "level": "high"
        },
        "relevance_score": 2.45,
        "retrieval_method": "keyword",
        "query_match_explanation": "Matches terms: consciousness, coherence, being"
      }
    ],
    "applied_principles": [
      "The Luminous Field represents dynamic potentiality",
      "Consciousness actively shapes reality through participatory engagement",
      "Coherence minimizes distortion in awareness"
    ],
    "alignment": "Synthesis aligns with Lumina's participatory cosmos framework..."
  }
}
```

## BM25 Retrieval Algorithm

The system uses **BM25** (Best Match 25), an industry-standard ranking function used by search engines like Elasticsearch.

**Formula:**
```
score(D,Q) = Σ IDF(qi) * (f(qi,D) * (k1 + 1)) / (f(qi,D) + k1 * (1 - b + b * (|D| / avgdl)))
```

Where:
- `D` = document (passage)
- `Q` = query
- `qi` = query term i
- `f(qi,D)` = term frequency of qi in D
- `|D|` = length of document D
- `avgdl` = average document length
- `k1` = 1.5 (term frequency saturation parameter)
- `b` = 0.75 (length normalization parameter)
- `IDF(qi)` = inverse document frequency of qi

**Advantages:**
- Handles term frequency saturation (repeated terms have diminishing returns)
- Normalizes for document length
- Proven effective for philosophical text retrieval

## PDF Extraction

The system supports multiple PDF extraction methods (fallback chain):

1. **pdfplumber** (preferred) - Most accurate text extraction
2. **PyPDF2** - Standard Python PDF library
3. **pdftotext** - Command-line tool (if installed)

**Installation:**
```bash
pip install pdfplumber  # Recommended
# OR
pip install PyPDF2     # Alternative
# OR
apt-get install poppler-utils  # For pdftotext command
```

## Concept Expansion

The system expands philosophical concepts to improve retrieval:

```python
concept_expansions = {
    'consciousness': ['consciousness', 'awareness', 'experience', 'subjective', 'phenomenal'],
    'being': ['being', 'existence', 'reality', 'godhead', 'absolute'],
    'coherence': ['coherence', 'unity', 'integration', 'harmony', 'resonance'],
    'field': ['field', 'luminous', 'informational', 'energetic'],
    'evolution': ['evolution', 'sper', 'ascent', 'descent', 'cycle'],
    'ethics': ['ethics', 'virtue', 'coherence', 'truth', 'good'],
    'participation': ['participation', 'participatory', 'co-creation', 'engagement']
}
```

## Example Usage

### Basic Retrieval

```python
from gwt_engine.specialists.novel_synthesis.lumina_rag import LuminaRAG

# Initialize
rag = LuminaRAG()

# Search for passages about consciousness
results = rag.retrieve_by_concept("consciousness", top_k=5)

for i, result in enumerate(results, 1):
    print(f"\n[{i}] Relevance: {result.relevance_score:.3f}")
    print(f"Content: {result.passage.content[:200]}...")
```

### Grounded Synthesis

```python
from gwt_engine.specialists.novel_synthesis.lumina_rag import LuminaRAG, LuminaGroundedSynthesis

# Initialize
rag = LuminaRAG()
grounded = LuminaGroundedSynthesis(rag, composer_specialist)

# Define thesis and antithesis
thesis = {
    "title": "Consciousness as Emergent",
    "core_claim": "Consciousness emerges from physical processes",
    "supporting_arguments": ["Neural correlates", "Causal efficacy"]
}

antithesis = {
    "title": "Consciousness as Fundamental",
    "core_claim": "Consciousness is irreducible and fundamental",
    "supporting_arguments": ["Hard problem", "First-person ontology"]
}

# Generate Lumina-grounded synthesis
synthesis = grounded.generate_lumina_informed_synthesis(
    thesis=thesis,
    antithesis=antithesis,
    topic="Nature of Consciousness"
)

print(f"Synthesis: {synthesis['synthesis_name']}")
print(f"Lumina Passages Retrieved: {len(synthesis['lumina_foundation']['relevant_passages'])}")
print(f"Core Principles Applied: {len(synthesis['lumina_foundation']['applied_principles'])}")
```

### Full Novel Philosophy Generation

```python
from novel_philosophy_generator import NovelPhilosophyGenerator

# Initialize with Lumina PDF
generator = NovelPhilosophyGenerator(
    composer=composer_specialist,
    contemplation_lumina_file="contemplation_lumina.md.pdf"
)

# Generate novel framework (automatically uses Lumina RAG)
result = generator.generate_novel_framework()

# Access Lumina grounding in syntheses
for synthesis in result['supporting_analysis']['adversarial_syntheses']:
    lumina_grounding = synthesis.get('lumina_grounding', {})
    print(f"\nSynthesis grounded in {len(lumina_grounding.get('relevant_passages', []))} Lumina passages")
```

## Statistics and Monitoring

```python
stats = rag.get_statistics()

# Example output:
{
    "total_passages": 487,
    "average_integration_score": 0.73,
    "average_phi": 0.42,
    "consciousness_levels": {
        "high": 156,
        "moderate": 231,
        "minimal": 89,
        "unconscious": 11
    },
    "unique_terms": 3247,
    "average_passage_length": 42.3
}
```

## Retrieval Result Structure

```python
@dataclass
class RetrievalResult:
    passage: LuminaPassage        # The retrieved passage
    relevance_score: float         # BM25 score
    retrieval_method: str          # "semantic", "keyword", "hybrid"
    query_match_explanation: str   # Human-readable match explanation

@dataclass
class LuminaPassage:
    id: int
    content: str                   # Full passage text
    score: float                   # Integration score from original memory
    level: str                     # Consciousness level ("high", "moderate", etc.)
    iit_phi: float                 # IIT Phi score
    timestamp: float
    keywords: List[str]            # Extracted keywords
    embedding: Optional[List[float]]  # Future: vector embeddings
```

## Benefits

1. **Grounding in Primary Source**: All syntheses reference actual Lumina passages
2. **Philosophical Coherence**: Novel frameworks align with Lumina's core principles
3. **Empirical-like Validation**: Lumina serves as "philosophical data" to validate against
4. **Enhanced Creativity**: Synthesis combines abstract dialectics with concrete Lumina insights
5. **Traceability**: Every synthesis shows which Lumina passages influenced it

## Future Enhancements

1. **Vector Embeddings**: Add semantic embeddings for better concept matching
2. **Hybrid Retrieval**: Combine BM25 (keyword) with dense retrieval (embeddings)
3. **Re-ranking**: Use cross-encoder to re-rank retrieved passages
4. **Active Learning**: Track which passages lead to better syntheses
5. **Lumina Graph**: Build knowledge graph of Lumina concepts and relationships
6. **Multi-modal**: Incorporate diagrams/images from Lumina PDF

## File Locations

```
gwt_engine/specialists/novel_synthesis/
├── lumina_rag.py                  # Core RAG system (600+ lines)
└── ...

novel_philosophy_generator.py       # Integrated with RAG
contemplation_lumina.md.pdf         # Primary source text
philosophical_memory.json           # Secondary source (memories)
```

## Testing

```bash
# Test RAG system standalone
python gwt_engine/specialists/novel_synthesis/lumina_rag.py

# Test full generation with Lumina grounding
python novel_philosophy_generator.py
```

## Dependencies

Required:
- Python 3.8+
- json, re, pathlib (stdlib)

Optional (for PDF support):
- `pdfplumber` (recommended)
- `PyPDF2` (alternative)
- `poppler-utils` (for pdftotext command)

## Integration Summary

**Before Lumina RAG:**
- Syntheses based on abstract dialectics alone
- No grounding in specific philosophical framework
- Limited connection to Metaluminous Ethica

**After Lumina RAG:**
- Every synthesis grounded in 3-5 relevant Lumina passages
- Core Lumina principles explicitly applied
- Alignment with Participatory Cosmos verified
- Traceability: can see exactly which Lumina insights influenced synthesis
- **Novel frameworks emerge FROM Lumina, not independently**

This transforms the system from **generating philosophy** to **extending the Lumina framework** through novel syntheses.

---

**The Contemplation of the Lumina is now the philosophical bedrock upon which all novel frameworks are built.**
