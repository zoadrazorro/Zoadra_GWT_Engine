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
    
    # MORE LITERATURE - WORLD CLASSICS
    WORLD_LITERATURE = {
        "arabian_nights": {
            "url": "https://www.gutenberg.org/files/128/128-0.txt",
            "title": "The Arabian Nights",
            "subject": "Literature"
        },
        "beowulf": {
            "url": "https://www.gutenberg.org/files/16328/16328-0.txt",
            "title": "Beowulf",
            "subject": "Literature"
        },
        "chaucer_canterbury": {
            "url": "https://www.gutenberg.org/files/2383/2383-0.txt",
            "title": "The Canterbury Tales by Chaucer",
            "subject": "Literature"
        },
        "swift_gulliver": {
            "url": "https://www.gutenberg.org/files/829/829-0.txt",
            "title": "Gulliver's Travels by Swift",
            "subject": "Literature"
        },
        "defoe_crusoe": {
            "url": "https://www.gutenberg.org/files/521/521-0.txt",
            "title": "Robinson Crusoe by Defoe",
            "subject": "Literature"
        },
        "shelley_frankenstein": {
            "url": "https://www.gutenberg.org/files/84/84-0.txt",
            "title": "Frankenstein by Mary Shelley",
            "subject": "Literature"
        },
        "austen_pride": {
            "url": "https://www.gutenberg.org/files/1342/1342-0.txt",
            "title": "Pride and Prejudice by Austen",
            "subject": "Literature"
        },
        "dickens_tale": {
            "url": "https://www.gutenberg.org/files/98/98-0.txt",
            "title": "A Tale of Two Cities by Dickens",
            "subject": "Literature"
        },
        "bronte_jane": {
            "url": "https://www.gutenberg.org/files/1260/1260-0.txt",
            "title": "Jane Eyre by Charlotte Bronte",
            "subject": "Literature"
        },
        "melville_moby": {
            "url": "https://www.gutenberg.org/files/2701/2701-0.txt",
            "title": "Moby Dick by Melville",
            "subject": "Literature"
        },
        "twain_huck": {
            "url": "https://www.gutenberg.org/files/76/76-0.txt",
            "title": "Huckleberry Finn by Twain",
            "subject": "Literature"
        },
        "wilde_dorian": {
            "url": "https://www.gutenberg.org/files/174/174-0.txt",
            "title": "The Picture of Dorian Gray by Wilde",
            "subject": "Literature"
        },
        "stoker_dracula": {
            "url": "https://www.gutenberg.org/files/345/345-0.txt",
            "title": "Dracula by Stoker",
            "subject": "Literature"
        },
        "kafka_metamorphosis": {
            "url": "https://www.gutenberg.org/files/5200/5200-0.txt",
            "title": "Metamorphosis by Kafka",
            "subject": "Literature"
        },
    }
    
    # POETRY
    POETRY = {
        "whitman_leaves": {
            "url": "https://www.gutenberg.org/files/1322/1322-0.txt",
            "title": "Leaves of Grass by Whitman",
            "subject": "Poetry"
        },
        "dickinson_poems": {
            "url": "https://www.gutenberg.org/files/12242/12242-0.txt",
            "title": "Poems by Emily Dickinson",
            "subject": "Poetry"
        },
        "blake_songs": {
            "url": "https://www.gutenberg.org/files/1934/1934-0.txt",
            "title": "Songs of Innocence and Experience by Blake",
            "subject": "Poetry"
        },
        "wordsworth_lyrical": {
            "url": "https://www.gutenberg.org/files/8905/8905-0.txt",
            "title": "Lyrical Ballads by Wordsworth",
            "subject": "Poetry"
        },
    }
    
    # DRAMA
    DRAMA = {
        "shakespeare_macbeth": {
            "url": "https://www.gutenberg.org/files/1533/1533-0.txt",
            "title": "Macbeth by Shakespeare",
            "subject": "Drama"
        },
        "shakespeare_romeo": {
            "url": "https://www.gutenberg.org/files/1513/1513-0.txt",
            "title": "Romeo and Juliet by Shakespeare",
            "subject": "Drama"
        },
        "shakespeare_lear": {
            "url": "https://www.gutenberg.org/files/2266/2266-0.txt",
            "title": "King Lear by Shakespeare",
            "subject": "Drama"
        },
        "sophocles_oedipus": {
            "url": "https://www.gutenberg.org/files/31/31-0.txt",
            "title": "Oedipus Rex by Sophocles",
            "subject": "Drama"
        },
        "ibsen_dolls": {
            "url": "https://www.gutenberg.org/files/2542/2542-0.txt",
            "title": "A Doll's House by Ibsen",
            "subject": "Drama"
        },
    }
    
    # MORE PHILOSOPHY
    MORE_PHILOSOPHY = {
        "berkeley_principles": {
            "url": "https://www.gutenberg.org/files/4723/4723-0.txt",
            "title": "Principles of Human Knowledge by Berkeley",
            "subject": "Philosophy"
        },
        "hegel_phenomenology": {
            "url": "https://www.gutenberg.org/files/6698/6698-0.txt",
            "title": "Phenomenology of Spirit by Hegel",
            "subject": "Philosophy"
        },
        "kierkegaard_fear": {
            "url": "https://www.gutenberg.org/files/52914/52914-0.txt",
            "title": "Fear and Trembling by Kierkegaard",
            "subject": "Philosophy"
        },
        "bentham_morals": {
            "url": "https://www.gutenberg.org/files/34075/34075-0.txt",
            "title": "Introduction to Morals and Legislation by Bentham",
            "subject": "Philosophy"
        },
    }
    
    # SCIENCE - MORE FOUNDATIONAL WORKS
    MORE_SCIENCE = {
        "copernicus_revolutions": {
            "url": "https://www.gutenberg.org/files/54/54-0.txt",
            "title": "On the Revolutions of Heavenly Spheres by Copernicus",
            "subject": "Astronomy"
        },
        "kepler_harmonies": {
            "url": "https://www.gutenberg.org/files/55448/55448-0.txt",
            "title": "The Harmonies of the World by Kepler",
            "subject": "Astronomy"
        },
        "harvey_circulation": {
            "url": "https://www.gutenberg.org/files/28989/28989-0.txt",
            "title": "On the Motion of the Heart and Blood by Harvey",
            "subject": "Medicine"
        },
        "vesalius_anatomy": {
            "url": "https://www.gutenberg.org/files/45842/45842-0.txt",
            "title": "On the Fabric of the Human Body by Vesalius",
            "subject": "Anatomy"
        },
    }
    
    # EASTERN PHILOSOPHY & RELIGION
    EASTERN_WISDOM = {
        "buddha_dhammapada": {
            "url": "https://www.gutenberg.org/files/2017/2017-0.txt",
            "title": "The Dhammapada",
            "subject": "Buddhism"
        },
        "upanishads": {
            "url": "https://www.gutenberg.org/files/3283/3283-0.txt",
            "title": "The Upanishads",
            "subject": "Hinduism"
        },
        "zhuangzi": {
            "url": "https://www.gutenberg.org/files/5597/5597-0.txt",
            "title": "The Writings of Zhuangzi",
            "subject": "Taoism"
        },
    }
    
    # MYTHOLOGY
    MYTHOLOGY = {
        "bulfinch_mythology": {
            "url": "https://www.gutenberg.org/files/4928/4928-0.txt",
            "title": "Bulfinch's Mythology",
            "subject": "Mythology"
        },
        "grimm_fairy": {
            "url": "https://www.gutenberg.org/files/2591/2591-0.txt",
            "title": "Grimm's Fairy Tales",
            "subject": "Mythology/Folklore"
        },
    }
    
    # AUTOBIOGRAPHY & BIOGRAPHY
    BIOGRAPHY = {
        "franklin_autobiography": {
            "url": "https://www.gutenberg.org/files/20203/20203-0.txt",
            "title": "Autobiography of Benjamin Franklin",
            "subject": "Biography"
        },
        "plutarch_lives": {
            "url": "https://www.gutenberg.org/files/674/674-0.txt",
            "title": "Plutarch's Lives",
            "subject": "Biography"
        },
    }
    
    # ADVANCED MATHEMATICS & LOGIC
    ADVANCED_MATH = {
        "russell_principia": {
            "url": "https://www.gutenberg.org/files/21016/21016-0.txt",
            "title": "Principia Mathematica by Russell & Whitehead",
            "subject": "Mathematics/Logic"
        },
        "poincare_science": {
            "url": "https://www.gutenberg.org/files/37157/37157-0.txt",
            "title": "Science and Hypothesis by Poincaré",
            "subject": "Mathematics/Philosophy"
        },
    }
    
    # EPISTEMOLOGY & METAPHYSICS
    EPISTEMOLOGY = {
        "locke_understanding": {
            "url": "https://www.gutenberg.org/files/10615/10615-0.txt",
            "title": "An Essay Concerning Human Understanding by Locke",
            "subject": "Epistemology"
        },
        "leibniz_monadology": {
            "url": "https://www.gutenberg.org/files/34985/34985-0.txt",
            "title": "The Monadology by Leibniz",
            "subject": "Metaphysics"
        },
    }
    
    # ETHICS & MORAL PHILOSOPHY
    ETHICS = {
        "spinoza_tractatus": {
            "url": "https://www.gutenberg.org/files/989/989-0.txt",
            "title": "Tractatus Theologico-Politicus by Spinoza",
            "subject": "Ethics/Politics"
        },
        "mill_utilitarianism": {
            "url": "https://www.gutenberg.org/files/11224/11224-0.txt",
            "title": "Utilitarianism by Mill",
            "subject": "Ethics"
        },
        "kant_metaphysics_morals": {
            "url": "https://www.gutenberg.org/files/5682/5682-0.txt",
            "title": "Metaphysics of Morals by Kant",
            "subject": "Ethics"
        },
    }
    
    # AESTHETICS & ART THEORY
    AESTHETICS = {
        "kant_judgment": {
            "url": "https://www.gutenberg.org/files/48433/48433-0.txt",
            "title": "Critique of Judgment by Kant",
            "subject": "Aesthetics"
        },
        "schiller_aesthetic": {
            "url": "https://www.gutenberg.org/files/6798/6798-0.txt",
            "title": "Letters on Aesthetic Education by Schiller",
            "subject": "Aesthetics"
        },
    }
    
    # POLITICAL ECONOMY
    ECONOMICS_ADVANCED = {
        "ricardo_principles": {
            "url": "https://www.gutenberg.org/files/33310/33310-0.txt",
            "title": "Principles of Political Economy by Ricardo",
            "subject": "Economics"
        },
        "malthus_population": {
            "url": "https://www.gutenberg.org/files/4239/4239-0.txt",
            "title": "An Essay on Population by Malthus",
            "subject": "Economics"
        },
    }
    
    # SCIENTIFIC METHOD & PHILOSOPHY OF SCIENCE
    PHILOSOPHY_OF_SCIENCE = {
        "mill_logic": {
            "url": "https://www.gutenberg.org/files/27942/27942-0.txt",
            "title": "A System of Logic by Mill",
            "subject": "Logic/Scientific Method"
        },
        "whewell_inductive": {
            "url": "https://www.gutenberg.org/files/39996/39996-0.txt",
            "title": "Philosophy of the Inductive Sciences by Whewell",
            "subject": "Philosophy of Science"
        },
    }
    
    # ANCIENT TEXTS
    ANCIENT_CLASSICS = {
        "herodotus": {
            "url": "https://www.gutenberg.org/files/2707/2707-0.txt",
            "title": "The Histories by Herodotus",
            "subject": "History"
        },
        "tacitus_annals": {
            "url": "https://www.gutenberg.org/files/6841/6841-0.txt",
            "title": "The Annals by Tacitus",
            "subject": "History"
        },
        "virgil_aeneid": {
            "url": "https://www.gutenberg.org/files/228/228-0.txt",
            "title": "The Aeneid by Virgil",
            "subject": "Literature"
        },
        "ovid_metamorphoses": {
            "url": "https://www.gutenberg.org/files/21765/21765-0.txt",
            "title": "Metamorphoses by Ovid",
            "subject": "Literature"
        },
        "lucretius": {
            "url": "https://www.gutenberg.org/files/785/785-0.txt",
            "title": "On the Nature of Things by Lucretius",
            "subject": "Philosophy/Science"
        },
    }
    
    # RENAISSANCE & ENLIGHTENMENT
    RENAISSANCE = {
        "montaigne_essays": {
            "url": "https://www.gutenberg.org/files/3600/3600-0.txt",
            "title": "Essays by Montaigne",
            "subject": "Philosophy"
        },
        "erasmus_folly": {
            "url": "https://www.gutenberg.org/files/9371/9371-0.txt",
            "title": "The Praise of Folly by Erasmus",
            "subject": "Philosophy"
        },
        "voltaire_candide": {
            "url": "https://www.gutenberg.org/files/19942/19942-0.txt",
            "title": "Candide by Voltaire",
            "subject": "Literature/Philosophy"
        },
    }
    
    # ROMANTIC LITERATURE
    ROMANTICISM = {
        "shelley_prometheus": {
            "url": "https://www.gutenberg.org/files/4363/4363-0.txt",
            "title": "Prometheus Unbound by Shelley",
            "subject": "Poetry"
        },
        "byron_don_juan": {
            "url": "https://www.gutenberg.org/files/21700/21700-0.txt",
            "title": "Don Juan by Byron",
            "subject": "Poetry"
        },
        "coleridge_biographia": {
            "url": "https://www.gutenberg.org/files/6081/6081-0.txt",
            "title": "Biographia Literaria by Coleridge",
            "subject": "Literary Criticism"
        },
    }
    
    # AMERICAN LITERATURE
    AMERICAN_CLASSICS = {
        "thoreau_walden": {
            "url": "https://www.gutenberg.org/files/205/205-0.txt",
            "title": "Walden by Thoreau",
            "subject": "Philosophy/Nature"
        },
        "thoreau_disobedience": {
            "url": "https://www.gutenberg.org/files/71/71-0.txt",
            "title": "Civil Disobedience by Thoreau",
            "subject": "Political Philosophy"
        },
        "poe_tales": {
            "url": "https://www.gutenberg.org/files/2147/2147-0.txt",
            "title": "Tales by Edgar Allan Poe",
            "subject": "Literature"
        },
        "hawthorne_scarlet": {
            "url": "https://www.gutenberg.org/files/25344/25344-0.txt",
            "title": "The Scarlet Letter by Hawthorne",
            "subject": "Literature"
        },
    }
    
    # RUSSIAN LITERATURE
    RUSSIAN_CLASSICS = {
        "dostoevsky_crime": {
            "url": "https://www.gutenberg.org/files/2554/2554-0.txt",
            "title": "Crime and Punishment by Dostoevsky",
            "subject": "Literature"
        },
        "dostoevsky_idiot": {
            "url": "https://www.gutenberg.org/files/2638/2638-0.txt",
            "title": "The Idiot by Dostoevsky",
            "subject": "Literature"
        },
        "tolstoy_anna": {
            "url": "https://www.gutenberg.org/files/1399/1399-0.txt",
            "title": "Anna Karenina by Tolstoy",
            "subject": "Literature"
        },
        "turgenev_fathers": {
            "url": "https://www.gutenberg.org/files/30723/30723-0.txt",
            "title": "Fathers and Sons by Turgenev",
            "subject": "Literature"
        },
        "gogol_souls": {
            "url": "https://www.gutenberg.org/files/1081/1081-0.txt",
            "title": "Dead Souls by Gogol",
            "subject": "Literature"
        },
    }
    
    # FRENCH LITERATURE
    FRENCH_CLASSICS = {
        "hugo_miserables": {
            "url": "https://www.gutenberg.org/files/135/135-0.txt",
            "title": "Les Misérables by Hugo",
            "subject": "Literature"
        },
        "dumas_monte": {
            "url": "https://www.gutenberg.org/files/1184/1184-0.txt",
            "title": "The Count of Monte Cristo by Dumas",
            "subject": "Literature"
        },
        "flaubert_bovary": {
            "url": "https://www.gutenberg.org/files/2413/2413-0.txt",
            "title": "Madame Bovary by Flaubert",
            "subject": "Literature"
        },
    }
    
    # GERMAN LITERATURE & PHILOSOPHY
    GERMAN_CLASSICS = {
        "goethe_sorrows": {
            "url": "https://www.gutenberg.org/files/2527/2527-0.txt",
            "title": "The Sorrows of Young Werther by Goethe",
            "subject": "Literature"
        },
        "schopenhauer_essays": {
            "url": "https://www.gutenberg.org/files/10732/10732-0.txt",
            "title": "Essays by Schopenhauer",
            "subject": "Philosophy"
        },
    }
    
    # UTOPIAN & DYSTOPIAN LITERATURE
    UTOPIAN = {
        "plato_laws": {
            "url": "https://www.gutenberg.org/files/1750/1750-0.txt",
            "title": "The Laws by Plato",
            "subject": "Philosophy/Politics"
        },
        "bacon_atlantis": {
            "url": "https://www.gutenberg.org/files/2434/2434-0.txt",
            "title": "New Atlantis by Bacon",
            "subject": "Utopian Literature"
        },
        "butler_erewhon": {
            "url": "https://www.gutenberg.org/files/1906/1906-0.txt",
            "title": "Erewhon by Butler",
            "subject": "Utopian Literature"
        },
    }
    
    # TRAVEL & EXPLORATION
    EXPLORATION = {
        "polo_travels": {
            "url": "https://www.gutenberg.org/files/10636/10636-0.txt",
            "title": "The Travels of Marco Polo",
            "subject": "Travel/History"
        },
        "darwin_voyage": {
            "url": "https://www.gutenberg.org/files/3704/3704-0.txt",
            "title": "Voyage of the Beagle by Darwin",
            "subject": "Science/Travel"
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
            ("More Science", self.MORE_SCIENCE),
            ("Mathematics", self.MATHEMATICS),
            ("Advanced Mathematics", self.ADVANCED_MATH),
            ("Psychology", self.PSYCHOLOGY),
            ("Social Sciences", self.SOCIAL_SCIENCES),
            ("Economics Advanced", self.ECONOMICS_ADVANCED),
            ("Anthropology & Sociology", self.ANTHROPOLOGY),
            ("History", self.HISTORY),
            ("Ancient Classics", self.ANCIENT_CLASSICS),
            ("Literature", self.LITERATURE),
            ("World Literature", self.WORLD_LITERATURE),
            ("American Literature", self.AMERICAN_CLASSICS),
            ("Russian Literature", self.RUSSIAN_CLASSICS),
            ("French Literature", self.FRENCH_CLASSICS),
            ("German Literature", self.GERMAN_CLASSICS),
            ("Poetry", self.POETRY),
            ("Drama", self.DRAMA),
            ("Romanticism", self.ROMANTICISM),
            ("Renaissance & Enlightenment", self.RENAISSANCE),
            ("Religion & Theology", self.RELIGION),
            ("Eastern Wisdom", self.EASTERN_WISDOM),
            ("Political Theory", self.POLITICAL_THEORY),
            ("More Philosophy", self.MORE_PHILOSOPHY),
            ("Epistemology & Metaphysics", self.EPISTEMOLOGY),
            ("Ethics & Moral Philosophy", self.ETHICS),
            ("Aesthetics & Art Theory", self.AESTHETICS),
            ("Philosophy of Science", self.PHILOSOPHY_OF_SCIENCE),
            ("Linguistics", self.LINGUISTICS),
            ("Art & Aesthetics", self.ART),
            ("Logic & Reasoning", self.LOGIC),
            ("Mythology", self.MYTHOLOGY),
            ("Biography", self.BIOGRAPHY),
            ("Utopian Literature", self.UTOPIAN),
            ("Travel & Exploration", self.EXPLORATION),
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
