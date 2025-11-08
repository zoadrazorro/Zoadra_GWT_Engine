"""
Predictive Processing (Clark/Friston)

Implements hierarchical prediction error minimization:
1. Top-down predictions from Llama 70B about workspace state
2. Bottom-up sensory input from specialists
3. Prediction error = actual - predicted
4. Precision-weighted errors → consciousness when high precision

Free Energy Principle: Minimize variational free energy F = -log P(observations)
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
import numpy as np

from gwt_engine.core.types import WorkspaceMessage, ConsciousnessState

logger = logging.getLogger(__name__)


class PredictiveProcessor:
    """
    Predictive processing layer for consciousness

    Consciousness = high-precision prediction errors that cross threshold
    (Similar to anesthesia: reduced precision → reduced consciousness)
    """

    def __init__(self, precision_threshold: float = 0.7):
        self.precision_threshold = precision_threshold
        self.predictions: List[str] = []
        self.prediction_errors: List[float] = []
        self.precision_history: List[float] = []

    async def generate_prediction(
        self,
        current_state: ConsciousnessState,
        prediction_generator: Any,  # LLM client
    ) -> str:
        """
        Generate top-down prediction about next workspace state

        Args:
            current_state: Current consciousness state
            prediction_generator: LLM to generate prediction

        Returns:
            Predicted workspace content
        """
        # Build prediction prompt
        recent_content = [
            msg.content for msg in current_state.workspace_content[-3:]
        ]

        prompt = f"""Based on recent consciousness states:
{chr(10).join(f"- {content[:100]}..." for content in recent_content)}

Predict the next likely conscious thought (one sentence):"""

        try:
            from gwt_engine.inference.ollama_backend.client import OllamaGenerationRequest

            response = await prediction_generator.generate(
                OllamaGenerationRequest(
                    prompt=prompt,
                    model=prediction_generator.model_name,
                    max_tokens=100,
                    temperature=0.5,  # Lower temp for prediction
                )
            )

            prediction = response.text.strip()
            self.predictions.append(prediction)

            if len(self.predictions) > 50:
                self.predictions.pop(0)

            return prediction

        except Exception as e:
            logger.error(f"Prediction generation failed: {e}")
            return ""

    async def calculate_prediction_error(
        self, predicted: str, actual: str
    ) -> float:
        """
        Calculate prediction error between predicted and actual states

        Uses semantic similarity proxy (simplified: token overlap)
        Full implementation would use embeddings

        Returns:
            Prediction error (0-1), higher = more surprising/conscious
        """
        if not predicted or not actual:
            return 0.0

        # Simple token overlap measure (proxy for semantic similarity)
        pred_tokens = set(predicted.lower().split())
        actual_tokens = set(actual.lower().split())

        if not pred_tokens or not actual_tokens:
            return 0.0

        overlap = len(pred_tokens & actual_tokens)
        total = len(pred_tokens | actual_tokens)

        similarity = overlap / total if total > 0 else 0.0

        # Prediction error = 1 - similarity
        error = 1.0 - similarity

        self.prediction_errors.append(error)
        if len(self.prediction_errors) > 100:
            self.prediction_errors.pop(0)

        return error

    async def calculate_precision(self) -> float:
        """
        Calculate prediction precision (inverse of uncertainty)

        High precision → confident predictions → conscious processing
        Low precision → uncertain → unconscious (like anesthesia)

        Precision = 1 / variance(prediction_errors)
        """
        if len(self.prediction_errors) < 5:
            return 0.5

        variance = np.var(self.prediction_errors)

        # Precision = 1 / (variance + epsilon)
        precision = 1.0 / (variance + 0.01)

        # Normalize to 0-1
        precision = min(1.0, precision / 10.0)

        self.precision_history.append(precision)
        if len(self.precision_history) > 100:
            self.precision_history.pop(0)

        return precision

    async def is_conscious_by_precision(self) -> bool:
        """
        Consciousness test: High precision prediction errors

        Returns True if precision > threshold
        """
        precision = await self.calculate_precision()
        return precision > self.precision_threshold

    async def update_prediction_error(self, error: float):
        """
        Manually update prediction error
        
        Args:
            error: Prediction error value (0-1)
        """
        self.prediction_errors.append(error)
        if len(self.prediction_errors) > 100:
            self.prediction_errors.pop(0)
    
    async def calculate_free_energy(self) -> float:
        """
        Calculate variational free energy (simplified)

        F ≈ prediction_error + complexity
        System minimizes F through action and perception

        Lower F → better model of world
        """
        if not self.prediction_errors:
            return 1.0

        # Simplified: F ≈ mean(prediction_error)
        recent_errors = self.prediction_errors[-10:]
        free_energy = np.mean(recent_errors)

        return free_energy

    async def get_predictive_metrics(self) -> Dict[str, Any]:
        """Get predictive processing metrics"""
        precision = await self.calculate_precision()
        free_energy = await self.calculate_free_energy()

        return {
            "precision": precision,
            "precision_threshold": self.precision_threshold,
            "is_conscious_precision": precision > self.precision_threshold,
            "free_energy": free_energy,
            "mean_prediction_error": (
                np.mean(self.prediction_errors[-10:])
                if self.prediction_errors
                else 0.0
            ),
            "prediction_count": len(self.predictions),
        }
