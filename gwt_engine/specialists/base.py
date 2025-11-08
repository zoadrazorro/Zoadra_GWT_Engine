"""Base class for specialist modules"""

import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

from gwt_engine.core.types import (
    WorkspaceMessage,
    SpecialistResponse,
    SpecialistRole,
)
from gwt_engine.inference.vllm_client import VLLMClient, GenerationRequest

logger = logging.getLogger(__name__)


class BaseSpecialist(ABC):
    """
    Base class for all specialist modules in GWT architecture

    Each specialist:
    - Processes specific types of information
    - Competes for workspace attention
    - Responds to workspace broadcasts
    - Has specialized prompting for its domain
    """

    def __init__(self, vllm_client: VLLMClient, role: SpecialistRole):
        self.vllm_client = vllm_client
        self.role = role
        self.requests_processed = 0
        self.total_processing_time_ms = 0.0
        self.error_count = 0

        logger.info(f"{self.role.value} specialist initialized")

    @abstractmethod
    async def process(self, message: WorkspaceMessage) -> SpecialistResponse:
        """
        Process a workspace message and generate specialist response

        Args:
            message: Input message to process

        Returns:
            SpecialistResponse with specialist's output
        """
        pass

    @abstractmethod
    def _create_specialist_prompt(
        self, message: WorkspaceMessage, context: Dict[str, Any]
    ) -> str:
        """
        Create specialized prompt for this module's domain

        Args:
            message: Input message
            context: Additional context for processing

        Returns:
            Formatted prompt string
        """
        pass

    async def _generate_response(
        self, prompt: str, max_tokens: int = 512, temperature: float = 0.7
    ) -> str:
        """Generate text response using vLLM"""
        try:
            response = await self.vllm_client.generate(
                GenerationRequest(
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=0.9,
                )
            )
            return response.text.strip()

        except Exception as e:
            logger.error(f"{self.role.value} generation failed: {e}")
            self.error_count += 1
            raise

    def _calculate_confidence(self, context: Dict[str, Any]) -> float:
        """
        Calculate confidence score for this specialist's response

        Override in subclasses for specialist-specific confidence calculation
        """
        # Default: moderate confidence
        return 0.7

    async def process_with_timing(
        self, message: WorkspaceMessage
    ) -> SpecialistResponse:
        """
        Process message with timing and error handling

        This wraps the specialist's process() method with common functionality
        """
        start_time = time.time()
        self.requests_processed += 1

        try:
            response = await self.process(message)
            processing_time = (time.time() - start_time) * 1000
            self.total_processing_time_ms += processing_time

            # Update response with timing
            response.processing_time_ms = processing_time

            logger.debug(
                f"{self.role.value} processed message in {processing_time:.1f}ms "
                f"(confidence: {response.confidence:.2f})"
            )

            return response

        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            logger.error(
                f"{self.role.value} processing failed after {processing_time:.1f}ms: {e}"
            )
            raise

    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for this specialist"""
        avg_processing_time = (
            self.total_processing_time_ms / self.requests_processed
            if self.requests_processed > 0
            else 0
        )

        return {
            "role": self.role.value,
            "requests_processed": self.requests_processed,
            "average_processing_time_ms": avg_processing_time,
            "error_count": self.error_count,
            "error_rate": (
                self.error_count / self.requests_processed
                if self.requests_processed > 0
                else 0
            ),
        }
