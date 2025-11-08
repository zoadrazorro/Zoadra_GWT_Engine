"""
Planning Specialist - Decision-making and action planning

Model: Llama 3.1 8B (Q5_K_M)
Role: Reasoning, planning, and decision generation
"""

import logging
from typing import Dict, Any, List

from gwt_engine.specialists.base import BaseSpecialist
from gwt_engine.core.types import (
    WorkspaceMessage,
    SpecialistResponse,
    SpecialistRole,
)
from gwt_engine.inference.vllm_client import VLLMClient

logger = logging.getLogger(__name__)


class PlanningSpecialist(BaseSpecialist):
    """
    Planning specialist handles reasoning and action planning

    Responsibilities:
    - Evaluate possible actions and outcomes
    - Generate step-by-step plans
    - Assess consequences and risks
    - Make decisions based on goals and constraints
    """

    def __init__(self, vllm_client: VLLMClient):
        super().__init__(vllm_client, SpecialistRole.PLANNING)
        self.active_goals: List[str] = []
        self.recent_decisions: List[Dict[str, Any]] = []

    async def process(self, message: WorkspaceMessage) -> SpecialistResponse:
        """Process planning requests"""

        context = {
            "request": message.content,
            "active_goals": self.active_goals,
            "recent_decisions": self.recent_decisions[-5:],
        }

        prompt = self._create_specialist_prompt(message, context)
        response_text = await self._generate_response(
            prompt, max_tokens=384, temperature=0.8  # Higher creativity for planning
        )

        confidence = self._calculate_confidence(context)

        # Store decision
        decision = {
            "input": message.content,
            "output": response_text,
            "confidence": confidence,
        }
        self.recent_decisions.append(decision)
        if len(self.recent_decisions) > 20:
            self.recent_decisions.pop(0)

        return SpecialistResponse(
            message_id=message.id,
            role=self.role,
            content=response_text,
            confidence=confidence,
            processing_time_ms=0.0,
            tokens_generated=len(response_text.split()),
            metadata={
                "planning_type": self._classify_planning_type(message),
                "active_goals_count": len(self.active_goals),
            },
        )

    def _create_specialist_prompt(
        self, message: WorkspaceMessage, context: Dict[str, Any]
    ) -> str:
        """Create planning-specific prompt"""

        prompt = """You are the Planning & Reasoning Specialist in a consciousness simulation.

Your role is to generate action plans, evaluate decisions, and reason about consequences.

## Active Goals:
"""
        goals = context.get("active_goals", [])
        if goals:
            for i, goal in enumerate(goals, 1):
                prompt += f"{i}. {goal}\n"
        else:
            prompt += "- [No active goals]\n"

        prompt += "\n## Recent Decisions:\n"
        decisions = context.get("recent_decisions", [])
        if decisions:
            for decision in decisions[-3:]:
                prompt += f"- {decision['output'][:80]}...\n"
        else:
            prompt += "- [No recent decisions]\n"

        prompt += f"""
## Planning Request:
{context.get('request', message.content)}

## Task:
Analyze the request and provide:
1. What are the possible actions or approaches?
2. What are the likely consequences of each?
3. What's the recommended course of action?
4. What steps are needed to execute?

Provide planning response (2-4 sentences):
"""

        return prompt

    def _calculate_confidence(self, context: Dict[str, Any]) -> float:
        """Calculate confidence based on goal clarity"""
        goals_count = len(context.get("active_goals", []))
        decisions_count = len(context.get("recent_decisions", []))

        # Higher confidence with clear goals and experience
        goals_factor = min(goals_count / 5.0, 0.3)
        experience_factor = min(decisions_count / 10.0, 0.3)

        return 0.5 + goals_factor + experience_factor

    def _classify_planning_type(self, message: WorkspaceMessage) -> str:
        """Classify the type of planning request"""
        content_lower = message.content.lower()

        if any(word in content_lower for word in ["how", "steps", "procedure"]):
            return "procedural"
        elif any(word in content_lower for word in ["should", "which", "choose"]):
            return "decision"
        elif any(word in content_lower for word in ["why", "because", "reason"]):
            return "reasoning"
        elif any(word in content_lower for word in ["goal", "achieve", "accomplish"]):
            return "goal_oriented"
        else:
            return "general"

    async def set_goals(self, goals: List[str]):
        """Set active goals for planning context"""
        self.active_goals = goals
        logger.info(f"Planning specialist goals updated: {len(goals)} active goals")

    async def add_goal(self, goal: str):
        """Add a new goal"""
        self.active_goals.append(goal)
        logger.debug(f"Goal added: {goal}")

    async def clear_goals(self):
        """Clear all active goals"""
        self.active_goals.clear()
        logger.debug("All goals cleared")
