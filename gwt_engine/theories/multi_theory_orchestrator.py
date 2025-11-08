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

# ChromaDB import with error handling
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except Exception as e:
    logging.warning(f"ChromaDB not available: {e}")
    CHROMADB_AVAILABLE = False

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
        
        # Initialize simple persistent memory (JSON-based fallback since ChromaDB incompatible with Python 3.14)
        import json
        from pathlib import Path
        
        self.memory_file = Path("./philosophical_memory.json")
        self.philosophical_memories = []
        self.memory_counter = 0
        
        # Load existing memories
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.philosophical_memories = data.get("memories", [])
                    self.memory_counter = data.get("counter", 0)
                logger.info(f"Loaded {len(self.philosophical_memories)} existing memories from disk")
            except Exception as e:
                logger.warning(f"Could not load memories: {e}")
        
        self.memory_enabled = True
        logger.info("Multi-Theory Orchestrator initialized with JSON-based persistent memory")

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
        # === Phase 0: Memory Retrieval ===
        # Retrieve relevant past insights (simple keyword matching)
        input_with_memory = input_content
        memories_retrieved = 0
        
        if self.memory_enabled and self.philosophical_memories:
            try:
                # Simple keyword-based retrieval
                input_words = set(input_content.lower().split())
                relevant = []
                
                for mem in reversed(self.philosophical_memories[-50:]):  # Check last 50
                    mem_words = set(mem['content'].lower().split())
                    overlap = len(input_words & mem_words)
                    if overlap > 2:  # At least 3 words in common
                        relevant.append((overlap, mem))
                
                if relevant:
                    # Sort by relevance (by overlap score) and take top 10 (AMPLIFIED!)
                    relevant.sort(key=lambda x: x[0], reverse=True)
                    memory_context = "\n\nRELEVANT PAST INSIGHTS:\n"
                    for i, (overlap_score, mem) in enumerate(relevant[:10], 1):
                        memory_context += f"{i}. {mem['content'][:200]}... [Score: {mem['score']:.1f}]\n"
                    
                    input_with_memory = f"{input_content}{memory_context}"
                    memories_retrieved = len(relevant[:10])
                    logger.info(f"🧠 Retrieved {memories_retrieved} relevant memories (AMPLIFIED)")
                    
            except Exception as e:
                logger.warning(f"Memory retrieval failed: {e}")
        
        # === LIDA Cycle Start ===
        await self.lida_controller.start_cycle(input_with_memory)

        # === Phase 1: Perception (Implicit Level) ===
        await self.lida_controller.advance_to_perception(None)

        from gwt_engine.core.types import WorkspaceMessage, MessageType

        input_msg = WorkspaceMessage(
            type=MessageType.PERCEPTION,
            content=input_with_memory,  # Use memory-enhanced input
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
            specialist="perception",
            content=perception_response.content,
            confidence=perception_response.confidence,
        )

        # Record activation (IIT) - use varying confidence based on content length
        activation_strength = min(1.0, len(perception_response.content) / 500.0)
        await self.phi_calculator.record_activation(
            "perception",
            activation_strength,
        )

        # === Phase 2: Coalition Competition (LIDA) ===
        await self.lida_controller.register_coalition(
            coalition_id="perception_coalition",
            specialists=["perception"],
            content=perception_response.content,
            activation_strength=perception_response.confidence,
        )

        # === Phase 3: Workspace Integration (GWT) ===
        await self.central_workspace.receive_specialist_input(perception_response)

        # Get current consciousness state
        consciousness_state = await self.central_workspace.get_consciousness_state()

        # === Phase 4: Predictive Processing ===
        # Generate prediction about next state
        workspace_client = self.ollama_pool.get_client("central_workspace")
        prediction = await self.predictive_processor.generate_prediction(
            consciousness_state,
            workspace_client,
        )
        
        # Update prediction error based on actual vs predicted
        if prediction and input_content:
            # Simple heuristic: lower error if prediction contains key terms from input
            input_words = input_content.lower().split()[:5]
            prediction_error = 0.3 if input_words and any(word in prediction.lower() for word in input_words) else 0.7
            await self.predictive_processor.update_prediction_error(prediction_error)
        else:
            # Default moderate error if no prediction
            await self.predictive_processor.update_prediction_error(0.5)

        # === Phase 5: Attention Schema Observation ===
        await self.ast_observer.observe_attention(
            active_specialists=consciousness_state.active_specialists,
            workspace_focus=consciousness_state.attention_focus,
            confidence=consciousness_state.integration_coherence,
        )

        # Generate attention schema
        metacog_client = self.ollama_pool.get_client("metacognition")
        attention_schema = await self.ast_observer.generate_attention_schema(metacog_client)

        # === Phase 6: Higher-Order Thought Generation ===
        # Generate HOT about perception
        # Record more specialist activations for IIT
        await self.phi_calculator.record_activation(
            "memory",
            0.7 + (consciousness_state.integration_coherence * 0.3),
        )
        await self.phi_calculator.record_activation(
            "planning",
            0.6 + (consciousness_state.consciousness_level * 0.4),
        )
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
        consciousness_score_result = await self.consciousness_scorer.calculate_total_score(
            gwt_metrics={
                "integration_coherence": consciousness_state.integration_coherence,
                "consciousness_level": consciousness_state.consciousness_level,
            },
            iit_metrics=iit_metrics,
            predictive_metrics=predictive_metrics,
            ast_metrics=ast_metrics,
            hot_metrics=hot_metrics,
            clarion_metrics=clarion_metrics,
            memory_count=len(self.philosophical_memories) if self.memory_enabled else 0,
            memory_retrieved=memories_retrieved,
        )

        # === LIDA Cycle Complete ===
        await self.lida_controller.complete_cycle()
        
        # === Phase 11: Store in Persistent Memory ===
        # Store the integrated understanding
        if self.memory_enabled:
            try:
                import json
                self.memory_counter += 1
                
                # BOMBSHELL: Add emotional valence and significance
                score_val = float(consciousness_score_result.get("total_score", 0))
                phi_val = float(iit_metrics.get("phi", 0))
                
                # Emotional valence based on consciousness level
                level = consciousness_score_result.get("level", "unconscious")
                emotion_map = {
                    "unconscious": ("neutral", 0.0),
                    "minimal": ("curiosity", 0.3),
                    "moderate": ("engagement", 0.6),
                    "high": ("fascination", 0.8),
                    "very_high": ("awe", 0.9)
                }
                emotion, valence = emotion_map.get(level, ("neutral", 0.0))
                
                # Significance based on score and phi
                significance = min(1.0, (score_val / 50.0) * (phi_val * 10))
                
                memory_entry = {
                    "id": self.memory_counter,
                    "content": broadcast.content if broadcast else perception_response.content,
                    "score": score_val,
                    "level": level,
                    "iit_phi": phi_val,
                    "emotion": emotion,  # NEW: Emotional tag
                    "valence": valence,  # NEW: Emotional intensity
                    "significance": significance,  # NEW: Memory importance
                    "timestamp": asyncio.get_event_loop().time()
                }
                self.philosophical_memories.append(memory_entry)
                
                # Save to disk every 10 memories
                if self.memory_counter % 10 == 0:
                    with open(self.memory_file, 'w', encoding='utf-8') as f:
                        json.dump({
                            "counter": self.memory_counter,
                            "memories": self.philosophical_memories
                        }, f, indent=2)
                    logger.info(f"💾 Saved {len(self.philosophical_memories)} memories to disk")
                
                logger.info(f"💾 Memory #{self.memory_counter} - Score: {memory_entry['score']:.2f}")
                
            except Exception as e:
                logger.error(f"Memory storage failed: {e}")

        # === Return Complete Results ===
        return {
            "consciousness_score": consciousness_score_result.get("total_score", 0),
            "consciousness_level": consciousness_score_result.get("level", "unconscious"),
            "component_scores": consciousness_score_result.get("component_scores", {}),
            "consciousness_state": consciousness_state.to_dict() if hasattr(consciousness_state, 'to_dict') else {},
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
