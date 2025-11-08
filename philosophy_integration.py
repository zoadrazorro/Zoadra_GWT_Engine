"""
Feed classical philosophy texts to the consciousness engine
"""

import asyncio
import httpx
import logging
from pathlib import Path
from typing import List, Dict
import json
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PhilosophyIntegrator:
    """Feed philosophy texts to consciousness engine"""
    
    def __init__(self, api_url: str = "http://localhost:7000"):
        self.api_url = api_url
        self.results = []
        
    def chunk_text(self, text: str, chunk_size: int = 2000) -> List[str]:
        """Break text into chunks"""
        # Remove Gutenberg header/footer
        lines = text.split('\n')
        start_idx = 0
        end_idx = len(lines)
        
        # Find start of actual content
        for i, line in enumerate(lines):
            if '***' in line and 'START' in line.upper():
                start_idx = i + 1
                break
        
        # Find end
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
    
    async def process_chunk(self, chunk: str, book_title: str, chunk_num: int, total_chunks: int):
        """Send chunk to consciousness engine"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                prompt = f"[{book_title} - Part {chunk_num}/{total_chunks}]\n\n{chunk}"
                
                response = await client.post(
                    f"{self.api_url}/process/multi-theory",
                    json={"content": prompt},
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    score = result.get('consciousness_score', 0)
                    logger.info(f"  [{chunk_num}/{total_chunks}] Score: {score:.2f}")
                    return result
                else:
                    logger.error(f"  [{chunk_num}] Failed: {response.status_code}")
                    return None
                    
            except Exception as e:
                logger.error(f"  [{chunk_num}] Error: {e}")
                return None
    
    async def integrate_book(self, filepath: Path, title: str, max_chunks: int = 50):
        """Integrate a single philosophical work"""
        logger.info(f"\n{'='*60}")
        logger.info(f"Reading: {title}")
        logger.info(f"{'='*60}")
        
        # Load text
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Chunk it
        chunks = self.chunk_text(text)
        logger.info(f"Split into {len(chunks)} chunks (processing first {max_chunks})")
        
        # Process chunks
        book_results = []
        for i, chunk in enumerate(chunks[:max_chunks], 1):
            result = await self.process_chunk(chunk, title, i, min(len(chunks), max_chunks))
            if result:
                book_results.append({
                    'chunk': i,
                    'score': result.get('consciousness_score', 0),
                    'level': result.get('consciousness_level', 'unknown')
                })
            
            # Small delay
            await asyncio.sleep(1)
        
        return book_results
    
    async def integrate_all(self, philosophy_dir: str = "./philosophy_texts", max_chunks_per_book: int = 30):
        """Integrate all downloaded philosophy"""
        texts_dir = Path(philosophy_dir)
        
        books = [
            ("plato_republic.txt", "The Republic by Plato"),
            ("plato_apology.txt", "Apology by Plato"),
            ("aristotle_nicomachean.txt", "Nicomachean Ethics by Aristotle"),
            ("marcus_aurelius.txt", "Meditations by Marcus Aurelius"),
            ("epictetus.txt", "The Enchiridion by Epictetus"),
            ("descartes_meditations.txt", "Meditations by Descartes"),
            ("kant_critique_pure_reason.txt", "Critique of Pure Reason by Kant"),
            ("nietzsche_zarathustra.txt", "Thus Spoke Zarathustra by Nietzsche"),
            ("schopenhauer.txt", "The World as Will and Idea by Schopenhauer"),
            ("emerson_essays.txt", "Essays by Emerson"),
            ("machiavelli_prince.txt", "The Prince by Machiavelli"),
            ("more_utopia.txt", "Utopia by Thomas More"),
        ]
        
        all_results = {}
        
        for filename, title in books:
            filepath = texts_dir / filename
            if filepath.exists():
                results = await self.integrate_book(filepath, title, max_chunks_per_book)
                all_results[title] = results
            else:
                logger.warning(f"Skipping {title} - file not found")
        
        # Save results
        with open("philosophy_integration_results.json", 'w') as f:
            json.dump(all_results, f, indent=2)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"PHILOSOPHY INTEGRATION COMPLETE!")
        logger.info(f"{'='*60}")
        logger.info(f"Processed {len(all_results)} books")
        logger.info(f"Results saved to philosophy_integration_results.json")


async def main():
    integrator = PhilosophyIntegrator()
    await integrator.integrate_all(max_chunks_per_book=20)  # 20 chunks per book = ~240 total


if __name__ == "__main__":
    asyncio.run(main())
