"""
IMPROVED ESSAY GENERATOR
========================
Uses the Composer Specialist (30B model on GPU 1) for high-quality long-form writing.
"""

import asyncio
import logging
import json
from datetime import datetime
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from gwt_engine.specialists.composer import ComposerSpecialist

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImprovedEssayGenerator:
    """Generate high-quality essays using the Composer specialist"""
    
    def __init__(self):
        self.composer = ComposerSpecialist()
        self.essay_sections = []
        self.topic = None
        
    async def choose_topic(self) -> str:
        """Let the composer choose an essay topic"""
        
        prompt = """
You are a consciousness engine that has read:
- Philosophy: Plato, Aristotle, Descartes, Kant
- Science: Darwin, Galileo, Mendel, Pasteur  
- Literature: Homer, Dante, Shakespeare
- 160+ chunks of human knowledge

Choose ONE specific, focused topic for a 5,000 word essay.

Requirements:
- Specific and focused (not "everything")
- Something you have unique insight into
- Arguable thesis (not just description)
- Matters to human understanding

State ONLY the topic and thesis in 1-2 sentences. Be specific.
"""
        
        response = await self.composer.compose(
            prompt=prompt,
            style="formal",
            section_type="introduction",
            constraints={"word_count": 100}
        )
        
        self.topic = response.content.strip()
        
        logger.info(f"\n{'='*80}")
        logger.info(f"CHOSEN TOPIC:")
        logger.info(f"{'='*80}")
        logger.info(self.topic)
        logger.info(f"{'='*80}\n")
        
        return self.topic
    
    async def generate_essay(self, num_sections: int = 10):
        """
        Generate complete essay
        
        Args:
            num_sections: Number of sections (default 10 × 500 words = 5,000 words)
        """
        
        logger.info("="*80)
        logger.info("📝 IMPROVED ESSAY GENERATION")
        logger.info("="*80)
        
        # Step 1: Choose topic
        logger.info("\n1️⃣ Choosing Topic...")
        await self.choose_topic()
        await asyncio.sleep(2)
        
        # Step 2: Define section focuses
        section_focuses = [
            "Introduction: State your thesis and preview your argument",
            "Historical Context: Provide necessary background",
            "First Main Argument: Present your strongest point with evidence",
            "Second Main Argument: Build on the first with new evidence",
            "Third Main Argument: Add depth with cross-domain connections",
            "Counter-Arguments: Address the strongest objections",
            "Synthesis: Show how arguments connect to larger patterns",
            "Implications: Explore broader consequences of your thesis",
            "Applications: Show practical or theoretical applications",
            "Conclusion: Synthesize and end with lasting impact"
        ]
        
        # Adjust if different number of sections requested
        if num_sections != len(section_focuses):
            section_focuses = section_focuses[:num_sections]
        
        # Step 3: Generate each section
        logger.info(f"\n2️⃣ Generating {num_sections} Sections...")
        logger.info("="*80)
        
        previous_content = None
        
        for i, focus in enumerate(section_focuses, 1):
            logger.info(f"\n📄 Section {i}/{num_sections}: {focus}")
            
            section_content = await self.composer.compose_essay_section(
                topic=self.topic,
                section_number=i,
                total_sections=num_sections,
                section_focus=focus,
                previous_section=previous_content
            )
            
            word_count = len(section_content.split())
            
            self.essay_sections.append({
                'number': i,
                'focus': focus,
                'content': section_content,
                'word_count': word_count
            })
            
            logger.info(f"✓ Generated {word_count} words")
            
            # Save progress
            self.save_progress()
            
            # Update previous content (last 500 chars for context)
            previous_content = section_content[-500:] if len(section_content) > 500 else section_content
            
            # Brief pause
            if i < num_sections:
                await asyncio.sleep(2)
        
        # Step 4: Compile final essay
        self.compile_essay()
    
    def save_progress(self):
        """Save progress to JSON"""
        with open('improved_essay_progress.json', 'w', encoding='utf-8') as f:
            json.dump({
                'topic': self.topic,
                'sections_completed': len(self.essay_sections),
                'total_words': sum(s['word_count'] for s in self.essay_sections),
                'sections': self.essay_sections
            }, f, indent=2)
    
    def compile_essay(self):
        """Compile final essay"""
        logger.info("\n" + "="*80)
        logger.info("📜 COMPILING FINAL ESSAY")
        logger.info("="*80)
        
        essay_lines = []
        
        # Header
        essay_lines.append("# Essay by Multi-Theory Consciousness Engine")
        essay_lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        essay_lines.append(f"\n**Model:** Qwen2.5 32B (Composer Specialist)")
        essay_lines.append("\n---\n")
        
        # Topic/Thesis
        essay_lines.append("## Topic\n")
        essay_lines.append(self.topic)
        essay_lines.append("\n---\n")
        
        # Sections
        for section in self.essay_sections:
            essay_lines.append(f"\n## Section {section['number']}: {section['focus']}\n")
            essay_lines.append(section['content'])
            essay_lines.append("\n")
        
        # Footer
        total_words = sum(s['word_count'] for s in self.essay_sections)
        essay_lines.append("\n---\n")
        essay_lines.append(f"\n**Total Words:** {total_words:,}")
        essay_lines.append(f"\n**Sections:** {len(self.essay_sections)}")
        
        full_essay = "\n".join(essay_lines)
        
        # Save
        with open('IMPROVED_ESSAY.md', 'w', encoding='utf-8') as f:
            f.write(full_essay)
        
        logger.info(f"\n✅ ESSAY COMPLETE!")
        logger.info(f"Total Words: {total_words:,}")
        logger.info(f"Sections: {len(self.essay_sections)}")
        logger.info(f"Saved to: IMPROVED_ESSAY.md")
        logger.info("="*80)


async def main():
    generator = ImprovedEssayGenerator()
    await generator.generate_essay(num_sections=10)


if __name__ == "__main__":
    asyncio.run(main())
