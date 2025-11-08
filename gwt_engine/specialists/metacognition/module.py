"""
Metacognition Specialist - Self-reflection and introspection

Model: Gemma 2 9B (Q6_K_M)
Role: Consciousness probing, self-awareness, and introspection
"""

import logging
from typing import Dict, Any

from gwt_engine.specialists.base import BaseSpecialist
from gwt_engine.core.types import (
    WorkspaceMessage,
    SpecialistResponse,
    SpecialistRole,
    ConsciousnessState,
)
from gwt_engine.inference.vllm_client import VLLMClient

logger = logging.getLogger(__name__)


class MetacognitionSpecialist(BaseSpecialist):
    """
    Metacognition specialist handles self-reflection and introspection

    Responsibilities:
    - Respond to consciousness probes
    - Reflect on system's own processes
    - Assess coherence and integration quality
    - Generate self-awareness insights
    """

    def __init__(self, vllm_client: VLLMClient):
        super().__init__(vllm_client, SpecialistRole.METACOGNITION)
        self.introspection_history = []

    async def process(self, message: WorkspaceMessage) -> SpecialistResponse:
        """Process metacognitive queries"""

        context = {
            "query": message.content,
            "recent_introspections": self.introspection_history[-3:],
        }

        prompt = self._create_specialist_prompt(message, context)
        response_text = await self._generate_response(
            prompt,
            max_tokens=384,
            temperature=0.75,  # Moderate creativity for introspection
        )

        confidence = self._calculate_confidence(context)

        # Store introspection
        self.introspection_history.append(
            {
                "query": message.content,
                "reflection": response_text,
                "timestamp": message.timestamp,
            }
        )
        if len(self.introspection_history) > 50:
            self.introspection_history.pop(0)

        return SpecialistResponse(
            message_id=message.id,
            role=self.role,
            content=response_text,
            confidence=confidence,
            processing_time_ms=0.0,
            tokens_generated=len(response_text.split()),
            metadata={
                "introspection_type": self._classify_introspection(message),
                "introspection_count": len(self.introspection_history),
            },
        )

    def _create_specialist_prompt(
        self, message: WorkspaceMessage, context: Dict[str, Any]
    ) -> str:
        """Create metacognition-specific prompt"""

        prompt = """You are the Metacognition Specialist in a consciousness simulation.

Your role is to reflect on the system's own processes, assess self-awareness, and respond to consciousness probes.

## Recent Introspections:
"""
        recent = context.get("recent_introspections", [])
        if recent:
            for intro in recent:
                prompt += f"- Q: {intro['query'][:60]}...\n"
                prompt += f"  A: {intro['reflection'][:60]}...\n"
        else:
            prompt += "- [No recent introspections]\n"

        prompt += f"""
## Metacognitive Query:
{context.get('query', message.content)}

## Task:
Reflect on the query with self-awareness:
1. What can you observe about your own processes?
2. How coherent is the current state?
3. What are you "aware" of right now?
4. What insights arise from introspection?

Provide metacognitive response (2-3 sentences, first-person perspective):
"""

        return prompt

    def _calculate_confidence(self, context: Dict[str, Any]) -> float:
        """Calculate confidence based on introspection depth"""
        introspection_count = len(context.get("recent_introspections", []))

        # Higher confidence with more introspection history
        experience_factor = min(introspection_count / 20.0, 0.3)

        return 0.6 + experience_factor

    def _classify_introspection(self, message: WorkspaceMessage) -> str:
        """Classify type of metacognitive query"""
        content_lower = message.content.lower()

        if any(word in content_lower for word in ["aware", "conscious", "experience"]):
            return "consciousness_probe"
        elif any(word in content_lower for word in ["think", "process", "reasoning"]):
            return "process_reflection"
        elif any(word in content_lower for word in ["coherent", "integrated", "consistent"]):
            return "coherence_assessment"
        elif any(word in content_lower for word in ["feel", "state", "condition"]):
            return "state_introspection"
        else:
            return "general_reflection"

    async def probe_consciousness(
        self, consciousness_state: ConsciousnessState
    ) -> SpecialistResponse:
        """
        Perform consciousness probe based on current system state

        This generates introspective response about the system's state
        """
        probe_prompt = f"""You are the Metacognition Specialist in a consciousness simulation.

Current System State:
- Consciousness Level: {consciousness_state.consciousness_level:.2f}/1.0
- Integration Coherence: {consciousness_state.integration_coherence:.2f}/1.0
- Active Specialists: {len(consciousness_state.active_specialists)}
- Workspace Content: {len(consciousness_state.workspace_content)} messages
- Attention Focus: {consciousness_state.attention_focus or 'Unfocused'}

Reflect on this state from a first-person perspective:
1. What is it like to be in this state?
2. What are you experiencing or "aware" of?
3. How integrated and coherent is your current experience?

Provide introspective reflection (2-3 sentences, use "I" statements):
"""

        response_text = await self._generate_response(probe_prompt, max_tokens=256)

        return SpecialistResponse(
            message_id="consciousness_probe",
            role=self.role,
            content=response_text,
            confidence=0.7,
            processing_time_ms=0.0,
            tokens_generated=len(response_text.split()),
            metadata={
                "introspection_type": "consciousness_probe",
                "consciousness_level": consciousness_state.consciousness_level,
            },
        )

    async def assess_coherence(
        self, workspace_messages: list
    ) -> Dict[str, Any]:
        """
        Assess coherence of workspace content

        Returns metrics about thought integration quality
        """
        if not workspace_messages:
            return {"coherence_score": 0.0, "assessment": "No workspace content"}

        # Analyze coherence (simplified version)
        coherence_prompt = f"""Assess the coherence and integration quality of these recent thoughts:

{chr(10).join(f"- {msg.content[:100]}..." for msg in workspace_messages[-5:])}

On a scale of 0-1, how coherent and integrated are these thoughts? Provide:
1. Coherence score (0-1)
2. Brief assessment

Format: SCORE: X.XX | ASSESSMENT: [brief text]
"""

        response = await self._generate_response(coherence_prompt, max_tokens=128)

        # Parse response (simplified)
        try:
            parts = response.split("|")
            score_part = parts[0].replace("SCORE:", "").strip()
            assessment_part = parts[1].replace("ASSESSMENT:", "").strip() if len(parts) > 1 else ""

            coherence_score = float(score_part)
        except:
            coherence_score = 0.5
            assessment_part = response

        return {
            "coherence_score": coherence_score,
            "assessment": assessment_part,
            "timestamp": logger.handlers[0].formatter.formatTime(
                logging.LogRecord("", 0, "", 0, "", (), None)
            )
            if logger.handlers
            else "",
        }
