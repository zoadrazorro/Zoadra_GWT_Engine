"""
Cross-Temporal Philosophical Debate System
==========================================

Combines three philosophical methodologies:
1. Plato's Dialogues - Socratic questioning and conversational truth-seeking
2. Spinoza's Ethics - Geometric/axiomatic reasoning (axioms → propositions → proofs)
3. Whitehead's Process Philosophy - Temporal becoming and actual occasions

This system enables debates between historical philosophers across time,
integrating their distinct methodological styles into a unified discourse.
"""

import json
import time
from typing import List, Dict, Any, Tuple
from datetime import datetime
from pathlib import Path


class PhilosopherPersona:
    """Represents a historical philosopher with their characteristic style and positions."""

    def __init__(self, name: str, era: str, key_concepts: List[str],
                 style: str, method: str):
        self.name = name
        self.era = era
        self.key_concepts = key_concepts
        self.style = style  # platonic, spinozist, whiteheadian
        self.method = method  # dialogue, geometric, process
        self.positions_held = []

    def __repr__(self):
        return f"<Philosopher: {self.name} ({self.era})>"


class ActualOccasion:
    """
    Whitehead's fundamental unit of reality - a quantum of becoming.
    Each debate exchange is an actual occasion that perishes into objective immortality.
    """

    def __init__(self, speaker: str, content: str, style: str,
                 prehensions: List[str] = None):
        self.speaker = speaker
        self.content = content
        self.style = style  # platonic, spinozist, whiteheadian
        self.timestamp = time.time()
        self.prehensions = prehensions or []  # What this occasion grasps from prior occasions
        self.satisfaction = None  # The completion/resolution of this occasion

    def achieve_satisfaction(self, resolution: str):
        """The occasion completes and becomes objectively immortal."""
        self.satisfaction = resolution

    def to_dict(self):
        return {
            "speaker": self.speaker,
            "content": self.content,
            "style": self.style,
            "timestamp": self.timestamp,
            "prehensions": self.prehensions,
            "satisfaction": self.satisfaction
        }


class GeometricProposition:
    """
    Spinoza-style geometric proposition with axioms, definitions, and proof.
    More geometrico - in the geometric manner.
    """

    def __init__(self, proposition: str, axioms: List[str] = None,
                 definitions: List[str] = None, proof: str = None):
        self.proposition = proposition
        self.axioms = axioms or []
        self.definitions = definitions or []
        self.proof = proof
        self.corollaries = []
        self.scholium = None  # Explanatory note

    def add_corollary(self, corollary: str):
        self.corollaries.append(corollary)

    def add_scholium(self, scholium: str):
        self.scholium = scholium

    def to_dict(self):
        return {
            "proposition": self.proposition,
            "axioms": self.axioms,
            "definitions": self.definitions,
            "proof": self.proof,
            "corollaries": self.corollaries,
            "scholium": self.scholium
        }


class PlatonicExchange:
    """
    A Socratic dialogue exchange with question, response, and clarification.
    Embodies elenchus - the Socratic method of questioning.
    """

    def __init__(self, questioner: str, respondent: str,
                 question: str, response: str, elenchus: str = None):
        self.questioner = questioner
        self.respondent = respondent
        self.question = question
        self.response = response
        self.elenchus = elenchus  # The refutation/examination
        self.aporia = None  # The perplexity reached

    def reach_aporia(self, aporia: str):
        """Reach a state of puzzlement - productive confusion."""
        self.aporia = aporia

    def to_dict(self):
        return {
            "questioner": self.questioner,
            "respondent": self.respondent,
            "question": self.question,
            "response": self.response,
            "elenchus": self.elenchus,
            "aporia": self.aporia
        }


class CrossTemporalDebate:
    """
    Main debate orchestrator that combines the three philosophical styles
    into a unified cross-temporal dialogue.
    """

    def __init__(self, topic: str, philosophers: List[PhilosopherPersona],
                 consciousness_framework=None):
        self.topic = topic
        self.philosophers = {p.name: p for p in philosophers}
        self.consciousness_framework = consciousness_framework

        # Three streams of discourse
        self.platonic_exchanges: List[PlatonicExchange] = []
        self.geometric_propositions: List[GeometricProposition] = []
        self.actual_occasions: List[ActualOccasion] = []

        # Metacognitive monitoring
        self.metacognitive_observations = []
        self.consciousness_scores = []

        # Unified transcript
        self.full_transcript = []

        self.start_time = time.time()

    def initiate_platonic_dialogue(self, questioner_name: str,
                                   respondent_name: str,
                                   opening_question: str) -> PlatonicExchange:
        """
        Begin a Socratic dialogue between two philosophers.
        """
        questioner = self.philosophers[questioner_name]
        respondent = self.philosophers[respondent_name]

        # Generate response based on respondent's key concepts
        response = self._generate_platonic_response(
            respondent, opening_question
        )

        exchange = PlatonicExchange(
            questioner=questioner_name,
            respondent=respondent_name,
            question=opening_question,
            response=response
        )

        self.platonic_exchanges.append(exchange)
        self.full_transcript.append({
            "type": "platonic_dialogue",
            "exchange": exchange.to_dict(),
            "timestamp": time.time()
        })

        return exchange

    def propose_geometric_axiom(self, philosopher_name: str,
                               proposition: str,
                               axioms: List[str],
                               proof: str) -> GeometricProposition:
        """
        Introduce a Spinoza-style geometric proposition.
        """
        philosopher = self.philosophers[philosopher_name]

        geometric_prop = GeometricProposition(
            proposition=proposition,
            axioms=axioms,
            proof=proof
        )

        self.geometric_propositions.append(geometric_prop)
        self.full_transcript.append({
            "type": "geometric_proposition",
            "philosopher": philosopher_name,
            "proposition": geometric_prop.to_dict(),
            "timestamp": time.time()
        })

        return geometric_prop

    def create_actual_occasion(self, philosopher_name: str,
                              content: str,
                              prehensions: List[str] = None) -> ActualOccasion:
        """
        Generate a Whiteheadian actual occasion - a quantum of becoming.
        Each occasion prehends (grasps) prior occasions.
        """
        philosopher = self.philosophers[philosopher_name]

        occasion = ActualOccasion(
            speaker=philosopher_name,
            content=content,
            style=philosopher.style,
            prehensions=prehensions or []
        )

        self.actual_occasions.append(occasion)
        self.full_transcript.append({
            "type": "actual_occasion",
            "occasion": occasion.to_dict(),
            "timestamp": time.time()
        })

        return occasion

    def synthesize_positions(self) -> Dict[str, Any]:
        """
        Integrate all three streams into a unified understanding.
        This is where the consciousness framework performs meta-integration.
        """
        synthesis = {
            "topic": self.topic,
            "participants": list(self.philosophers.keys()),
            "duration": time.time() - self.start_time,

            "platonic_insights": self._extract_platonic_insights(),
            "geometric_conclusions": self._extract_geometric_conclusions(),
            "process_becoming": self._extract_process_flow(),

            "unified_position": self._generate_unified_position(),
            "remaining_aporias": self._identify_aporias(),

            "metacognitive_summary": self.metacognitive_observations,
            "consciousness_progression": self.consciousness_scores
        }

        return synthesis

    def _generate_platonic_response(self, respondent: PhilosopherPersona,
                                   question: str) -> str:
        """
        Generate a response in the style of the philosopher.
        """
        # This would integrate with the consciousness framework's composer
        # For now, a template-based response
        response_template = (
            f"In the manner of {respondent.name}, considering {', '.join(respondent.key_concepts[:3])}, "
            f"I would respond: Let us examine this question carefully. "
            f"When you ask '{question}', we must first define our terms..."
        )
        return response_template

    def _extract_platonic_insights(self) -> List[str]:
        """Extract key insights from Socratic dialogues."""
        insights = []
        for exchange in self.platonic_exchanges:
            if exchange.aporia:
                insights.append(f"Aporia reached: {exchange.aporia}")
            if exchange.elenchus:
                insights.append(f"Refutation: {exchange.elenchus}")
        return insights

    def _extract_geometric_conclusions(self) -> List[str]:
        """Extract proven propositions."""
        return [prop.proposition for prop in self.geometric_propositions if prop.proof]

    def _extract_process_flow(self) -> List[Dict]:
        """Map the temporal flow of actual occasions."""
        return [
            {
                "speaker": occ.speaker,
                "content": occ.content,
                "prehends": occ.prehensions,
                "satisfied": occ.satisfaction is not None
            }
            for occ in self.actual_occasions
        ]

    def _generate_unified_position(self) -> str:
        """
        Synthesize all three streams into a coherent position.
        """
        return (
            f"Through dialectical examination (Plato), geometric demonstration (Spinoza), "
            f"and process integration (Whitehead), we arrive at a position that honors "
            f"the becoming of truth through conversation, the necessity of logical proof, "
            f"and the temporal unfolding of understanding."
        )

    def _identify_aporias(self) -> List[str]:
        """Identify remaining puzzles and contradictions."""
        aporias = []
        for exchange in self.platonic_exchanges:
            if exchange.aporia:
                aporias.append(exchange.aporia)
        return aporias

    def add_metacognitive_observation(self, observation: str,
                                     consciousness_score: float = None):
        """
        Record metacognitive awareness during the debate.
        """
        self.metacognitive_observations.append({
            "timestamp": time.time(),
            "observation": observation,
            "consciousness_score": consciousness_score
        })

        if consciousness_score is not None:
            self.consciousness_scores.append(consciousness_score)

    def export_full_transcript(self, filepath: str):
        """
        Export the complete debate transcript.
        """
        output = {
            "metadata": {
                "topic": self.topic,
                "participants": list(self.philosophers.keys()),
                "start_time": self.start_time,
                "duration": time.time() - self.start_time,
                "total_exchanges": len(self.full_transcript)
            },
            "transcript": self.full_transcript,
            "synthesis": self.synthesize_positions()
        }

        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)

        return filepath


# Pre-configured historical philosophers
HISTORICAL_PHILOSOPHERS = {
    "plato": PhilosopherPersona(
        name="Plato",
        era="Ancient Greece (428-348 BCE)",
        key_concepts=["Forms", "The Good", "Knowledge vs Opinion", "Recollection",
                      "Tripartite Soul", "Philosopher-Kings"],
        style="platonic",
        method="dialogue"
    ),

    "aristotle": PhilosopherPersona(
        name="Aristotle",
        era="Ancient Greece (384-322 BCE)",
        key_concepts=["Substance", "Potentiality and Actuality", "Four Causes",
                      "Virtue Ethics", "Golden Mean", "Unmoved Mover"],
        style="platonic",
        method="systematic"
    ),

    "spinoza": PhilosopherPersona(
        name="Baruch Spinoza",
        era="Early Modern (1632-1677)",
        key_concepts=["Substance Monism", "God or Nature", "Modes and Attributes",
                      "Conatus", "Intellectual Love of God", "Determinism"],
        style="spinozist",
        method="geometric"
    ),

    "leibniz": PhilosopherPersona(
        name="Gottfried Wilhelm Leibniz",
        era="Early Modern (1646-1716)",
        key_concepts=["Monads", "Pre-established Harmony", "Best of All Possible Worlds",
                      "Principle of Sufficient Reason", "Identity of Indiscernibles"],
        style="spinozist",
        method="geometric"
    ),

    "whitehead": PhilosopherPersona(
        name="Alfred North Whitehead",
        era="20th Century (1861-1947)",
        key_concepts=["Actual Occasions", "Prehension", "Process and Reality",
                      "Creativity", "Eternal Objects", "Concrescence"],
        style="whiteheadian",
        method="process"
    ),

    "bergson": PhilosopherPersona(
        name="Henri Bergson",
        era="20th Century (1859-1941)",
        key_concepts=["Duration", "Élan Vital", "Intuition vs Intellect",
                      "Creative Evolution", "Memory and Matter"],
        style="whiteheadian",
        method="process"
    ),

    "hegel": PhilosopherPersona(
        name="Georg Wilhelm Friedrich Hegel",
        era="German Idealism (1770-1831)",
        key_concepts=["Dialectic", "Absolute Spirit", "Master-Slave",
                      "Aufhebung", "World-Historical Individuals"],
        style="platonic",
        method="dialectical"
    ),

    "kant": PhilosopherPersona(
        name="Immanuel Kant",
        era="Enlightenment (1724-1804)",
        key_concepts=["Categorical Imperative", "Transcendental Idealism",
                      "Synthetic A Priori", "Noumena and Phenomena", "Autonomy"],
        style="spinozist",
        method="critical"
    ),

    "descartes": PhilosopherPersona(
        name="René Descartes",
        era="Early Modern (1596-1650)",
        key_concepts=["Cogito Ergo Sum", "Mind-Body Dualism", "Clear and Distinct Ideas",
                      "Method of Doubt", "God as Guarantor"],
        style="spinozist",
        method="geometric"
    ),

    "hume": PhilosopherPersona(
        name="David Hume",
        era="Enlightenment (1711-1776)",
        key_concepts=["Impressions and Ideas", "Problem of Induction",
                      "Bundle Theory of Self", "Is-Ought Gap", "Custom and Habit"],
        style="platonic",
        method="empirical"
    ),

    "nietzsche": PhilosopherPersona(
        name="Friedrich Nietzsche",
        era="19th Century (1844-1900)",
        key_concepts=["Will to Power", "Eternal Recurrence", "Übermensch",
                      "Death of God", "Master-Slave Morality", "Perspectivism"],
        style="platonic",
        method="aphoristic"
    ),

    "wittgenstein": PhilosopherPersona(
        name="Ludwig Wittgenstein",
        era="20th Century (1889-1951)",
        key_concepts=["Language Games", "Forms of Life", "Family Resemblance",
                      "Showing vs Saying", "Private Language Argument"],
        style="platonic",
        method="linguistic"
    )
}


def create_debate(topic: str, philosopher_names: List[str],
                 consciousness_framework=None) -> CrossTemporalDebate:
    """
    Factory function to create a cross-temporal debate.

    Args:
        topic: The philosophical question or theme
        philosopher_names: List of philosopher keys from HISTORICAL_PHILOSOPHERS
        consciousness_framework: Optional GWT consciousness framework for integration

    Returns:
        CrossTemporalDebate instance
    """
    philosophers = [HISTORICAL_PHILOSOPHERS[name] for name in philosopher_names]
    return CrossTemporalDebate(topic, philosophers, consciousness_framework)
