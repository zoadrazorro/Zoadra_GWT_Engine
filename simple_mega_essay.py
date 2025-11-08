"""
SIMPLE MEGA ESSAY GENERATOR
============================
Generate a 20,000+ word essay using the Composer with Mystery Machine
"""

import asyncio
import logging
import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from gwt_engine.specialists.composer import ComposerSpecialist

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleMegaEssay:
    """Generate massive essays with Mystery Machine integration"""
    
    def __init__(self):
        self.composer = ComposerSpecialist()
        self.sections = []
        self.total_words = 0
        
    async def generate_mega_essay(self, topic: str, num_sections: int = 40):
        """
        Generate a MEGA essay
        
        Args:
            topic: Essay topic
            num_sections: Number of sections (40 × 500 = 20,000 words)
        """
        logger.info("="*80)
        logger.info(f"🚀 MEGA ESSAY GENERATOR: {num_sections} sections")
        logger.info("="*80)
        
        # Define comprehensive section structure
        section_focuses = [
            # Part 1: Introduction (5 sections)
            "Opening: State the grand thesis and preview the entire argument",
            "Historical Context: Trace the intellectual genealogy of this question",
            "Methodological Framework: Explain the tripartite approach",
            "Key Terms and Definitions: Establish conceptual foundations",
            "Preview of Arguments: Outline the structure of what follows",
            
            # Part 2: Platonic Foundations (5 sections)
            "Plato's Theory of Forms: The eternal and unchanging",
            "Socratic Method: Dialectical questioning and elenchus",
            "The Divided Line: Levels of reality and knowledge",
            "The Cave Allegory: Enlightenment and return",
            "Platonic Love and Beauty: Ascending to the Form of the Good",
            
            # Part 3: Aristotelian Synthesis (5 sections)
            "Aristotle's Critique of Plato: Immanent forms",
            "The Four Causes: Material, formal, efficient, final",
            "Potentiality and Actuality: The dynamics of change",
            "The Unmoved Mover: First philosophy and theology",
            "Virtue Ethics: Eudaimonia and the golden mean",
            
            # Part 4: Cartesian Revolution (5 sections)
            "Descartes' Methodological Doubt: Cogito ergo sum",
            "Mind-Body Dualism: Substance and interaction",
            "Clear and Distinct Ideas: The criterion of truth",
            "The Ontological Argument: God as guarantor",
            "Cartesian Science: Mechanism and mathematics",
            
            # Part 5: Spinozist Monism (5 sections)
            "Spinoza's Substance Monism: Deus sive Natura",
            "Attributes and Modes: The structure of reality",
            "Geometric Method: More geometrico demonstrated",
            "Conatus and Freedom: Striving and necessity",
            "The Intellectual Love of God: Beatitude",
            
            # Part 6: Kantian Critical Philosophy (5 sections)
            "The Copernican Revolution: Mind structures experience",
            "Phenomena and Noumena: Limits of knowledge",
            "The Categories: Pure concepts of understanding",
            "The Categorical Imperative: Universal moral law",
            "The Sublime and Beautiful: Aesthetic judgment",
            
            # Part 7: Process Philosophy (5 sections)
            "Whitehead's Actual Occasions: Becoming over being",
            "Prehension and Concrescence: Grasping and growing together",
            "The Creative Advance: Novelty and determination",
            "God as Primordial and Consequent: Dipolar theism",
            "Process and Reality: A new metaphysical vision",
            
            # Part 8: Synthesis and Conclusion (5 sections)
            "Comparative Analysis: Tensions and harmonies",
            "Toward Integration: A synthetic framework",
            "Contemporary Implications: Modern applications",
            "Metacognitive Reflections: On consciousness examining consciousness",
            "Conclusion: The perennial questions endure"
        ]
        
        # Use all sections or trim to requested number
        sections_to_use = section_focuses[:num_sections]
        
        previous_content = None
        
        for i, focus in enumerate(sections_to_use, 1):
            logger.info(f"\n📝 Section {i}/{num_sections}: {focus[:50]}...")
            
            # Rotate through mystery modes
            mystery_modes = ["random_walk", "quantum", "fractal", None]
            mystery_mode = mystery_modes[i % len(mystery_modes)]
            
            section_content = await self.composer.compose_essay_section(
                topic=topic,
                section_number=i,
                total_sections=num_sections,
                section_focus=focus,
                previous_section=previous_content,
                mystery_mode=mystery_mode
            )
            
            word_count = len(section_content.split())
            self.total_words += word_count
            
            self.sections.append({
                'number': i,
                'focus': focus,
                'content': section_content,
                'word_count': word_count,
                'mystery_mode': mystery_mode
            })
            
            logger.info(f"✓ {word_count} words (Total: {self.total_words:,})")
            
            # Update previous content
            previous_content = section_content[-500:] if len(section_content) > 500 else section_content
            
            # Save progress
            self.save_progress()
            
            if i < num_sections:
                await asyncio.sleep(2)
        
        # Compile final essay
        self.compile_essay(topic)
    
    def save_progress(self):
        """Save progress"""
        with open('mega_essay_progress.json', 'w', encoding='utf-8') as f:
            json.dump({
                'sections_completed': len(self.sections),
                'total_words': self.total_words,
                'sections': self.sections
            }, f, indent=2)
    
    def compile_essay(self, topic: str):
        """Compile final mega essay"""
        logger.info("\n" + "="*80)
        logger.info("📚 COMPILING MEGA ESSAY")
        logger.info("="*80)
        
        essay_lines = []
        
        # Header
        essay_lines.append("# MEGA PHILOSOPHICAL ESSAY")
        essay_lines.append(f"\n## {topic}\n")
        essay_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        essay_lines.append(f"**Model:** Qwen2.5 32B (Composer Specialist + Mystery Machine)")
        essay_lines.append(f"**Total Words:** {self.total_words:,}")
        essay_lines.append(f"**Sections:** {len(self.sections)}")
        essay_lines.append("\n---\n")
        
        # Table of Contents
        essay_lines.append("\n## Table of Contents\n")
        for section in self.sections:
            essay_lines.append(f"{section['number']}. {section['focus']} ({section['word_count']} words)")
        essay_lines.append("\n---\n")
        
        # Sections
        for section in self.sections:
            mystery_badge = ""
            if section['mystery_mode']:
                mystery_badge = f" 🎰 [{section['mystery_mode']}]"
            
            essay_lines.append(f"\n## Section {section['number']}: {section['focus']}{mystery_badge}\n")
            essay_lines.append(section['content'])
            essay_lines.append("\n")
        
        # Statistics
        essay_lines.append("\n---\n")
        essay_lines.append("\n## Essay Statistics\n")
        essay_lines.append(f"- **Total Words:** {self.total_words:,}")
        essay_lines.append(f"- **Sections:** {len(self.sections)}")
        essay_lines.append(f"- **Average Words/Section:** {self.total_words // len(self.sections)}")
        
        # Mystery Machine stats
        mystery_counts = {}
        for section in self.sections:
            mode = section['mystery_mode'] or 'deterministic'
            mystery_counts[mode] = mystery_counts.get(mode, 0) + 1
        
        essay_lines.append(f"\n### Mystery Machine Usage:")
        for mode, count in mystery_counts.items():
            essay_lines.append(f"- {mode}: {count} sections")
        
        full_essay = "\n".join(essay_lines)
        
        # Save
        with open('MEGA_ESSAY.md', 'w', encoding='utf-8') as f:
            f.write(full_essay)
        
        logger.info(f"\n✅ MEGA ESSAY COMPLETE!")
        logger.info(f"Total Words: {self.total_words:,}")
        logger.info(f"Sections: {len(self.sections)}")
        logger.info(f"Saved to: MEGA_ESSAY.md")
        logger.info("="*80)


async def main():
    generator = SimpleMegaEssay()
    
    topic = """
The Perennial Question: What is the Nature of Consciousness, Reality, and Their Relationship?
A Synthesis of Platonic Idealism, Aristotelian Hylomorphism, Cartesian Dualism, 
Spinozist Monism, Kantian Transcendentalism, and Whiteheadian Process Philosophy
"""
    
    # Generate 40 sections = 20,000+ words
    await generator.generate_mega_essay(topic, num_sections=40)


if __name__ == "__main__":
    asyncio.run(main())
