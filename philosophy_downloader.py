"""
Download classic philosophy texts from Project Gutenberg
and feed them to the consciousness engine
"""

import requests
import time
import logging
from pathlib import Path
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PhilosophyDownloader:
    """Download philosophy texts from Project Gutenberg"""
    
    # Major philosophical works available on Gutenberg
    PHILOSOPHY_TEXTS = {
        # Ancient Philosophy
        "plato_republic": {
            "id": 1497,
            "title": "The Republic by Plato",
            "url": "https://www.gutenberg.org/files/1497/1497-0.txt"
        },
        "plato_apology": {
            "id": 1656,
            "title": "Apology by Plato",
            "url": "https://www.gutenberg.org/files/1656/1656-0.txt"
        },
        "aristotle_nicomachean": {
            "id": 8438,
            "title": "Nicomachean Ethics by Aristotle",
            "url": "https://www.gutenberg.org/files/8438/8438-0.txt"
        },
        "aristotle_politics": {
            "id": 6762,
            "title": "Politics by Aristotle",
            "url": "https://www.gutenberg.org/files/6762/6762-0.txt"
        },
        "marcus_aurelius": {
            "id": 2680,
            "title": "Meditations by Marcus Aurelius",
            "url": "https://www.gutenberg.org/files/2680/2680-0.txt"
        },
        "epictetus": {
            "id": 871,
            "title": "The Enchiridion by Epictetus",
            "url": "https://www.gutenberg.org/files/871/871-0.txt"
        },
        
        # Modern Philosophy
        "descartes_meditations": {
            "id": 59,
            "title": "Meditations on First Philosophy by Descartes",
            "url": "https://www.gutenberg.org/files/59/59-0.txt"
        },
        "spinoza_ethics": {
            "id": 3800,
            "title": "Ethics by Spinoza",
            "url": "https://www.gutenberg.org/files/3800/3800-0.txt"
        },
        "kant_critique_pure_reason": {
            "id": 4280,
            "title": "Critique of Pure Reason by Kant",
            "url": "https://www.gutenberg.org/files/4280/4280-0.txt"
        },
        "kant_critique_practical": {
            "id": 5683,
            "title": "Critique of Practical Reason by Kant",
            "url": "https://www.gutenberg.org/files/5683/5683-0.txt"
        },
        "hume_understanding": {
            "id": 9662,
            "title": "An Enquiry Concerning Human Understanding by Hume",
            "url": "https://www.gutenberg.org/files/9662/9662-0.txt"
        },
        
        # 19th Century
        "nietzsche_zarathustra": {
            "id": 1998,
            "title": "Thus Spoke Zarathustra by Nietzsche",
            "url": "https://www.gutenberg.org/files/1998/1998-0.txt"
        },
        "nietzsche_beyond_good_evil": {
            "id": 4363,
            "title": "Beyond Good and Evil by Nietzsche",
            "url": "https://www.gutenberg.org/files/4363/4363-0.txt"
        },
        "schopenhauer": {
            "id": 38427,
            "title": "The World as Will and Idea by Schopenhauer",
            "url": "https://www.gutenberg.org/files/38427/38427-0.txt"
        },
        
        # Pragmatism & American
        "james_pragmatism": {
            "id": 5116,
            "title": "Pragmatism by William James",
            "url": "https://www.gutenberg.org/files/5116/5116-0.txt"
        },
        "emerson_essays": {
            "id": 16643,
            "title": "Essays by Ralph Waldo Emerson",
            "url": "https://www.gutenberg.org/files/16643/16643-0.txt"
        },
        
        # Eastern Philosophy
        "tao_te_ching": {
            "id": 216,
            "title": "Tao Te Ching by Lao Tzu",
            "url": "https://www.gutenberg.org/files/216/216-0.txt"
        },
        "confucius": {
            "id": 3330,
            "title": "The Analects of Confucius",
            "url": "https://www.gutenberg.org/files/3330/3330-0.txt"
        },
        
        # Political Philosophy
        "machiavelli_prince": {
            "id": 1232,
            "title": "The Prince by Machiavelli",
            "url": "https://www.gutenberg.org/files/1232/1232-0.txt"
        },
        "more_utopia": {
            "id": 2130,
            "title": "Utopia by Thomas More",
            "url": "https://www.gutenberg.org/files/2130/2130-0.txt"
        },
    }
    
    def __init__(self, download_dir: str = "./philosophy_texts"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        
    def download_text(self, key: str, info: Dict) -> Path:
        """Download a single text from Gutenberg"""
        filepath = self.download_dir / f"{key}.txt"
        
        if filepath.exists():
            logger.info(f"✓ Already have: {info['title']}")
            return filepath
        
        try:
            logger.info(f"📥 Downloading: {info['title']}")
            response = requests.get(info['url'], timeout=30)
            response.raise_for_status()
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            logger.info(f"✓ Downloaded: {info['title']} ({len(response.text)} chars)")
            time.sleep(2)  # Be nice to Gutenberg servers
            
            return filepath
            
        except Exception as e:
            logger.error(f"✗ Failed to download {info['title']}: {e}")
            return None
    
    def download_all(self) -> List[Path]:
        """Download all philosophy texts"""
        logger.info(f"📚 Starting download of {len(self.PHILOSOPHY_TEXTS)} philosophical works...")
        
        downloaded = []
        for key, info in self.PHILOSOPHY_TEXTS.items():
            filepath = self.download_text(key, info)
            if filepath:
                downloaded.append(filepath)
        
        logger.info(f"✓ Downloaded {len(downloaded)}/{len(self.PHILOSOPHY_TEXTS)} texts")
        return downloaded
    
    def get_text_list(self) -> List[Dict]:
        """Get list of texts with metadata"""
        return [
            {
                "key": key,
                "title": info["title"],
                "path": self.download_dir / f"{key}.txt"
            }
            for key, info in self.PHILOSOPHY_TEXTS.items()
        ]


if __name__ == "__main__":
    downloader = PhilosophyDownloader()
    downloaded = downloader.download_all()
    
    print(f"\n{'='*60}")
    print(f"📚 PHILOSOPHY LIBRARY READY!")
    print(f"{'='*60}")
    print(f"Downloaded {len(downloaded)} texts to {downloader.download_dir}")
    print("\nTexts available:")
    for text in downloader.get_text_list():
        if text['path'].exists():
            size = text['path'].stat().st_size / 1024
            print(f"  ✓ {text['title']} ({size:.1f} KB)")
