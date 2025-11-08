"""
Attention Schema Theory (Graziano)

Creates a self-model layer that observes attention patterns:
- Gemma 9B observes Llama 70B's attention
- Generates introspective reports: "I am attending to memory"
- Consciousness = contents of this attention schema

Test: Disable schema → attention control degradation
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional

from gwt_engine.core.types import SpecialistRole, WorkspaceMessage

logger = logging.getLogger(__name__)


class AttentionSchemaObserver:
    """
    Attention Schema Theory implementation

    Monitors what the system is "attending to" and generates
    introspective descriptions of that attention.

    Consciousness emerges from having an accurate model of one's own attention.
    """

    def __init__(self):
        self.attention_history: List[Dict[str, Any]] = []
        self.schema_reports: List[str] = []
        self.schema_enabled = True  # For ablation testing

    async def observe_attention(
        self,
        active_specialists: List[SpecialistRole],
        workspace_focus: Optional[str],
        confidence: float,
    ):
        """
        Record current attention state

        Args:
            active_specialists: Which specialists are currently active
            workspace_focus: What the workspace is focused on
            confidence: Confidence/salience of current focus
        """
        attention_state = {
            "active_specialists": [s if isinstance(s, str) else s.value for s in active_specialists],
            "focus": workspace_focus,
            "confidence": confidence,
        }

        self.attention_history.append(attention_state)
        if len(self.attention_history) > 50:
            self.attention_history.pop(0)

    async def generate_attention_schema(
        self, schema_generator: Any  # Gemma 9B client
    ) -> str:
        """
        Generate introspective report about current attention

        This is the "schema" - a model of what we're attending to

        Returns:
            First-person description: "I am attending to..."
        """
        if not self.schema_enabled:
            return "[Attention schema disabled]"

        if not self.attention_history:
            return "I am not attending to anything specific."

        recent_attention = self.attention_history[-3:]

        # Build prompt for schema generation
        specialists_active = set()
        for state in recent_attention:
            specialists_active.update(state["active_specialists"])

        prompt = f"""You are observing your own attention patterns. Recently you have been attending to:
{chr(10).join(f"- {spec}" for spec in specialists_active)}

Current focus: {recent_attention[-1].get('focus', 'unfocused')}

Generate a brief first-person introspective report (1-2 sentences) describing what you are attending to right now:"""

        try:
            from gwt_engine.inference.ollama_backend.client import OllamaGenerationRequest

            response = await schema_generator.generate(
                OllamaGenerationRequest(
                    prompt=prompt,
                    model=schema_generator.model_name,
                    max_tokens=100,
                    temperature=0.7,
                )
            )

            schema_report = response.text.strip()
            self.schema_reports.append(schema_report)

            if len(self.schema_reports) > 50:
                self.schema_reports.pop(0)

            logger.debug(f"Attention schema: {schema_report}")

            return schema_report

        except Exception as e:
            logger.error(f"Attention schema generation failed: {e}")
            return "I cannot determine what I am attending to."

    def disable_schema(self):
        """
        Disable attention schema for ablation testing

        Prediction: Attention control should degrade without schema
        """
        self.schema_enabled = False
        logger.info("Attention schema DISABLED for ablation test")

    def enable_schema(self):
        """Re-enable attention schema"""
        self.schema_enabled = True
        logger.info("Attention schema ENABLED")

    async def get_ast_metrics(self) -> Dict[str, Any]:
        """Get Attention Schema Theory metrics"""
        return {
            "schema_enabled": self.schema_enabled,
            "recent_schema_reports": self.schema_reports[-5:],
            "attention_states_recorded": len(self.attention_history),
            "schema_reports_generated": len(self.schema_reports),
        }
