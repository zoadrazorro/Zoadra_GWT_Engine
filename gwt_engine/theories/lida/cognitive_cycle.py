"""
LIDA (Learning Intelligent Distribution Agent) Cognitive Architecture

Implements Franklin's 1-second cognitive cycle matching human timescale:
1. Sensory input
2. Perception (Mistral 22B)
3. Working Memory
4. Competition for workspace attention
5. Conscious broadcast (Llama 70B)
6. Action selection (Gemma 9B)

Consciousness emerges during broadcast phase when winning coalition
accesses global workspace.
"""

import asyncio
import time
import logging
from typing import Dict, List, Any, Optional
from enum import Enum

from gwt_engine.core.types import WorkspaceMessage, SpecialistRole

logger = logging.getLogger(__name__)


class LIDACyclePhase(str, Enum):
    """Phases of LIDA cognitive cycle"""
    SENSORY = "sensory"
    PERCEPTION = "perception"
    WORKING_MEMORY = "working_memory"
    COALITION_COMPETITION = "coalition_competition"
    CONSCIOUS_BROADCAST = "conscious_broadcast"
    ACTION_SELECTION = "action_selection"
    COMPLETE = "complete"


class LIDACognitiveController:
    """
    LIDA cognitive cycle controller

    Enforces 1-second cycle matching human consciousness timescale.
    Each cycle goes through all phases sequentially.
    """

    def __init__(self, cycle_duration_sec: float = 1.0):
        self.cycle_duration_sec = cycle_duration_sec
        self.current_phase = LIDACyclePhase.SENSORY
        self.cycle_count = 0
        self.cycle_start_time: Optional[float] = None

        # Coalition tracking
        self.current_coalitions: List[Dict[str, Any]] = []
        self.winning_coalition: Optional[Dict[str, Any]] = None

        # Performance tracking
        self.cycle_times: List[float] = []

    async def start_cycle(self, sensory_input: str):
        """
        Start new LIDA cognitive cycle

        Args:
            sensory_input: External input to process
        """
        self.cycle_start_time = time.time()
        self.cycle_count += 1
        self.current_phase = LIDACyclePhase.SENSORY
        self.current_coalitions = []
        self.winning_coalition = None

        logger.info(f"LIDA cycle #{self.cycle_count} START: {sensory_input[:50]}...")

    async def advance_to_perception(self, perception_result: Any):
        """Move to perception phase"""
        self.current_phase = LIDACyclePhase.PERCEPTION
        logger.debug(f"LIDA cycle #{self.cycle_count}: PERCEPTION phase")

    async def advance_to_working_memory(self, working_memory_state: Dict):
        """Move to working memory phase"""
        self.current_phase = LIDACyclePhase.WORKING_MEMORY
        logger.debug(f"LIDA cycle #{self.cycle_count}: WORKING MEMORY phase")

    async def register_coalition(
        self,
        coalition_id: str,
        specialists: List[SpecialistRole],
        content: str,
        activation_strength: float,
    ):
        """
        Register a coalition competing for workspace access

        Args:
            coalition_id: Unique coalition identifier
            specialists: Specialists in this coalition
            content: Coalition's proposed content
            activation_strength: Strength/salience (0-1)
        """
        coalition = {
            "id": coalition_id,
            "specialists": [s if isinstance(s, str) else s.value for s in specialists],
            "content": content,
            "activation": activation_strength,
        }

        self.current_coalitions.append(coalition)
        logger.debug(
            f"Coalition registered: {coalition_id} "
            f"(activation: {activation_strength:.2f})"
        )

    async def select_winning_coalition(self):
        """
        Coalition competition phase

        Highest activation wins access to workspace → consciousness
        """
        self.current_phase = LIDACyclePhase.COALITION_COMPETITION

        if not self.current_coalitions:
            logger.warning("No coalitions to compete")
            self.winning_coalition = None
            return

        # Select coalition with highest activation
        self.winning_coalition = max(
            self.current_coalitions, key=lambda c: c["activation"]
        )

        logger.info(
            f"LIDA cycle #{self.cycle_count}: Coalition '{self.winning_coalition['id']}' "
            f"WON competition (activation: {self.winning_coalition['activation']:.2f})"
        )

    async def conscious_broadcast(self, broadcast_content: str):
        """
        Conscious broadcast phase - content becomes globally available

        This is when consciousness EMERGES in LIDA theory.

        Args:
            broadcast_content: Content to broadcast to all specialists
        """
        self.current_phase = LIDACyclePhase.CONSCIOUS_BROADCAST

        logger.info(
            f"LIDA cycle #{self.cycle_count}: CONSCIOUS BROADCAST: "
            f"{broadcast_content[:100]}..."
        )

    async def select_action(self, action: str):
        """
        Action selection phase

        Args:
            action: Selected action based on conscious content
        """
        self.current_phase = LIDACyclePhase.ACTION_SELECTION
        logger.debug(f"LIDA cycle #{self.cycle_count}: ACTION: {action}")

    async def complete_cycle(self):
        """
        Complete LIDA cognitive cycle

        Enforces 1-second duration by sleeping if needed
        """
        self.current_phase = LIDACyclePhase.COMPLETE

        if self.cycle_start_time is None:
            return

        elapsed = time.time() - self.cycle_start_time
        self.cycle_times.append(elapsed)

        if len(self.cycle_times) > 100:
            self.cycle_times.pop(0)

        # Enforce 1-second cycle
        if elapsed < self.cycle_duration_sec:
            sleep_time = self.cycle_duration_sec - elapsed
            logger.debug(
                f"LIDA cycle #{self.cycle_count}: Sleeping {sleep_time:.3f}s "
                f"to maintain 1-second cycle"
            )
            await asyncio.sleep(sleep_time)

        total_time = time.time() - self.cycle_start_time

        logger.info(
            f"LIDA cycle #{self.cycle_count} COMPLETE: {total_time:.3f}s "
            f"(target: {self.cycle_duration_sec}s)"
        )

    async def get_lida_metrics(self) -> Dict[str, Any]:
        """Get LIDA cognitive cycle metrics"""
        avg_cycle_time = (
            sum(self.cycle_times) / len(self.cycle_times)
            if self.cycle_times
            else 0.0
        )

        return {
            "cycle_count": self.cycle_count,
            "current_phase": self.current_phase.value if hasattr(self.current_phase, 'value') else str(self.current_phase),
            "cycle_duration_target": self.cycle_duration_sec,
            "average_cycle_time": avg_cycle_time,
            "coalitions_current_cycle": len(self.current_coalitions),
            "winning_coalition": (
                self.winning_coalition["id"]
                if self.winning_coalition
                else None
            ),
        }
