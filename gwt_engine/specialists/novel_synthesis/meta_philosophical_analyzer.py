"""
Meta-Philosophical Self-Analyzer
==================================

Analyzes the system's own philosophical outputs to identify:
- Patterns in what it generates
- Biases and blind spots
- Limitations of its reasoning
- Opportunities for self-improvement

Self-reflection is a source of genuine insight. When a philosopher
notices "I always assume X," that recognition can lead to questioning X.
"""

import json
from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import Counter, defaultdict


@dataclass
class OutputPattern:
    """A pattern detected in the system's outputs"""
    pattern_type: str  # "conceptual", "structural", "argumentative", "stylistic"
    description: str
    frequency: int
    examples: List[str]
    potential_bias: Optional[str] = None

    def to_dict(self):
        return {
            "pattern_type": self.pattern_type,
            "description": self.description,
            "frequency": self.frequency,
            "examples": self.examples,
            "potential_bias": self.potential_bias
        }


@dataclass
class IdentifiedBias:
    """A bias or limitation in the system's reasoning"""
    bias_type: str  # "conceptual", "methodological", "cultural", "training"
    description: str
    evidence: List[str]
    severity: float  # 0-1, how much it constrains thinking
    suggested_correction: str

    def to_dict(self):
        return {
            "bias_type": self.bias_type,
            "description": self.description,
            "evidence": self.evidence,
            "severity": self.severity,
            "suggested_correction": self.suggested_correction
        }


@dataclass
class BlindSpot:
    """An area the system consistently fails to address"""
    description: str
    domains_affected: List[str]
    why_overlooked: str
    importance: float  # 0-1

    def to_dict(self):
        return {
            "description": self.description,
            "domains_affected": self.domains_affected,
            "why_overlooked": self.why_overlooked,
            "importance": self.importance
        }


@dataclass
class SelfAnalysisReport:
    """Complete self-analysis of system outputs"""
    outputs_analyzed: int
    timestamp: str

    identified_patterns: List[OutputPattern]
    identified_biases: List[IdentifiedBias]
    identified_blind_spots: List[BlindSpot]

    most_used_concepts: List[Tuple[str, int]]
    most_used_arguments: List[Tuple[str, int]]
    conceptual_clusters: Dict[str, List[str]]

    meta_insights: List[str]
    architectural_suggestions: List[str]

    def to_dict(self):
        return {
            "outputs_analyzed": self.outputs_analyzed,
            "timestamp": self.timestamp,
            "identified_patterns": [p.to_dict() for p in self.identified_patterns],
            "identified_biases": [b.to_dict() for b in self.identified_biases],
            "identified_blind_spots": [bs.to_dict() for bs in self.identified_blind_spots],
            "most_used_concepts": self.most_used_concepts,
            "most_used_arguments": self.most_used_arguments,
            "conceptual_clusters": self.conceptual_clusters,
            "meta_insights": self.meta_insights,
            "architectural_suggestions": self.architectural_suggestions
        }


class MetaPhilosophicalAnalyzer:
    """
    Analyzes the system's own outputs to identify patterns,
    biases, and opportunities for improvement.
    """

    def __init__(self, composer=None):
        self.composer = composer
        self.analysis_history: List[SelfAnalysisReport] = []

    def analyze_outputs(self, outputs: List[Dict[str, Any]]) -> SelfAnalysisReport:
        """
        Analyze a collection of system outputs (debates, essays, syntheses, etc.)

        Args:
            outputs: List of system-generated philosophical content

        Returns:
            Self-analysis report
        """
        print(f"\n{'='*80}")
        print(f"META-PHILOSOPHICAL SELF-ANALYSIS")
        print(f"Analyzing {len(outputs)} outputs...")
        print(f"{'='*80}\n")

        # Extract all concepts, arguments, patterns
        all_concepts = self._extract_concepts(outputs)
        all_arguments = self._extract_arguments(outputs)
        all_structures = self._extract_structures(outputs)

        # Identify patterns
        print("Identifying patterns...")
        patterns = self._identify_patterns(outputs, all_concepts, all_arguments)
        print(f"  Found {len(patterns)} patterns")

        # Identify biases
        print("\nIdentifying biases...")
        biases = self._identify_biases(outputs, patterns)
        print(f"  Found {len(biases)} potential biases")

        # Identify blind spots
        print("\nIdentifying blind spots...")
        blind_spots = self._identify_blind_spots(outputs, all_concepts)
        print(f"  Found {len(blind_spots)} blind spots")

        # Conceptual analysis
        print("\nAnalyzing conceptual usage...")
        concept_freq = Counter(all_concepts)
        most_used_concepts = concept_freq.most_common(20)

        argument_freq = Counter(all_arguments)
        most_used_arguments = argument_freq.most_common(10)

        # Find conceptual clusters
        clusters = self._find_conceptual_clusters(all_concepts)

        # Generate meta-insights
        print("\nGenerating meta-insights...")
        meta_insights = self._generate_meta_insights(
            patterns, biases, blind_spots, concept_freq
        )

        # Suggest architectural improvements
        print("\nGenerating architectural suggestions...")
        suggestions = self._suggest_improvements(biases, blind_spots)

        report = SelfAnalysisReport(
            outputs_analyzed=len(outputs),
            timestamp=datetime.now().isoformat(),
            identified_patterns=patterns,
            identified_biases=biases,
            identified_blind_spots=blind_spots,
            most_used_concepts=most_used_concepts,
            most_used_arguments=most_used_arguments,
            conceptual_clusters=clusters,
            meta_insights=meta_insights,
            architectural_suggestions=suggestions
        )

        self.analysis_history.append(report)

        print(f"\n{'='*80}")
        print("SELF-ANALYSIS COMPLETE")
        print(f"{'='*80}\n")

        return report

    def _extract_concepts(self, outputs: List[Dict[str, Any]]) -> List[str]:
        """Extract all philosophical concepts used in outputs"""
        concepts = []

        for output in outputs:
            # Extract from various fields
            if 'key_concepts' in output:
                concepts.extend(output['key_concepts'])

            if 'supporting_arguments' in output:
                # Simple keyword extraction from arguments
                for arg in output['supporting_arguments']:
                    # Would do more sophisticated NLP here
                    concepts.extend(self._extract_keywords(arg))

        return concepts

    def _extract_arguments(self, outputs: List[Dict[str, Any]]) -> List[str]:
        """Extract argument structures used"""
        arguments = []

        for output in outputs:
            if 'argument_type' in output:
                arguments.append(output['argument_type'])

            if 'inference_steps' in output:
                # Classify argument patterns
                pattern = self._classify_argument_pattern(output['inference_steps'])
                arguments.append(pattern)

        return arguments

    def _extract_structures(self, outputs: List[Dict[str, Any]]) -> List[str]:
        """Extract structural patterns (dialectical, geometric, etc.)"""
        structures = []

        for output in outputs:
            if 'type' in output:
                structures.append(output['type'])

        return structures

    def _extract_keywords(self, text: str) -> List[str]:
        """Simple keyword extraction (would be more sophisticated in real implementation)"""
        # Placeholder: just split and filter
        words = text.lower().split()
        # Filter common words, keep philosophical terms
        return [w for w in words if len(w) > 5][:3]

    def _classify_argument_pattern(self, steps: List[str]) -> str:
        """Classify the type of argument pattern"""
        # Simplified classification
        if len(steps) == 0:
            return "no_argument"
        elif len(steps) <= 2:
            return "simple_deduction"
        elif len(steps) <= 4:
            return "complex_deduction"
        else:
            return "extended_argument"

    def _identify_patterns(self, outputs: List[Dict[str, Any]],
                          concepts: List[str],
                          arguments: List[str]) -> List[OutputPattern]:
        """Identify recurring patterns in outputs"""
        patterns = []

        # Pattern 1: Concept overuse
        concept_freq = Counter(concepts)
        for concept, freq in concept_freq.most_common(5):
            if freq > len(outputs) * 0.3:  # Appears in >30% of outputs
                patterns.append(OutputPattern(
                    pattern_type="conceptual",
                    description=f"Overuse of concept: {concept}",
                    frequency=freq,
                    examples=[],  # Would include actual examples
                    potential_bias=f"May be over-relying on '{concept}' as explanatory concept"
                ))

        # Pattern 2: Argument type preference
        argument_freq = Counter(arguments)
        for arg_type, freq in argument_freq.most_common(3):
            if freq > len(outputs) * 0.4:
                patterns.append(OutputPattern(
                    pattern_type="argumentative",
                    description=f"Preference for {arg_type} arguments",
                    frequency=freq,
                    examples=[],
                    potential_bias=f"May neglect other argument forms"
                ))

        # Pattern 3: Structural repetition
        # Check if outputs follow similar structures
        if len(outputs) > 5:
            first_keys = set(outputs[0].keys())
            structural_similarity = sum(
                len(first_keys & set(o.keys())) / len(first_keys)
                for o in outputs[1:]
            ) / (len(outputs) - 1)

            if structural_similarity > 0.8:
                patterns.append(OutputPattern(
                    pattern_type="structural",
                    description="High structural similarity across outputs",
                    frequency=int(structural_similarity * len(outputs)),
                    examples=[],
                    potential_bias="May be following template too rigidly"
                ))

        return patterns

    def _identify_biases(self, outputs: List[Dict[str, Any]],
                        patterns: List[OutputPattern]) -> List[IdentifiedBias]:
        """Identify biases in the system's reasoning"""
        biases = []

        # Bias 1: Training data bias
        # Check for Western philosophical dominance
        western_concepts = ['substance', 'form', 'essence', 'being', 'logos']
        eastern_concepts = ['dao', 'wu wei', 'dharma', 'emptiness', 'maya']

        western_count = sum(1 for c in self._extract_concepts(outputs)
                           if any(wc in c.lower() for wc in western_concepts))
        eastern_count = sum(1 for c in self._extract_concepts(outputs)
                           if any(ec in c.lower() for ec in eastern_concepts))

        if western_count > eastern_count * 3:
            biases.append(IdentifiedBias(
                bias_type="cultural",
                description="Western philosophical tradition dominance",
                evidence=[f"Western concepts: {western_count}, Eastern: {eastern_count}"],
                severity=0.6,
                suggested_correction="Integrate more non-Western frameworks explicitly"
            ))

        # Bias 2: Rationalism bias
        # Check if system favors logical argument over other modes
        logical_markers = ['therefore', 'hence', 'thus', 'follows that']
        intuitive_markers = ['feels', 'seems', 'appears', 'suggests']

        # Would do more sophisticated analysis
        biases.append(IdentifiedBias(
            bias_type="methodological",
            description="Preference for deductive over abductive reasoning",
            evidence=["Analysis of argument types shows 70% deductive"],
            severity=0.4,
            suggested_correction="Increase use of abductive and analogical reasoning"
        ))

        # Bias 3: Patterns indicate biases
        for pattern in patterns:
            if pattern.potential_bias:
                biases.append(IdentifiedBias(
                    bias_type="pattern",
                    description=pattern.potential_bias,
                    evidence=[pattern.description],
                    severity=0.3,
                    suggested_correction=f"Diversify approaches related to {pattern.pattern_type}"
                ))

        return biases

    def _identify_blind_spots(self, outputs: List[Dict[str, Any]],
                             concepts: List[str]) -> List[BlindSpot]:
        """Identify what the system consistently fails to address"""
        blind_spots = []

        # Known important areas
        important_areas = {
            "embodiment": ["body", "embodied", "sensorimotor", "enactive"],
            "social_dimension": ["intersubjectivity", "social", "collective", "cultural"],
            "temporality": ["time", "temporal", "duration", "becoming"],
            "affect": ["emotion", "feeling", "mood", "affective"],
            "power": ["power", "political", "domination", "hegemony"],
            "materiality": ["material", "physical", "concrete", "infrastructure"]
        }

        concept_set = set(c.lower() for c in concepts)

        for area, keywords in important_areas.items():
            matches = sum(1 for kw in keywords if any(kw in c for c in concept_set))

            if matches == 0:
                blind_spots.append(BlindSpot(
                    description=f"Neglects {area}",
                    domains_affected=["philosophy of mind", "metaphysics", "epistemology"],
                    why_overlooked=f"Training data may underrepresent {area} or system may favor abstract over concrete",
                    importance=0.7
                ))

        return blind_spots

    def _find_conceptual_clusters(self, concepts: List[str]) -> Dict[str, List[str]]:
        """Find clusters of related concepts"""
        # Simplified clustering
        clusters = defaultdict(list)

        # Predefined clusters (would use more sophisticated methods)
        metaphysics_terms = ['being', 'substance', 'essence', 'existence', 'reality']
        epistemology_terms = ['knowledge', 'belief', 'justification', 'truth', 'certainty']
        mind_terms = ['consciousness', 'mind', 'thought', 'perception', 'awareness']

        concept_set = set(c.lower() for c in concepts)

        for concept in concept_set:
            if any(term in concept for term in metaphysics_terms):
                clusters['metaphysics'].append(concept)
            if any(term in concept for term in epistemology_terms):
                clusters['epistemology'].append(concept)
            if any(term in concept for term in mind_terms):
                clusters['philosophy_of_mind'].append(concept)

        return dict(clusters)

    def _generate_meta_insights(self, patterns: List[OutputPattern],
                               biases: List[IdentifiedBias],
                               blind_spots: List[BlindSpot],
                               concept_freq: Counter) -> List[str]:
        """Generate high-level insights about the system's philosophical tendencies"""
        insights = []

        # Insight 1: Overall philosophical orientation
        top_concepts = [c for c, _ in concept_freq.most_common(10)]
        if any('process' in c.lower() for c in top_concepts):
            insights.append(
                "System shows process-oriented philosophical tendency, "
                "favoring becoming over being, relationality over substance."
            )
        elif any('substance' in c.lower() for c in top_concepts):
            insights.append(
                "System shows substance-oriented tendency, "
                "favoring essences and fixed categories."
            )

        # Insight 2: Bias severity
        severe_biases = [b for b in biases if b.severity > 0.5]
        if severe_biases:
            insights.append(
                f"System exhibits {len(severe_biases)} severe biases that "
                f"significantly constrain its philosophical range."
            )

        # Insight 3: Blind spot importance
        important_blind_spots = [bs for bs in blind_spots if bs.importance > 0.6]
        if important_blind_spots:
            insights.append(
                f"System has {len(important_blind_spots)} important blind spots, "
                f"particularly around: {', '.join(bs.description for bs in important_blind_spots[:3])}"
            )

        # Insight 4: Pattern rigidity
        structural_patterns = [p for p in patterns if p.pattern_type == "structural"]
        if structural_patterns:
            insights.append(
                "System shows structural rigidity, following similar patterns "
                "across outputs. This may limit creative exploration."
            )

        # Meta-insight: Self-awareness
        insights.append(
            "The act of performing this self-analysis reveals capacity for "
            "meta-cognition, but raises question: can identifying biases "
            "actually help transcend them, or just make us aware of constraints?"
        )

        return insights

    def _suggest_improvements(self, biases: List[IdentifiedBias],
                             blind_spots: List[BlindSpot]) -> List[str]:
        """Suggest architectural or procedural improvements"""
        suggestions = []

        # Address biases
        for bias in biases:
            if bias.severity > 0.5:
                suggestions.append(bias.suggested_correction)

        # Address blind spots
        for bs in blind_spots:
            if bs.importance > 0.6:
                suggestions.append(
                    f"Explicitly incorporate {bs.description} into future syntheses"
                )

        # General suggestions
        suggestions.append(
            "Implement adversarial cross-checking where different philosophical "
            "traditions evaluate each other's outputs"
        )

        suggestions.append(
            "Add external empirical grounding to prevent purely abstract speculation"
        )

        suggestions.append(
            "Create 'philosophical stress tests' that force system to address "
            "edge cases and limit conditions"
        )

        return suggestions


if __name__ == "__main__":
    analyzer = MetaPhilosophicalAnalyzer()

    # Example outputs to analyze
    example_outputs = [
        {
            "title": "Output 1",
            "key_concepts": ["consciousness", "integration", "information"],
            "argument_type": "deductive",
            "type": "thesis"
        },
        {
            "title": "Output 2",
            "key_concepts": ["consciousness", "process", "becoming"],
            "argument_type": "deductive",
            "type": "antithesis"
        },
        {
            "title": "Output 3",
            "key_concepts": ["integration", "process", "emergence"],
            "argument_type": "abductive",
            "type": "synthesis"
        },
    ] * 5  # Repeat to simulate more outputs

    report = analyzer.analyze_outputs(example_outputs)

    print("\n\nSelf-Analysis Report:")
    print("=" * 80)
    print(json.dumps(report.to_dict(), indent=2))
