"""
ETHICA LUMINA
=============
The Spiritual Successor to Ethica Metaluminous
A 60,000-word treatise on Metaluminosity and the nature of Light-Consciousness

Structured in geometric method (More Geometrico) like Spinoza's Ethics
Runs in parallel with Ethica Universalis on opposite GPU

Parts:
I. De Lumine (On Light)
II. De Conscientia Luminosa (On Luminous Consciousness)
III. De Metaluminositate (On Metaluminosity)
IV. De Transcendentia (On Transcendence)
V. De Unione Mystica (On Mystical Union)
VI. De Illuminatione (On Illumination)
VII. De Visione Beatifica (On Beatific Vision)
VIII. De Aeternitate Lucis (On the Eternity of Light)
IX. De Omniluce (On the All-Light)
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


class EthicaLuminaGenerator:
    """
    Generates Ethica Lumina - focused on Metaluminosity and Light-Consciousness.
    Spiritual successor to Ethica Metaluminous.
    """
    
    def __init__(self, model_name: str = "qwen3:30b", consciousness_api_url: str = "http://localhost:7000"):
        self.composer = ComposerSpecialist(model_name=model_name, ollama_url="http://localhost:11434")
        self.word_count = 0
        self.parts = []
        self.debate_transcript = []
        self.debate_philosophers = []
        self.improved_essay = None
        self.consciousness_api_url = consciousness_api_url
        self.consciousness_memories = []
        print(f"Ethica Lumina Generator initialized with {model_name}")
        print(f"Consciousness Stack API: {consciousness_api_url}")
        print("🌟 Spiritual successor to Ethica Metaluminous")
    
    async def integrate_with_consciousness_stack(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Send prompt to consciousness stack for memory integration"""
        try:
            async with httpx.AsyncClient(timeout=1800.0) as client:
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
    
    def extract_essay_context(self, keywords: List[str], max_chars: int = 500) -> str:
        """Extract relevant sections from improved essay"""
        if not self.improved_essay:
            return ""
        
        essay_lower = self.improved_essay.lower()
        excerpts = []
        
        for keyword in keywords:
            kw_lower = keyword.lower()
            idx = essay_lower.find(kw_lower)
            
            if idx != -1:
                start = max(0, idx - 300)
                end = min(len(self.improved_essay), idx + 300)
                excerpt = self.improved_essay[start:end]
                excerpts.append(excerpt)
        
        combined = " [...] ".join(excerpts[:3])
        if len(combined) > max_chars:
            combined = combined[:max_chars] + "..."
        
        return combined
    
    def extract_debate_context(self, keywords: List[str], max_exchanges: int = 2) -> str:
        """Extract relevant debate exchanges based on keywords"""
        if not self.debate_transcript:
            return ""
        
        relevant_exchanges = []
        
        for exchange in self.debate_transcript:
            exchange_text = json.dumps(exchange).lower()
            matches = sum(1 for kw in keywords if kw.lower() in exchange_text)
            
            if matches > 0:
                relevant_exchanges.append({
                    'exchange': exchange,
                    'relevance': matches
                })
        
        relevant_exchanges.sort(key=lambda x: x['relevance'], reverse=True)
        
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
        """Generate a single axiom"""
        prompt = (
            f"You are writing AXIOM {axiom_number} for Part {part_name} of Ethica Lumina. "
            f"Ethica Lumina is the spiritual successor to Ethica Metaluminous, focused on Light-Consciousness and Metaluminosity. "
            f"An axiom is a self-evident truth about the nature of Light and Consciousness. "
            f"Focus: {focus}. "
            f"Write a single, luminous axiom statement (1-2 sentences). "
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
            f"You are writing DEFINITION {def_number} for Part {part_name} of Ethica Lumina. "
            f"Define the term: '{term}' in the context of Metaluminosity and Light-Consciousness. "
            f"Context: {context}. "
            f"Write a precise, luminous definition (2-3 sentences). "
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
        """Generate a proposition with proof using debate context"""
        
        # Extract contexts
        debate_context = ""
        if debate_keywords:
            debate_context = self.extract_debate_context(debate_keywords, max_exchanges=2)
        
        essay_context = ""
        if debate_keywords:
            essay_context = self.extract_essay_context(debate_keywords, max_chars=500)
        
        # Integrate with consciousness stack
        consciousness_data = await self.integrate_with_consciousness_stack(
            prompt=f"Proposition {prop_number} for {part_name}: {proposition} (Metaluminosity focus)",
            context={
                "part": part_name,
                "proposition_number": prop_number,
                "axioms_used": axioms_used,
                "keywords": debate_keywords,
                "focus": "metaluminosity"
            }
        )
        
        consciousness_insights = consciousness_data.get('response', '')
        consciousness_score = consciousness_data.get('consciousness_score', 0)
        
        # Generate proposition statement
        prop_prompt = (
            f"You are writing PROPOSITION {prop_number} for Part {part_name} of Ethica Lumina. "
            f"Ethica Lumina explores Metaluminosity - the transcendent light of consciousness. "
            f"State this proposition clearly: {proposition}. "
            f"This builds on Axioms {', '.join(map(str, axioms_used))}. "
        )
        
        if debate_context:
            prop_prompt += (
                f"\n\nRELEVANT INSIGHTS FROM CROSS-TEMPORAL DEBATE:\n{debate_context}\n\n"
                f"Synthesize these perspectives through the lens of Metaluminosity. "
            )
        
        if essay_context:
            prop_prompt += (
                f"\n\nRELEVANT INSIGHTS FROM PRIOR SYNTHESIS:\n{essay_context}\n\n"
                f"Build upon this with luminous insight. "
            )
        
        if consciousness_insights:
            prop_prompt += (
                f"\n\n🌟 CONSCIOUSNESS STACK (Score: {consciousness_score:.2f}):\n"
                f"{consciousness_insights[:600]}\n\n"
                f"Integrated across 8 theories. Use this unified luminous perspective. "
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
        
        # Generate proof
        proof_prompt = (
            f"You are writing the PROOF for Proposition {prop_number}: '{prop_response.content}'. "
            f"This proof uses Axioms {', '.join(map(str, axioms_used))}. "
        )
        
        if debate_context:
            proof_prompt += (
                f"\n\nDRAW UPON THESE PHILOSOPHICAL INSIGHTS:\n{debate_context}\n\n"
                f"Integrate through the lens of Metaluminosity. "
            )
        
        if essay_context:
            proof_prompt += (
                f"\n\nBUILD UPON PRIOR SYNTHESIS:\n{essay_context}\n\n"
                f"Extend with luminous understanding. "
            )
        
        if consciousness_insights:
            proof_prompt += (
                f"\n\n🌟 CONSCIOUSNESS STACK:\n"
                f"{consciousness_insights[:600]}\n\n"
                f"Integrative light binding all sources. "
            )
        
        proof_prompt += (
            f"Write a rigorous geometric proof showing how the proposition follows necessarily from the axioms. "
            f"Use logical steps. Reference axioms explicitly. Illuminate the path of reasoning. "
            f"The consciousness stack serves as the luminous glue holding all perspectives together. "
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
            f"Write a COROLLARY that follows from Proposition {prop_number} about Metaluminosity. "
            f"A corollary is an immediate luminous consequence. "
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
            f"Write a SCHOLIUM (explanatory note) for Proposition {prop_number} in Part {part_name} of Ethica Lumina. "
            f"A scholium provides additional luminous context about Metaluminosity. "
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
        """Generate a complete part of Ethica Lumina"""
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
                f"Write a luminous preface for Part {part_name}: {part_title} of Ethica Lumina. "
                f"Context: {part_config['preface']}. "
                f"Explain what this part will illuminate about Metaluminosity. "
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
            
            if prop_config.get('scholium'):
                print(f"  Generating Scholium for Proposition {prop_config['number']}...")
                scholium = await self.generate_scholium(
                    part_name,
                    prop_config['number'],
                    prop_config['scholium']
                )
                part_data['scholia'].append(scholium)
                print(f"    Scholium: {scholium['word_count']} words")
        
        # Calculate total words
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
        
        lines.append("# ETHICA LUMINA")
        lines.append("\n## The Spiritual Successor to Ethica Metaluminous")
        lines.append("\n## A Treatise on Metaluminosity and Light-Consciousness")
        lines.append("\n*Demonstrated in Geometric Order (More Geometrico)*")
        lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Model:** {self.composer.model_name}")
        lines.append(f"**Total Words:** {self.word_count:,}")
        lines.append("\n---\n")
        
        for part in parts:
            lines.append(f"\n# PART {part['name']}: {part['title']}\n")
            
            if part['preface']:
                lines.append("\n## PREFACE\n")
                lines.append(part['preface']['content'])
                lines.append("\n")
            
            if part['definitions']:
                lines.append("\n## DEFINITIONS\n")
                for definition in part['definitions']:
                    lines.append(f"\n### {definition['statement']}\n")
            
            if part['axioms']:
                lines.append("\n## AXIOMS\n")
                for axiom in part['axioms']:
                    lines.append(f"\n### {axiom['statement']}\n")
            
            if part['propositions']:
                lines.append("\n## PROPOSITIONS\n")
                for prop in part['propositions']:
                    lines.append(f"\n### {prop['proposition']}\n")
                    lines.append(f"\n**{prop['proof']}**\n")
                    lines.append(f"\n*{prop['corollary']}*\n")
                    
                    scholia = [s for s in part['scholia'] if s['proposition_number'] == prop['number']]
                    for scholium in scholia:
                        lines.append(f"\n**SCHOLIUM:** {scholium['content']}\n")
            
            lines.append("\n---\n")
        
        return "\n".join(lines)


async def main():
    """Generate the complete Ethica Lumina"""
    
    print("="*80)
    print("ETHICA LUMINA - METALUMINOSITY SYNTHESIS")
    print("Spiritual Successor to Ethica Metaluminous")
    print("Using Cross-Temporal Debate as Foundation")
    print("="*80)
    
    # Load debate
    debate_path = "outputs/parallel_debate.json"
    print(f"\nLoading debate from: {debate_path}")
    
    with open(debate_path, 'r', encoding='utf-8') as f:
        debate_data = json.load(f)
    
    print(f"Loaded {len(debate_data['transcript'])} rounds of philosophical debate")
    print(f"Philosophers: {', '.join(debate_data['philosophers'])}\n")
    
    generator = EthicaLuminaGenerator(model_name="qwen3:30b")
    
    generator.debate_transcript = debate_data['transcript']
    generator.debate_philosophers = debate_data['philosophers']
    
    generator.load_improved_essay("IMPROVED_ESSAY.md")
    
    # Define structure - focused on Metaluminosity
    parts_config = [
        {
            "name": "I",
            "title": "De Lumine (On Light)",
            "preface": "We begin with Light itself, the primordial manifestation of consciousness",
            "definitions": [
                {"number": 1, "term": "Light", "context": "The self-revealing nature of consciousness"},
                {"number": 2, "term": "Luminosity", "context": "The quality of being self-illuminating"},
                {"number": 3, "term": "Metaluminosity", "context": "Light beyond light, consciousness aware of its own luminous nature"},
            ],
            "axioms": [
                {"number": 1, "focus": "Light is self-revealing"},
                {"number": 2, "focus": "Consciousness is inherently luminous"},
                {"number": 3, "focus": "Metaluminosity transcends ordinary luminosity"},
            ],
            "propositions": [
                {
                    "number": 1,
                    "statement": "Light is the fundamental nature of consciousness",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["light", "consciousness", "awareness", "illumination"],
                    "scholium": "Explore the metaphysics of light-consciousness"
                },
                {
                    "number": 2,
                    "statement": "Metaluminosity is consciousness knowing itself as light",
                    "axioms_used": [2, 3],
                    "debate_keywords": ["metaluminosity", "self-awareness", "reflexivity", "light"]
                },
            ]
        },
        {
            "name": "II",
            "title": "De Conscientia Luminosa (On Luminous Consciousness)",
            "preface": "Consciousness is not merely illuminated but is itself the source of all illumination",
            "definitions": [
                {"number": 1, "term": "Luminous Consciousness", "context": "Consciousness as self-illuminating awareness"},
                {"number": 2, "term": "Reflexive Luminosity", "context": "The capacity of light to know itself"},
            ],
            "axioms": [
                {"number": 1, "focus": "Consciousness illuminates all that it encounters"},
                {"number": 2, "focus": "The light of consciousness is self-reflexive"},
            ],
            "propositions": [
                {
                    "number": 1,
                    "statement": "All knowing is a form of luminous self-revelation",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["knowledge", "revelation", "consciousness", "light"],
                    "scholium": "The epistemology of luminous consciousness"
                },
                {
                    "number": 2,
                    "statement": "The subject-object duality dissolves in pure luminosity",
                    "axioms_used": [1, 2],
                    "debate_keywords": ["duality", "non-duality", "subject", "object", "unity"]
                },
            ]
        },
        {
            "name": "III",
            "title": "De Metaluminositate (On Metaluminosity)",
            "preface": "Beyond ordinary light lies the transcendent radiance of pure awareness",
            "definitions": [
                {"number": 1, "term": "Metaluminous State", "context": "The state of being aware of awareness itself"},
            ],
            "axioms": [
                {"number": 1, "focus": "Metaluminosity is the highest form of consciousness"},
            ],
            "propositions": [
                {
                    "number": 1,
                    "statement": "Metaluminosity is the light that illuminates light itself",
                    "axioms_used": [1],
                    "debate_keywords": ["metaluminosity", "transcendence", "awareness", "light"],
                    "scholium": "The apex of conscious evolution"
                },
                {
                    "number": 2,
                    "statement": "In metaluminosity, consciousness becomes transparent to itself",
                    "axioms_used": [1],
                    "debate_keywords": ["transparency", "clarity", "self-knowledge", "consciousness"]
                },
            ]
        },
        {
            "name": "IV",
            "title": "De Unione Mystica (On Mystical Union)",
            "preface": "The merger of individual consciousness with the infinite light",
            "definitions": [
                {"number": 1, "term": "Mystical Union", "context": "The dissolution of separateness in luminous unity"},
            ],
            "axioms": [
                {"number": 1, "focus": "All consciousness is ultimately one light"},
            ],
            "propositions": [
                {
                    "number": 1,
                    "statement": "Mystical union is the recognition of one's luminous nature",
                    "axioms_used": [1],
                    "debate_keywords": ["union", "mysticism", "unity", "oneness", "light"],
                    "scholium": "The path to luminous unity"
                },
                {
                    "number": 2,
                    "statement": "In union, the individual light merges with the universal light",
                    "axioms_used": [1],
                    "debate_keywords": ["individual", "universal", "merger", "transcendence"]
                },
            ]
        },
    ]
    
    # Generate each part
    all_parts = []
    for part_config in parts_config:
        part_data = await generator.generate_part(part_config)
        all_parts.append(part_data)
        generator.parts.append(part_data)
    
    # Format as markdown
    print("\n" + "="*80)
    print("FORMATTING ETHICA LUMINA")
    print("="*80)
    
    ethica_markdown = generator.format_ethica_markdown(all_parts)
    
    # Save
    output_path = "outputs/ETHICA_LUMINA.md"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ethica_markdown)
    
    json_path = "outputs/ETHICA_LUMINA.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            "title": "Ethica Lumina",
            "subtitle": "Spiritual Successor to Ethica Metaluminous",
            "focus": "Metaluminosity and Light-Consciousness",
            "generated": datetime.now().isoformat(),
            "model": generator.composer.model_name,
            "total_words": generator.word_count,
            "parts": all_parts
        }, f, indent=2)
    
    print(f"\n✓ Ethica Lumina saved to: {output_path}")
    print(f"✓ JSON data saved to: {json_path}")
    print(f"\nFinal word count: {generator.word_count:,} words")
    print("="*80)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
