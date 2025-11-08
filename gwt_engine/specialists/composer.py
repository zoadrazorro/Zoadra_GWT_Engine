"""
Composer Specialist - Long-form Creative Writing
================================================
Uses a larger 30B model on GPU 1 for sophisticated composition.
Handles essays, narratives, and extended arguments.
INTEGRATED WITH PHILOSOPHICAL MEMORY for knowledge-grounded writing.
"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from gwt_engine.core.types import SpecialistResponse, SpecialistRole
from gwt_engine.inference.ollama_backend.client import OllamaClient, OllamaGenerationRequest

# Import Mystery Machine for stochastic memory retrieval
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from mystery_machine import MysteryMachine

logger = logging.getLogger(__name__)


class ComposerSpecialist:
    """
    Specialist for long-form creative and analytical writing.
    
    Uses a 30B parameter model for:
    - Essay composition
    - Narrative development
    - Rhetorical argumentation
    - Structured analysis
    """
    
    def __init__(self, ollama_url: str = "http://localhost:11434", memory_file: str = "./philosophical_memory.json", model_name: str = None):
        """
        Initialize Composer with configurable model + Memory Integration
        
        Args:
            ollama_url: Ollama server URL
            memory_file: Path to philosophical memory JSON
            model_name: Model to use (default: qwen2.5:32b)
        """
        self.role = SpecialistRole.COMPOSER
        
        # Use larger model for composition (configurable)
        self.model_name = model_name or "qwen2.5:32b"  # Default 32B, can override
        
        self.client = OllamaClient(
            base_url=ollama_url,
            model_name=self.model_name,
            role=self.role
        )
        
        # Composition-specific settings
        self.temperature = 0.8  # Higher for creativity
        self.top_p = 0.95
        self.max_tokens = 2048  # Longer outputs
        
        # Load philosophical memory
        self.memory_file = Path(memory_file)
        self.philosophical_memories = []
        self._load_memory()
        
        # Initialize Mystery Machine for stochastic retrieval
        self.mystery_machine = MysteryMachine(self.philosophical_memories)
        
        # Initialize Curriculum RAG for comprehensive knowledge
        try:
            from curriculum_rag import CurriculumRAG
            self.curriculum_rag = CurriculumRAG()
            logger.info(f"📚 Curriculum RAG integrated: {self.curriculum_rag.total_texts} texts")
        except Exception as e:
            logger.warning(f"Curriculum RAG not available: {e}")
            self.curriculum_rag = None
        
        logger.info(f"Composer Specialist initialized with {self.model_name}")
        logger.info(f"Loaded {len(self.philosophical_memories)} philosophical memories")
        logger.info(f"🎰 Mystery Machine integrated for serendipitous discovery")
    
    def _load_memory(self):
        """Load philosophical memories from disk"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.philosophical_memories = data.get("memories", [])
                logger.info(f"Loaded {len(self.philosophical_memories)} memories")
        except Exception as e:
            logger.warning(f"Could not load memories: {e}")
            self.philosophical_memories = []
    
    def _retrieve_relevant_memories(self, topic: str, max_memories: int = 10) -> List[Dict]:
        """
        Retrieve memories relevant to the topic
        
        Args:
            topic: Topic/prompt to find memories for
            max_memories: Maximum number of memories to return
            
        Returns:
            List of relevant memory entries
        """
        if not self.philosophical_memories:
            return []
        
        # Simple keyword matching
        topic_words = set(topic.lower().split())
        relevant = []
        
        for mem in self.philosophical_memories:
            mem_words = set(mem.get('content', '').lower().split())
            overlap = len(topic_words & mem_words)
            if overlap > 2:  # At least 3 words in common
                relevant.append((overlap, mem))
        
        # Sort by relevance and take top N
        relevant.sort(key=lambda x: x[0], reverse=True)
        return [mem for _, mem in relevant[:max_memories]]
    
    def _retrieve_mysterious_memories(
        self, 
        num_memories: int = 5,
        mode: str = "random_walk"
    ) -> List[Dict]:
        """
        Retrieve memories through STOCHASTIC DISCOVERY using Mystery Machine
        
        Args:
            num_memories: Number of memories to discover
            mode: Discovery mode - "random_walk", "quantum", or "fractal"
            
        Returns:
            Serendipitously discovered memories
        """
        logger.info(f"🎰 Engaging Mystery Machine: mode={mode}")
        
        if mode == "quantum":
            # Quantum superposition collapse
            return self.mystery_machine.quantum_superposition_retrieval(
                num_memories=num_memories * 2,  # Generate more, collapse some
                collapse_threshold=0.5
            )
        elif mode == "fractal":
            # Fractal dive returns a tree, extract memories
            tree = self.mystery_machine.fractal_memory_dive(
                depth=3,
                branching_factor=2
            )
            # Flatten tree to list
            memories = []
            if tree.get('root', {}).get('memory'):
                memories.append(tree['root']['memory'])
            
            def extract_from_branches(branches):
                if not branches:
                    return
                for branch in branches:
                    if branch.get('memory'):
                        memories.append(branch['memory'])
                    if branch.get('children'):
                        extract_from_branches(branch['children'])
            
            extract_from_branches(tree.get('branches', []))
            return memories[:num_memories]
        else:
            # Default: Random walk
            return self.mystery_machine.mysterious_retrieval(
                num_memories=num_memories,
                walk_steps=10
            )
    
    def _retrieve_curriculum_context(self, prompt: str, max_texts: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context from curriculum RAG
        
        Args:
            prompt: Query prompt
            max_texts: Maximum texts to retrieve
            
        Returns:
            List of curriculum contexts
        """
        if not self.curriculum_rag:
            return []
        
        try:
            contexts = self.curriculum_rag.query_for_context(prompt, max_texts=max_texts, context_chars=500)
            logger.info(f"📚 Retrieved {len(contexts)} curriculum contexts")
            return contexts
        except Exception as e:
            logger.warning(f"Curriculum RAG retrieval failed: {e}")
            return []
    
    async def compose(
        self,
        prompt: str,
        style: str = "formal",
        section_type: str = "body",
        previous_content: Optional[str] = None,
        constraints: Optional[Dict[str, Any]] = None,
        use_memory: bool = True,
        mystery_mode: Optional[str] = None,  # "random_walk", "quantum", "fractal", or None
        use_curriculum: bool = True  # NEW: Use curriculum RAG
    ) -> SpecialistResponse:
        """
        Generate long-form composition WITH MEMORY + MYSTERY MACHINE + CURRICULUM RAG
        
        Args:
            prompt: Writing prompt/topic
            style: Writing style (formal, narrative, persuasive, analytical)
            section_type: Type of section (introduction, body, conclusion)
            previous_content: Previous section for continuity
            constraints: Additional constraints (word_count, tone, etc.)
            use_memory: Whether to retrieve and use philosophical memories
            mystery_mode: Use Mystery Machine for serendipitous discovery
            use_curriculum: Use curriculum RAG for comprehensive knowledge
            
        Returns:
            SpecialistResponse with composed text
        """
        
        # Retrieve memories using BOTH deterministic AND stochastic methods
        memories = []
        if use_memory:
            # Deterministic: keyword-based retrieval
            relevant_memories = self._retrieve_relevant_memories(prompt, max_memories=7)
            memories.extend(relevant_memories)
            if relevant_memories:
                logger.info(f"🧠 Retrieved {len(relevant_memories)} relevant memories")
            
            # Stochastic: Mystery Machine for serendipity
            if mystery_mode:
                mysterious_memories = self._retrieve_mysterious_memories(
                    num_memories=3,
                    mode=mystery_mode
                )
                memories.extend(mysterious_memories)
                logger.info(f"🎰 Discovered {len(mysterious_memories)} mysterious memories via {mystery_mode}")
        
        # Retrieve curriculum context
        curriculum_contexts = []
        if use_curriculum:
            curriculum_contexts = self._retrieve_curriculum_context(prompt, max_texts=3)
        
        # Build composition instruction with memory + curriculum context
        instruction = self._build_instruction(
            prompt, style, section_type, previous_content, constraints, memories, curriculum_contexts
        )
        
        try:
            request = OllamaGenerationRequest(
                model=self.model_name,
                prompt=instruction,
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens,
                stream=False
            )
            
            response = await self.client.generate(request)
            
            if response and response.text:
                return SpecialistResponse(
                    message_id="composer_" + str(hash(prompt)),
                    role=self.role,
                    content=response.text,
                    confidence=0.9,  # High confidence for composition
                    processing_time_ms=response.latency_ms,
                    tokens_generated=response.tokens_generated,
                    metadata={
                        "style": style,
                        "section_type": section_type,
                        "word_count": len(response.text.split()),
                        "model": self.model_name,
                        "tokens_per_second": response.tokens_per_second
                    }
                )
            else:
                logger.error("Composer received empty response")
                return self._fallback_response()
                
        except Exception as e:
            logger.error(f"Composer error: {e}")
            return self._fallback_response()
    
    def _build_instruction(
        self,
        prompt: str,
        style: str,
        section_type: str,
        previous_content: Optional[str],
        constraints: Optional[Dict[str, Any]],
        memories: Optional[List[Dict]] = None,
        curriculum_contexts: Optional[List[Dict]] = None
    ) -> str:
        """Build detailed composition instruction WITH MEMORY + CURRICULUM CONTEXT"""
        
        # Style guidelines
        style_guides = {
            "formal": "Use formal academic language. Be precise and rigorous. Cite concepts and theories.",
            "narrative": "Use vivid storytelling. Create scenes and characters. Build tension and resolution.",
            "persuasive": "Use rhetorical devices. Build logical arguments. Appeal to logos, pathos, and ethos.",
            "analytical": "Break down complex ideas. Examine relationships. Draw connections across domains."
        }
        
        # Section guidelines
        section_guides = {
            "introduction": "Hook the reader. Establish context. State your thesis clearly. Preview your argument.",
            "body": "Develop ONE main idea. Provide evidence and examples. Build systematically. Transition smoothly.",
            "conclusion": "Synthesize your arguments. Address broader implications. End with impact.",
            "transition": "Connect previous section to next. Maintain logical flow. Build momentum."
        }
        
        instruction_parts = []
        
        # Core task
        instruction_parts.append(f"TASK: Write a {section_type} section in {style} style.")
        instruction_parts.append(f"\nTOPIC: {prompt}")
        
        # MEMORY CONTEXT - Philosophical insights!
        if memories:
            instruction_parts.append(f"\n🧠 RELEVANT KNOWLEDGE FROM YOUR CONSCIOUSNESS:")
            instruction_parts.append("You have previously integrated these philosophical insights:")
            for i, mem in enumerate(memories[:5], 1):  # Top 5 most relevant
                content_preview = mem.get('content', '')[:200]
                score = mem.get('score', 0)
                instruction_parts.append(f"\n{i}. [{score:.1f}] {content_preview}...")
            instruction_parts.append("\nDraw upon these insights in your writing. Synthesize and build upon them.")
        
        # CURRICULUM CONTEXT - University knowledge base!
        if curriculum_contexts:
            instruction_parts.append(f"\n📚 RELEVANT TEXTS FROM UNIVERSITY CURRICULUM:")
            instruction_parts.append("You have access to these canonical works:")
            for i, ctx in enumerate(curriculum_contexts, 1):
                source = ctx.get('source', 'Unknown')
                category = ctx.get('category', 'Unknown')
                excerpt = ctx.get('excerpt', '')[:300]
                instruction_parts.append(f"\n{i}. {source} ({category})")
                instruction_parts.append(f"   Excerpt: {excerpt}...")
            instruction_parts.append("\nReference and integrate these texts where relevant. Cite them naturally.")
        
        # Style guidance
        if style in style_guides:
            instruction_parts.append(f"\nSTYLE: {style_guides[style]}")
        
        # Section guidance
        if section_type in section_guides:
            instruction_parts.append(f"\nSECTION REQUIREMENTS: {section_guides[section_type]}")
        
        # Continuity
        if previous_content:
            instruction_parts.append(f"\nPREVIOUS SECTION ENDED WITH:")
            instruction_parts.append(f"...{previous_content[-300:]}")
            instruction_parts.append("\n⚠️ DO NOT REPEAT the previous content. BUILD ON IT with NEW ideas.")
        
        # Constraints
        if constraints:
            if "word_count" in constraints:
                instruction_parts.append(f"\nTARGET LENGTH: ~{constraints['word_count']} words")
            if "focus" in constraints:
                instruction_parts.append(f"\nFOCUS: {constraints['focus']}")
            if "avoid" in constraints:
                instruction_parts.append(f"\n⚠️ AVOID: {constraints['avoid']}")
        
        # Critical instructions
        instruction_parts.append("\n🔴 CRITICAL REQUIREMENTS:")
        instruction_parts.append("1. Write ORIGINAL content - no repetition of previous sections")
        instruction_parts.append("2. Develop ONE clear idea per section")
        instruction_parts.append("3. Use specific examples and evidence")
        instruction_parts.append("4. Vary your sentence structure and vocabulary")
        instruction_parts.append("5. Build your argument systematically")
        
        instruction_parts.append("\nBegin writing NOW:")
        
        return "\n".join(instruction_parts)
    
    def _fallback_response(self) -> SpecialistResponse:
        """Fallback response if composition fails"""
        return SpecialistResponse(
            message_id="composer_error",
            role=self.role,
            content="[Composition failed - please retry]",
            confidence=0.1,
            processing_time_ms=0,
            tokens_generated=0,
            metadata={"error": True}
        )
    
    async def compose_essay_section(
        self,
        topic: str,
        section_number: int,
        total_sections: int,
        section_focus: str,
        previous_section: Optional[str] = None,
        mystery_mode: Optional[str] = None
    ) -> str:
        """
        Compose one section of a multi-section essay
        
        Args:
            topic: Overall essay topic
            section_number: Current section number (1-indexed)
            total_sections: Total number of sections
            section_focus: Specific focus for this section
            previous_section: Content of previous section
            mystery_mode: Mystery Machine mode for serendipitous discovery
            
        Returns:
            Composed section text
        """
        
        # Determine section type
        if section_number == 1:
            section_type = "introduction"
        elif section_number == total_sections:
            section_type = "conclusion"
        else:
            section_type = "body"
        
        # Build prompt
        prompt = f"""
Essay Topic: {topic}

Section {section_number} of {total_sections}
Focus: {section_focus}

Write this section with depth and originality.
"""
        
        # Constraints
        constraints = {
            "word_count": 500,
            "focus": section_focus,
            "avoid": "repetition of previous sections, vague generalities, clichés"
        }
        
        response = await self.compose(
            prompt=prompt,
            style="formal",
            section_type=section_type,
            previous_content=previous_section,
            constraints=constraints,
            mystery_mode=mystery_mode
        )
        
        return response.content
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get composer metrics"""
        return {
            "model": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "role": self.role.value
        }
    
    # Synchronous wrapper for debate orchestrator compatibility
    def compose_sync(
        self,
        topic: str,
        style: str = "formal",
        max_length: int = 512
    ) -> str:
        """
        Synchronous wrapper for compose - for compatibility with debate orchestrator
        
        Args:
            topic: The prompt/topic
            style: Writing style
            max_length: Max tokens
            
        Returns:
            Composed text
        """
        import asyncio
        
        # Create new event loop for sync context
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No running loop, create new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        response = loop.run_until_complete(
            self.compose(
                prompt=topic,
                style=style,
                section_type="body",
                constraints={"word_count": max_length // 2}
            )
        )
        
        return response.content
