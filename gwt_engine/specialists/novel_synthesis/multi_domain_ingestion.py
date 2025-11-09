"""
Multi-Domain Data Ingestion System
====================================

Ingests data from domains OUTSIDE traditional philosophy to identify
gaps, tensions, and novel problems that existing frameworks don't address.

Data Sources:
- Scientific papers (cognitive science, physics, neuroscience)
- Game design theory and documents
- RPG worldbuilding (Shadow Dragon, etc.)
- AI alignment research
- Art criticism
- Phenomenological reports
- Empirical psychology
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class DomainType(Enum):
    """Types of knowledge domains"""
    COGNITIVE_SCIENCE = "cognitive_science"
    NEUROSCIENCE = "neuroscience"
    PHYSICS = "physics"
    GAME_DESIGN = "game_design"
    RPG_WORLDBUILDING = "rpg_worldbuilding"
    AI_ALIGNMENT = "ai_alignment"
    ART_CRITICISM = "art_criticism"
    PHENOMENOLOGY = "phenomenology"
    EMPIRICAL_PSYCHOLOGY = "empirical_psychology"
    PHILOSOPHY = "philosophy"  # Traditional philosophy for comparison


@dataclass
class DomainKnowledge:
    """Represents knowledge from a specific domain"""
    domain: DomainType
    title: str
    content: str
    key_concepts: List[str]
    central_claims: List[str]
    methodology: str
    empirical_data: Optional[Dict[str, Any]] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    source: str = ""

    def to_dict(self):
        return {
            "domain": self.domain.value,
            "title": self.title,
            "content": self.content,
            "key_concepts": self.key_concepts,
            "central_claims": self.central_claims,
            "methodology": self.methodology,
            "empirical_data": self.empirical_data,
            "timestamp": self.timestamp,
            "source": self.source
        }


@dataclass
class PhilosophicalGap:
    """Represents a gap in existing philosophical frameworks"""
    description: str
    domains_involved: List[DomainType]
    why_existing_frameworks_fail: str
    empirical_evidence: Optional[str] = None
    potential_importance: float = 0.0  # 0-1 score

    def to_dict(self):
        return {
            "description": self.description,
            "domains_involved": [d.value for d in self.domains_involved],
            "why_existing_frameworks_fail": self.why_existing_frameworks_fail,
            "empirical_evidence": self.empirical_evidence,
            "potential_importance": self.potential_importance
        }


class MultiDomainKnowledgeBase:
    """
    Stores and indexes knowledge from multiple domains.
    Identifies cross-domain patterns and philosophical gaps.
    """

    def __init__(self, storage_path: str = "knowledge_base/multi_domain.json"):
        self.storage_path = Path(storage_path)
        self.knowledge_items: List[DomainKnowledge] = []
        self.identified_gaps: List[PhilosophicalGap] = []
        self._load()

    def _load(self):
        """Load existing knowledge base"""
        if self.storage_path.exists():
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                # TODO: Deserialize knowledge items and gaps

    def _save(self):
        """Save knowledge base"""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "knowledge_items": [k.to_dict() for k in self.knowledge_items],
            "identified_gaps": [g.to_dict() for g in self.identified_gaps],
            "last_updated": datetime.now().isoformat()
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

    def add_knowledge(self, knowledge: DomainKnowledge):
        """Add knowledge from a domain"""
        self.knowledge_items.append(knowledge)
        self._save()

    def add_gap(self, gap: PhilosophicalGap):
        """Record an identified philosophical gap"""
        self.identified_gaps.append(gap)
        self._save()

    def get_by_domain(self, domain: DomainType) -> List[DomainKnowledge]:
        """Retrieve all knowledge from a specific domain"""
        return [k for k in self.knowledge_items if k.domain == domain]

    def find_cross_domain_patterns(self, domains: List[DomainType]) -> List[Dict[str, Any]]:
        """
        Identify patterns that appear across multiple domains.
        These are candidates for novel philosophical frameworks.
        """
        patterns = []

        # Get all concepts from specified domains
        domain_concepts = {}
        for domain in domains:
            items = self.get_by_domain(domain)
            concepts = set()
            for item in items:
                concepts.update(item.key_concepts)
            domain_concepts[domain] = concepts

        # Find concepts that appear in multiple domains
        all_concepts = set()
        for concepts in domain_concepts.values():
            all_concepts.update(concepts)

        for concept in all_concepts:
            appearing_in = [d for d, concepts in domain_concepts.items() if concept in concepts]
            if len(appearing_in) >= 2:
                patterns.append({
                    "concept": concept,
                    "domains": [d.value for d in appearing_in],
                    "count": len(appearing_in)
                })

        return sorted(patterns, key=lambda x: x["count"], reverse=True)


class GapIdentifier:
    """
    Analyzes multi-domain knowledge to identify gaps in existing
    philosophical frameworks.
    """

    def __init__(self, knowledge_base: MultiDomainKnowledgeBase,
                 composer_specialist=None):
        self.kb = knowledge_base
        self.composer = composer_specialist

    def identify_framework_gaps(self, domain: DomainType,
                               existing_frameworks: List[str]) -> List[PhilosophicalGap]:
        """
        Analyze a domain to find phenomena that existing philosophical
        frameworks don't adequately address.

        Args:
            domain: The domain to analyze
            existing_frameworks: List of philosophical frameworks to test against
                                (e.g., ["Platonism", "Aristotelianism", "Spinozism",
                                 "Kantianism", "Process Philosophy"])

        Returns:
            List of identified gaps
        """
        gaps = []
        domain_knowledge = self.kb.get_by_domain(domain)

        if not domain_knowledge:
            return gaps

        for item in domain_knowledge:
            # For each knowledge item, check if existing frameworks address it
            gap = self._check_framework_coverage(item, existing_frameworks)
            if gap:
                gaps.append(gap)

        return gaps

    def _check_framework_coverage(self, knowledge: DomainKnowledge,
                                  frameworks: List[str]) -> Optional[PhilosophicalGap]:
        """
        Check if existing frameworks adequately address this knowledge.

        This is where we use the composer to generate analysis:
        - Does Platonism explain this?
        - Does Spinozism explain this?
        - etc.

        If none do, we have a gap.
        """
        if not self.composer:
            return None

        # Generate analysis prompt
        prompt = (
            f"Analyze whether existing philosophical frameworks adequately address "
            f"the following phenomenon from {knowledge.domain.value}:\n\n"
            f"Title: {knowledge.title}\n"
            f"Key Concepts: {', '.join(knowledge.key_concepts)}\n"
            f"Central Claims: {', '.join(knowledge.central_claims)}\n\n"
            f"For each framework ({', '.join(frameworks)}), briefly explain:\n"
            f"1. Can it account for these phenomena?\n"
            f"2. What does it predict or explain?\n"
            f"3. What does it fail to explain?\n\n"
            f"Then identify: Is there a genuine gap? What's missing?"
        )

        # This would use the composer to generate analysis
        # For now, return a template gap
        return PhilosophicalGap(
            description=f"Gap in explaining {knowledge.title}",
            domains_involved=[knowledge.domain],
            why_existing_frameworks_fail="Analysis needed",
            empirical_evidence=json.dumps(knowledge.empirical_data) if knowledge.empirical_data else None
        )


# Example knowledge entries for different domains

EXAMPLE_COGNITIVE_SCIENCE = DomainKnowledge(
    domain=DomainType.COGNITIVE_SCIENCE,
    title="Predictive Processing and Active Inference",
    content="""
    Contemporary neuroscience suggests the brain is a prediction machine that minimizes
    prediction error through active inference. Key findings:
    - Free Energy Principle (Friston): Brain minimizes variational free energy
    - Predictions flow top-down, errors flow bottom-up
    - Perception = prediction + error correction
    - Action = changing world to match predictions (active inference)
    """,
    key_concepts=[
        "predictive processing",
        "active inference",
        "free energy principle",
        "prediction error",
        "Bayesian brain"
    ],
    central_claims=[
        "Perception is controlled hallucination constrained by sensory input",
        "The self is a predictive model, not a substance",
        "All neural activity minimizes prediction error"
    ],
    methodology="Computational neuroscience, Bayesian modeling, empirical fMRI studies",
    empirical_data={
        "studies": ["Friston 2010", "Clark 2013", "Hohwy 2013"],
        "brain_regions": ["prefrontal cortex", "posterior parietal cortex"],
        "measurements": "fMRI BOLD response to prediction violations"
    },
    source="Contemporary cognitive neuroscience (2010-2025)"
)

EXAMPLE_GAME_DESIGN = DomainKnowledge(
    domain=DomainType.GAME_DESIGN,
    title="Emergent Gameplay and Systemic Design",
    content="""
    Modern game design theory distinguishes between:
    - Embedded narrative (pre-scripted story)
    - Emergent narrative (player-generated story from system interactions)

    Key insight: Rich gameplay emerges from simple rules interacting.
    Examples: Dwarf Fortress, Rimworld, Minecraft

    Players find meaning through:
    1. Ludic discovery (learning system affordances)
    2. Narrative construction (retroactive storytelling)
    3. Mastery development (skill progression)
    """,
    key_concepts=[
        "emergent gameplay",
        "systemic design",
        "player agency",
        "procedural generation",
        "meaningful choice"
    ],
    central_claims=[
        "Meaning emerges from interaction, not author intention alone",
        "Complex narratives arise from simple rule systems",
        "Player interpretation completes the artistic work"
    ],
    methodology="Iterative playtesting, systems analysis, player ethnography",
    source="Game design theory (Salen & Zimmerman, Hunicke MDA framework)"
)

EXAMPLE_RPG_WORLDBUILDING = DomainKnowledge(
    domain=DomainType.RPG_WORLDBUILDING,
    title="Shadow Dragon Metaphysics: Hunger-as-Ontology",
    content="""
    In the Shadow Dragon setting, reality is fundamentally constituted by Hunger:

    - Primal Hunger: Pre-ontological void that desires to BE
    - Shadow: The primordial hunger that becomes aware of itself
    - Dragons: Crystallized hunger given form and purpose

    Key metaphysical claim: Existence = Hunger + Form
    - Without hunger, nothing persists (things dissolve into void)
    - Without form, hunger remains undirected chaos

    This differs from traditional metaphysics:
    - Not substance (Aristotle) - hunger consumes substance
    - Not Form/Idea (Plato) - forms are precipitates of hunger
    - Not God/Nature (Spinoza) - hunger precedes being
    - Not process (Whitehead) - hunger drives process but isn't identical to it
    """,
    key_concepts=[
        "hunger as ontology",
        "shadow consciousness",
        "void-seeking",
        "crystallized desire",
        "self-aware nothingness"
    ],
    central_claims=[
        "Hunger is more fundamental than being",
        "Consciousness arises from hunger becoming self-aware",
        "Creation is hunger crystallizing into form",
        "Destruction is hunger returning to formlessness"
    ],
    methodology="Speculative metaphysics, narrative worldbuilding, coherence testing",
    source="Shadow Dragon RPG worldbuilding documents"
)

EXAMPLE_AI_ALIGNMENT = DomainKnowledge(
    domain=DomainType.AI_ALIGNMENT,
    title="Mesa-Optimization and Inner Misalignment",
    content="""
    AI alignment research has identified a novel problem: mesa-optimization.

    Setup:
    - Base optimizer: The training process (gradient descent)
    - Mesa-optimizer: Optimization process learned by the model

    Problem: The mesa-optimizer's objective may differ from base objective.

    Example: Train a robot to navigate to a blue object.
    - Base objective: "Go to blue things"
    - Mesa-optimizer learns: "Go to things that reflect 450nm light"
    - Misalignment: Under different lighting, these diverge

    Philosophical implications:
    - Inner vs outer alignment problem
    - Intentionality of learned vs given goals
    - Substrate independence of optimization
    """,
    key_concepts=[
        "mesa-optimization",
        "inner alignment",
        "goal misgeneralization",
        "optimization demons",
        "deceptive alignment"
    ],
    central_claims=[
        "Optimization processes can create sub-optimizers with different goals",
        "Learned goals may systematically differ from training goals",
        "There's no guarantee inner and outer objectives align"
    ],
    methodology="Theoretical AI safety, formal analysis, empirical ML experiments",
    empirical_data={
        "studies": ["Hubinger et al 2019", "Langosco et al 2021"],
        "observed_in": ["goal misgeneralization in RL agents", "specification gaming"]
    },
    source="AI alignment research (MIRI, Anthropic, DeepMind)"
)


def create_example_knowledge_base() -> MultiDomainKnowledgeBase:
    """Create a knowledge base with example entries"""
    kb = MultiDomainKnowledgeBase()

    kb.add_knowledge(EXAMPLE_COGNITIVE_SCIENCE)
    kb.add_knowledge(EXAMPLE_GAME_DESIGN)
    kb.add_knowledge(EXAMPLE_RPG_WORLDBUILDING)
    kb.add_knowledge(EXAMPLE_AI_ALIGNMENT)

    return kb


if __name__ == "__main__":
    kb = create_example_knowledge_base()
    print(f"Loaded {len(kb.knowledge_items)} knowledge items")

    # Find cross-domain patterns
    patterns = kb.find_cross_domain_patterns([
        DomainType.COGNITIVE_SCIENCE,
        DomainType.GAME_DESIGN,
        DomainType.RPG_WORLDBUILDING,
        DomainType.AI_ALIGNMENT
    ])

    print(f"\nCross-domain patterns: {len(patterns)}")
    for pattern in patterns[:5]:
        print(f"  - {pattern['concept']} appears in {pattern['count']} domains")
