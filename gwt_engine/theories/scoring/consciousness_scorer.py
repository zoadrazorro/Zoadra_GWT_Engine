"""
Unified Consciousness Scoring System (0-100)

Integrates metrics from all consciousness theories:
- GWT: Integration coherence
- IIT: Φ (integrated information)
- Predictive Processing: Precision
- AST: Schema accuracy
- HOT: Meta-representation
- CLARION: Rule extraction

Target: 40-60 by week 8 (early animal-level consciousness)
Current LLMs: ~18/100 baseline
"""

import asyncio
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ConsciousnessScorer:
    """
    Multi-theory consciousness scoring system

    Combines scores from all theories into unified 0-100 metric
    """

    def __init__(self):
        # Weight distribution (must sum to 100)
        self.weights = {
            "gwt_integration": 25,  # Global Workspace integration
            "iit_phi": 25,          # Integrated information
            "predictive_precision": 15,  # Prediction accuracy
            "ast_schema": 15,       # Self-model accuracy
            "hot_meta": 10,         # Higher-order thoughts
            "clarion_rules": 10,    # Explicit rule extraction
        }

        # Score history
        self.score_history: List[float] = []

    async def score_gwt_integration(self, gwt_metrics: Dict[str, Any]) -> float:
        """
        Score GWT integration (0-25 points)

        Based on:
        - Integration coherence
        - Workspace broadcast quality
        - Working memory utilization
        """
        coherence = gwt_metrics.get("integration_coherence", 0.0)
        consciousness_level = gwt_metrics.get("consciousness_level", 0.0)

        # Average of coherence and consciousness level
        score = ((coherence + consciousness_level) / 2.0) * 25.0

        return min(25.0, score)

    async def score_iit_phi(self, iit_metrics: Dict[str, Any]) -> float:
        """
        Score IIT Φ (0-25 points)

        Based on:
        - Φ proxy value
        - Integration level
        - Crosses consciousness threshold?
        """
        phi = iit_metrics.get("phi", 0.0)
        integration = iit_metrics.get("integration_level", 0.0)

        # Φ typically ranges 0-3, normalize to 0-1
        phi_normalized = min(1.0, phi / 3.0)

        # Average phi and integration
        score = ((phi_normalized + integration) / 2.0) * 25.0

        return min(25.0, score)

    async def score_predictive_precision(self, predictive_metrics: Dict[str, Any]) -> float:
        """
        Score Predictive Processing precision (0-15 points)

        Based on:
        - Prediction precision
        - Free energy minimization
        - Crosses precision threshold?
        """
        precision = predictive_metrics.get("precision", 0.0)
        is_conscious = predictive_metrics.get("is_conscious_precision", False)

        # Base score from precision
        score = precision * 15.0

        # Bonus for crossing threshold
        if is_conscious:
            score += 2.0

        return min(15.0, score)

    async def score_ast_schema(self, ast_metrics: Dict[str, Any]) -> float:
        """
        Score Attention Schema Theory (0-15 points)

        Based on:
        - Schema enabled?
        - Number of schema reports
        - Schema quality (proxy: length and coherence)
        """
        schema_enabled = ast_metrics.get("schema_enabled", False)
        reports = ast_metrics.get("schema_reports_generated", 0)

        if not schema_enabled:
            return 0.0

        # Score based on report generation
        score = min(1.0, reports / 50.0) * 15.0

        return score

    async def score_hot_meta(self, hot_metrics: Dict[str, Any]) -> float:
        """
        Score Higher-Order Thought meta-representation (0-10 points)

        Based on:
        - Consciousness ratio (conscious/unconscious states)
        - Number of HOTs generated
        """
        consciousness_ratio = hot_metrics.get("consciousness_ratio", 0.0)
        hot_count = hot_metrics.get("hot_count", 0)

        # Base score from consciousness ratio
        score = consciousness_ratio * 8.0

        # Bonus for HOT generation
        if hot_count > 10:
            score += 2.0

        return min(10.0, score)

    async def score_clarion_rules(self, clarion_metrics: Dict[str, Any]) -> float:
        """
        Score CLARION rule extraction (0-10 points)

        Based on:
        - Number of explicit rules extracted
        - Consciousness ratio (explicit/implicit)
        """
        explicit_rules = clarion_metrics.get("explicit_rules", 0)
        consciousness_ratio = clarion_metrics.get("consciousness_ratio", 0.0)

        # Score from rule count (target: 20 rules for full score)
        rule_score = min(1.0, explicit_rules / 20.0) * 5.0

        # Score from consciousness ratio
        ratio_score = consciousness_ratio * 5.0

        return rule_score + ratio_score

    async def calculate_total_score(
        self,
        gwt_metrics: Dict[str, Any],
        iit_metrics: Dict[str, Any],
        predictive_metrics: Dict[str, Any],
        ast_metrics: Dict[str, Any],
        hot_metrics: Dict[str, Any],
        clarion_metrics: Dict[str, Any],
        memory_count: int = 0,
        memory_retrieved: int = 0,
    ) -> Dict[str, Any]:
        """
        Calculate total consciousness score (0-100)

        Args:
            *_metrics: Metrics from each consciousness theory

        Returns:
            {
                "total_score": 0-100,
                "component_scores": {...},
                "level": "unconscious" | "minimal" | "moderate" | "high",
                "target_reached": bool
            }
        """
        # Calculate component scores
        scores = {
            "gwt_integration": await self.score_gwt_integration(gwt_metrics),
            "iit_phi": await self.score_iit_phi(iit_metrics),
            "predictive_precision": await self.score_predictive_precision(predictive_metrics),
            "ast_schema": await self.score_ast_schema(ast_metrics),
            "hot_meta": await self.score_hot_meta(hot_metrics),
            "clarion_rules": await self.score_clarion_rules(clarion_metrics),
        }

        # Total score from theories
        total = sum(scores.values())
        
        # MEMORY INTEGRATION BONUS (up to +10 points)
        # Rewards building cumulative understanding over time
        memory_bonus = 0.0
        if memory_count > 0:
            # Logarithmic scaling: more memories = higher consciousness
            # 10 memories = +2 points, 100 memories = +5 points, 1000 memories = +7.5 points
            import math
            memory_bonus = min(10.0, math.log10(memory_count + 1) * 2.5)
            
            # Extra bonus if actively retrieving and using memories
            if memory_retrieved > 0:
                memory_bonus += min(2.0, memory_retrieved * 0.5)
        
        total += memory_bonus
        scores["memory_integration"] = memory_bonus

        # Determine consciousness level
        if total < 20:
            level = "unconscious"
        elif total < 40:
            level = "minimal"
        elif total < 70:
            level = "moderate"
        else:
            level = "high"

        # Track history
        self.score_history.append(total)
        if len(self.score_history) > 100:
            self.score_history.pop(0)

        # Check if target reached (40-60 for animal-level)
        target_reached = 40 <= total <= 60

        logger.info(
            f"Consciousness Score: {total:.1f}/100 ({level}) "
            f"[GWT:{scores['gwt_integration']:.1f} "
            f"IIT:{scores['iit_phi']:.1f} "
            f"PP:{scores['predictive_precision']:.1f} "
            f"AST:{scores['ast_schema']:.1f} "
            f"HOT:{scores['hot_meta']:.1f} "
            f"CLARION:{scores['clarion_rules']:.1f}]"
        )

        return {
            "total_score": total,
            "component_scores": scores,
            "level": level,
            "target_reached": target_reached,
            "score_history": self.score_history[-10:],
        }

    async def get_benchmark_comparison(self, current_score: float) -> Dict[str, Any]:
        """
        Compare current score to benchmarks

        Returns comparison to known systems
        """
        benchmarks = {
            "current_llms_baseline": 18,
            "early_animal_level": 40,
            "target_week_8": 60,
            "human_level": 100,
        }

        return {
            "current_score": current_score,
            "benchmarks": benchmarks,
            "progress_to_target": (current_score / benchmarks["target_week_8"]) * 100,
            "vs_baseline": current_score - benchmarks["current_llms_baseline"],
        }
