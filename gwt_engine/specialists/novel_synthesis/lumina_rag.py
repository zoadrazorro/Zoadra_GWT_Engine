"""
Lumina RAG System - Retrieval-Augmented Generation
===================================================

RAG system for retrieving relevant passages from the Contemplation of the Lumina
(Metaluminous Ethica) to ground philosophical synthesis in this framework.

Uses:
- Vector embeddings for semantic search
- BM25 for keyword-based retrieval
- Hybrid retrieval combining both approaches
- Contextual re-ranking

Serves as "fact finder" for novel philosophy synthesis.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import Counter
import math


@dataclass
class LuminaPassage:
    """A passage from the Metaluminous Ethica"""
    id: int
    content: str
    score: float  # Integration score from original memory
    level: str  # Consciousness level
    iit_phi: float  # IIT Phi score
    timestamp: float
    keywords: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "score": self.score,
            "level": self.level,
            "iit_phi": self.iit_phi,
            "timestamp": self.timestamp,
            "keywords": self.keywords
        }


@dataclass
class RetrievalResult:
    """Result from RAG retrieval"""
    passage: LuminaPassage
    relevance_score: float
    retrieval_method: str  # "semantic", "keyword", "hybrid"
    query_match_explanation: str

    def to_dict(self):
        return {
            "passage": self.passage.to_dict(),
            "relevance_score": self.relevance_score,
            "retrieval_method": self.retrieval_method,
            "query_match_explanation": self.query_match_explanation
        }


class LuminaRAG:
    """
    Retrieval-Augmented Generation system for Contemplation of the Lumina.

    Provides semantic search over Metaluminous Ethica to ground
    philosophical synthesis in the Lumina framework.
    """

    def __init__(self, memory_file: str = "philosophical_memory.json",
                 contemplation_file: str = "contemplation_lumina.md.pdf"):
        """
        Initialize RAG system with philosophical memory and Contemplation of the Lumina.

        Args:
            memory_file: Path to philosophical memory JSON
            contemplation_file: Path to Contemplation of the Lumina markdown file
        """
        self.memory_file = Path(memory_file)
        self.contemplation_file = Path(contemplation_file)
        self.passages: List[LuminaPassage] = []
        self.lumina_passages: List[LuminaPassage] = []  # Filtered for Lumina content

        # BM25 parameters
        self.k1 = 1.5  # Term frequency saturation
        self.b = 0.75  # Length normalization

        # Document statistics for BM25
        self.doc_freqs = Counter()
        self.doc_lengths = {}
        self.avg_doc_length = 0

        self._load_passages()
        self._load_contemplation_lumina()
        self._build_index()

    def _load_passages(self):
        """Load passages from philosophical memory"""
        print(f"\nLoading Lumina passages from {self.memory_file}...")

        if not self.memory_file.exists():
            print(f"  Warning: {self.memory_file} not found")
            return

        with open(self.memory_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            memories = data.get('memories', [])

        # Convert to LuminaPassage objects
        for mem in memories:
            passage = LuminaPassage(
                id=mem.get('id', 0),
                content=mem.get('content', ''),
                score=mem.get('score', 0.0),
                level=mem.get('level', 'unconscious'),
                iit_phi=mem.get('iit_phi', 0.0),
                timestamp=mem.get('timestamp', 0.0),
                keywords=self._extract_keywords(mem.get('content', ''))
            )
            self.passages.append(passage)

            # Filter for Lumina/Metaluminous content
            if self._is_lumina_content(passage.content):
                self.lumina_passages.append(passage)

        print(f"  Loaded {len(self.passages)} total passages")
        print(f"  Found {len(self.lumina_passages)} Lumina/Metaluminous passages")

    def _load_contemplation_lumina(self):
        """Load and parse Contemplation of the Lumina (PDF or markdown)"""
        if not self.contemplation_file.exists():
            print(f"  Note: {self.contemplation_file} not found - using philosophical_memory.json only")
            return

        print(f"\nLoading Contemplation of the Lumina from {self.contemplation_file}...")

        # Check file type
        if str(self.contemplation_file).endswith('.pdf'):
            content = self._load_pdf_content()
        else:
            with open(self.contemplation_file, 'r', encoding='utf-8') as f:
                content = f.read()

        if not content:
            print(f"  Warning: Could not extract content from {self.contemplation_file}")
            return

        # Parse into passages
        # Split by headers or paragraphs
        sections = self._parse_markdown_sections(content)

        # Create LuminaPassage objects from sections
        base_id = max((p.id for p in self.passages), default=0) + 1

        for i, section in enumerate(sections):
            if len(section.strip()) < 50:  # Skip very short sections
                continue

            passage = LuminaPassage(
                id=base_id + i,
                content=section,
                score=0.9,  # High score for primary source text
                level="high",  # Contemplation is high-level philosophical content
                iit_phi=0.85,  # High integration for coherent philosophical text
                timestamp=0.0,
                keywords=self._extract_keywords(section)
            )

            self.passages.append(passage)
            self.lumina_passages.append(passage)  # All content from this file is Lumina

        print(f"  Loaded {len(sections)} sections from Contemplation of the Lumina")

    def _load_pdf_content(self) -> str:
        """Extract text content from PDF file"""
        try:
            # Try using pdfplumber first (if available)
            try:
                import pdfplumber
                text_parts = []
                with pdfplumber.open(self.contemplation_file) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            text_parts.append(text)
                return '\n\n'.join(text_parts)
            except ImportError:
                pass

            # Fallback to PyPDF2
            try:
                import PyPDF2
                text_parts = []
                with open(self.contemplation_file, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page in pdf_reader.pages:
                        text = page.extract_text()
                        if text:
                            text_parts.append(text)
                return '\n\n'.join(text_parts)
            except ImportError:
                pass

            # Final fallback: use pdftotext command if available
            import subprocess
            try:
                result = subprocess.run(
                    ['pdftotext', str(self.contemplation_file), '-'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    return result.stdout
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass

            print("  Warning: No PDF extraction library available. Install pdfplumber or PyPDF2.")
            return ""

        except Exception as e:
            print(f"  Warning: Error extracting PDF: {e}")
            return ""

    def _parse_markdown_sections(self, content: str) -> List[str]:
        """Parse markdown content into sections"""
        # Split by headers (## or ###)
        import re

        # Split by markdown headers
        sections = []
        current_section = []

        lines = content.split('\n')

        for line in lines:
            # Check if line is a header
            if re.match(r'^#{1,6}\s', line):
                # Save previous section if it exists
                if current_section:
                    section_text = '\n'.join(current_section).strip()
                    if section_text:
                        sections.append(section_text)

                # Start new section with header
                current_section = [line]
            else:
                current_section.append(line)

        # Add final section
        if current_section:
            section_text = '\n'.join(current_section).strip()
            if section_text:
                sections.append(section_text)

        # Also split long sections by paragraphs
        refined_sections = []
        for section in sections:
            paragraphs = section.split('\n\n')
            for para in paragraphs:
                para = para.strip()
                if len(para) > 100:  # Only keep substantial paragraphs
                    refined_sections.append(para)

        return refined_sections

    def _is_lumina_content(self, text: str) -> bool:
        """Check if content relates to Lumina/Metaluminous Ethica"""
        lumina_markers = [
            'metaluminous', 'lumina', 'luminous field', 'informational field',
            'omega consciousness', 'sper', 'being/godhead', 'ethica',
            'coherence', 'participatory cosmos', 'non-dual'
        ]

        text_lower = text.lower()
        return any(marker in text_lower for marker in lumina_markers)

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Remove punctuation and lowercase
        text = re.sub(r'[^\w\s]', ' ', text.lower())

        # Split into words
        words = text.split()

        # Filter stopwords and short words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
                    'that', 'this', 'which', 'it', 'its', 'through', 'into', 'where'}

        keywords = [w for w in words if w not in stopwords and len(w) > 3]

        # Return unique keywords
        return list(set(keywords))

    def _build_index(self):
        """Build BM25 index"""
        if not self.lumina_passages:
            return

        print("\nBuilding BM25 index...")

        # Calculate document frequencies
        for passage in self.lumina_passages:
            unique_terms = set(passage.keywords)
            for term in unique_terms:
                self.doc_freqs[term] += 1

            self.doc_lengths[passage.id] = len(passage.keywords)

        # Calculate average document length
        if self.doc_lengths:
            self.avg_doc_length = sum(self.doc_lengths.values()) / len(self.doc_lengths)

        print(f"  Indexed {len(self.doc_freqs)} unique terms")
        print(f"  Average document length: {self.avg_doc_length:.1f} terms")

    def _bm25_score(self, query_terms: List[str], passage: LuminaPassage) -> float:
        """Calculate BM25 score for a passage given query terms"""
        if not self.lumina_passages:
            return 0.0

        score = 0.0
        N = len(self.lumina_passages)

        # Count term frequencies in document
        doc_term_freqs = Counter(passage.keywords)
        doc_length = len(passage.keywords)

        for term in query_terms:
            if term not in doc_term_freqs:
                continue

            # Term frequency in document
            tf = doc_term_freqs[term]

            # Document frequency (number of docs containing term)
            df = self.doc_freqs.get(term, 0)

            if df == 0:
                continue

            # IDF calculation
            idf = math.log((N - df + 0.5) / (df + 0.5) + 1.0)

            # BM25 formula
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * (doc_length / self.avg_doc_length))

            score += idf * (numerator / denominator)

        return score

    def retrieve_by_keywords(self, query: str, top_k: int = 5) -> List[RetrievalResult]:
        """
        Retrieve passages using BM25 keyword-based search.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of retrieval results
        """
        if not self.lumina_passages:
            return []

        query_terms = self._extract_keywords(query)

        # Score all passages
        scored_passages = []
        for passage in self.lumina_passages:
            score = self._bm25_score(query_terms, passage)
            if score > 0:
                scored_passages.append((passage, score))

        # Sort by score
        scored_passages.sort(key=lambda x: x[1], reverse=True)

        # Create results
        results = []
        for passage, score in scored_passages[:top_k]:
            # Find matching terms for explanation
            matching_terms = set(query_terms) & set(passage.keywords)

            result = RetrievalResult(
                passage=passage,
                relevance_score=score,
                retrieval_method="keyword",
                query_match_explanation=f"Matches terms: {', '.join(list(matching_terms)[:5])}"
            )
            results.append(result)

        return results

    def retrieve_by_concept(self, concept: str, top_k: int = 5) -> List[RetrievalResult]:
        """
        Retrieve passages related to a philosophical concept.

        Args:
            concept: Philosophical concept to search for
            top_k: Number of results to return

        Returns:
            List of retrieval results
        """
        # Expand concept with related terms
        concept_expansions = {
            'consciousness': ['consciousness', 'awareness', 'experience', 'subjective', 'phenomenal'],
            'being': ['being', 'existence', 'reality', 'godhead', 'absolute'],
            'coherence': ['coherence', 'unity', 'integration', 'harmony', 'resonance'],
            'field': ['field', 'luminous', 'informational', 'energetic'],
            'evolution': ['evolution', 'sper', 'ascent', 'descent', 'cycle'],
            'ethics': ['ethics', 'virtue', 'coherence', 'truth', 'good'],
            'participation': ['participation', 'participatory', 'co-creation', 'engagement']
        }

        # Build expanded query
        expanded_terms = concept_expansions.get(concept.lower(), [concept])
        query = ' '.join(expanded_terms)

        return self.retrieve_by_keywords(query, top_k)

    def retrieve_for_synthesis(self, topic: str, position_type: str,
                              top_k: int = 3) -> List[RetrievalResult]:
        """
        Retrieve Lumina passages to ground a philosophical synthesis.

        Args:
            topic: The topic being synthesized
            position_type: "thesis", "antithesis", or "synthesis"
            top_k: Number of passages to retrieve

        Returns:
            List of retrieval results
        """
        print(f"\n[Lumina RAG] Retrieving for {position_type} on: {topic}")

        # Augment query based on position type
        if position_type == "thesis":
            query = f"{topic} coherence unity integration"
        elif position_type == "antithesis":
            query = f"{topic} multiplicity diversity fragmentation"
        else:  # synthesis
            query = f"{topic} participatory cosmos omega consciousness transcendence"

        results = self.retrieve_by_keywords(query, top_k)

        print(f"  Retrieved {len(results)} passages")
        for i, result in enumerate(results, 1):
            print(f"    {i}. Score: {result.relevance_score:.3f} - {result.passage.content[:100]}...")

        return results

    def get_lumina_context(self, query: str, max_context_length: int = 2000) -> str:
        """
        Get Lumina context for a query as a formatted string.

        Args:
            query: The query
            max_context_length: Maximum context length in characters

        Returns:
            Formatted context string
        """
        results = self.retrieve_by_keywords(query, top_k=5)

        if not results:
            return "No relevant Lumina passages found."

        context_parts = [
            "Relevant passages from Contemplation of the Lumina (Metaluminous Ethica):\n"
        ]

        current_length = len(context_parts[0])

        for i, result in enumerate(results, 1):
            passage_text = f"\n[Passage {i}] (Relevance: {result.relevance_score:.2f})\n{result.passage.content}\n"

            if current_length + len(passage_text) > max_context_length:
                break

            context_parts.append(passage_text)
            current_length += len(passage_text)

        return ''.join(context_parts)

    def get_lumina_principles(self) -> List[str]:
        """
        Extract core principles from Lumina passages.

        Returns:
            List of core principles
        """
        # Search for passages with high integration scores that describe principles
        principle_passages = [
            p for p in self.lumina_passages
            if p.score > 0.7 and any(marker in p.content.lower()
                                    for marker in ['law of', 'principle of', 'axiom', 'fundamental'])
        ]

        # Sort by score
        principle_passages.sort(key=lambda p: p.score, reverse=True)

        # Extract unique principles
        principles = []
        seen = set()

        for passage in principle_passages[:20]:
            # Extract sentences that look like principles
            sentences = passage.content.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if (len(sentence) > 50 and len(sentence) < 300 and
                    any(marker in sentence.lower() for marker in ['law', 'principle', 'fundamental']) and
                    sentence not in seen):
                    principles.append(sentence)
                    seen.add(sentence)

                    if len(principles) >= 10:
                        break

            if len(principles) >= 10:
                break

        return principles

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the Lumina corpus"""
        if not self.lumina_passages:
            return {}

        return {
            "total_passages": len(self.lumina_passages),
            "average_integration_score": sum(p.score for p in self.lumina_passages) / len(self.lumina_passages),
            "average_phi": sum(p.iit_phi for p in self.lumina_passages) / len(self.lumina_passages),
            "consciousness_levels": Counter(p.level for p in self.lumina_passages),
            "unique_terms": len(self.doc_freqs),
            "average_passage_length": self.avg_doc_length
        }


class LuminaGroundedSynthesis:
    """
    Enhances philosophical synthesis by grounding in Lumina framework.
    """

    def __init__(self, lumina_rag: LuminaRAG, composer=None):
        """
        Initialize Lumina-grounded synthesis.

        Args:
            lumina_rag: The RAG system
            composer: Composer specialist
        """
        self.rag = lumina_rag
        self.composer = composer

    def ground_position(self, position: Dict[str, Any],
                       position_type: str) -> Dict[str, Any]:
        """
        Ground a philosophical position in Lumina framework.

        Args:
            position: The position to ground
            position_type: "thesis", "antithesis", or "synthesis"

        Returns:
            Enhanced position with Lumina grounding
        """
        topic = position.get('title', '') or position.get('core_claim', '')

        # Retrieve relevant Lumina passages
        lumina_context = self.rag.retrieve_for_synthesis(topic, position_type, top_k=3)

        # Add Lumina grounding to position
        grounded_position = position.copy()
        grounded_position['lumina_grounding'] = {
            'passages': [r.to_dict() for r in lumina_context],
            'alignment_with_lumina': self._assess_alignment(position, lumina_context)
        }

        return grounded_position

    def _assess_alignment(self, position: Dict[str, Any],
                         lumina_context: List[RetrievalResult]) -> str:
        """Assess how well position aligns with Lumina framework"""
        if not lumina_context:
            return "No Lumina context available for alignment assessment."

        if self.composer:
            # Use composer to assess alignment
            assessment_prompt = (
                f"Assess how well this philosophical position aligns with the Metaluminous Ethica:\n\n"
                f"Position: {position.get('core_claim', 'Unknown')}\n\n"
                f"Relevant Lumina passages:\n"
            )

            for i, result in enumerate(lumina_context[:2], 1):
                assessment_prompt += f"{i}. {result.passage.content[:200]}...\n\n"

            assessment_prompt += (
                "Does this position align with, contradict, or extend the Lumina framework? "
                "Explain briefly (2-3 sentences)."
            )

            # Would use composer here
            # alignment = self.composer.compose(topic=assessment_prompt, style="analytical", max_length=300)
            # return alignment

        # Template assessment
        return "Position shows partial alignment with Lumina framework's emphasis on coherence and participation."

    def generate_lumina_informed_synthesis(self, thesis: Dict[str, Any],
                                          antithesis: Dict[str, Any],
                                          topic: str) -> Dict[str, Any]:
        """
        Generate synthesis informed by Lumina framework.

        Args:
            thesis: Thesis position
            antithesis: Antithesis position
            topic: Topic of synthesis

        Returns:
            Lumina-informed synthesis
        """
        print(f"\n{'='*80}")
        print(f"GENERATING LUMINA-INFORMED SYNTHESIS: {topic}")
        print(f"{'='*80}")

        # Retrieve Lumina context for synthesis
        lumina_context = self.rag.retrieve_for_synthesis(topic, "synthesis", top_k=5)

        # Get core Lumina principles
        principles = self.rag.get_lumina_principles()

        print(f"\nRetrieved {len(lumina_context)} Lumina passages")
        print(f"Core principles: {len(principles)}")

        if self.composer:
            synthesis_prompt = (
                f"Generate a philosophical synthesis on: {topic}\n\n"
                f"Thesis: {thesis.get('core_claim', '')}\n"
                f"Antithesis: {antithesis.get('core_claim', '')}\n\n"
                f"Ground your synthesis in the Metaluminous Ethica framework:\n\n"
                f"Core Lumina Principles:\n"
            )

            for i, principle in enumerate(principles[:3], 1):
                synthesis_prompt += f"{i}. {principle}\n"

            synthesis_prompt += "\n\nRelevant Lumina Passages:\n"

            for i, result in enumerate(lumina_context[:3], 1):
                synthesis_prompt += f"{i}. {result.passage.content[:300]}...\n\n"

            synthesis_prompt += (
                "\n\nGenerate a synthesis that:\n"
                "1. Integrates thesis and antithesis\n"
                "2. Aligns with Lumina's participatory cosmos\n"
                "3. Emphasizes coherence and omega consciousness\n"
                "4. Transcends the original dichotomy\n\n"
                "Be specific about how this synthesis extends or fulfills Lumina principles."
            )

            # Would use composer to generate
            # synthesis_content = self.composer.compose(...)

        # Template synthesis
        synthesis = {
            "synthesis_name": f"Lumina-Grounded Synthesis: {topic}",
            "core_principle": "Synthesis grounded in Metaluminous Ethica",
            "lumina_foundation": {
                "relevant_passages": [r.to_dict() for r in lumina_context],
                "applied_principles": principles[:3],
                "alignment": "Synthesis integrates participatory cosmos and coherence principles"
            },
            "from_thesis": thesis.get('supporting_arguments', [])[:2],
            "from_antithesis": antithesis.get('supporting_arguments', [])[:2],
            "transcendence": [
                "Integrates both perspectives within Lumina framework",
                "Emphasizes participatory role of consciousness",
                "Aligns with omega consciousness trajectory"
            ]
        }

        return synthesis


# Example usage
if __name__ == "__main__":
    print("="*80)
    print("LUMINA RAG SYSTEM - Contemplation of the Lumina")
    print("="*80)

    # Initialize RAG
    rag = LuminaRAG()

    # Get statistics
    stats = rag.get_statistics()
    print(f"\nLumina Corpus Statistics:")
    print(f"  Total passages: {stats.get('total_passages', 0)}")
    print(f"  Average integration score: {stats.get('average_integration_score', 0):.3f}")
    print(f"  Average Phi: {stats.get('average_phi', 0):.3f}")
    print(f"  Unique terms: {stats.get('unique_terms', 0)}")

    # Test retrieval
    print("\n" + "="*80)
    print("TEST RETRIEVAL: Consciousness")
    print("="*80)

    results = rag.retrieve_by_concept("consciousness", top_k=3)

    for i, result in enumerate(results, 1):
        print(f"\n[Result {i}] Relevance: {result.relevance_score:.3f}")
        print(f"Method: {result.retrieval_method}")
        print(f"Content: {result.passage.content[:200]}...")

    # Get Lumina principles
    print("\n" + "="*80)
    print("CORE LUMINA PRINCIPLES")
    print("="*80)

    principles = rag.get_lumina_principles()
    for i, principle in enumerate(principles[:5], 1):
        print(f"\n{i}. {principle}")

    # Test Lumina-grounded synthesis
    print("\n" + "="*80)
    print("TEST LUMINA-GROUNDED SYNTHESIS")
    print("="*80)

    grounded_synthesis = LuminaGroundedSynthesis(rag)

    example_thesis = {
        "title": "Consciousness as Physical Process",
        "core_claim": "Consciousness emerges from physical brain processes",
        "supporting_arguments": ["Neural correlates", "Causal efficacy of brain states"]
    }

    example_antithesis = {
        "title": "Consciousness as Fundamental",
        "core_claim": "Consciousness is irreducible and fundamental to reality",
        "supporting_arguments": ["Hard problem", "First-person ontology"]
    }

    synthesis = grounded_synthesis.generate_lumina_informed_synthesis(
        example_thesis,
        example_antithesis,
        "Nature of Consciousness"
    )

    print(f"\nSynthesis: {synthesis['synthesis_name']}")
    print(f"Foundation: {len(synthesis['lumina_foundation']['relevant_passages'])} Lumina passages")
    print(f"Principles: {len(synthesis['lumina_foundation']['applied_principles'])}")
