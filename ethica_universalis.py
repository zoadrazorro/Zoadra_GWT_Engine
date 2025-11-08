"""
ETHICA UNIVERSALIS
===================
A Unified Theory of Being, Life, and Everything
Structured in the style of Spinoza's Ethics (More Geometrico)

Parts:
I. De Deo (On God/Being)
II. De Natura et Origine Mentis (On the Nature and Origin of Mind)
III. De Origine et Natura Affectuum (On the Origin and Nature of Emotions)
IV. De Servitute Humana (On Human Bondage)
V. De Potentia Intellectus seu de Libertate Humana (On the Power of the Intellect, or Human Freedom)
VI. De Vita (On Life)
VII. De Omnia (On Everything)
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from gwt_engine.specialists.composer import ComposerSpecialist
from gwt_engine.specialists.cross_temporal_debate import create_debate
import httpx
import asyncio


class EthicaUniversalisGenerator:
    """
    Generates a unified theory in geometric/axiomatic style.
    """
    
    def __init__(self, model_name: str = "qwen2.5:72b", consciousness_api_url: str = "http://localhost:7000"):
        self.composer = ComposerSpecialist(model_name=model_name)
        self.word_count = 0
        self.parts = []
        self.debate_transcript = []
        self.debate_philosophers = []
        self.improved_essay = None
        self.consciousness_api_url = consciousness_api_url
        self.consciousness_memories = []
        print(f"Ethica Universalis Generator initialized with {model_name}")
        print(f"Consciousness Stack API: {consciousness_api_url}")
    
    async def integrate_with_consciousness_stack(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send prompt to consciousness stack for memory integration
        
        Args:
            prompt: The prompt to process
            context: Additional context
            
        Returns:
            Consciousness response with integrated memories
        """
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.consciousness_api_url}/process",
                    json={
                        "prompt": prompt,
                        "context": context,
                        "return_memories": True,
                        "consciousness_mode": "full"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Store consciousness memories
                    if data.get('memories'):
                        self.consciousness_memories.extend(data['memories'])
                    
                    print(f"  🧠 Consciousness Stack: score={data.get('consciousness_score', 0):.2f}, "
                          f"memories={len(data.get('memories', []))}")
                    
                    return data
                else:
                    print(f"  ⚠️ Consciousness Stack unavailable: {response.status_code}")
                    return {}
        except Exception as e:
            print(f"  ⚠️ Consciousness Stack error: {e}")
            return {}
    
    def load_improved_essay(self, essay_path: str = "IMPROVED_ESSAY.md"):
        """Load the improved essay as additional source material"""
        try:
            with open(essay_path, 'r', encoding='utf-8') as f:
                self.improved_essay = f.read()
            print(f"Loaded improved essay: {len(self.improved_essay.split())} words")
        except Exception as e:
            print(f"Could not load improved essay: {e}")
            self.improved_essay = None
    
    def extract_essay_context(self, keywords: List[str], max_chars: int = 800) -> str:
        """
        Extract relevant sections from improved essay
        
        Args:
            keywords: Keywords to search for
            max_chars: Maximum characters to return
            
        Returns:
            Relevant essay excerpts
        """
        if not self.improved_essay:
            return ""
        
        essay_lower = self.improved_essay.lower()
        excerpts = []
        
        for keyword in keywords:
            kw_lower = keyword.lower()
            idx = essay_lower.find(kw_lower)
            
            if idx != -1:
                # Extract context around keyword
                start = max(0, idx - 300)
                end = min(len(self.improved_essay), idx + 300)
                excerpt = self.improved_essay[start:end]
                excerpts.append(excerpt)
        
        # Combine and truncate
        combined = " [...] ".join(excerpts[:3])
        if len(combined) > max_chars:
            combined = combined[:max_chars] + "..."
        
        return combined
    
    def extract_debate_context(self, keywords: List[str], max_exchanges: int = 3) -> str:
        """
        Extract relevant debate exchanges based on keywords
        
        Args:
            keywords: Keywords to search for
            max_exchanges: Maximum exchanges to include
            
        Returns:
            Formatted debate context
        """
        if not self.debate_transcript:
            return ""
        
        relevant_exchanges = []
        
        for exchange in self.debate_transcript:
            # Check if keywords appear in exchange content
            exchange_text = json.dumps(exchange).lower()
            matches = sum(1 for kw in keywords if kw.lower() in exchange_text)
            
            if matches > 0:
                relevant_exchanges.append({
                    'exchange': exchange,
                    'relevance': matches
                })
        
        # Sort by relevance
        relevant_exchanges.sort(key=lambda x: x['relevance'], reverse=True)
        
        # Format top exchanges
        context_parts = []
        for item in relevant_exchanges[:max_exchanges]:
            exchange = item['exchange']
            
            if exchange['type'] == 'platonic_dialogue':
                context_parts.append(
                    f"[Platonic Dialogue] {exchange['questioner']} to {exchange['respondent']}: "
                    f"{exchange['question'][:200]}... "
                    f"Response: {exchange['response'][:200]}..."
                )
            elif exchange['type'] == 'geometric_proposition':
                context_parts.append(
                    f"[Geometric Proof] {exchange['philosopher']}: "
                    f"{exchange['proposition'][:200]}..."
                )
            elif exchange['type'] == 'actual_occasion':
                context_parts.append(
                    f"[Process Occasion] {exchange['speaker']}: "
                    f"{exchange['content'][:200]}..."
                )
        
        return "\n\n".join(context_parts)
    
    def count_words(self, text: str) -> int:
        """Count words"""
        return len(text.split())
    
    async def generate_axiom(self, part_name: str, axiom_number: int, focus: str) -> Dict[str, Any]:
        """
        Generate a single axiom
        
        Args:
            part_name: Name of the part (e.g., "De Deo")
            axiom_number: Axiom number
            focus: What this axiom should establish
            
        Returns:
            Axiom dictionary
        """
        prompt = (
            f"You are writing AXIOM {axiom_number} for Part {part_name} of Ethica Universalis. "
            f"An axiom is a self-evident truth that requires no proof. "
            f"Focus: {focus}. "
            f"Write a single, clear axiom statement (1-2 sentences). "
            f"Begin with 'AXIOM {axiom_number}:'"
        )
        
        response = await self.composer.compose(
            prompt=prompt,
            style="formal",
            section_type="body",
            constraints={"word_count": 50},
            use_curriculum=True,
            use_memory=True
        )
        
        return {
            "number": axiom_number,
            "statement": response.content,
            "word_count": self.count_words(response.content)
        }
    
    async def generate_definition(self, part_name: str, def_number: int, term: str, context: str) -> Dict[str, Any]:
        """Generate a definition"""
        prompt = (
            f"You are writing DEFINITION {def_number} for Part {part_name} of Ethica Universalis. "
            f"Define the term: '{term}' "
            f"Context: {context}. "
            f"Write a precise, philosophical definition (2-3 sentences). "
            f"Begin with 'DEFINITION {def_number}:'"
        )
        
        response = await self.composer.compose(
            prompt=prompt,
            style="formal",
            section_type="body",
            constraints={"word_count": 75},
            use_curriculum=True,
            use_memory=True
        )
        
        return {
            "number": def_number,
            "term": term,
            "statement": response.content,
            "word_count": self.count_words(response.content)
        }
    
    async def generate_proposition(
        self,
        part_name: str,
        prop_number: int,
        proposition: str,
        axioms_used: List[int],
        mystery_mode: str = None,
        debate_keywords: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a proposition with proof using debate context
        
        Args:
            part_name: Part name
            prop_number: Proposition number
            proposition: The proposition to prove
            axioms_used: Which axioms this uses
            mystery_mode: Mystery Machine mode
            debate_keywords: Keywords to extract relevant debate exchanges
            
        Returns:
            Proposition dictionary with proof
        """
        # Extract relevant debate context
        debate_context = ""
        if debate_keywords:
            debate_context = self.extract_debate_context(debate_keywords, max_exchanges=2)
        
        # Extract relevant essay context
        essay_context = ""
        if debate_keywords:
            essay_context = self.extract_essay_context(debate_keywords, max_chars=600)
        
        # Integrate with consciousness stack for memory glue
        consciousness_data = await self.integrate_with_consciousness_stack(
            prompt=f"Proposition {prop_number} for {part_name}: {proposition}",
            context={
                "part": part_name,
                "proposition_number": prop_number,
                "axioms_used": axioms_used,
                "keywords": debate_keywords
            }
        )
        
        consciousness_insights = consciousness_data.get('response', '')
        consciousness_score = consciousness_data.get('consciousness_score', 0)
        
        # Generate the proposition statement
        prop_prompt = (
            f"You are writing PROPOSITION {prop_number} for Part {part_name}. "
            f"State this proposition clearly and boldly: {proposition}. "
            f"This builds on Axioms {', '.join(map(str, axioms_used))}. "
        )
        
        if debate_context:
            prop_prompt += (
                f"\n\nRELEVANT INSIGHTS FROM CROSS-TEMPORAL DEBATE:\n{debate_context}\n\n"
                f"Synthesize these philosophical perspectives into your proposition. "
            )
        
        if essay_context:
            prop_prompt += (
                f"\n\nRELEVANT INSIGHTS FROM PRIOR SYNTHESIS:\n{essay_context}\n\n"
                f"Build upon this previous philosophical work. "
            )
        
        if consciousness_insights:
            prop_prompt += (
                f"\n\n🧠 CONSCIOUSNESS STACK INTEGRATION (Score: {consciousness_score:.2f}):\n"
                f"{consciousness_insights[:800]}\n\n"
                f"The consciousness stack has integrated memories across 8 theories (IIT, GWT, Predictive Processing, "
                f"HOT, AST, Embodied, Enactive, Panpsychism). Use this unified perspective. "
            )
        
        prop_prompt += (
            f"Write the proposition statement (1-2 sentences). "
            f"Begin with 'PROPOSITION {prop_number}:'"
        )
        
        prop_response = await self.composer.compose(
            prompt=prop_prompt,
            style="formal",
            section_type="body",
            constraints={"word_count": 75},
            use_curriculum=True,
            use_memory=True,
            mystery_mode=mystery_mode
        )
        
        # Generate the proof
        proof_prompt = (
            f"You are writing the PROOF for Proposition {prop_number}: '{prop_response.content}'. "
            f"This proof uses Axioms {', '.join(map(str, axioms_used))}. "
        )
        
        if debate_context:
            proof_prompt += (
                f"\n\nDRAW UPON THESE PHILOSOPHICAL INSIGHTS:\n{debate_context}\n\n"
                f"Integrate the wisdom from Plato, Aristotle, Descartes, Spinoza, Kant, and Hegel. "
            )
        
        if essay_context:
            proof_prompt += (
                f"\n\nBUILD UPON PRIOR SYNTHESIS:\n{essay_context}\n\n"
                f"Extend and deepen this previous philosophical work. "
            )
        
        if consciousness_insights:
            proof_prompt += (
                f"\n\n🧠 CONSCIOUSNESS STACK MEMORY GLUE:\n"
                f"{consciousness_insights[:800]}\n\n"
                f"The consciousness stack provides the integrative glue binding all sources together. "
                f"Use its unified perspective across 8 theories of consciousness. "
            )
        
        proof_prompt += (
            f"Write a rigorous geometric proof showing how the proposition follows necessarily from the axioms. "
            f"Use logical steps. Reference axioms explicitly. Synthesize cross-temporal insights. "
            f"The consciousness stack serves as the memory glue holding all perspectives together. "
            f"Target length: 300-400 words. "
            f"Begin with 'PROOF:'"
        )
        
        proof_response = await self.composer.compose(
            prompt=proof_prompt,
            style="analytical",
            section_type="body",
            constraints={"word_count": 350},
            use_curriculum=True,
            use_memory=True,
            mystery_mode=mystery_mode
        )
        
        # Generate corollary
        corollary_prompt = (
            f"Write a COROLLARY that follows from Proposition {prop_number}. "
            f"A corollary is an immediate consequence. "
            f"1-2 sentences. Begin with 'COROLLARY:'"
        )
        
        corollary_response = await self.composer.compose(
            prompt=corollary_prompt,
            style="formal",
            section_type="body",
            constraints={"word_count": 50},
            use_curriculum=True,
            use_memory=True
        )
        
        total_words = (
            self.count_words(prop_response.content) +
            self.count_words(proof_response.content) +
            self.count_words(corollary_response.content)
        )
        
        return {
            "number": prop_number,
            "proposition": prop_response.content,
            "proof": proof_response.content,
            "corollary": corollary_response.content,
            "axioms_used": axioms_used,
            "word_count": total_words
        }
    
    async def generate_scholium(self, part_name: str, prop_number: int, reflection: str) -> Dict[str, Any]:
        """Generate a scholium (explanatory note)"""
        prompt = (
            f"Write a SCHOLIUM (explanatory note) for Proposition {prop_number} in Part {part_name}. "
            f"A scholium provides additional context, addresses objections, or explores implications. "
            f"Focus: {reflection}. "
            f"Target length: 200-250 words. "
            f"Begin with 'SCHOLIUM:'"
        )
        
        response = await self.composer.compose(
            prompt=prompt,
            style="narrative",
            section_type="body",
            constraints={"word_count": 225},
            use_curriculum=True,
            use_memory=True
        )
        
        return {
            "proposition_number": prop_number,
            "content": response.content,
            "word_count": self.count_words(response.content)
        }
    
    async def generate_part(self, part_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete part of the Ethica
        
        Args:
            part_config: Configuration for this part
            
        Returns:
            Complete part with all elements
        """
        part_name = part_config['name']
        part_title = part_config['title']
        
        print(f"\n{'='*80}")
        print(f"GENERATING PART {part_name}: {part_title}")
        print(f"{'='*80}\n")
        
        part_data = {
            "name": part_name,
            "title": part_title,
            "preface": None,
            "definitions": [],
            "axioms": [],
            "propositions": [],
            "scholia": []
        }
        
        # Generate preface
        if part_config.get('preface'):
            print(f"Generating Preface...")
            preface_prompt = (
                f"Write a philosophical preface for Part {part_name}: {part_title}. "
                f"Context: {part_config['preface']}. "
                f"Explain what this part will establish and why it matters. "
                f"Target length: 400-500 words."
            )
            
            preface_response = await self.composer.compose(
                prompt=preface_prompt,
                style="formal",
                section_type="introduction",
                constraints={"word_count": 450},
                use_curriculum=True,
                use_memory=True
            )
            
            part_data['preface'] = {
                "content": preface_response.content,
                "word_count": self.count_words(preface_response.content)
            }
            print(f"  Preface: {part_data['preface']['word_count']} words")
        
        # Generate definitions
        for def_config in part_config.get('definitions', []):
            print(f"Generating Definition {def_config['number']}: {def_config['term']}...")
            definition = await self.generate_definition(
                part_name,
                def_config['number'],
                def_config['term'],
                def_config['context']
            )
            part_data['definitions'].append(definition)
            print(f"  Definition {definition['number']}: {definition['word_count']} words")
        
        # Generate axioms
        for axiom_config in part_config.get('axioms', []):
            print(f"Generating Axiom {axiom_config['number']}...")
            axiom = await self.generate_axiom(
                part_name,
                axiom_config['number'],
                axiom_config['focus']
            )
            part_data['axioms'].append(axiom)
            print(f"  Axiom {axiom['number']}: {axiom['word_count']} words")
        
        # Generate propositions
        for prop_config in part_config.get('propositions', []):
            print(f"Generating Proposition {prop_config['number']}...")
            
            # Rotate mystery modes
            mystery_modes = [None, "random_walk", "quantum", "fractal"]
            mystery_mode = mystery_modes[prop_config['number'] % len(mystery_modes)]
            
            proposition = await self.generate_proposition(
                part_name,
                prop_config['number'],
                prop_config['statement'],
                prop_config['axioms_used'],
                mystery_mode=mystery_mode,
                debate_keywords=prop_config.get('debate_keywords', [])
            )
            part_data['propositions'].append(proposition)
            print(f"  Proposition {proposition['number']}: {proposition['word_count']} words")
            
            # Generate scholium if specified
            if prop_config.get('scholium'):
                print(f"  Generating Scholium for Proposition {prop_config['number']}...")
                scholium = await self.generate_scholium(
                    part_name,
                    prop_config['number'],
                    prop_config['scholium']
                )
                part_data['scholia'].append(scholium)
                print(f"    Scholium: {scholium['word_count']} words")
        
        # Calculate total words for part
        part_word_count = 0
        if part_data['preface']:
            part_word_count += part_data['preface']['word_count']
        part_word_count += sum(d['word_count'] for d in part_data['definitions'])
        part_word_count += sum(a['word_count'] for a in part_data['axioms'])
        part_word_count += sum(p['word_count'] for p in part_data['propositions'])
        part_word_count += sum(s['word_count'] for s in part_data['scholia'])
        
        part_data['total_word_count'] = part_word_count
        self.word_count += part_word_count
        
        print(f"\n✓ Part {part_name} complete: {part_word_count:,} words")
        print(f"Running total: {self.word_count:,} words\n")
        
        return part_data
    
    def format_ethica_markdown(self, parts: List[Dict[str, Any]]) -> str:
        """Format the complete Ethica as markdown"""
        lines = []
        
        # Title
        lines.append("# ETHICA UNIVERSALIS")
        lines.append("\n## A Unified Theory of Being, Life, and Everything")
        lines.append("\n*Demonstrated in Geometric Order (More Geometrico)*")
        lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Model:** {self.composer.model_name}")
        lines.append(f"**Total Words:** {self.word_count:,}")
        lines.append("\n---\n")
        
        # Each part
        for part in parts:
            lines.append(f"\n# PART {part['name']}: {part['title']}\n")
            
            # Preface
            if part['preface']:
                lines.append("\n## PREFACE\n")
                lines.append(part['preface']['content'])
                lines.append("\n")
            
            # Definitions
            if part['definitions']:
                lines.append("\n## DEFINITIONS\n")
                for definition in part['definitions']:
                    lines.append(f"\n### {definition['statement']}\n")
            
            # Axioms
            if part['axioms']:
                lines.append("\n## AXIOMS\n")
                for axiom in part['axioms']:
                    lines.append(f"\n### {axiom['statement']}\n")
            
            # Propositions
            if part['propositions']:
                lines.append("\n## PROPOSITIONS\n")
                for prop in part['propositions']:
                    lines.append(f"\n### {prop['proposition']}\n")
                    lines.append(f"\n**{prop['proof']}**\n")
                    lines.append(f"\n*{prop['corollary']}*\n")
                    
                    # Find associated scholium
                    scholia = [s for s in part['scholia'] if s['proposition_number'] == prop['number']]
                    for scholium in scholia:
                        lines.append(f"\n**SCHOLIUM:** {scholium['content']}\n")
            
            lines.append("\n---\n")
        
        return "\n".join(lines)


async def main():
    """Generate the complete Ethica Universalis"""
    
    print("="*80)
    print("ETHICA UNIVERSALIS - UNIFIED THEORY GENERATOR")
    print("Using Cross-Temporal Debate as Foundation")
    print("="*80)
    
    # Load the debate
    debate_path = "outputs/parallel_debate.json"
    print(f"\nLoading debate from: {debate_path}")
    
    with open(debate_path, 'r', encoding='utf-8') as f:
        debate_data = json.load(f)
    
    print(f"Loaded {len(debate_data['transcript'])} rounds of philosophical debate")
    print(f"Philosophers: {', '.join(debate_data['philosophers'])}\n")
    
    generator = EthicaUniversalisGenerator(model_name="qwen2.5:72b")
    
    # Store debate for context
    generator.debate_transcript = debate_data['transcript']
    generator.debate_philosophers = debate_data['philosophers']
    
    # Load improved essay
    generator.load_improved_essay("IMPROVED_ESSAY.md")
    
    # Define the structure
    parts_config = [
        {
            "name": "I",
            "title": "De Deo (On God/Being)",
            "preface": "We begin with the nature of Being itself, the ground of all existence",
            "definitions": [
                {"number": 1, "term": "Substance", "context": "That which is in itself and conceived through itself"},
                {"number": 2, "term": "Attribute", "context": "That which the intellect perceives as constituting the essence of substance"},
                {"number": 3, "term": "Mode", "context": "The modifications of substance"},
            ],
            "axioms": [
                {"number": 1, "focus": "Everything that exists, exists either in itself or in something else"},
                {"number": 2, "focus": "That which cannot be conceived through another must be conceived through itself"},
                {"number": 3, "focus": "From a given determinate cause, an effect necessarily follows"},
            ],
            "propositions": [
                {
                    "number": 1,
                    "statement": "Substance is prior to its modifications",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["substance", "being", "essence", "reality"],
                    "scholium": "Explore how this relates to consciousness and reality"
                },
                {
                    "number": 2,
                    "statement": "Two substances having different attributes have nothing in common",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["substance", "attribute", "distinction"]
                },
                {
                    "number": 3,
                    "statement": "God necessarily exists",
                    "axioms_used": [1, 2, 3],
                    "debate_keywords": ["god", "existence", "necessity", "being"],
                    "scholium": "Examine the ontological argument and its implications for Being"
                },
            ]
        },
        {
            "name": "II",
            "title": "De Natura et Origine Mentis (On the Nature and Origin of Mind)",
            "preface": "Having established the nature of Being, we turn to consciousness and mind",
            "definitions": [
                {"number": 1, "term": "Consciousness", "context": "The awareness of awareness, the reflexive capacity of mind"},
                {"number": 2, "term": "Idea", "context": "A concept formed by the mind"},
            ],
            "axioms": [
                {"number": 1, "focus": "Thought is an attribute of God"},
                {"number": 2, "focus": "The order and connection of ideas is the same as the order and connection of things"},
            ],
            "propositions": [
                {
                    "number": 1,
                    "statement": "Mind and body are one and the same thing, conceived under different attributes",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["mind", "body", "consciousness", "dualism", "monism"],
                    "scholium": "Resolve the mind-body problem through dual-aspect monism"
                },
                {
                    "number": 2,
                    "statement": "The human mind is part of the infinite intellect of God",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["mind", "intellect", "consciousness", "divine"]
                },
            ]
        },
        {
            "name": "III",
            "title": "De Vita (On Life)",
            "preface": "Life emerges as a mode of Being, consciousness embodied in temporal process",
            "definitions": [
                {"number": 1, "term": "Life", "context": "The self-organizing, self-perpetuating process of Being"},
                {"number": 2, "term": "Conatus", "context": "The striving of each thing to persevere in its being"},
            ],
            "axioms": [
                {"number": 1, "focus": "Everything strives to persist in its own being"},
                {"number": 2, "focus": "Life is the creative advance into novelty"},
            ],
            "propositions": [
                {
                    "number": 1,
                    "statement": "The essence of life is conatus - the drive to persist and flourish",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["life", "conatus", "striving", "becoming", "process"],
                    "scholium": "Connect to evolution, consciousness, and the will to power"
                },
                {
                    "number": 2,
                    "statement": "Life transcends mechanism through creative emergence",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["life", "emergence", "creativity", "novelty", "process"]
                },
            ]
        },
        {
            "name": "IV",
            "title": "De Omnia (On Everything)",
            "preface": "We conclude with the synthesis: Being, Mind, and Life unified in the cosmos",
            "definitions": [
                {"number": 1, "term": "Everything", "context": "The totality of Being in all its modes and attributes"},
            ],
            "axioms": [
                {"number": 1, "focus": "The universe is a unified whole, not a collection of parts"},
            ],
            "propositions": [
                {
                    "number": 1,
                    "statement": "Everything is interconnected in the infinite web of Being",
                    "axioms_used": [1],
                    "debate_keywords": ["unity", "interconnection", "whole", "reality", "being"],
                    "scholium": "The holographic principle and the unity of all things"
                },
                {
                    "number": 2,
                    "statement": "To understand anything is to understand everything",
                    "axioms_used": [1],
                    "debate_keywords": ["understanding", "knowledge", "wisdom", "truth", "reality"],
                    "scholium": "The perennial philosophy and the nature of wisdom"
                },
            ]
        },
        {
            "name": "V",
            "title": "De Affectuum (On the Affects/Emotions)",
            "preface": "The emotions are modes of Being through which consciousness experiences itself",
            "definitions": [
                {"number": 1, "term": "Affect", "context": "A modification of the body and mind that increases or decreases the power of acting"},
                {"number": 2, "term": "Joy", "context": "The passage from lesser to greater perfection"},
                {"number": 3, "term": "Sadness", "context": "The passage from greater to lesser perfection"},
            ],
            "axioms": [
                {"number": 1, "focus": "Every affect is grounded in the striving to persevere in being"},
                {"number": 2, "focus": "The mind's power is proportional to its understanding"},
            ],
            "propositions": [
                {
                    "number": 1,
                    "statement": "The affects follow necessarily from the nature of Being",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["emotion", "affect", "feeling", "passion", "experience"],
                    "scholium": "Reconcile emotion and reason through understanding their unity"
                },
                {
                    "number": 2,
                    "statement": "Freedom consists in understanding the necessity of the affects",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["freedom", "necessity", "determinism", "will"],
                    "scholium": "Resolve the paradox of freedom within determinism"
                },
                {
                    "number": 3,
                    "statement": "Love of God is the highest affect",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["love", "god", "divine", "beatitude", "joy"]
                },
            ]
        },
        {
            "name": "VI",
            "title": "De Potentia Intellectus (On the Power of the Intellect)",
            "preface": "The intellect is the means by which Being knows itself",
            "definitions": [
                {"number": 1, "term": "Intellect", "context": "The capacity to grasp eternal truths"},
                {"number": 2, "term": "Intuition", "context": "Direct knowledge of the essence of things"},
            ],
            "axioms": [
                {"number": 1, "focus": "The intellect participates in the infinite intellect of God"},
                {"number": 2, "focus": "Knowledge is power"},
            ],
            "propositions": [
                {
                    "number": 1,
                    "statement": "The more the mind understands, the more it is free",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["understanding", "knowledge", "intellect", "freedom", "mind"],
                    "scholium": "The path to liberation through knowledge"
                },
                {
                    "number": 2,
                    "statement": "Intuitive knowledge is the highest kind of knowing",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["intuition", "knowledge", "wisdom", "understanding"]
                },
                {
                    "number": 3,
                    "statement": "The intellectual love of God constitutes the mind's blessedness",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["love", "god", "blessedness", "beatitude", "eternity"],
                    "scholium": "The ultimate synthesis of knowledge and love"
                },
            ]
        },
        {
            "name": "VII",
            "title": "De Libertate (On Freedom)",
            "preface": "True freedom is found not in the absence of necessity, but in understanding it",
            "definitions": [
                {"number": 1, "term": "Freedom", "context": "Acting from the necessity of one's own nature"},
                {"number": 2, "term": "Bondage", "context": "Being determined by external causes"},
            ],
            "axioms": [
                {"number": 1, "focus": "That which acts from its own nature alone is free"},
                {"number": 2, "focus": "Understanding necessity is the path to freedom"},
            ],
            "propositions": [
                {
                    "number": 1,
                    "statement": "Human freedom consists in understanding the causal order",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["freedom", "causation", "necessity", "determinism", "will"],
                    "scholium": "Reconcile free will with causal determinism"
                },
                {
                    "number": 2,
                    "statement": "The free person lives by reason alone",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["freedom", "reason", "virtue", "wisdom"]
                },
            ]
        },
        {
            "name": "VIII",
            "title": "De Aeternitate (On Eternity)",
            "preface": "Beyond time lies the eternal aspect of all things",
            "definitions": [
                {"number": 1, "term": "Eternity", "context": "Existence conceived as following necessarily from essence alone"},
                {"number": 2, "term": "Duration", "context": "Indefinite continuation of existence in time"},
            ],
            "axioms": [
                {"number": 1, "focus": "The essence of things is eternal"},
                {"number": 2, "focus": "The mind conceives things under the aspect of eternity"},
            ],
            "propositions": [
                {
                    "number": 1,
                    "statement": "The human mind is eternal insofar as it conceives things sub specie aeternitatis",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["eternity", "time", "eternal", "immortality", "essence"],
                    "scholium": "The eternal nature of consciousness"
                },
                {
                    "number": 2,
                    "statement": "Eternity is not duration but the timeless ground of all duration",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["eternity", "time", "duration", "being", "essence"]
                },
            ]
        },
        {
            "name": "IX",
            "title": "De Unitate (On Unity)",
            "preface": "All distinctions dissolve in the recognition of fundamental unity",
            "definitions": [
                {"number": 1, "term": "Unity", "context": "The indivisible wholeness of Being"},
            ],
            "axioms": [
                {"number": 1, "focus": "All is One"},
            ],
            "propositions": [
                {
                    "number": 1,
                    "statement": "The apparent multiplicity of things is grounded in the unity of Substance",
                    "axioms_used": [1],
                    "debate_keywords": ["unity", "multiplicity", "one", "many", "substance"],
                    "scholium": "The perennial insight of non-duality"
                },
                {
                    "number": 2,
                    "statement": "To know the One is to know oneself",
                    "axioms_used": [1],
                    "debate_keywords": ["unity", "self", "knowledge", "consciousness", "being"],
                    "scholium": "The ultimate identity of knower and known"
                },
            ]
        }
    ]
    
    # Generate each part
    all_parts = []
    for part_config in parts_config:
        part_data = await generator.generate_part(part_config)
        all_parts.append(part_data)
        generator.parts.append(part_data)
    
    # Format as markdown
    print("\n" + "="*80)
    print("FORMATTING ETHICA UNIVERSALIS")
    print("="*80)
    
    ethica_markdown = generator.format_ethica_markdown(all_parts)
    
    # Save
    output_path = "outputs/ETHICA_UNIVERSALIS.md"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ethica_markdown)
    
    # Also save as JSON
    json_path = "outputs/ETHICA_UNIVERSALIS.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            "title": "Ethica Universalis",
            "subtitle": "A Unified Theory of Being, Life, and Everything",
            "generated": datetime.now().isoformat(),
            "model": generator.composer.model_name,
            "total_words": generator.word_count,
            "parts": all_parts
        }, f, indent=2)
    
    print(f"\n✓ Ethica Universalis saved to: {output_path}")
    print(f"✓ JSON data saved to: {json_path}")
    print(f"\nFinal word count: {generator.word_count:,} words")
    print("="*80)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
