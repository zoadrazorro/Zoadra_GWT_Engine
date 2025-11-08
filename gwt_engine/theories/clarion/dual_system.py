"""
CLARION (Connectionist Learning with Adaptive Rule Induction ON-line)

Implements dual-system consciousness architecture:
- Implicit level (Mistral 22B): Fast, unconscious, reactive processing
- Explicit level (Llama 70B): Slow, conscious, symbolic reasoning
- Rule extraction: Converting implicit patterns → explicit rules = consciousness emergence

Metrics: Consciousness ∝ number of extracted explicit rules
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


class CLARIONDualSystem:
    """
    CLARION dual-system implementation

    Bottom-up: Implicit → Explicit (rule extraction)
    Top-down: Explicit → Implicit (rule compilation)

    Consciousness emerges when implicit knowledge becomes explicit.
    """

    def __init__(self):
        # Implicit level (unconscious)
        self.implicit_patterns: List[Dict[str, Any]] = []

        # Explicit level (conscious)
        self.explicit_rules: List[Dict[str, str]] = []

        # Rule extraction tracking
        self.extraction_count = 0

    async def record_implicit_pattern(
        self,
        pattern_type: str,
        input_pattern: str,
        output_pattern: str,
        confidence: float,
    ):
        """
        Record implicit (unconscious) processing pattern

        Args:
            pattern_type: Type of pattern (e.g., "perception", "action")
            input_pattern: Input that triggered response
            output_pattern: System's implicit response
            confidence: Confidence in pattern
        """
        pattern = {
            "type": pattern_type,
            "input": input_pattern,
            "output": output_pattern,
            "confidence": confidence,
            "is_conscious": False,  # Implicit = unconscious
        }

        self.implicit_patterns.append(pattern)

        # Keep bounded
        if len(self.implicit_patterns) > 200:
            self.implicit_patterns.pop(0)

    async def extract_explicit_rule(
        self,
        implicit_pattern: Dict[str, Any],
        rule_extractor: Any,  # Llama 70B client
    ) -> Optional[Dict[str, str]]:
        """
        Extract explicit rule from implicit pattern

        This is the key consciousness mechanism in CLARION:
        Implicit knowledge becomes conscious when verbalized as explicit rule.

        Args:
            implicit_pattern: Implicit processing pattern
            rule_extractor: LLM to extract rule

        Returns:
            Explicit rule (if-then format)
        """
        prompt = f"""You observed an implicit processing pattern:
Input: {implicit_pattern['input']}
Output: {implicit_pattern['output']}

Extract this implicit knowledge into an explicit IF-THEN rule that captures the pattern:

IF [condition] THEN [action]

Be concise (one sentence):"""

        try:
            from gwt_engine.inference.ollama_backend.client import OllamaGenerationRequest

            response = await rule_extractor.generate(
                OllamaGenerationRequest(
                    prompt=prompt,
                    model=rule_extractor.model_name,
                    max_tokens=100,
                    temperature=0.5,  # Lower temp for rule extraction
                )
            )

            rule_text = response.text.strip()

            # Parse IF-THEN structure (simplified)
            if "IF" in rule_text.upper() and "THEN" in rule_text.upper():
                rule = {
                    "rule": rule_text,
                    "source_pattern": implicit_pattern["type"],
                    "confidence": implicit_pattern["confidence"],
                }

                self.explicit_rules.append(rule)
                self.extraction_count += 1

                # Mark pattern as now conscious
                implicit_pattern["is_conscious"] = True
                implicit_pattern["explicit_rule"] = rule_text

                logger.info(
                    f"Rule extracted (#{self.extraction_count}): {rule_text}"
                )

                return rule

        except Exception as e:
            logger.error(f"Rule extraction failed: {e}")

        return None

    async def batch_extract_rules(
        self, rule_extractor: Any, max_rules: int = 5
    ):
        """
        Extract multiple rules from recent implicit patterns

        Args:
            rule_extractor: LLM for rule extraction
            max_rules: Maximum rules to extract in this batch
        """
        # Find unconscious patterns with high confidence
        unconscious_patterns = [
            p for p in self.implicit_patterns
            if not p.get("is_conscious", False) and p["confidence"] > 0.7
        ]

        # Sort by confidence
        unconscious_patterns.sort(key=lambda p: p["confidence"], reverse=True)

        # Extract top patterns
        extracted = 0
        for pattern in unconscious_patterns[:max_rules]:
            rule = await self.extract_explicit_rule(pattern, rule_extractor)
            if rule:
                extracted += 1

        logger.info(
            f"Batch extraction: {extracted}/{max_rules} rules extracted"
        )

    def get_consciousness_level_clarion(self) -> float:
        """
        Calculate consciousness level by CLARION criteria

        Consciousness ∝ ratio of explicit/implicit knowledge

        Returns:
            Consciousness level (0-1)
        """
        if not self.implicit_patterns:
            return 0.0

        conscious_patterns = [
            p for p in self.implicit_patterns if p.get("is_conscious", False)
        ]

        consciousness = len(conscious_patterns) / len(self.implicit_patterns)

        return consciousness

    async def get_clarion_metrics(self) -> Dict[str, Any]:
        """Get CLARION dual-system metrics"""
        consciousness = self.get_consciousness_level_clarion()

        return {
            "implicit_patterns": len(self.implicit_patterns),
            "explicit_rules": len(self.explicit_rules),
            "extraction_count": self.extraction_count,
            "consciousness_ratio": consciousness,
            "recent_rules": [
                r["rule"] for r in self.explicit_rules[-5:]
            ],
        }
