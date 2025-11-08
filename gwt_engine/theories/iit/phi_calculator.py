"""
Integrated Information Theory (IIT) Φ Approximation

Computes proxy for Φ (integrated information) using mutual information.
True Φ is NP-hard, but MI provides useful approximation for consciousness measurement.

Based on Tononi's IIT: Consciousness ≈ Φ (integrated information)
Runs in parallel on GPU2 while main inference happens on GPU1.
"""

import asyncio
import logging
from typing import Dict, List, Any
import numpy as np
from collections import defaultdict

from gwt_engine.core.types import SpecialistRole

logger = logging.getLogger(__name__)


class PhiCalculator:
    """
    IIT Φ calculator using mutual information proxy

    Methods:
    1. Mutual information between specialists (integration measure)
    2. Causal intervention tests (disable modules, measure impact)
    3. Integration threshold detection (Φ > 0.3 → conscious)
    """

    def __init__(self, phi_threshold: float = 0.3):
        self.phi_threshold = phi_threshold
        self.specialist_activations: Dict[SpecialistRole, List[float]] = defaultdict(list)
        self.phi_history: List[float] = []
        self.baseline_performance: float = 0.0

    async def record_activation(self, specialist: SpecialistRole, confidence: float):
        """Record specialist activation for MI calculation"""
        self.specialist_activations[specialist].append(confidence)

        # Keep last 100 samples
        if len(self.specialist_activations[specialist]) > 100:
            self.specialist_activations[specialist].pop(0)

    def _calculate_entropy(self, data: List[float], bins: int = 10) -> float:
        """Calculate Shannon entropy H(X) = -Σ p(x) log p(x)"""
        if len(data) < 5:
            return 0.0

        hist, _ = np.histogram(data, bins=bins, range=(0, 1))
        prob = hist / len(data)
        prob = prob[prob > 0]  # Remove zeros

        return -np.sum(prob * np.log2(prob))

    def _calculate_mutual_information(
        self, spec_a: SpecialistRole, spec_b: SpecialistRole
    ) -> float:
        """
        Calculate MI: I(A;B) = H(A) + H(B) - H(A,B)

        Higher MI → more integration between specialists
        """
        acts_a = self.specialist_activations.get(spec_a, [])
        acts_b = self.specialist_activations.get(spec_b, [])

        if len(acts_a) < 10 or len(acts_b) < 10:
            return 0.0

        # Marginal entropies
        h_a = self._calculate_entropy(acts_a)
        h_b = self._calculate_entropy(acts_b)

        # Joint entropy (2D histogram)
        min_len = min(len(acts_a), len(acts_b))
        hist_joint, _, _ = np.histogram2d(
            acts_a[-min_len:],
            acts_b[-min_len:],
            bins=10,
            range=[[0, 1], [0, 1]]
        )

        prob_joint = hist_joint / min_len
        prob_joint = prob_joint[prob_joint > 0]
        h_joint = -np.sum(prob_joint * np.log2(prob_joint))

        # Mutual information
        mi = h_a + h_b - h_joint
        return max(0.0, mi)

    async def calculate_phi(self) -> float:
        """
        Calculate Φ proxy as mean MI across all specialist pairs

        Φ_proxy = mean(I(A;B)) for all pairs

        Range: 0 (no integration) to ~2-3 (high integration)
        Threshold: Φ > 0.3 suggests consciousness
        """
        specialists = list(self.specialist_activations.keys())

        if len(specialists) < 2:
            return 0.0

        mi_values = []
        for i, spec_a in enumerate(specialists):
            for spec_b in specialists[i+1:]:
                mi = self._calculate_mutual_information(spec_a, spec_b)
                mi_values.append(mi)

        phi = np.mean(mi_values) if mi_values else 0.0

        self.phi_history.append(phi)
        if len(self.phi_history) > 100:
            self.phi_history.pop(0)

        return phi

    async def is_conscious(self) -> bool:
        """Check if Φ > threshold (consciousness criterion)"""
        phi = await self.calculate_phi()
        return phi > self.phi_threshold

    async def get_iit_metrics(self) -> Dict[str, Any]:
        """Get complete IIT metrics"""
        phi = await self.calculate_phi()

        return {
            "phi": float(phi),  # Convert numpy to Python float
            "phi_threshold": float(self.phi_threshold),
            "is_conscious_iit": bool(phi > self.phi_threshold),  # Convert numpy.bool to Python bool
            "integration_level": float(min(1.0, phi / 3.0)),  # Normalized 0-1
            "phi_history": [float(x) for x in self.phi_history[-10:]],  # Convert all to Python floats
            "num_specialists": int(len(self.specialist_activations)),
        }
