"""Central Workspace - Core of GWT consciousness architecture"""

import asyncio
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

from gwt_engine.core.types import (
    WorkspaceMessage,
    SpecialistResponse,
    ConsciousnessState,
    MessageType,
    SpecialistRole,
)
# Support both vLLM and Ollama clients
try:
    from gwt_engine.inference.vllm_client import (
        VLLMClient,
        GenerationRequest,
        GenerationResponse,
    )
except ImportError:
    VLLMClient = None
    GenerationRequest = None
    GenerationResponse = None

from gwt_engine.inference.ollama_client import OllamaClient
from gwt_engine.config.loader import get_models_config

logger = logging.getLogger(__name__)


class CentralWorkspace:
    """
    Central Global Workspace - Integrates specialist outputs into unified consciousness

    Based on Global Workspace Theory (Baars, 1988):
    - Receives competing inputs from specialist modules
    - Integrates information into coherent thought
    - Broadcasts consolidated understanding to all specialists
    - Maintains working memory and attention focus
    """

    def __init__(
        self,
        client,  # Can be VLLMClient or OllamaClient
        broadcast_threshold: float = 0.75,
        integration_window_ms: float = 500,
        max_workspace_messages: int = 10,
    ):
        self.client = client
        self.broadcast_threshold = broadcast_threshold
        self.integration_window_ms = integration_window_ms
        self.max_workspace_messages = max_workspace_messages

        # Workspace state
        self.pending_messages: List[WorkspaceMessage] = []
        self.workspace_content: List[WorkspaceMessage] = []
        self.recent_broadcasts: List[WorkspaceMessage] = []
        self.working_memory: Dict[str, Any] = {}
        self.attention_focus: Optional[str] = None

        # Performance tracking
        self.integration_count = 0
        self.broadcast_count = 0
        self.total_processing_time_ms = 0.0

        # Configuration
        config = get_models_config()
        self.gwt_config = config.get("gwt_workspace", {})

        logger.info("Central Workspace initialized")

    async def receive_specialist_input(self, response: SpecialistResponse):
        """Receive input from a specialist module for workspace integration"""
        message = response.to_workspace_message()
        self.pending_messages.append(message)

        logger.debug(
            f"Received {response.role.value} input: "
            f"{response.content[:100]}... (confidence: {response.confidence:.2f})"
        )

        # Trigger integration if enough time has passed or high-priority message
        if (
            message.priority >= 8
            or len(self.pending_messages) >= 3
        ):
            await self.integrate_and_broadcast()

    async def integrate_and_broadcast(self):
        """
        Core GWT function: Integrate pending specialist inputs into unified thought

        This implements the "global broadcasting" mechanism from GWT theory
        """
        if not self.pending_messages:
            return

        start_time = time.time()
        self.integration_count += 1

        # Gather context from pending messages
        integration_context = self._build_integration_context()

        # Generate integrated thought using central workspace model (Llama 70B)
        prompt = self._create_integration_prompt(integration_context)

        try:
            # Check if using Ollama client
            if isinstance(self.client, OllamaClient):
                response = await self.client.generate(
                    prompt=prompt,
                    max_tokens=512,
                    temperature=0.7,
                )
                response_text = response["text"]
                tokens_generated = response.get("eval_count", 0)
                latency_ms = response.get("total_duration", 0) / 1_000_000  # Convert ns to ms
            else:
                # vLLM client
                response = await self.client.generate(
                    GenerationRequest(
                        prompt=prompt,
                        max_tokens=512,
                        temperature=0.7,
                        top_p=0.9,
                    )
                )
                response_text = response.text
                tokens_generated = response.tokens_generated
                latency_ms = response.latency_ms

            # Create broadcast message
            broadcast_message = WorkspaceMessage(
                type=MessageType.WORKSPACE_BROADCAST,
                content=response_text,
                source=SpecialistRole.CENTRAL_WORKSPACE,
                confidence=self._calculate_integration_confidence(integration_context),
                metadata={
                    "integration_id": self.integration_count,
                    "sources": [msg.source.value for msg in self.pending_messages],
                    "tokens_generated": tokens_generated,
                    "latency_ms": latency_ms,
                },
                priority=self._determine_broadcast_priority(integration_context),
            )

            # Update workspace state
            self.workspace_content.append(broadcast_message)
            self.recent_broadcasts.append(broadcast_message)
            self._update_working_memory(broadcast_message)

            # Keep workspace content bounded
            if len(self.workspace_content) > self.max_workspace_messages:
                self.workspace_content.pop(0)

            # Clear pending messages
            self.pending_messages.clear()

            processing_time = (time.time() - start_time) * 1000
            self.total_processing_time_ms += processing_time
            self.broadcast_count += 1

            logger.info(
                f"Workspace broadcast #{self.broadcast_count}: "
                f"{broadcast_message.content[:100]}... "
                f"(confidence: {broadcast_message.confidence:.2f}, "
                f"time: {processing_time:.1f}ms)"
            )

            return broadcast_message

        except Exception as e:
            logger.error(f"Integration failed: {e}")
            self.pending_messages.clear()
            raise

    def _build_integration_context(self) -> Dict[str, Any]:
        """Build context dictionary from pending messages"""
        return {
            "messages": self.pending_messages,
            "working_memory": self.working_memory,
            "recent_broadcasts": self.recent_broadcasts[-3:]
            if self.recent_broadcasts
            else [],
            "attention_focus": self.attention_focus,
        }

    def _create_integration_prompt(self, context: Dict[str, Any]) -> str:
        """
        Create prompt for central workspace integration

        This prompt instructs the model to act as the "global workspace"
        that integrates competing specialist inputs
        """
        messages = context["messages"]
        working_memory = context["working_memory"]
        recent_thoughts = context["recent_broadcasts"]

        prompt = """You are the Central Global Workspace of a consciousness simulation based on Global Workspace Theory.

Your role is to integrate multiple specialist inputs into a single, coherent thought that will be broadcast to all cognitive modules.

## Recent Context (Working Memory):
"""
        if working_memory:
            for key, value in working_memory.items():
                prompt += f"- {key}: {value}\n"
        else:
            prompt += "- [Empty]\n"

        prompt += "\n## Recent Thoughts:\n"
        if recent_thoughts:
            for thought in recent_thoughts:
                prompt += f"- {thought.content}\n"
        else:
            prompt += "- [No recent thoughts]\n"

        prompt += "\n## Specialist Inputs to Integrate:\n"
        for msg in messages:
            source_name = msg.source.value if msg.source else "unknown"
            prompt += f"\n### {source_name.upper()} (confidence: {msg.confidence:.2f}):\n"
            prompt += f"{msg.content}\n"

        prompt += """
## Task:
Synthesize these specialist inputs into ONE unified, coherent thought that:
1. Integrates the most salient information from each specialist
2. Resolves any contradictions or conflicts between inputs
3. Maintains continuity with recent thoughts and working memory
4. Forms a clear, actionable understanding

Output only the integrated thought (2-4 sentences), as if you are the unified consciousness speaking:
"""

        return prompt

    def _calculate_integration_confidence(self, context: Dict[str, Any]) -> float:
        """Calculate confidence score for integrated thought"""
        messages = context["messages"]

        if not messages:
            return 0.0

        # Average confidence weighted by source reliability
        source_weights = {
            SpecialistRole.PERCEPTION: 0.8,
            SpecialistRole.MEMORY: 1.0,
            SpecialistRole.PLANNING: 0.9,
            SpecialistRole.METACOGNITION: 0.7,
        }

        weighted_sum = 0.0
        total_weight = 0.0

        for msg in messages:
            if msg.source:
                weight = source_weights.get(msg.source, 0.5)
                weighted_sum += msg.confidence * weight
                total_weight += weight

        return weighted_sum / total_weight if total_weight > 0 else 0.5

    def _determine_broadcast_priority(self, context: Dict[str, Any]) -> int:
        """Determine priority of broadcast based on context"""
        messages = context["messages"]
        max_priority = max((msg.priority for msg in messages), default=5)
        return max_priority

    def _update_working_memory(self, broadcast: WorkspaceMessage):
        """Update working memory with broadcast content"""
        # Extract key concepts from broadcast for working memory
        # In a full implementation, this would use semantic extraction
        self.working_memory["last_broadcast"] = broadcast.content
        self.working_memory["last_broadcast_time"] = broadcast.timestamp.isoformat()
        self.working_memory["broadcast_count"] = self.broadcast_count

        # Maintain bounded working memory
        if len(self.working_memory) > 20:
            # Remove oldest entries (simple LRU)
            oldest_key = min(
                self.working_memory.keys(),
                key=lambda k: self.working_memory.get(f"{k}_time", ""),
                default=None,
            )
            if oldest_key and not oldest_key.endswith("_time"):
                self.working_memory.pop(oldest_key, None)
                self.working_memory.pop(f"{oldest_key}_time", None)

    async def get_consciousness_state(self) -> ConsciousnessState:
        """Get current state of consciousness workspace"""
        # Calculate integration coherence (how well thoughts connect)
        coherence = self._calculate_coherence()

        # Calculate consciousness level (activity and integration quality)
        consciousness_level = self._calculate_consciousness_level()

        return ConsciousnessState(
            workspace_content=self.workspace_content,
            active_specialists=self._get_active_specialists(),
            working_memory=self.working_memory,
            attention_focus=self.attention_focus,
            integration_coherence=coherence,
            consciousness_level=consciousness_level,
            recent_broadcasts=[msg.id for msg in self.recent_broadcasts[-5:]],
        )

    def _calculate_coherence(self) -> float:
        """Calculate coherence of recent workspace content"""
        if len(self.workspace_content) < 2:
            return 0.5

        # In full implementation, use semantic similarity between broadcasts
        # For now, use confidence and recency as proxy
        recent_confidences = [
            msg.confidence for msg in self.workspace_content[-5:]
        ]
        return sum(recent_confidences) / len(recent_confidences)

    def _calculate_consciousness_level(self) -> float:
        """
        Calculate overall consciousness level

        Based on:
        - Recent activity (broadcasts)
        - Integration quality (coherence)
        - Working memory utilization
        """
        # Activity component (0-0.4)
        recent_window = datetime.utcnow() - timedelta(seconds=30)
        recent_activity = sum(
            1 for msg in self.workspace_content if msg.timestamp > recent_window
        )
        activity_score = min(recent_activity / 10.0, 0.4)

        # Integration quality (0-0.4)
        coherence = self._calculate_coherence()
        integration_score = coherence * 0.4

        # Working memory utilization (0-0.2)
        memory_score = min(len(self.working_memory) / 20.0, 0.2)

        return activity_score + integration_score + memory_score

    def _get_active_specialists(self) -> List[SpecialistRole]:
        """Get list of recently active specialist roles"""
        recent_window = datetime.utcnow() - timedelta(seconds=10)
        active = set()

        for msg in self.workspace_content:
            if msg.timestamp > recent_window and msg.source:
                active.add(msg.source)

        return list(active)

    def get_metrics(self) -> Dict[str, Any]:
        """Get workspace performance metrics"""
        avg_processing_time = (
            self.total_processing_time_ms / self.integration_count
            if self.integration_count > 0
            else 0
        )

        return {
            "integration_count": self.integration_count,
            "broadcast_count": self.broadcast_count,
            "average_processing_time_ms": avg_processing_time,
            "workspace_content_size": len(self.workspace_content),
            "working_memory_size": len(self.working_memory),
            "consciousness_level": self._calculate_consciousness_level(),
        }
