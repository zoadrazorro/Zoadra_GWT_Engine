"""
Debate Orchestrator - Generates Cross-Temporal Philosophical Debates
===================================================================

This orchestrator uses the consciousness framework to generate debates
between historical philosophers, integrating:
- Composer specialist for content generation
- Memory system for philosophical context
- Metacognition for debate monitoring
- Central workspace for synthesis
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add gwt_engine to path
sys.path.insert(0, str(Path(__file__).parent))

from gwt_engine.specialists.cross_temporal_debate import (
    CrossTemporalDebate,
    create_debate,
    HISTORICAL_PHILOSOPHERS,
    PlatonicExchange,
    GeometricProposition,
    ActualOccasion
)
from gwt_engine.specialists.composer import ComposerSpecialist
from gwt_engine.specialists.metacognition.module import MetacognitionModule
from gwt_engine.core.workspace import Workspace


class DebateOrchestrator:
    """
    Orchestrates multi-round debates between philosophers using
    the consciousness framework for content generation and integration.
    """

    def __init__(self):
        """Initialize the debate orchestrator with consciousness components."""
        self.composer = ComposerSpecialist()
        self.metacognition = MetacognitionModule()
        self.workspace = Workspace()

        # Debate topics
        self.debate_topics = [
            "What is the nature of consciousness itself?",
            "Is free will compatible with determinism?",
            "What is the relationship between mind and matter?",
            "How does knowledge arise from experience?",
            "What is the nature of time and becoming?",
            "Can God's existence be proven through reason?",
            "What is the relationship between language and reality?",
            "How should we define the Good?",
            "What is the nature of personal identity across time?",
            "Is reality fundamentally substance or process?"
        ]

    def generate_debate_round(self, debate: CrossTemporalDebate,
                            round_num: int,
                            exchange_type: str) -> Dict[str, Any]:
        """
        Generate a single round of debate in one of three styles.

        Args:
            debate: The debate instance
            round_num: Current round number
            exchange_type: 'platonic', 'geometric', or 'process'

        Returns:
            Dictionary with generated content
        """
        if exchange_type == 'platonic':
            return self._generate_platonic_round(debate, round_num)
        elif exchange_type == 'geometric':
            return self._generate_geometric_round(debate, round_num)
        elif exchange_type == 'process':
            return self._generate_process_round(debate, round_num)
        else:
            raise ValueError(f"Unknown exchange type: {exchange_type}")

    def _generate_platonic_round(self, debate: CrossTemporalDebate,
                                round_num: int) -> Dict[str, Any]:
        """
        Generate a Socratic dialogue round using the composer.
        """
        philosophers = list(debate.philosophers.keys())
        questioner = philosophers[round_num % len(philosophers)]
        respondent = philosophers[(round_num + 1) % len(philosophers)]

        questioner_obj = debate.philosophers[questioner]
        respondent_obj = debate.philosophers[respondent]

        # Use composer to generate the question
        question_prompt = (
            f"You are {questioner} ({questioner_obj.era}). "
            f"Using the Socratic method, pose a probing question to {respondent} "
            f"about the topic: '{debate.topic}'. "
            f"Your question should embody your philosophical approach centered on: "
            f"{', '.join(questioner_obj.key_concepts[:3])}. "
            f"Make it a genuine philosophical inquiry that seeks truth through dialogue. "
            f"Keep it to 2-3 sentences."
        )

        question = self.composer.compose(
            topic=question_prompt,
            style="formal",
            max_length=200
        )

        # Generate the response
        response_prompt = (
            f"You are {respondent} ({respondent_obj.era}). "
            f"{questioner} has asked you: '{question}'. "
            f"Respond in your characteristic philosophical style, drawing on your key concepts: "
            f"{', '.join(respondent_obj.key_concepts[:3])}. "
            f"Provide a thoughtful response that advances the dialogue. "
            f"Keep it to 3-4 sentences."
        )

        response = self.composer.compose(
            topic=response_prompt,
            style="formal",
            max_length=300
        )

        # Generate elenchus (examination/refutation)
        elenchus_prompt = (
            f"You are {questioner}. {respondent} has responded: '{response}'. "
            f"Provide a Socratic examination (elenchus) of this response. "
            f"Identify assumptions, probe deeper, or reveal contradictions. "
            f"Keep it to 2-3 sentences."
        )

        elenchus = self.composer.compose(
            topic=elenchus_prompt,
            style="analytical",
            max_length=200
        )

        # Create the exchange
        exchange = debate.initiate_platonic_dialogue(
            questioner_name=questioner,
            respondent_name=respondent,
            opening_question=question
        )

        exchange.response = response
        exchange.elenchus = elenchus

        # Check if aporia (perplexity) has been reached
        if round_num % 3 == 2:  # Every third round, reach aporia
            aporia_prompt = (
                f"Based on this exchange between {questioner} and {respondent}, "
                f"what productive perplexity (aporia) has been reached? "
                f"What deeper question emerges? Keep it to 1-2 sentences."
            )
            aporia = self.composer.compose(
                topic=aporia_prompt,
                style="analytical",
                max_length=150
            )
            exchange.reach_aporia(aporia)

        return {
            "type": "platonic",
            "questioner": questioner,
            "respondent": respondent,
            "question": question,
            "response": response,
            "elenchus": elenchus,
            "aporia": exchange.aporia
        }

    def _generate_geometric_round(self, debate: CrossTemporalDebate,
                                 round_num: int) -> Dict[str, Any]:
        """
        Generate a Spinoza-style geometric proposition.
        """
        philosophers = list(debate.philosophers.keys())
        proposer = philosophers[round_num % len(philosophers)]
        proposer_obj = debate.philosophers[proposer]

        # Generate axioms
        axioms_prompt = (
            f"You are {proposer}. State 2-3 axioms (self-evident truths) "
            f"related to '{debate.topic}' that align with your philosophy "
            f"centered on {', '.join(proposer_obj.key_concepts[:2])}. "
            f"Format as numbered axioms. Be concise - one sentence each."
        )

        axioms_text = self.composer.compose(
            topic=axioms_prompt,
            style="formal",
            max_length=300
        )

        # Parse axioms (simple split by newline)
        axioms = [a.strip() for a in axioms_text.split('\n') if a.strip() and any(c.isdigit() for c in a[:3])]

        # Generate proposition
        prop_prompt = (
            f"You are {proposer}. Based on your axioms, state a PROPOSITION "
            f"about '{debate.topic}'. This should be a bold claim that follows "
            f"from your axioms. One sentence, starting with 'PROPOSITION:'"
        )

        proposition = self.composer.compose(
            topic=prop_prompt,
            style="formal",
            max_length=150
        )

        # Generate proof
        proof_prompt = (
            f"You are {proposer}. Provide a PROOF of your proposition: '{proposition}' "
            f"using your stated axioms. Show the logical steps. "
            f"Keep it to 3-4 sentences. Start with 'PROOF:'"
        )

        proof = self.composer.compose(
            topic=proof_prompt,
            style="analytical",
            max_length=400
        )

        # Create geometric proposition
        geom_prop = debate.propose_geometric_axiom(
            philosopher_name=proposer,
            proposition=proposition,
            axioms=axioms,
            proof=proof
        )

        # Generate corollary
        corollary_prompt = (
            f"State a COROLLARY (consequence) that follows from this proposition: "
            f"'{proposition}'. One sentence."
        )

        corollary = self.composer.compose(
            topic=corollary_prompt,
            style="formal",
            max_length=150
        )

        geom_prop.add_corollary(corollary)

        # Generate scholium (explanatory note)
        if round_num % 2 == 0:
            scholium_prompt = (
                f"Provide a SCHOLIUM (explanatory note) for this proposition, "
                f"clarifying its significance or addressing potential objections. "
                f"2-3 sentences."
            )

            scholium = self.composer.compose(
                topic=scholium_prompt,
                style="narrative",
                max_length=250
            )

            geom_prop.add_scholium(scholium)

        return {
            "type": "geometric",
            "philosopher": proposer,
            "axioms": axioms,
            "proposition": proposition,
            "proof": proof,
            "corollary": corollary,
            "scholium": geom_prop.scholium
        }

    def _generate_process_round(self, debate: CrossTemporalDebate,
                               round_num: int) -> Dict[str, Any]:
        """
        Generate a Whiteheadian actual occasion - a quantum of becoming.
        """
        philosophers = list(debate.philosophers.keys())
        speaker = philosophers[round_num % len(philosophers)]
        speaker_obj = debate.philosophers[speaker]

        # Identify what this occasion prehends (grasps from prior occasions)
        prior_occasions = debate.actual_occasions[-3:] if debate.actual_occasions else []
        prehensions = [occ.speaker + "'s insight" for occ in prior_occasions]

        # Generate the occasion content
        occasion_prompt = (
            f"You are {speaker}. Speak about '{debate.topic}' as a moment of becoming, "
            f"a process of creative advance. "
        )

        if prehensions:
            occasion_prompt += (
                f"Your thought prehends (grasps and integrates) the prior insights from "
                f"{', '.join(prehensions)}. "
            )

        occasion_prompt += (
            f"Express how reality is not static substance but creative process, "
            f"drawing on your concepts: {', '.join(speaker_obj.key_concepts[:2])}. "
            f"3-4 sentences. Emphasize temporal flow and becoming."
        )

        content = self.composer.compose(
            topic=occasion_prompt,
            style="narrative",
            max_length=350
        )

        # Create the actual occasion
        occasion = debate.create_actual_occasion(
            philosopher_name=speaker,
            content=content,
            prehensions=prehensions
        )

        # Generate satisfaction (completion/resolution)
        satisfaction_prompt = (
            f"This occasion of thought reaches its SATISFACTION (completion). "
            f"What is the unified feeling or resolution that this moment of becoming achieves? "
            f"One sentence."
        )

        satisfaction = self.composer.compose(
            topic=satisfaction_prompt,
            style="formal",
            max_length=150
        )

        occasion.achieve_satisfaction(satisfaction)

        return {
            "type": "process",
            "speaker": speaker,
            "content": content,
            "prehensions": prehensions,
            "satisfaction": satisfaction
        }

    def run_full_debate(self, topic: str,
                       philosopher_names: List[str],
                       num_rounds: int = 15) -> CrossTemporalDebate:
        """
        Run a complete multi-round debate alternating between all three styles.

        Args:
            topic: The debate topic
            philosopher_names: List of participating philosophers
            num_rounds: Total number of rounds (should be divisible by 3)

        Returns:
            Complete debate with all exchanges
        """
        print(f"\n{'='*80}")
        print(f"CROSS-TEMPORAL PHILOSOPHICAL DEBATE")
        print(f"{'='*80}")
        print(f"Topic: {topic}")
        print(f"Participants: {', '.join(philosopher_names)}")
        print(f"Rounds: {num_rounds}")
        print(f"{'='*80}\n")

        # Create debate
        debate = create_debate(topic, philosopher_names)

        # Alternate between three styles
        styles = ['platonic', 'geometric', 'process']

        for round_num in range(num_rounds):
            style = styles[round_num % 3]

            print(f"\nRound {round_num + 1} - {style.upper()} MODE")
            print("-" * 60)

            # Generate the round
            result = self.generate_debate_round(debate, round_num, style)

            # Display the round
            if style == 'platonic':
                print(f"\n[QUESTION - {result['questioner']}]")
                print(result['question'])
                print(f"\n[RESPONSE - {result['respondent']}]")
                print(result['response'])
                print(f"\n[ELENCHUS - {result['questioner']}]")
                print(result['elenchus'])
                if result['aporia']:
                    print(f"\n[APORIA REACHED]")
                    print(result['aporia'])

            elif style == 'geometric':
                print(f"\n[GEOMETRIC DEMONSTRATION - {result['philosopher']}]")
                print("\nAXIOMS:")
                for axiom in result['axioms']:
                    print(f"  {axiom}")
                print(f"\n{result['proposition']}")
                print(f"\n{result['proof']}")
                print(f"\nCOROLLARY: {result['corollary']}")
                if result['scholium']:
                    print(f"\nSCHOLIUM: {result['scholium']}")

            elif style == 'process':
                print(f"\n[ACTUAL OCCASION - {result['speaker']}]")
                if result['prehensions']:
                    print(f"Prehending: {', '.join(result['prehensions'])}")
                print(f"\n{result['content']}")
                print(f"\nSATISFACTION: {result['satisfaction']}")

            # Metacognitive observation every 3 rounds
            if (round_num + 1) % 3 == 0:
                observation = self._generate_metacognitive_observation(debate, round_num + 1)
                debate.add_metacognitive_observation(observation, consciousness_score=None)
                print(f"\n[METACOGNITIVE OBSERVATION]")
                print(observation)

        print(f"\n{'='*80}")
        print("DEBATE SYNTHESIS")
        print(f"{'='*80}\n")

        synthesis = debate.synthesize_positions()
        print(json.dumps(synthesis, indent=2))

        return debate

    def _generate_metacognitive_observation(self, debate: CrossTemporalDebate,
                                          round_num: int) -> str:
        """Generate metacognitive observation about the debate progress."""
        observation_prompt = (
            f"After {round_num} rounds of debate on '{debate.topic}', "
            f"provide a metacognitive observation about the debate's progress. "
            f"What patterns are emerging? What tensions between the three methodologies "
            f"(Platonic dialogue, geometric proof, process becoming) are evident? "
            f"3-4 sentences."
        )

        observation = self.composer.compose(
            topic=observation_prompt,
            style="analytical",
            max_length=300
        )

        return observation


def main():
    """
    Main entry point - run a sample debate.
    """
    orchestrator = DebateOrchestrator()

    # Select debate topic and philosophers
    topic = "What is the nature of consciousness and its relationship to matter?"

    philosophers = [
        "plato",        # Forms and immaterial soul
        "spinoza",      # Mind and body as attributes of one substance
        "whitehead",    # Consciousness as process of prehension
        "descartes",    # Mind-body dualism
        "hume"          # Bundle theory of consciousness
    ]

    # Run the debate
    debate = orchestrator.run_full_debate(
        topic=topic,
        philosopher_names=philosophers,
        num_rounds=15  # 5 cycles of platonic/geometric/process
    )

    # Export transcript
    output_path = "outputs/cross_temporal_debate_transcript.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    debate.export_full_transcript(output_path)

    print(f"\n\nFull transcript exported to: {output_path}")

    return debate


if __name__ == "__main__":
    main()
