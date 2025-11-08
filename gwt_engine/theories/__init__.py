"""
Multi-theory consciousness integration modules

Integrates multiple consciousness theories:
- GWT (Global Workspace Theory) - Baars/Dehaene
- IIT (Integrated Information Theory) - Tononi
- Predictive Processing - Clark/Friston
- Attention Schema Theory - Graziano
- Higher-Order Thought Theory - Rosenthal
- LIDA Cognitive Architecture - Franklin
- CLARION Dual-System - Sun
- Consciousness Scoring (0-100)
"""

from gwt_engine.theories.iit.phi_calculator import PhiCalculator
from gwt_engine.theories.predictive.predictor import PredictiveProcessor
from gwt_engine.theories.attention_schema.observer import AttentionSchemaObserver
from gwt_engine.theories.higher_order.hot_generator import HigherOrderThoughtGenerator
from gwt_engine.theories.lida.cognitive_cycle import LIDACognitiveController, LIDACyclePhase
from gwt_engine.theories.clarion.dual_system import CLARIONDualSystem
from gwt_engine.theories.scoring.consciousness_scorer import ConsciousnessScorer
from gwt_engine.theories.multi_theory_orchestrator import MultiTheoryOrchestrator

__all__ = [
    "PhiCalculator",
    "PredictiveProcessor",
    "AttentionSchemaObserver",
    "HigherOrderThoughtGenerator",
    "LIDACognitiveController",
    "LIDACyclePhase",
    "CLARIONDualSystem",
    "ConsciousnessScorer",
    "MultiTheoryOrchestrator",
]
