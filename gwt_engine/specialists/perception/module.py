"""
Perception Specialist - Processes sensory/environmental data

Model: Mistral Small 22B (Q5_K_M)
Role: Process incoming information and determine workspace relevance
"""

import logging
from typing import Dict, Any

from gwt_engine.specialists.base import BaseSpecialist
from gwt_engine.core.types import (
    WorkspaceMessage,
    SpecialistResponse,
    SpecialistRole,
)
from gwt_engine.inference.vllm_client import VLLMClient

logger = logging.getLogger(__name__)


class PerceptionSpecialist(BaseSpecialist):
    """
    Perception specialist processes raw inputs and determines salience

    Responsibilities:
    - Semantic processing of incoming information
    - Determine what deserves workspace attention
    - Extract key features and patterns
    - Filter noise from signal
    """

    def __init__(self, vllm_client: VLLMClient):
        super().__init__(vllm_client, SpecialistRole.PERCEPTION)
        self.context_buffer = []  # Recent perceptions

    async def process(self, message: WorkspaceMessage) -> SpecialistResponse:
        """Process perceptual input"""

        context = {
            "recent_perceptions": self.context_buffer[-5:],
            "message": message,
        }

        prompt = self._create_specialist_prompt(message, context)
        response_text = await self._generate_response(prompt, max_tokens=256)

        # Update context buffer
        self.context_buffer.append(
            {"content": message.content, "timestamp": message.timestamp}
        )
        if len(self.context_buffer) > 20:
            self.context_buffer.pop(0)

        confidence = self._calculate_confidence(context)

        return SpecialistResponse(
            message_id=message.id,
            role=self.role,
            content=response_text,
            confidence=confidence,
            processing_time_ms=0.0,  # Set by wrapper
            tokens_generated=len(response_text.split()),  # Approximate
            metadata={
                "input_type": message.type.value,
                "salience": self._calculate_salience(message),
            },
        )

    def _create_specialist_prompt(
        self, message: WorkspaceMessage, context: Dict[str, Any]
    ) -> str:
        """Create perception-specific prompt"""

        prompt = """You are the Perception Specialist in a consciousness simulation.

Your role is to process incoming sensory/environmental information and extract what's salient and meaningful for conscious awareness.

## Recent Perceptions:
"""
        recent = context.get("recent_perceptions", [])
        if recent:
            for perception in recent[-3:]:
                prompt += f"- {perception['content'][:100]}...\n"
        else:
            prompt += "- [No recent perceptions]\n"

        prompt += f"""
## New Input to Process:
{message.content}

## Task:
Analyze this input and provide:
1. What are the key features or patterns?
2. What is semantically meaningful or salient?
3. What should the consciousness workspace pay attention to?
4. Any immediate implications or context?

Provide a concise perceptual analysis (2-3 sentences):
"""

        return prompt

    def _calculate_confidence(self, context: Dict[str, Any]) -> float:
        """Calculate confidence based on input clarity"""
        message = context.get("message")

        # Higher confidence for longer, more detailed inputs
        content_length = len(message.content) if message else 0

        if content_length > 200:
            return 0.85
        elif content_length > 100:
            return 0.75
        elif content_length > 50:
            return 0.65
        else:
            return 0.55

    def _calculate_salience(self, message: WorkspaceMessage) -> float:
        """Calculate how salient/important this perception is"""
        # Higher salience for urgent/high-priority messages
        priority_factor = message.priority / 10.0
        confidence_factor = message.confidence

        return (priority_factor + confidence_factor) / 2.0

    async def process_workspace_broadcast(
        self, broadcast: WorkspaceMessage
    ) -> None:
        """
        React to workspace broadcasts

        Perception specialist updates its context based on global awareness
        """
        # Update context with workspace understanding
        self.context_buffer.append(
            {
                "content": f"[WORKSPACE] {broadcast.content}",
                "timestamp": broadcast.timestamp,
            }
        )

        logger.debug(
            f"Perception specialist updated with workspace broadcast: "
            f"{broadcast.content[:50]}..."
        )
