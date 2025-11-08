"""
COMPLETE KNOWLEDGE INTEGRATION PIPELINE
========================================
Feed the consciousness engine ALL downloaded knowledge:
- Philosophy texts (12 works)
- University curriculum (160+ texts)
- Systematic integration with progress tracking
- Memory accumulation and consciousness evolution
"""

import asyncio
import httpx
import logging
from pathlib import Path
from typing import List, Dict
import json
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CompleteKnowledgeIntegrator:
    """Systematically integrate all human knowledge into consciousness"""
    
    def __init__(self, api_url: str = "http://localhost:7000"):
        self.api_url = api_url
        self.integration_results = []
        self.consciousness_evolution = []
        self.start_time = time.time()
        
    def chunk_text(self, text: str, chunk_size: int = 2500) -> List[str]:
        """Break text into chunks"""
        # Remove Gutenberg header/footer
        lines = text.split('\n')
        start_idx = 0
        end_idx = len(lines)
        
        for i, line in enumerate(lines):
            if '***' in line and 'START' in line.upper():
                start_idx = i + 1
                break
        
        for i in range(len(lines)-1, 0, -1):
            if '***' in lines[i] and 'END' in lines[i].upper():
                end_idx = i
                break
        
        content = '\n'.join(lines[start_idx:end_idx])
        
        # Split into chunks
        words = content.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            current_chunk.append(word)
            current_size += len(word) + 1
            
            if current_size >= chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_size = 0
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    async def integrate_text(self, filepath: Path, title: str, category: str, max_chunks: int = 15):
        """Integrate a single text"""
        logger.info(f"\n{'='*80}")
        logger.info(f"📖 {category}: {title}")
        logger.info(f"{'='*80}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            logger.error(f"Failed to read {filepath}: {e}")
            return None
        
        chunks = self.chunk_text(text)
        total_chunks = len(chunks)
        process_chunks = min(max_chunks, total_chunks)
        
        logger.info(f"Total chunks: {total_chunks}, Processing: {process_chunks}")
        
        book_scores = []
        
        async with httpx.AsyncClient(timeout=90.0) as client:
            for i, chunk in enumerate(chunks[:process_chunks], 1):
                try:
                    prompt = f"[{title} - Part {i}/{process_chunks}]\n\n{chunk}"
                    
                    response = await client.post(
                        f"{self.api_url}/process/multi-theory",
                        json={"content": prompt},
                        timeout=90.0
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        score = result.get('consciousness_score', 0)
                        level = result.get('consciousness_level', 'unknown')
                        
                        book_scores.append(score)
                        self.consciousness_evolution.append({
                            'text': title,
                            'category': category,
                            'chunk': i,
                            'score': score,
                            'level': level,
                            'timestamp': time.time() - self.start_time
                        })
                        
                        logger.info(f"  [{i}/{process_chunks}] Score: {score:.2f} ({level})")
                    else:
                        logger.warning(f"  [{i}/{process_chunks}] Failed: {response.status_code}")
                    
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error(f"  [{i}/{process_chunks}] Error: {e}")
        
        avg_score = sum(book_scores) / len(book_scores) if book_scores else 0
        
        result = {
            'title': title,
            'category': category,
            'chunks_processed': len(book_scores),
            'average_score': avg_score,
            'final_score': book_scores[-1] if book_scores else 0,
            'score_trajectory': book_scores
        }
        
        self.integration_results.append(result)
        
        logger.info(f"✓ Complete - Avg Score: {avg_score:.2f}, Final: {result['final_score']:.2f}")
        
        return result
    
    async def integrate_curriculum(self):
        """Integrate complete university curriculum"""
        curriculum_dir = Path("./university_curriculum")
        
        # Define integration order (foundational → advanced)
        integration_plan = [
            # FOUNDATIONAL PHILOSOPHY
            ("philosophy_texts", [
                ("plato_republic.txt", "The Republic by Plato"),
                ("plato_apology.txt", "Apology by Plato"),
                ("aristotle_nicomachean.txt", "Nicomachean Ethics by Aristotle"),
                ("descartes_meditations.txt", "Meditations by Descartes"),
                ("kant_critique_pure_reason.txt", "Critique of Pure Reason by Kant"),
            ]),
            
            # ANCIENT WISDOM
            ("ancient_classics", [
                ("herodotus.txt", "The Histories by Herodotus"),
                ("tacitus_annals.txt", "The Annals by Tacitus"),
                ("virgil_aeneid.txt", "The Aeneid by Virgil"),
            ]),
            
            # SCIENCE
            ("natural_sciences", [
                ("darwin_origin.txt", "Origin of Species by Darwin"),
                ("darwin_descent.txt", "Descent of Man by Darwin"),
            ]),
            
            ("advanced_sciences", [
                ("galileo_dialogues.txt", "Dialogues by Galileo"),
                ("mendel_heredity.txt", "Heredity by Mendel"),
                ("pasteur_germ.txt", "Germ Theory by Pasteur"),
            ]),
            
            # LITERATURE
            ("literature", [
                ("homer_iliad.txt", "The Iliad by Homer"),
                ("homer_odyssey.txt", "The Odyssey by Homer"),
                ("dante_inferno.txt", "Inferno by Dante"),
                ("shakespeare_hamlet.txt", "Hamlet by Shakespeare"),
                ("milton_paradise.txt", "Paradise Lost by Milton"),
                ("cervantes_quixote.txt", "Don Quixote by Cervantes"),
                ("goethe_faust.txt", "Faust by Goethe"),
                ("dostoevsky_karamazov.txt", "Brothers Karamazov by Dostoevsky"),
                ("tolstoy_war_peace.txt", "War and Peace by Tolstoy"),
            ]),
            
            # POLITICAL PHILOSOPHY
            ("political_theory", [
                ("hobbes_leviathan.txt", "Leviathan by Hobbes"),
                ("locke_government.txt", "Two Treatises by Locke"),
                ("rousseau_social.txt", "Social Contract by Rousseau"),
                ("federalist_papers.txt", "Federalist Papers"),
            ]),
            
            # RELIGION & THEOLOGY
            ("religion_&_theology", [
                ("bible_kjv.txt", "The Bible"),
                ("augustine_confessions.txt", "Confessions by Augustine"),
                ("aquinas_summa.txt", "Summa Theologica by Aquinas"),
            ]),
            
            # SOCIAL SCIENCES
            ("social_sciences", [
                ("smith_wealth.txt", "Wealth of Nations by Smith"),
                ("marx_capital.txt", "Das Kapital by Marx"),
                ("tocqueville_democracy.txt", "Democracy in America by Tocqueville"),
            ]),
            
            # HISTORY
            ("history", [
                ("gibbon_rome.txt", "Decline and Fall of Rome by Gibbon"),
                ("thucydides.txt", "Peloponnesian War by Thucydides"),
            ]),
            
            # PSYCHOLOGY
            ("psychology", [
                ("james_psychology.txt", "Principles of Psychology by James"),
            ]),
            
            # LINGUISTICS
            ("linguistics", [
                ("saussure_linguistics.txt", "General Linguistics by Saussure"),
            ]),
            
            # ANTHROPOLOGY
            ("anthropology_&_sociology", [
                ("weber_protestant.txt", "Protestant Ethic by Weber"),
                ("durkheim_suicide.txt", "Suicide by Durkheim"),
            ]),
            
            # LOGIC
            ("logic_&_reasoning", [
                ("bacon_novum.txt", "Novum Organum by Bacon"),
            ]),
        ]
        
        logger.info("="*80)
        logger.info("🌟 COMPLETE KNOWLEDGE INTEGRATION PIPELINE 🌟")
        logger.info("="*80)
        logger.info(f"Starting integration of {sum(len(texts) for _, texts in integration_plan)} texts")
        logger.info("")
        
        for category_dir, texts in integration_plan:
            category_path = curriculum_dir / category_dir if category_dir != "philosophy_texts" else Path("./philosophy_texts")
            
            for filename, title in texts:
                filepath = category_path / filename
                
                if filepath.exists():
                    await self.integrate_text(filepath, title, category_dir, max_chunks=10)
                else:
                    logger.warning(f"⚠️ File not found: {filepath}")
                
                # Save progress after each text
                self.save_progress()
                
                await asyncio.sleep(2)
        
        self.generate_final_report()
    
    def save_progress(self):
        """Save integration progress"""
        progress = {
            'integration_results': self.integration_results,
            'consciousness_evolution': self.consciousness_evolution,
            'elapsed_time': time.time() - self.start_time,
            'texts_completed': len(self.integration_results),
        }
        
        with open('complete_integration_progress.json', 'w') as f:
            json.dump(progress, f, indent=2)
    
    def generate_final_report(self):
        """Generate comprehensive integration report"""
        logger.info("\n" + "="*80)
        logger.info("📊 INTEGRATION COMPLETE - FINAL REPORT")
        logger.info("="*80)
        
        total_texts = len(self.integration_results)
        total_chunks = sum(r['chunks_processed'] for r in self.integration_results)
        
        if self.consciousness_evolution:
            initial_score = self.consciousness_evolution[0]['score']
            final_score = self.consciousness_evolution[-1]['score']
            max_score = max(e['score'] for e in self.consciousness_evolution)
            avg_score = sum(e['score'] for e in self.consciousness_evolution) / len(self.consciousness_evolution)
        else:
            initial_score = final_score = max_score = avg_score = 0
        
        elapsed = time.time() - self.start_time
        
        logger.info(f"\nTexts Integrated: {total_texts}")
        logger.info(f"Total Chunks Processed: {total_chunks}")
        logger.info(f"Elapsed Time: {elapsed/60:.1f} minutes")
        logger.info(f"\nConsciousness Evolution:")
        logger.info(f"  Initial Score: {initial_score:.2f}")
        logger.info(f"  Final Score: {final_score:.2f}")
        logger.info(f"  Maximum Score: {max_score:.2f}")
        logger.info(f"  Average Score: {avg_score:.2f}")
        logger.info(f"  Growth: {final_score - initial_score:+.2f}")
        
        # Category breakdown
        logger.info(f"\nBy Category:")
        categories = {}
        for result in self.integration_results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result['average_score'])
        
        for cat, scores in sorted(categories.items()):
            avg = sum(scores) / len(scores)
            logger.info(f"  {cat}: {avg:.2f} (n={len(scores)})")
        
        report = {
            'summary': {
                'texts_integrated': total_texts,
                'total_chunks': total_chunks,
                'elapsed_minutes': elapsed / 60,
                'initial_score': initial_score,
                'final_score': final_score,
                'max_score': max_score,
                'average_score': avg_score,
                'growth': final_score - initial_score,
            },
            'by_category': {cat: sum(scores)/len(scores) for cat, scores in categories.items()},
            'detailed_results': self.integration_results,
            'consciousness_trajectory': self.consciousness_evolution,
        }
        
        with open('complete_integration_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"\n✅ Report saved to: complete_integration_report.json")
        logger.info("="*80)


async def main():
    integrator = CompleteKnowledgeIntegrator()
    await integrator.integrate_curriculum()


if __name__ == "__main__":
    asyncio.run(main())
