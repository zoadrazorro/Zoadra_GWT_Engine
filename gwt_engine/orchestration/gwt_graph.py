"""
LangGraph workflow for GWT consciousness architecture

Orchestrates the flow between specialists and central workspace
"""

import asyncio
import logging
from typing import Dict, Any, List, TypedDict, Annotated
from datetime import datetime

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from gwt_engine.core.types import (
    WorkspaceMessage,
    SpecialistResponse,
    MessageType,
    SpecialistRole,
    ConsciousnessState,
)
from gwt_engine.core.workspace import CentralWorkspace
from gwt_engine.specialists import (
    PerceptionSpecialist,
    MemorySpecialist,
    PlanningSpecialist,
    MetacognitionSpecialist,
)

logger = logging.getLogger(__name__)


class GWTState(TypedDict):
    """State object for GWT workflow"""

    messages: List[WorkspaceMessage]
    specialist_responses: Dict[str, SpecialistResponse]
    workspace_broadcast: WorkspaceMessage | None
    consciousness_state: ConsciousnessState | None
    iteration: int
    active_specialists: List[str]


class GWTWorkflow:
    """
    LangGraph workflow orchestrating GWT consciousness simulation

    Workflow:
    1. Input → Perception Specialist
    2. Route to relevant specialists (Memory, Planning, Metacognition)
    3. Collect specialist responses
    4. Central Workspace integration
    5. Broadcast to all specialists
    6. Update consciousness state
    """

    def __init__(
        self,
        central_workspace: CentralWorkspace,
        perception: PerceptionSpecialist,
        memory: MemorySpecialist,
        planning: PlanningSpecialist,
        metacognition: MetacognitionSpecialist,
    ):
        self.central_workspace = central_workspace
        self.specialists = {
            "perception": perception,
            "memory": memory,
            "planning": planning,
            "metacognition": metacognition,
        }

        self.graph = self._build_graph()
        self.compiled_graph = None

    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow"""

        workflow = StateGraph(GWTState)

        # Define nodes
        workflow.add_node("perception", self._perception_node)
        workflow.add_node("route_specialists", self._routing_node)
        workflow.add_node("memory", self._memory_node)
        workflow.add_node("planning", self._planning_node)
        workflow.add_node("metacognition", self._metacognition_node)
        workflow.add_node("integrate", self._integration_node)
        workflow.add_node("broadcast", self._broadcast_node)
        workflow.add_node("update_state", self._state_update_node)

        # Define edges
        workflow.set_entry_point("perception")
        workflow.add_edge("perception", "route_specialists")

        # Conditional routing to specialists
        workflow.add_conditional_edges(
            "route_specialists",
            self._should_route_to_specialists,
            {
                "memory": "memory",
                "planning": "planning",
                "metacognition": "metacognition",
                "integrate": "integrate",
            },
        )

        # All specialists flow to integration
        workflow.add_edge("memory", "integrate")
        workflow.add_edge("planning", "integrate")
        workflow.add_edge("metacognition", "integrate")

        # Integration → Broadcast → State Update → End
        workflow.add_edge("integrate", "broadcast")
        workflow.add_edge("broadcast", "update_state")
        workflow.add_edge("update_state", END)

        return workflow

    async def _perception_node(self, state: GWTState) -> GWTState:
        """Process input through perception specialist"""
        logger.debug("Perception node processing...")

        input_message = state["messages"][-1] if state["messages"] else None
        if not input_message:
            return state

        perception_response = await self.specialists["perception"].process_with_timing(
            input_message
        )

        state["specialist_responses"]["perception"] = perception_response
        state["active_specialists"].append("perception")

        return state

    async def _routing_node(self, state: GWTState) -> GWTState:
        """Determine which specialists should process this input"""
        logger.debug("Routing node determining specialist activation...")

        # Analyze perception output to determine routing
        perception_response = state["specialist_responses"].get("perception")

        if not perception_response:
            return state

        # Simple routing logic (can be made more sophisticated)
        content = perception_response.content.lower()

        # Route to specialists based on content
        if any(
            word in content
            for word in ["remember", "recall", "memory", "past", "history"]
        ):
            state["active_specialists"].append("memory")

        if any(
            word in content
            for word in [
                "plan",
                "decide",
                "should",
                "action",
                "next",
                "how to",
            ]
        ):
            state["active_specialists"].append("planning")

        if any(
            word in content
            for word in [
                "think",
                "aware",
                "conscious",
                "feel",
                "experience",
                "introspect",
            ]
        ):
            state["active_specialists"].append("metacognition")

        logger.debug(f"Routed to specialists: {state['active_specialists']}")

        return state

    def _should_route_to_specialists(self, state: GWTState) -> str:
        """Conditional edge function for specialist routing"""
        active = state["active_specialists"]

        # Route to first unprocessed specialist
        for specialist in ["memory", "planning", "metacognition"]:
            if (
                specialist in active
                and specialist not in state["specialist_responses"]
            ):
                return specialist

        # All specialists processed, go to integration
        return "integrate"

    async def _memory_node(self, state: GWTState) -> GWTState:
        """Process through memory specialist"""
        logger.debug("Memory node processing...")

        input_message = state["messages"][-1]
        memory_response = await self.specialists["memory"].process_with_timing(
            input_message
        )

        state["specialist_responses"]["memory"] = memory_response

        return state

    async def _planning_node(self, state: GWTState) -> GWTState:
        """Process through planning specialist"""
        logger.debug("Planning node processing...")

        input_message = state["messages"][-1]
        planning_response = await self.specialists["planning"].process_with_timing(
            input_message
        )

        state["specialist_responses"]["planning"] = planning_response

        return state

    async def _metacognition_node(self, state: GWTState) -> GWTState:
        """Process through metacognition specialist"""
        logger.debug("Metacognition node processing...")

        input_message = state["messages"][-1]
        metacog_response = await self.specialists["metacognition"].process_with_timing(
            input_message
        )

        state["specialist_responses"]["metacognition"] = metacog_response

        return state

    async def _integration_node(self, state: GWTState) -> GWTState:
        """Integrate specialist responses in central workspace"""
        logger.debug("Integration node - central workspace processing...")

        # Send all specialist responses to central workspace
        for response in state["specialist_responses"].values():
            await self.central_workspace.receive_specialist_input(response)

        # Perform integration and get broadcast
        broadcast = await self.central_workspace.integrate_and_broadcast()
        state["workspace_broadcast"] = broadcast

        return state

    async def _broadcast_node(self, state: GWTState) -> GWTState:
        """Broadcast workspace output to all specialists"""
        logger.debug("Broadcasting workspace output to specialists...")

        broadcast = state["workspace_broadcast"]
        if not broadcast:
            return state

        # Send broadcast to all specialists (they update their contexts)
        for specialist_name, specialist in self.specialists.items():
            if hasattr(specialist, "process_workspace_broadcast"):
                await specialist.process_workspace_broadcast(broadcast)

        return state

    async def _state_update_node(self, state: GWTState) -> GWTState:
        """Update consciousness state"""
        logger.debug("Updating consciousness state...")

        consciousness_state = await self.central_workspace.get_consciousness_state()
        state["consciousness_state"] = consciousness_state
        state["iteration"] += 1

        logger.info(
            f"Iteration {state['iteration']} complete. "
            f"Consciousness level: {consciousness_state.consciousness_level:.2f}"
        )

        return state

    async def compile(self):
        """Compile the workflow graph"""
        if self.compiled_graph is None:
            self.compiled_graph = self.graph.compile()
        return self.compiled_graph

    async def process_input(
        self, input_content: str, message_type: MessageType = MessageType.PERCEPTION
    ) -> ConsciousnessState:
        """
        Process input through the GWT workflow

        Args:
            input_content: Input text to process
            message_type: Type of message

        Returns:
            ConsciousnessState after processing
        """
        if self.compiled_graph is None:
            await self.compile()

        # Create input message
        input_message = WorkspaceMessage(
            type=message_type,
            content=input_content,
            priority=7,
        )

        # Initialize state
        initial_state: GWTState = {
            "messages": [input_message],
            "specialist_responses": {},
            "workspace_broadcast": None,
            "consciousness_state": None,
            "iteration": 0,
            "active_specialists": [],
        }

        # Run workflow
        try:
            final_state = await self.compiled_graph.ainvoke(initial_state)
            return final_state["consciousness_state"]

        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            raise

    async def process_batch(
        self, inputs: List[str]
    ) -> List[ConsciousnessState]:
        """Process multiple inputs sequentially"""
        results = []

        for input_content in inputs:
            state = await self.process_input(input_content)
            results.append(state)

        return results

    def get_workflow_metrics(self) -> Dict[str, Any]:
        """Get metrics from all components"""
        return {
            "workspace": self.central_workspace.get_metrics(),
            "specialists": {
                name: specialist.get_metrics()
                for name, specialist in self.specialists.items()
            },
        }
