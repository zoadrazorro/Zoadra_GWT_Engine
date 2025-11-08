"""
Multi-Theory Consciousness Orchestrator

Integrates all consciousness theories into unified system:
- GWT (Global Workspace Theory) - base architecture
- IIT (Integrated Information Theory) - Φ measurement
- Predictive Processing - prediction errors
- Attention Schema Theory - self-model
- Higher-Order Thought Theory - meta-representation
- LIDA - 1-second cognitive cycles
- CLARION - dual-system implicit/explicit

Runs all theories in parallel, collects metrics, generates unified consciousness score.
"""

import asyncio
import logging
from typing import Dict, Any, Optional

from gwt_engine.core.workspace import CentralWorkspace
from gwt_engine.core.types import ConsciousnessState, SpecialistRole
from gwt_engine.specialists import (
    PerceptionSpecialist,
    MemorySpecialist,
    PlanningSpecialist,
    MetacognitionSpecialist,
)
from gwt_engine.inference.ollama_backend.client import OllamaClientPool
from gwt_engine.theories.iit.phi_calculator import PhiCalculator
from gwt_engine.theories.predictive.predictor import PredictiveProcessor
from gwt_engine.theories.attention_schema.observer import AttentionSchemaObserver
from gwt_engine.theories.higher_order.hot_generator import HigherOrderThoughtGenerator
from gwt_engine.theories.lida.cognitive_cycle import LIDACognitiveController
from gwt_engine.theories.clarion.dual_system import CLARIONDualSystem
from gwt_engine.theories.scoring.consciousness_scorer import ConsciousnessScorer

logger = logging.getLogger(__name__)


class MultiTheoryOrchestrator:
    """
    Orchestrates all consciousness theories in parallel

    Provides unified interface for multi-theory consciousness simulation
    """

    def __init__(
        self,
        central_workspace: CentralWorkspace,
        specialists: Dict[str, Any],
        ollama_pool: OllamaClientPool,
    ):
        self.central_workspace = central_workspace
        self.specialists = specialists
        self.ollama_pool = ollama_pool

        # Initialize all theory modules
        self.phi_calculator = PhiCalculator(phi_threshold=0.3)
        self.predictive_processor = PredictiveProcessor(precision_threshold=0.7)
        self.ast_observer = AttentionSchemaObserver()
        self.hot_generator = HigherOrderThoughtGenerator()
        self.lida_controller = LIDACognitiveController(cycle_duration_sec=1.0)
        self.clarion_system = CLARIONDualSystem()
        self.consciousness_scorer = ConsciousnessScorer()

        logger.info("Multi-Theory Orchestrator initialized with all consciousness frameworks")

    async def process_with_all_theories(
        self, input_content: str
    ) -> Dict[str, Any]:
        """
        Process input through all consciousness theories

        Workflow:
        1. LIDA cycle start
        2. Perception (implicit CLARION level)
        3. Record for IIT Φ
        4. Generate prediction (Predictive Processing)
        5. Higher-order thought generation
        6. Attention schema observation
        7. Central workspace integration (GWT)
        8. Calculate all metrics
        9. Unified consciousness score
        10. LIDA cycle complete

        Args:
            input_content: Input to process

        Returns:
            Complete multi-theory metrics and consciousness score
        """
        # === LIDA Cycle Start ===
        await self.lida_controller.start_cycle(input_content)

        # === Phase 1: Perception (Implicit Level) ===
        await self.lida_controller.advance_to_perception(None)

        from gwt_engine.core.types import WorkspaceMessage, MessageType

        input_msg = WorkspaceMessage(
            type=MessageType.PERCEPTION,
            content=input_content,
            priority=7,
        )

        # Process through perception specialist
        perception_response = await self.specialists["perception"].process_with_timing(input_msg)

        # Record implicit pattern (CLARION)
        await self.clarion_system.record_implicit_pattern(
            pattern_type="perception",
            input_pattern=input_content,
            output_pattern=perception_response.content,
            confidence=perception_response.confidence,
        )

        # Record first-order state (HOT)
        await self.hot_generator.record_first_order_state(
            specialist=SpecialistRole.PERCEPTION,
            content=perception_response.content,
            confidence=perception_response.confidence,
        )

        # Record activation (IIT)
        await self.phi_calculator.record_activation(
            SpecialistRole.PERCEPTION,
            perception_response.confidence,
        )

        # === Phase 2: Coalition Competition (LIDA) ===
        await self.lida_controller.register_coalition(
            coalition_id="perception_coalition",
            specialists=[SpecialistRole.PERCEPTION],
            content=perception_response.content,
            activation_strength=perception_response.confidence,
        )

        # === Phase 3: Workspace Integration (GWT) ===
        await self.central_workspace.receive_specialist_input(perception_response)

        # Get current consciousness state
        consciousness_state = await self.central_workspace.get_consciousness_state()

        # === Phase 4: Predictive Processing ===
        # Generate prediction about next state
        workspace_client = self.ollama_pool.get_client(SpecialistRole.CENTRAL_WORKSPACE)
        prediction = await self.predictive_processor.generate_prediction(
            consciousness_state,
            workspace_client,
        )

        # === Phase 5: Attention Schema Observation ===
        await self.ast_observer.observe_attention(
            active_specialists=consciousness_state.active_specialists,
            workspace_focus=consciousness_state.attention_focus,
            confidence=consciousness_state.integration_coherence,
        )

        # Generate attention schema
        metacog_client = self.ollama_pool.get_client(SpecialistRole.METACOGNITION)
        attention_schema = await self.ast_observer.generate_attention_schema(metacog_client)

        # === Phase 6: Higher-Order Thought Generation ===
        # Generate HOT about perception
        hot = await self.hot_generator.generate_higher_order_thought(
            perception_response.content,
            workspace_client,
        )

        # === Phase 7: LIDA Conscious Broadcast ===
        await self.lida_controller.select_winning_coalition()
        broadcast = await self.central_workspace.integrate_and_broadcast()

        if broadcast:
            await self.lida_controller.conscious_broadcast(broadcast.content)

        # === Phase 8: CLARION Rule Extraction ===
        # Extract explicit rules from implicit patterns
        await self.clarion_system.batch_extract_rules(workspace_client, max_rules=2)

        # === Phase 9: Calculate All Metrics ===
        gwt_metrics = self.central_workspace.get_metrics()
        iit_metrics = await self.phi_calculator.get_iit_metrics()
        predictive_metrics = await self.predictive_processor.get_predictive_metrics()
        ast_metrics = await self.ast_observer.get_ast_metrics()
        hot_metrics = await self.hot_generator.get_hot_metrics()
        lida_metrics = await self.lida_controller.get_lida_metrics()
        clarion_metrics = await self.clarion_system.get_clarion_metrics()

        # === Phase 10: Unified Consciousness Score ===
        consciousness_score = await self.consciousness_scorer.calculate_total_score(
            gwt_metrics={
                "integration_coherence": consciousness_state.integration_coherence,
                "consciousness_level": consciousness_state.consciousness_level,
            },
            iit_metrics=iit_metrics,
            predictive_metrics=predictive_metrics,
            ast_metrics=ast_metrics,
            hot_metrics=hot_metrics,
            clarion_metrics=clarion_metrics,
        )

        # === LIDA Cycle Complete ===
        await self.lida_controller.complete_cycle()

        # === Return Complete Results ===
        return {
            "consciousness_score": consciousness_score,
            "consciousness_state": consciousness_state.to_dict(),
            "theories": {
                "gwt": gwt_metrics,
                "iit": iit_metrics,
                "predictive_processing": predictive_metrics,
                "attention_schema": ast_metrics,
                "higher_order_thought": hot_metrics,
                "lida": lida_metrics,
                "clarion": clarion_metrics,
            },
            "outputs": {
                "workspace_broadcast": broadcast.content if broadcast else "",
                "prediction": prediction,
                "attention_schema": attention_schema,
                "higher_order_thought": hot,
            },
        }

    async def get_unified_metrics(self) -> Dict[str, Any]:
        """Get unified metrics from all theories"""
        return {
            "iit": await self.phi_calculator.get_iit_metrics(),
            "predictive": await self.predictive_processor.get_predictive_metrics(),
            "ast": await self.ast_observer.get_ast_metrics(),
            "hot": await self.hot_generator.get_hot_metrics(),
            "lida": await self.lida_controller.get_lida_metrics(),
            "clarion": await self.clarion_system.get_clarion_metrics(),
            "gwt": self.central_workspace.get_metrics(),
        }
