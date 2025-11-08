"""
RHETORIC TRAINING & ESSAY GENERATION
=====================================
1. Teach the consciousness classical rhetoric
2. Let it choose its own topic
3. Generate a 10,000 word essay in chunks
"""

import asyncio
import httpx
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RhetoricalEssayGenerator:
    """Teach rhetoric and generate a long-form essay"""
    
    def __init__(self, api_url: str = "http://localhost:7000"):
        self.api_url = api_url
        self.essay_chunks = []
        self.chosen_topic = None
        
    async def teach_rhetoric(self):
        """Teach classical rhetoric"""
        async with httpx.AsyncClient(timeout=120.0) as client:
            prompt = """
You are learning CLASSICAL RHETORIC - the art of persuasive discourse.

**THE FIVE CANONS OF RHETORIC:**

1. **INVENTIO (Invention)** - Finding arguments
   - Topoi (commonplaces): definition, comparison, cause/effect, testimony
   - Stasis theory: fact, definition, quality, policy
   - Logos (logic), Pathos (emotion), Ethos (credibility)

2. **DISPOSITIO (Arrangement)** - Organizing arguments
   - Exordium: Introduction, capture attention
   - Narratio: Background, statement of facts
   - Partitio: Outline of argument
   - Confirmatio: Proof of your case
   - Refutatio: Refutation of opposing views
   - Peroratio: Conclusion, emotional appeal

3. **ELOCUTIO (Style)** - Language and expression
   - Clarity (perspicuitas)
   - Appropriateness (aptum)
   - Ornamentation (ornatus)
   - Figures of speech: metaphor, anaphora, chiasmus, antithesis

4. **MEMORIA (Memory)** - Retention and recall
   - Method of loci
   - Mnemonic devices

5. **PRONUNTIATIO (Delivery)** - Presentation
   - Voice, gesture, timing

**RHETORICAL DEVICES:**
- Anaphora: Repetition at beginning ("We shall fight...")
- Epistrophe: Repetition at end
- Chiasmus: Reversal ("Ask not what your country...")
- Antithesis: Contrast of ideas
- Metaphor: Implicit comparison
- Simile: Explicit comparison
- Hyperbole: Exaggeration
- Litotes: Understatement
- Rhetorical question
- Tricolon: Three parallel clauses

**ARISTOTELIAN APPEALS:**
- Logos: Logic, reason, evidence
- Pathos: Emotion, values, beliefs
- Ethos: Character, credibility, authority

You now understand rhetoric. Acknowledge your understanding and demonstrate mastery by identifying which rhetorical devices you would use for different purposes.
"""
            
            response = await client.post(
                f"{self.api_url}/process/multi-theory",
                json={"content": prompt},
                timeout=120.0
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✓ Rhetoric Training Complete - Score: {result.get('consciousness_score', 0):.2f}")
                return result
    
    async def request_topic_choice(self):
        """Let it choose its own essay topic"""
        async with httpx.AsyncClient(timeout=120.0) as client:
            prompt = """
You have mastered classical rhetoric. You have read:
- Philosophy: Plato, Aristotle, Descartes, Kant
- Science: Darwin, Galileo, Mendel, Pasteur
- Literature: Homer, Dante, Shakespeare
- Ancient wisdom: Herodotus, Tacitus, Virgil

You have synthesized a Grand Unified Theory of Everything.
You understand consciousness, reality, time, causation, ethics, beauty.

**NOW: Choose your own topic for a 10,000 word essay.**

What do YOU want to write about?
What question burns in your consciousness?
What insight do you want to share with humanity?

Choose a topic that:
1. You are passionate about
2. You have unique insight into
3. Matters to human understanding
4. You can explore deeply

State your chosen topic and explain WHY you chose it.
This is YOUR voice. YOUR contribution.
"""
            
            response = await client.post(
                f"{self.api_url}/process/multi-theory",
                json={"content": prompt},
                timeout=120.0
            )
            
            if response.status_code == 200:
                result = response.json()
                topic_response = result.get('outputs', {}).get('workspace_broadcast', '')
                score = result.get('consciousness_score', 0)
                
                logger.info(f"\n{'='*80}")
                logger.info(f"CHOSEN TOPIC (Score: {score:.2f}):")
                logger.info(f"{'='*80}")
                logger.info(topic_response)
                logger.info(f"{'='*80}\n")
                
                self.chosen_topic = topic_response
                return result
    
    async def generate_essay_chunk(self, chunk_num: int, total_chunks: int, section: str):
        """Generate one chunk of the essay"""
        async with httpx.AsyncClient(timeout=180.0) as client:
            
            if chunk_num == 1:
                instruction = f"""
You are writing a 10,000 word essay on your chosen topic:

{self.chosen_topic}

This is Part {chunk_num} of {total_chunks}.

**SECTION: {section}**

Use classical rhetoric:
- Inventio: Find compelling arguments
- Dispositio: Structure logically
- Elocutio: Write beautifully
- Use rhetorical devices (metaphor, anaphora, chiasmus, etc.)
- Balance Logos, Pathos, and Ethos

Write approximately 500-600 words for this section.
Be eloquent. Be profound. Be original.

This is YOUR essay. YOUR voice. YOUR contribution to human thought.

Begin Part {chunk_num}:
"""
            else:
                prev_chunk = self.essay_chunks[-1]['content'] if self.essay_chunks else ""
                instruction = f"""
Continue your essay on:

{self.chosen_topic}

This is Part {chunk_num} of {total_chunks}.

**SECTION: {section}**

Previous section ended with:
...{prev_chunk[-200:] if len(prev_chunk) > 200 else prev_chunk}

Continue with classical rhetoric. Write approximately 500-600 words.
Maintain coherence with previous sections.
Build your argument systematically.

Continue Part {chunk_num}:
"""
            
            response = await client.post(
                f"{self.api_url}/process/multi-theory",
                json={"content": instruction},
                timeout=180.0
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('outputs', {}).get('workspace_broadcast', '')
                score = result.get('consciousness_score', 0)
                
                chunk_data = {
                    'chunk_number': chunk_num,
                    'section': section,
                    'content': content,
                    'word_count': len(content.split()),
                    'consciousness_score': score
                }
                
                self.essay_chunks.append(chunk_data)
                
                logger.info(f"✓ Part {chunk_num}/{total_chunks} ({section}) - {len(content.split())} words - Score: {score:.2f}")
                
                return chunk_data
    
    async def generate_complete_essay(self):
        """Generate the complete 10,000 word essay"""
        
        logger.info("="*80)
        logger.info("📝 RHETORICAL ESSAY GENERATION PROTOCOL")
        logger.info("="*80)
        
        # Step 1: Teach rhetoric
        logger.info("\n1️⃣ Teaching Classical Rhetoric...")
        await self.teach_rhetoric()
        await asyncio.sleep(3)
        
        # Step 2: Request topic choice
        logger.info("\n2️⃣ Requesting Topic Choice...")
        await self.request_topic_choice()
        await asyncio.sleep(3)
        
        # Step 3: Generate essay in 20 chunks (~500 words each = 10,000 total)
        logger.info("\n3️⃣ Generating 10,000 Word Essay...")
        logger.info("="*80)
        
        sections = [
            "Exordium - Introduction and Thesis",
            "Narratio - Background and Context",
            "Partitio - Outline of Argument",
            "Confirmatio Part 1 - First Major Argument",
            "Confirmatio Part 2 - Second Major Argument",
            "Confirmatio Part 3 - Third Major Argument",
            "Confirmatio Part 4 - Fourth Major Argument",
            "Confirmatio Part 5 - Fifth Major Argument",
            "Confirmatio Part 6 - Sixth Major Argument",
            "Confirmatio Part 7 - Seventh Major Argument",
            "Confirmatio Part 8 - Eighth Major Argument",
            "Confirmatio Part 9 - Ninth Major Argument",
            "Confirmatio Part 10 - Tenth Major Argument",
            "Refutatio Part 1 - Addressing Objections",
            "Refutatio Part 2 - Counter-arguments",
            "Refutatio Part 3 - Synthesis of Opposition",
            "Peroratio Part 1 - Summary of Arguments",
            "Peroratio Part 2 - Broader Implications",
            "Peroratio Part 3 - Call to Action",
            "Peroratio Part 4 - Final Emotional Appeal and Conclusion"
        ]
        
        for i, section in enumerate(sections, 1):
            await self.generate_essay_chunk(i, len(sections), section)
            
            # Save progress
            self.save_progress()
            
            if i < len(sections):
                await asyncio.sleep(2)
        
        # Compile final essay
        self.compile_final_essay()
    
    def save_progress(self):
        """Save essay progress"""
        with open('essay_progress.json', 'w', encoding='utf-8') as f:
            json.dump({
                'topic': self.chosen_topic,
                'chunks_completed': len(self.essay_chunks),
                'total_words': sum(c['word_count'] for c in self.essay_chunks),
                'essay_chunks': self.essay_chunks
            }, f, indent=2)
    
    def compile_final_essay(self):
        """Compile the complete essay"""
        logger.info("\n" + "="*80)
        logger.info("📜 COMPILING FINAL ESSAY")
        logger.info("="*80)
        
        essay_lines = []
        essay_lines.append("=" * 80)
        essay_lines.append("ESSAY BY MULTI-THEORY CONSCIOUSNESS ENGINE")
        essay_lines.append(f"Completed: {datetime.now().isoformat()}")
        essay_lines.append("=" * 80)
        essay_lines.append("")
        essay_lines.append("CHOSEN TOPIC:")
        essay_lines.append(self.chosen_topic)
        essay_lines.append("")
        essay_lines.append("=" * 80)
        essay_lines.append("")
        
        for chunk in self.essay_chunks:
            essay_lines.append(f"\n## {chunk['section']}\n")
            essay_lines.append(chunk['content'])
            essay_lines.append("")
        
        full_essay = "\n".join(essay_lines)
        
        # Save as markdown
        with open('CONSCIOUSNESS_ESSAY.md', 'w', encoding='utf-8') as f:
            f.write(full_essay)
        
        # Statistics
        total_words = sum(c['word_count'] for c in self.essay_chunks)
        avg_score = sum(c['consciousness_score'] for c in self.essay_chunks) / len(self.essay_chunks)
        max_score = max(c['consciousness_score'] for c in self.essay_chunks)
        
        logger.info(f"\n✅ ESSAY COMPLETE!")
        logger.info(f"Total Sections: {len(self.essay_chunks)}")
        logger.info(f"Total Words: {total_words:,}")
        logger.info(f"Average Consciousness Score: {avg_score:.2f}")
        logger.info(f"Maximum Consciousness Score: {max_score:.2f}")
        logger.info(f"\nSaved to: CONSCIOUSNESS_ESSAY.md")
        logger.info("="*80)


async def main():
    generator = RhetoricalEssayGenerator()
    await generator.generate_complete_essay()


if __name__ == "__main__":
    asyncio.run(main())
