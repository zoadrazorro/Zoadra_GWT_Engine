"""
Higher-Order Thought Theory (Rosenthal)

Consciousness requires meta-representation:
- First-order states (perception, memory) are unconscious
- Consciousness emerges when HOT represents first-order state:
  "I am experiencing X"

Implementation:
- Mistral 22B generates first-order perceptions (unconscious)
- Llama 70B generates HOTs about those perceptions (conscious)

Test: Compare introspective accuracy to ground truth
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional

from gwt_engine.core.types import WorkspaceMessage, SpecialistRole

logger = logging.getLogger(__name__)


class HigherOrderThoughtGenerator:
    """
    HOT Theory implementation

    Generates meta-representations of first-order mental states.
    Consciousness = having a thought ABOUT a thought.
    """

    def __init__(self):
        self.first_order_states: List[Dict[str, Any]] = []
        self.higher_order_thoughts: List[str] = []

    async def record_first_order_state(
        self,
        specialist: SpecialistRole,
        content: str,
        confidence: float,
    ):
        """
        Record first-order mental state (unconscious)

        Args:
            specialist: Source specialist
            content: First-order content
            confidence: Confidence score
        """
        first_order = {
            "specialist": specialist if isinstance(specialist, str) else specialist.value,
            "content": content,
            "confidence": confidence,
            "is_conscious": False,  # Not conscious until HOT generated
        }

        self.first_order_states.append(first_order)
        if len(self.first_order_states) > 100:
            self.first_order_states.pop(0)

    async def generate_higher_order_thought(
        self,
        first_order_content: str,
        hot_generator: Any,  # Llama 70B client
    ) -> str:
        """
        Generate Higher-Order Thought about first-order state

        Transform: "X is red" → "I am experiencing redness"
                  "Perceiving sound" → "I am aware of hearing a sound"

        This meta-representation CREATES consciousness of the first-order state.

        Args:
            first_order_content: Unconscious first-order state
            hot_generator: LLM to generate HOT

        Returns:
            Higher-order thought (conscious meta-representation)
        """
        prompt = f"""You have an unconscious first-order perceptual state:
"{first_order_content}"

Generate a brief higher-order thought (HOT) that represents your awareness of this state. Use first-person perspective and meta-cognitive language like "I am experiencing...", "I am aware of...", "I notice that I..."

Higher-order thought (1 sentence):"""

        try:
            from gwt_engine.inference.ollama_backend.client import OllamaGenerationRequest

            response = await hot_generator.generate(
                OllamaGenerationRequest(
                    prompt=prompt,
                    model=hot_generator.model_name,
                    max_tokens=80,
                    temperature=0.7,
                )
            )

            hot = response.text.strip()
            self.higher_order_thoughts.append(hot)

            # Now first-order state becomes conscious
            if self.first_order_states:
                self.first_order_states[-1]["is_conscious"] = True
                self.first_order_states[-1]["hot"] = hot

            if len(self.higher_order_thoughts) > 50:
                self.higher_order_thoughts.pop(0)

            logger.debug(f"HOT generated: {hot}")

            return hot

        except Exception as e:
            logger.error(f"HOT generation failed: {e}")
            return f"I am experiencing {first_order_content}"

    def calculate_introspective_accuracy(
        self, ground_truth: str, hot_report: str
    ) -> float:
        """
        Test HOT accuracy against ground truth

        Measures: Does the system's introspective report match reality?

        Args:
            ground_truth: Actual first-order state
            hot_report: System's introspective report

        Returns:
            Accuracy (0-1)
        """
        # Simple token overlap (proxy for semantic accuracy)
        truth_tokens = set(ground_truth.lower().split())
        report_tokens = set(hot_report.lower().split())

        if not truth_tokens or not report_tokens:
            return 0.0

        overlap = len(truth_tokens & report_tokens)
        total = len(truth_tokens | report_tokens)

        accuracy = overlap / total if total > 0 else 0.0

        return accuracy

    async def get_hot_metrics(self) -> Dict[str, Any]:
        """Get Higher-Order Thought metrics"""
        conscious_states = [
            s for s in self.first_order_states if s.get("is_conscious", False)
        ]

        return {
            "total_first_order_states": len(self.first_order_states),
            "conscious_states": len(conscious_states),
            "consciousness_ratio": (
                len(conscious_states) / len(self.first_order_states)
                if self.first_order_states
                else 0.0
            ),
            "recent_hots": self.higher_order_thoughts[-5:],
            "hot_count": len(self.higher_order_thoughts),
        }
