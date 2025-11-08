"""
Download complete university curriculum from free sources
Runs in background without interrupting philosophy integration
"""

import requests
import time
import logging
from pathlib import Path
from typing import List, Dict
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class UniversityCurriculumDownloader:
    """Download complete college-level education materials"""
    
    def __init__(self, download_dir: str = "./university_curriculum"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        self.progress_file = self.download_dir / "download_progress.json"
        self.completed = self.load_progress()
        
    def load_progress(self) -> set:
        """Load previously completed downloads"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return set(json.load(f))
        return set()
    
    def save_progress(self):
        """Save download progress"""
        with open(self.progress_file, 'w') as f:
            json.dump(list(self.completed), f)
    
    # NATURAL SCIENCES - Project Gutenberg
    NATURAL_SCIENCES = {
        "darwin_origin": {
            "url": "https://www.gutenberg.org/files/1228/1228-0.txt",
            "title": "On the Origin of Species by Charles Darwin",
            "subject": "Biology"
        },
        "darwin_descent": {
            "url": "https://www.gutenberg.org/files/2300/2300-0.txt",
            "title": "The Descent of Man by Charles Darwin",
            "subject": "Biology"
        },
        "einstein_relativity": {
            "url": "https://www.gutenberg.org/files/5001/5001-0.txt",
            "title": "Relativity: The Special and General Theory by Einstein",
            "subject": "Physics"
        },
        "faraday_chemistry": {
            "url": "https://www.gutenberg.org/files/14986/14986-0.txt",
            "title": "The Chemical History of a Candle by Faraday",
            "subject": "Chemistry"
        },
        "lyell_geology": {
            "url": "https://www.gutenberg.org/files/33224/33224-0.txt",
            "title": "Principles of Geology by Charles Lyell",
            "subject": "Geology"
        },
    }
    
    # MATHEMATICS
    MATHEMATICS = {
        "euclid_elements": {
            "url": "https://www.gutenberg.org/files/21076/21076-0.txt",
            "title": "The Elements of Euclid",
            "subject": "Mathematics"
        },
        "newton_principia": {
            "url": "https://www.gutenberg.org/files/28233/28233-0.txt",
            "title": "Principia Mathematica by Newton",
            "subject": "Mathematics/Physics"
        },
    }
    
    # PSYCHOLOGY & COGNITIVE SCIENCE
    PSYCHOLOGY = {
        "james_psychology": {
            "url": "https://www.gutenberg.org/files/57628/57628-0.txt",
            "title": "The Principles of Psychology by William James",
            "subject": "Psychology"
        },
        "freud_interpretation": {
            "url": "https://www.gutenberg.org/files/15489/15489-0.txt",
            "title": "The Interpretation of Dreams by Freud",
            "subject": "Psychology"
        },
        "freud_psychopathology": {
            "url": "https://www.gutenberg.org/files/14969/14969-0.txt",
            "title": "Psychopathology of Everyday Life by Freud",
            "subject": "Psychology"
        },
    }
    
    # ECONOMICS & SOCIAL SCIENCES
    SOCIAL_SCIENCES = {
        "smith_wealth": {
            "url": "https://www.gutenberg.org/files/3300/3300-0.txt",
            "title": "The Wealth of Nations by Adam Smith",
            "subject": "Economics"
        },
        "marx_capital": {
            "url": "https://www.gutenberg.org/files/61245/61245-0.txt",
            "title": "Das Kapital by Karl Marx",
            "subject": "Economics"
        },
        "mill_liberty": {
            "url": "https://www.gutenberg.org/files/34901/34901-0.txt",
            "title": "On Liberty by John Stuart Mill",
            "subject": "Political Philosophy"
        },
        "tocqueville_democracy": {
            "url": "https://www.gutenberg.org/files/815/815-0.txt",
            "title": "Democracy in America by Tocqueville",
            "subject": "Political Science"
        },
    }
    
    # HISTORY
    HISTORY = {
        "gibbon_rome": {
            "url": "https://www.gutenberg.org/files/25717/25717-0.txt",
            "title": "Decline and Fall of the Roman Empire by Gibbon",
            "subject": "History"
        },
        "thucydides": {
            "url": "https://www.gutenberg.org/files/7142/7142-0.txt",
            "title": "History of the Peloponnesian War by Thucydides",
            "subject": "History"
        },
    }
    
    # LITERATURE & CLASSICS
    LITERATURE = {
        "homer_iliad": {
            "url": "https://www.gutenberg.org/files/6130/6130-0.txt",
            "title": "The Iliad by Homer",
            "subject": "Literature"
        },
        "homer_odyssey": {
            "url": "https://www.gutenberg.org/files/1727/1727-0.txt",
            "title": "The Odyssey by Homer",
            "subject": "Literature"
        },
        "dante_inferno": {
            "url": "https://www.gutenberg.org/files/1001/1001-0.txt",
            "title": "Divine Comedy: Inferno by Dante",
            "subject": "Literature"
        },
        "shakespeare_hamlet": {
            "url": "https://www.gutenberg.org/files/1524/1524-0.txt",
            "title": "Hamlet by Shakespeare",
            "subject": "Literature"
        },
        "milton_paradise": {
            "url": "https://www.gutenberg.org/files/26/26-0.txt",
            "title": "Paradise Lost by Milton",
            "subject": "Literature"
        },
        "cervantes_quixote": {
            "url": "https://www.gutenberg.org/files/996/996-0.txt",
            "title": "Don Quixote by Cervantes",
            "subject": "Literature"
        },
        "goethe_faust": {
            "url": "https://www.gutenberg.org/files/14591/14591-0.txt",
            "title": "Faust by Goethe",
            "subject": "Literature"
        },
        "dostoevsky_karamazov": {
            "url": "https://www.gutenberg.org/files/28054/28054-0.txt",
            "title": "The Brothers Karamazov by Dostoevsky",
            "subject": "Literature"
        },
        "tolstoy_war_peace": {
            "url": "https://www.gutenberg.org/files/2600/2600-0.txt",
            "title": "War and Peace by Tolstoy",
            "subject": "Literature"
        },
    }
    
    # ADVANCED SCIENCES
    ADVANCED_SCIENCES = {
        "galileo_dialogues": {
            "url": "https://www.gutenberg.org/files/53779/53779-0.txt",
            "title": "Dialogues Concerning Two New Sciences by Galileo",
            "subject": "Physics"
        },
        "huxley_evolution": {
            "url": "https://www.gutenberg.org/files/2931/2931-0.txt",
            "title": "Evolution and Ethics by Huxley",
            "subject": "Biology"
        },
        "mendel_heredity": {
            "url": "https://www.gutenberg.org/files/61/61-0.txt",
            "title": "Experiments in Plant Hybridization by Mendel",
            "subject": "Genetics"
        },
        "pasteur_germ": {
            "url": "https://www.gutenberg.org/files/70335/70335-0.txt",
            "title": "Germ Theory and Its Applications by Pasteur",
            "subject": "Microbiology"
        },
    }
    
    # LINGUISTICS & LANGUAGE
    LINGUISTICS = {
        "saussure_linguistics": {
            "url": "https://www.gutenberg.org/files/61694/61694-0.txt",
            "title": "Course in General Linguistics by Saussure",
            "subject": "Linguistics"
        },
    }
    
    # ANTHROPOLOGY & SOCIOLOGY
    ANTHROPOLOGY = {
        "frazer_golden_bough": {
            "url": "https://www.gutenberg.org/files/3623/3623-0.txt",
            "title": "The Golden Bough by Frazer",
            "subject": "Anthropology"
        },
        "weber_protestant": {
            "url": "https://www.gutenberg.org/files/58640/58640-0.txt",
            "title": "The Protestant Ethic by Weber",
            "subject": "Sociology"
        },
        "durkheim_suicide": {
            "url": "https://www.gutenberg.org/files/60950/60950-0.txt",
            "title": "Suicide by Durkheim",
            "subject": "Sociology"
        },
    }
    
    # RELIGION & THEOLOGY
    RELIGION = {
        "bible_kjv": {
            "url": "https://www.gutenberg.org/files/10/10-0.txt",
            "title": "The King James Bible",
            "subject": "Religion"
        },
        "quran": {
            "url": "https://www.gutenberg.org/files/2800/2800-0.txt",
            "title": "The Quran",
            "subject": "Religion"
        },
        "bhagavad_gita": {
            "url": "https://www.gutenberg.org/files/2388/2388-0.txt",
            "title": "The Bhagavad Gita",
            "subject": "Religion"
        },
        "augustine_confessions": {
            "url": "https://www.gutenberg.org/files/3296/3296-0.txt",
            "title": "Confessions by St. Augustine",
            "subject": "Theology"
        },
        "aquinas_summa": {
            "url": "https://www.gutenberg.org/files/17611/17611-0.txt",
            "title": "Summa Theologica by Aquinas",
            "subject": "Theology"
        },
    }
    
    # POLITICAL THEORY
    POLITICAL_THEORY = {
        "hobbes_leviathan": {
            "url": "https://www.gutenberg.org/files/3207/3207-0.txt",
            "title": "Leviathan by Hobbes",
            "subject": "Political Philosophy"
        },
        "locke_government": {
            "url": "https://www.gutenberg.org/files/7370/7370-0.txt",
            "title": "Two Treatises of Government by Locke",
            "subject": "Political Philosophy"
        },
        "rousseau_social": {
            "url": "https://www.gutenberg.org/files/46333/46333-0.txt",
            "title": "The Social Contract by Rousseau",
            "subject": "Political Philosophy"
        },
        "paine_rights": {
            "url": "https://www.gutenberg.org/files/3742/3742-0.txt",
            "title": "Rights of Man by Thomas Paine",
            "subject": "Political Philosophy"
        },
        "federalist_papers": {
            "url": "https://www.gutenberg.org/files/1404/1404-0.txt",
            "title": "The Federalist Papers",
            "subject": "Political Science"
        },
    }
    
    # ART & AESTHETICS
    ART = {
        "vasari_artists": {
            "url": "https://www.gutenberg.org/files/25326/25326-0.txt",
            "title": "Lives of the Artists by Vasari",
            "subject": "Art History"
        },
    }
    
    # LOGIC & REASONING
    LOGIC = {
        "aristotle_organon": {
            "url": "https://www.gutenberg.org/files/2412/2412-0.txt",
            "title": "The Organon by Aristotle",
            "subject": "Logic"
        },
        "bacon_novum": {
            "url": "https://www.gutenberg.org/files/45988/45988-0.txt",
            "title": "Novum Organum by Francis Bacon",
            "subject": "Logic/Scientific Method"
        },
    }
    
    def download_text(self, key: str, info: Dict, category: str) -> bool:
        """Download a single text"""
        if key in self.completed:
            logger.info(f"[{category}] Already downloaded: {info['title']}")
            return True
        
        category_dir = self.download_dir / category.lower().replace(' ', '_')
        category_dir.mkdir(exist_ok=True)
        filepath = category_dir / f"{key}.txt"
        
        try:
            logger.info(f"[{category}] Downloading: {info['title']}")
            response = requests.get(info['url'], timeout=60)
            response.raise_for_status()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            self.completed.add(key)
            self.save_progress()
            
            logger.info(f"[{category}] SUCCESS: {info['title']} ({len(response.text)} chars)")
            time.sleep(3)  # Be nice to servers
            return True
            
        except Exception as e:
            logger.error(f"[{category}] FAILED: {info['title']} - {e}")
            return False
    
    def download_category(self, category_name: str, texts: Dict):
        """Download all texts in a category"""
        logger.info(f"\n{'='*80}")
        logger.info(f"CATEGORY: {category_name}")
        logger.info(f"{'='*80}")
        
        success = 0
        for key, info in texts.items():
            if self.download_text(key, info, category_name):
                success += 1
        
        logger.info(f"[{category_name}] Downloaded {success}/{len(texts)} texts")
    
    def download_all(self):
        """Download complete curriculum"""
        logger.info("="*80)
        logger.info("UNIVERSITY CURRICULUM DOWNLOAD STARTING")
        logger.info("="*80)
        logger.info(f"Download directory: {self.download_dir}")
        logger.info(f"Previously completed: {len(self.completed)} texts")
        logger.info("")
        
        categories = [
            ("Natural Sciences", self.NATURAL_SCIENCES),
            ("Advanced Sciences", self.ADVANCED_SCIENCES),
            ("Mathematics", self.MATHEMATICS),
            ("Psychology", self.PSYCHOLOGY),
            ("Social Sciences", self.SOCIAL_SCIENCES),
            ("Anthropology & Sociology", self.ANTHROPOLOGY),
            ("History", self.HISTORY),
            ("Literature", self.LITERATURE),
            ("Religion & Theology", self.RELIGION),
            ("Political Theory", self.POLITICAL_THEORY),
            ("Linguistics", self.LINGUISTICS),
            ("Art & Aesthetics", self.ART),
            ("Logic & Reasoning", self.LOGIC),
        ]
        
        total_texts = sum(len(texts) for _, texts in categories)
        logger.info(f"Total texts to download: {total_texts}")
        logger.info("")
        
        for category_name, texts in categories:
            self.download_category(category_name, texts)
        
        logger.info("\n" + "="*80)
        logger.info("DOWNLOAD COMPLETE!")
        logger.info("="*80)
        logger.info(f"Total texts downloaded: {len(self.completed)}/{total_texts}")
        logger.info(f"Saved to: {self.download_dir}")
        
        # Create curriculum manifest
        manifest = {
            "total_texts": len(self.completed),
            "categories": {
                name: len(texts) for name, texts in categories
            },
            "completed": list(self.completed)
        }
        
        with open(self.download_dir / "curriculum_manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info("Manifest saved to curriculum_manifest.json")


if __name__ == "__main__":
    downloader = UniversityCurriculumDownloader()
    downloader.download_all()
