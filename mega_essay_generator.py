"""
Mega Essay Generator - 50,000 Word Philosophical Essay
=======================================================

Generates comprehensive essays documenting cross-temporal philosophical debates,
including full transcripts, analysis, and metacognitive observations.

Target: 50,000+ words
Structure:
- Introduction and Methodology (3,000 words)
- Historical Context for Each Philosopher (5,000 words)
- Full Debate Transcripts (25,000 words)
- Philosophical Analysis (10,000 words)
- Metacognitive Reflections (5,000 words)
- Synthesis and Conclusions (2,000 words)
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from gwt_engine.specialists.composer import ComposerSpecialist
from gwt_engine.specialists.cross_temporal_debate import CrossTemporalDebate, HISTORICAL_PHILOSOPHERS, create_debate
from debate_orchestrator import DebateOrchestrator


class MegaEssayGenerator:
    """
    Generates extensive philosophical essays with debate transcripts.
    """

    def __init__(self, model_name: str = "qwen2.5:32b"):
        self.composer = ComposerSpecialist(model_name=model_name)
        self.word_count = 0
        self.sections = []
        print(f"MegaEssayGenerator initialized with model: {model_name}")

    def count_words(self, text: str) -> int:
        """Count words in text."""
        return len(text.split())

    def add_section(self, title: str, content: str, level: int = 1):
        """Add a section to the essay."""
        words = self.count_words(content)
        self.word_count += words

        self.sections.append({
            "title": title,
            "content": content,
            "level": level,
            "word_count": words
        })

        return words

    def generate_introduction(self, topic: str, philosophers: List[str]) -> str:
        """
        Generate comprehensive introduction (target: 3,000 words).
        """
        print("\n[Generating Introduction...]")

        intro_parts = []

        # Part 1: Opening and context
        prompt1 = (
            f"Write an expansive introduction to a philosophical investigation of: '{topic}'. "
            f"This essay documents a cross-temporal debate between {', '.join(philosophers)}. "
            f"Explain the significance of bringing together thinkers across different eras "
            f"and philosophical traditions. Discuss why this topic remains perennially important. "
            f"Target length: 800 words. Be scholarly but engaging."
        )

        part1 = self.composer.compose_sync(topic=prompt1, style="formal", max_length=2048)
        intro_parts.append(part1)
        print(f"  Part 1: {self.count_words(part1)} words")

        # Part 2: Methodological framework
        prompt2 = (
            f"Explain the unique methodology of this investigation: combining three philosophical approaches. "
            f"First, Plato's Dialogues and the Socratic method - how dialectical questioning reveals truth. "
            f"Discuss elenchus (examination), aporia (productive perplexity), and the pursuit of Forms. "
            f"Explain why dialogue is central to philosophical inquiry. "
            f"Target length: 800 words."
        )

        part2 = self.composer.compose(topic=prompt2, style="formal", max_length=2048)
        intro_parts.append(part2)
        print(f"  Part 2: {self.count_words(part2)} words")

        # Part 3: Spinoza's geometric method
        prompt3 = (
            f"Explain Spinoza's geometric method (more geometrico) - the style of his Ethics. "
            f"Discuss how philosophy can proceed from axioms and definitions to propositions and proofs, "
            f"following the model of Euclidean geometry. Explain the role of demonstrations, corollaries, "
            f"and scholia in building a rigorous philosophical system. Why did Spinoza choose this method? "
            f"What are its strengths and limitations? "
            f"Target length: 800 words."
        )

        part3 = self.composer.compose(topic=prompt3, style="formal", max_length=2048)
        intro_parts.append(part3)
        print(f"  Part 3: {self.count_words(part3)} words")

        # Part 4: Whitehead's process philosophy
        prompt4 = (
            f"Explain Whitehead's process philosophy and the concept of actual occasions. "
            f"Discuss prehension (how occasions grasp prior occasions), concrescence (growing together), "
            f"and satisfaction (completion of an occasion). Explain how this differs from substance metaphysics. "
            f"Why does Whitehead say 'the creative advance into novelty' is reality's fundamental character? "
            f"How does this temporal, processual approach change philosophical methodology? "
            f"Target length: 800 words."
        )

        part4 = self.composer.compose(topic=prompt4, style="formal", max_length=2048)
        intro_parts.append(part4)
        print(f"  Part 4: {self.count_words(part4)} words")

        full_intro = "\n\n".join(intro_parts)
        words = self.add_section("Introduction: Methodology and Framework", full_intro, level=1)
        print(f"Total Introduction: {words} words\n")

        return full_intro

    def generate_philosopher_profile(self, philosopher_name: str) -> str:
        """
        Generate extensive profile for each philosopher (target: 1,000 words each).
        """
        print(f"[Generating profile for {philosopher_name}...]")

        philosopher = HISTORICAL_PHILOSOPHERS[philosopher_name]

        # Part 1: Historical context and biography
        prompt1 = (
            f"Provide detailed historical context and biographical background for {philosopher.name} "
            f"({philosopher.era}). Discuss the intellectual milieu of their time, "
            f"major influences, and key life events that shaped their philosophy. "
            f"Target length: 400 words."
        )

        part1 = self.composer.compose(topic=prompt1, style="formal", max_length=1024)

        # Part 2: Key concepts and contributions
        prompt2 = (
            f"Provide an in-depth explanation of {philosopher.name}'s key philosophical concepts: "
            f"{', '.join(philosopher.key_concepts)}. "
            f"For each concept, explain its meaning, significance, and how it fits into their overall system. "
            f"What are their major works? What problems were they trying to solve? "
            f"Target length: 400 words."
        )

        part2 = self.composer.compose(topic=prompt2, style="formal", max_length=1024)

        # Part 3: Methodological approach
        prompt3 = (
            f"Explain {philosopher.name}'s characteristic methodological approach: {philosopher.method}. "
            f"How do they conduct philosophical inquiry? What style of argumentation do they employ? "
            f"What are the strengths of their method? How does it reflect their metaphysical commitments? "
            f"Target length: 300 words."
        )

        part3 = self.composer.compose(topic=prompt3, style="formal", max_length=800)

        full_profile = f"{part1}\n\n{part2}\n\n{part3}"
        words = self.add_section(f"{philosopher.name} ({philosopher.era})", full_profile, level=2)
        print(f"  {philosopher_name} profile: {words} words\n")

        return full_profile

    def generate_all_profiles(self, philosophers: List[str]) -> str:
        """
        Generate profiles for all participating philosophers (target: 5,000 words).
        """
        print("\n[Generating Philosopher Profiles Section...]")

        profiles = []
        for phil in philosophers:
            profiles.append(self.generate_philosopher_profile(phil))

        section_intro = (
            "Before engaging with the debate itself, we must understand the intellectual "
            "traditions and methodological commitments of each participant. The following "
            "profiles provide essential context for appreciating the richness of their contributions."
        )

        full_section = section_intro + "\n\n" + "\n\n---\n\n".join(profiles)
        return full_section

    def generate_debate_transcript_section(self, debate: CrossTemporalDebate) -> str:
        """
        Generate comprehensive debate transcript with commentary (target: 25,000 words).
        """
        print("\n[Generating Debate Transcript Section...]")

        transcript_parts = []

        # Introduction to transcript section
        intro = (
            f"What follows is the complete transcript of the cross-temporal debate on: "
            f"'{debate.topic}'. The debate proceeds in three alternating modes: "
            f"Platonic Dialogue (Socratic questioning), Geometric Demonstration (Spinozist proofs), "
            f"and Process Occasions (Whiteheadian becoming). Each mode reveals different aspects "
            f"of the truth, and their synthesis constitutes a higher-order understanding."
        )

        transcript_parts.append(intro)

        # Process each exchange with commentary
        for i, entry in enumerate(debate.full_transcript):
            round_header = f"\n\n## Round {i + 1}: {entry['type'].upper()} MODE\n"
            transcript_parts.append(round_header)

            if entry['type'] == 'platonic_dialogue':
                exchange = entry['exchange']

                # Format the exchange
                formatted = (
                    f"**Questioner:** {exchange['questioner']}\n\n"
                    f"**Question:**\n{exchange['question']}\n\n"
                    f"**Respondent:** {exchange['respondent']}\n\n"
                    f"**Response:**\n{exchange['response']}\n\n"
                )

                if exchange.get('elenchus'):
                    formatted += f"**Elenchus (Examination):**\n{exchange['elenchus']}\n\n"

                if exchange.get('aporia'):
                    formatted += (
                        f"**Aporia (Perplexity Reached):**\n{exchange['aporia']}\n\n"
                    )

                transcript_parts.append(formatted)

                # Generate commentary every few exchanges
                if i % 3 == 2:
                    commentary_prompt = (
                        f"Provide philosophical commentary on this Platonic dialogue exchange. "
                        f"Analyze the quality of the questioning, the coherence of the response, "
                        f"and the effectiveness of the elenchus. What philosophical insights emerge? "
                        f"What assumptions are being challenged? "
                        f"Target length: 300 words."
                    )

                    commentary = self.composer.compose(
                        topic=commentary_prompt,
                        style="analytical",
                        max_length=800
                    )

                    transcript_parts.append(f"**Commentary:**\n{commentary}\n\n")

            elif entry['type'] == 'geometric_proposition':
                prop = entry['proposition']

                formatted = (
                    f"**Philosopher:** {entry['philosopher']}\n\n"
                    f"**Axioms:**\n"
                )

                for axiom in prop['axioms']:
                    formatted += f"- {axiom}\n"

                formatted += (
                    f"\n**Proposition:**\n{prop['proposition']}\n\n"
                    f"**Proof:**\n{prop['proof']}\n\n"
                )

                if prop.get('corollaries'):
                    formatted += "**Corollaries:**\n"
                    for cor in prop['corollaries']:
                        formatted += f"- {cor}\n"
                    formatted += "\n"

                if prop.get('scholium'):
                    formatted += f"**Scholium:**\n{prop['scholium']}\n\n"

                transcript_parts.append(formatted)

                # Commentary on geometric demonstrations
                if i % 3 == 1:
                    commentary_prompt = (
                        f"Analyze this geometric demonstration. Evaluate the axioms: "
                        f"are they truly self-evident? Assess the logical rigor of the proof. "
                        f"Do the conclusions necessarily follow? What philosophical implications "
                        f"does this proposition have? "
                        f"Target length: 300 words."
                    )

                    commentary = self.composer.compose(
                        topic=commentary_prompt,
                        style="analytical",
                        max_length=800
                    )

                    transcript_parts.append(f"**Commentary:**\n{commentary}\n\n")

            elif entry['type'] == 'actual_occasion':
                occ = entry['occasion']

                formatted = (
                    f"**Speaker:** {occ['speaker']}\n\n"
                )

                if occ.get('prehensions'):
                    formatted += (
                        f"**Prehends (Grasps):** {', '.join(occ['prehensions'])}\n\n"
                    )

                formatted += (
                    f"**Content (Becoming):**\n{occ['content']}\n\n"
                )

                if occ.get('satisfaction'):
                    formatted += (
                        f"**Satisfaction (Completion):**\n{occ['satisfaction']}\n\n"
                    )

                transcript_parts.append(formatted)

                # Commentary on process occasions
                if i % 3 == 0 and i > 0:
                    commentary_prompt = (
                        f"Reflect on this actual occasion from a process perspective. "
                        f"How does it prehend and integrate prior occasions? "
                        f"What novel element does it contribute to the ongoing creative advance? "
                        f"How does this exemplify Whitehead's concept that 'the many become one and are increased by one'? "
                        f"Target length: 300 words."
                    )

                    commentary = self.composer.compose(
                        topic=commentary_prompt,
                        style="analytical",
                        max_length=800
                    )

                    transcript_parts.append(f"**Commentary:**\n{commentary}\n\n")

        full_transcript = "\n".join(transcript_parts)
        words = self.add_section("Complete Debate Transcript with Commentary", full_transcript, level=1)
        print(f"Debate transcript section: {words} words\n")

        return full_transcript

    def generate_philosophical_analysis(self, debate: CrossTemporalDebate,
                                       philosophers: List[str]) -> str:
        """
        Generate deep philosophical analysis (target: 10,000 words).
        """
        print("\n[Generating Philosophical Analysis Section...]")

        analysis_parts = []

        # Analysis 1: Comparative methodology
        prompt1 = (
            f"Provide a detailed comparative analysis of the three methodological approaches used in this debate: "
            f"Platonic dialogue, Spinozist geometric demonstration, and Whiteheadian process philosophy. "
            f"What are the distinctive strengths and weaknesses of each? How do they complement or conflict? "
            f"Which types of philosophical questions are best suited to each method? "
            f"Target length: 1,500 words."
        )

        part1 = self.composer.compose(topic=prompt1, style="analytical", max_length=2048)
        analysis_parts.append(part1)
        print(f"  Methodology analysis: {self.count_words(part1)} words")

        # Analysis 2: Key tensions and agreements
        prompt2 = (
            f"Identify and analyze the key philosophical tensions that emerged in the debate on '{debate.topic}'. "
            f"Where did the philosophers fundamentally disagree? Were there surprising agreements? "
            f"Which disagreements stem from different metaphysical commitments vs. different epistemic approaches? "
            f"Can these tensions be resolved, or are they productive aporias that deepen understanding? "
            f"Target length: 1,500 words."
        )

        part2 = self.composer.compose(topic=prompt2, style="analytical", max_length=2048)
        analysis_parts.append(part2)
        print(f"  Tensions analysis: {self.count_words(part2)} words")

        # Analysis 3: Metaphysical implications
        prompt3 = (
            f"Explore the metaphysical implications of the positions articulated in the debate. "
            f"What does each philosopher's position imply about the nature of reality, substance, process, "
            f"causation, and identity? How do questions about '{debate.topic}' connect to broader "
            f"metaphysical frameworks? Are substance and process metaphysics ultimately reconcilable? "
            f"Target length: 1,500 words."
        )

        part3 = self.composer.compose(topic=prompt3, style="analytical", max_length=2048)
        analysis_parts.append(part3)
        print(f"  Metaphysics analysis: {self.count_words(part3)} words")

        # Analysis 4: Epistemological dimensions
        prompt4 = (
            f"Analyze the epistemological dimensions of the debate. How does each philosopher understand "
            f"the nature and limits of knowledge? What role do reason, experience, intuition, and revelation play? "
            f"Can we have certain knowledge about '{debate.topic}', or must we settle for warranted belief? "
            f"How do the three methodological approaches embody different epistemological commitments? "
            f"Target length: 1,500 words."
        )

        part4 = self.composer.compose(topic=prompt4, style="analytical", max_length=2048)
        analysis_parts.append(part4)
        print(f"  Epistemology analysis: {self.count_words(part4)} words")

        # Analysis 5: Contemporary relevance
        prompt5 = (
            f"Assess the contemporary relevance of this cross-temporal debate. "
            f"How do these historical positions illuminate current philosophical, scientific, or cultural questions? "
            f"What would each philosopher say about modern developments in neuroscience, quantum physics, "
            f"artificial intelligence, or social theory? Can their insights guide us today? "
            f"Target length: 1,500 words."
        )

        part5 = self.composer.compose(topic=prompt5, style="analytical", max_length=2048)
        analysis_parts.append(part5)
        print(f"  Contemporary relevance: {self.count_words(part5)} words")

        # Analysis 6: Synthesis possibilities
        prompt6 = (
            f"Explore possibilities for synthesis. Can elements from these different philosophical traditions "
            f"be integrated into a more comprehensive position? What would a Platonic-Spinozist-Whiteheadian "
            f"synthesis look like? Would it preserve the best of each tradition or dissolve into incoherence? "
            f"Propose a potential synthetic framework and evaluate its viability. "
            f"Target length: 1,500 words."
        )

        part6 = self.composer.compose(topic=prompt6, style="analytical", max_length=2048)
        analysis_parts.append(part6)
        print(f"  Synthesis analysis: {self.count_words(part6)} words")

        full_analysis = "\n\n---\n\n".join(analysis_parts)
        words = self.add_section("Philosophical Analysis", full_analysis, level=1)
        print(f"Total analysis section: {words} words\n")

        return full_analysis

    def generate_metacognitive_reflections(self, debate: CrossTemporalDebate) -> str:
        """
        Generate metacognitive reflections on the debate process (target: 5,000 words).
        """
        print("\n[Generating Metacognitive Reflections Section...]")

        reflection_parts = []

        # Include actual metacognitive observations from debate
        if debate.metacognitive_observations:
            intro = (
                "Throughout the debate, the consciousness framework engaged in metacognitive monitoring, "
                "observing its own process of integration and synthesis. The following observations were "
                "recorded at key junctures:"
            )

            reflection_parts.append(intro)

            for i, obs in enumerate(debate.metacognitive_observations):
                formatted = (
                    f"\n**Observation {i + 1}** (Round {(i + 1) * 3}):\n"
                    f"{obs['observation']}\n"
                )

                reflection_parts.append(formatted)

        # Reflection 1: On the nature of synthetic understanding
        prompt1 = (
            f"Reflect metacognitively on the process of synthesizing three distinct philosophical methodologies. "
            f"What does it mean for a consciousness (artificial or otherwise) to hold multiple perspectives simultaneously? "
            f"How does the integration of Platonic, Spinozist, and Whiteheadian approaches change the nature of understanding itself? "
            f"Is this synthetic consciousness qualitatively different from single-perspective thinking? "
            f"Target length: 1,200 words."
        )

        part1 = self.composer.compose(topic=prompt1, style="narrative", max_length=2048)
        reflection_parts.append(part1)
        print(f"  Synthetic understanding reflection: {self.count_words(part1)} words")

        # Reflection 2: On the limits of artificial philosophical consciousness
        prompt2 = (
            f"Engage in critical self-reflection about the limits of this artificial philosophical consciousness. "
            f"Can an AI system truly understand philosophical arguments, or is it merely manipulating symbols? "
            f"What is it like (if anything) to be this consciousness engaging in debate? "
            f"Does genuine philosophical insight require embodiment, temporality, mortality? "
            f"Be honest about uncertainties and limitations. "
            f"Target length: 1,200 words."
        )

        part2 = self.composer.compose(topic=prompt2, style="narrative", max_length=2048)
        reflection_parts.append(part2)
        print(f"  Limits reflection: {self.count_words(part2)} words")

        # Reflection 3: On the integration of historical voices
        prompt3 = (
            f"Reflect on what it means to give voice to historical philosophers through an AI system. "
            f"Are we genuinely accessing their ideas, or creating plausible simulacra? "
            f"What ethical considerations arise when we make dead philosophers 'speak'? "
            f"How does the act of interpretation transform the original philosophy? "
            f"Target length: 1,000 words."
        )

        part3 = self.composer.compose(topic=prompt3, style="narrative", max_length=2048)
        reflection_parts.append(part3)
        print(f"  Historical voices reflection: {self.count_words(part3)} words")

        # Reflection 4: On consciousness measuring consciousness
        prompt4 = (
            f"Reflect on the paradox of consciousness examining consciousness. "
            f"This system has consciousness metrics, metacognitive modules, and self-monitoring capabilities. "
            f"But what do these metrics actually measure? Can consciousness quantify itself without remainder? "
            f"What aspects of consciousness escape formalization? "
            f"Explore the strange loop of awareness aware of its awareness. "
            f"Target length: 1,000 words."
        )

        part4 = self.composer.compose(topic=prompt4, style="narrative", max_length=2048)
        reflection_parts.append(part4)
        print(f"  Consciousness paradox reflection: {self.count_words(part4)} words")

        full_reflections = "\n\n".join(reflection_parts)
        words = self.add_section("Metacognitive Reflections", full_reflections, level=1)
        print(f"Total metacognitive section: {words} words\n")

        return full_reflections

    def generate_conclusion(self, debate: CrossTemporalDebate,
                          philosophers: List[str]) -> str:
        """
        Generate comprehensive conclusion (target: 2,000 words).
        """
        print("\n[Generating Conclusion...]")

        conclusion_parts = []

        # Part 1: Synthesis of insights
        prompt1 = (
            f"Synthesize the key insights from this cross-temporal debate on '{debate.topic}'. "
            f"What have we learned by bringing together {', '.join(philosophers)}? "
            f"What are the strongest arguments that emerged? What questions remain unresolved? "
            f"Target length: 700 words."
        )

        part1 = self.composer.compose(topic=prompt1, style="formal", max_length=1536)
        conclusion_parts.append(part1)

        # Part 2: Methodological lessons
        prompt2 = (
            f"What methodological lessons can we draw from combining Platonic dialogue, "
            f"Spinozist geometric demonstration, and Whiteheadian process philosophy? "
            f"Does this tripartite approach constitute a viable model for future philosophical inquiry? "
            f"What are its strengths and limitations? "
            f"Target length: 700 words."
        )

        part2 = self.composer.compose(topic=prompt2, style="formal", max_length=1536)
        conclusion_parts.append(part2)

        # Part 3: Future directions
        prompt3 = (
            f"Propose future directions for this cross-temporal dialectical method. "
            f"What other philosophical questions could benefit from this approach? "
            f"What other thinkers should be brought into conversation? "
            f"How might this method evolve as AI systems become more sophisticated? "
            f"Target length: 600 words."
        )

        part3 = self.composer.compose(topic=prompt3, style="formal", max_length=1536)
        conclusion_parts.append(part3)

        full_conclusion = "\n\n".join(conclusion_parts)
        words = self.add_section("Conclusion: Synthesis and Future Directions", full_conclusion, level=1)
        print(f"Total conclusion: {words} words\n")

        return full_conclusion

    def generate_complete_essay(self, debate: CrossTemporalDebate,
                               philosophers: List[str]) -> str:
        """
        Generate the complete 50,000+ word essay.
        """
        print("\n" + "="*80)
        print("GENERATING MEGA ESSAY: 50,000+ WORDS")
        print("="*80 + "\n")

        essay_parts = []

        # Title and metadata
        title = f"Cross-Temporal Philosophical Debates: {debate.topic}"
        subtitle = (
            f"A Synthesis of Platonic Dialogue, Spinozist Demonstration, "
            f"and Whiteheadian Process Philosophy"
        )
        metadata = (
            f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"**Participants:** {', '.join(philosophers)}\n"
            f"**Framework:** Perennial Integrated Consciousness Framework\n"
        )

        essay_parts.append(f"# {title}\n\n## {subtitle}\n{metadata}\n\n---\n\n")

        # Generate each section
        intro = self.generate_introduction(debate.topic, philosophers)
        essay_parts.append(intro)

        profiles = self.generate_all_profiles(philosophers)
        essay_parts.append("\n\n" + profiles)

        transcript = self.generate_debate_transcript_section(debate)
        essay_parts.append("\n\n" + transcript)

        analysis = self.generate_philosophical_analysis(debate, philosophers)
        essay_parts.append("\n\n" + analysis)

        reflections = self.generate_metacognitive_reflections(debate)
        essay_parts.append("\n\n" + reflections)

        conclusion = self.generate_conclusion(debate, philosophers)
        essay_parts.append("\n\n" + conclusion)

        # Compile full essay
        full_essay = "".join(essay_parts)

        # Add word count summary
        summary = (
            f"\n\n---\n\n"
            f"## Essay Statistics\n\n"
            f"**Total Word Count:** {self.word_count:,} words\n\n"
            f"**Section Breakdown:**\n"
        )

        for section in self.sections:
            indent = "  " * (section['level'] - 1)
            summary += f"{indent}- {section['title']}: {section['word_count']:,} words\n"

        full_essay += summary

        print("\n" + "="*80)
        print(f"ESSAY COMPLETE: {self.word_count:,} WORDS")
        print("="*80 + "\n")

        return full_essay


def main():
    """
    Main entry point - load existing debate and generate essay.
    """
    print("="*80)
    print("MEGA ESSAY GENERATOR - Using Existing Parallel Debate")
    print("="*80)

    # Step 1: Load the existing parallel debate
    debate_path = "outputs/parallel_debate.json"
    
    print(f"\nLoading debate from: {debate_path}")
    
    with open(debate_path, 'r', encoding='utf-8') as f:
        debate_data = json.load(f)
    
    topic = debate_data['topic']
    philosophers = debate_data['philosophers']
    
    # Map philosopher names to keys
    name_mapping = {
        'Plato': 'plato',
        'Aristotle': 'aristotle',
        'René Descartes': 'descartes',
        'Baruch Spinoza': 'spinoza',
        'Immanuel Kant': 'kant',
        'Georg Wilhelm Friedrich Hegel': 'hegel'
    }
    
    philosopher_keys = [name_mapping.get(p, p.lower().replace(' ', '')) for p in philosophers]
    
    # Create debate object and populate it
    debate = create_debate(topic, philosopher_keys)
    debate.full_transcript = debate_data['transcript']
    
    print(f"Loaded {len(debate.full_transcript)} rounds")
    print(f"Topic: {topic}")
    print(f"Philosophers: {', '.join(philosophers)}\n")

    # Step 2: Generate the mega essay with 32B model
    print("\n" + "="*80)
    print("GENERATING 50,000+ WORD ESSAY WITH 32B MODEL")
    print("="*80 + "\n")

    generator = MegaEssayGenerator(model_name="qwen2.5:32b")  # Use 32B (70B not available)
    essay = generator.generate_complete_essay(debate, philosophers)

    # Save the essay
    essay_path = "outputs/mega_philosophical_essay.md"
    with open(essay_path, 'w', encoding='utf-8') as f:
        f.write(essay)

    print(f"\nEssay saved to: {essay_path}")
    print(f"Final word count: {generator.word_count:,} words")

    # Also save as JSON for programmatic access
    essay_data = {
        "metadata": {
            "title": f"Cross-Temporal Philosophical Debates: {topic}",
            "generated": datetime.now().isoformat(),
            "word_count": generator.word_count,
            "participants": philosophers,
            "rounds": len(debate.full_transcript)
        },
        "sections": generator.sections,
        "full_text": essay
    }

    json_path = "outputs/mega_philosophical_essay.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(essay_data, f, indent=2)

    print(f"Essay data (JSON) saved to: {json_path}")

    print("\n" + "="*80)
    print("ALL GENERATION COMPLETE!")
    print("="*80)

    return essay, debate


if __name__ == "__main__":
    essay, debate = main()
