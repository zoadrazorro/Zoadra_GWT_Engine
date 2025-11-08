"""
Memory Specialist - Manages episodic and working memory

Model: Qwen 2.5 Coder 32B (Q4_K_M)
Role: Memory retrieval, consolidation, and context management
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

from gwt_engine.specialists.base import BaseSpecialist
from gwt_engine.core.types import (
    WorkspaceMessage,
    SpecialistResponse,
    SpecialistRole,
)
from gwt_engine.inference.vllm_client import VLLMClient

logger = logging.getLogger(__name__)


class MemorySpecialist(BaseSpecialist):
    """
    Memory specialist manages episodic memory and retrieval

    Based on Tulving's synergistic ecphory model:
    - Episodic memory storage and retrieval
    - Working memory consolidation
    - Context-dependent recall
    - Memory integration with current experience
    """

    def __init__(self, vllm_client: VLLMClient):
        super().__init__(vllm_client, SpecialistRole.MEMORY)
        self.episodic_memory: List[Dict[str, Any]] = []
        self.working_memory_snapshot: Dict[str, Any] = {}

    async def process(self, message: WorkspaceMessage) -> SpecialistResponse:
        """Process memory queries and consolidation requests"""

        context = {
            "query": message.content,
            "episodic_memory": self.episodic_memory[-10:],  # Recent episodes
            "working_memory": self.working_memory_snapshot,
        }

        prompt = self._create_specialist_prompt(message, context)
        response_text = await self._generate_response(
            prompt, max_tokens=512, temperature=0.6  # Lower temp for factual recall
        )

        confidence = self._calculate_confidence(context)

        # Store interaction in episodic memory
        self._store_episode(message, response_text)

        return SpecialistResponse(
            message_id=message.id,
            role=self.role,
            content=response_text,
            confidence=confidence,
            processing_time_ms=0.0,
            tokens_generated=len(response_text.split()),
            metadata={
                "episodic_memory_size": len(self.episodic_memory),
                "retrieval_method": "semantic_search",  # Placeholder
            },
        )

    def _create_specialist_prompt(
        self, message: WorkspaceMessage, context: Dict[str, Any]
    ) -> str:
        """Create memory-specific prompt"""

        prompt = """You are the Memory Specialist in a consciousness simulation.

Your role is to retrieve relevant memories, consolidate experiences, and maintain continuity of self.

## Working Memory (Current State):
"""
        working_mem = context.get("working_memory", {})
        if working_mem:
            for key, value in list(working_mem.items())[:5]:
                prompt += f"- {key}: {value}\n"
        else:
            prompt += "- [Empty]\n"

        prompt += "\n## Episodic Memory (Recent Experiences):\n"
        episodes = context.get("episodic_memory", [])
        if episodes:
            for i, episode in enumerate(episodes[-5:], 1):
                prompt += f"{i}. {episode['summary'][:100]}...\n"
        else:
            prompt += "- [No stored episodes]\n"

        prompt += f"""
## Memory Query:
{context.get('query', message.content)}

## Task:
Based on the query, retrieve and synthesize relevant memories:
1. What past experiences are relevant?
2. What patterns or connections exist?
3. How does this relate to current working memory?
4. What context enriches current understanding?

Provide memory retrieval response (3-4 sentences):
"""

        return prompt

    def _calculate_confidence(self, context: Dict[str, Any]) -> float:
        """Calculate confidence based on memory availability"""
        episodic_count = len(context.get("episodic_memory", []))
        working_mem_count = len(context.get("working_memory", {}))

        # Higher confidence with more available memory
        episodic_factor = min(episodic_count / 10.0, 0.5)
        working_factor = min(working_mem_count / 10.0, 0.5)

        return 0.5 + episodic_factor + working_factor

    def _store_episode(self, message: WorkspaceMessage, response: str):
        """Store interaction in episodic memory"""
        episode = {
            "timestamp": datetime.utcnow(),
            "query": message.content,
            "response": response,
            "summary": f"{message.content[:50]}... -> {response[:50]}...",
            "source": message.source.value if message.source else "unknown",
        }

        self.episodic_memory.append(episode)

        # Keep memory bounded (in full system, would use ChromaDB)
        if len(self.episodic_memory) > 100:
            self.episodic_memory.pop(0)

    async def consolidate_from_workspace(self, workspace_state: Dict[str, Any]):
        """
        Consolidate working memory from workspace state

        This is called periodically to update long-term memory
        """
        self.working_memory_snapshot = workspace_state.get("working_memory", {})

        logger.debug(
            f"Memory consolidated: {len(self.working_memory_snapshot)} items in working memory"
        )

    async def retrieve_by_context(self, context_query: str) -> List[Dict[str, Any]]:
        """
        Retrieve memories by semantic context

        In full implementation, this would use vector embeddings
        """
        # Simple keyword matching for now
        relevant_episodes = []

        query_terms = set(context_query.lower().split())

        for episode in reversed(self.episodic_memory):
            episode_text = f"{episode['query']} {episode['response']}".lower()
            if any(term in episode_text for term in query_terms):
                relevant_episodes.append(episode)

            if len(relevant_episodes) >= 5:
                break

        return relevant_episodes
