"""Core data types for GWT Engine"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid


class MessageType(str, Enum):
    """Types of messages in the GWT system"""

    PERCEPTION = "perception"
    MEMORY_QUERY = "memory_query"
    MEMORY_RESPONSE = "memory_response"
    PLANNING_REQUEST = "planning_request"
    PLANNING_RESPONSE = "planning_response"
    METACOGNITION_PROBE = "metacognition_probe"
    METACOGNITION_RESPONSE = "metacognition_response"
    WORKSPACE_BROADCAST = "workspace_broadcast"
    CONSCIOUSNESS_PROBE = "consciousness_probe"
    SYSTEM_EVENT = "system_event"


class SpecialistRole(str, Enum):
    """Roles of specialist modules in GWT architecture"""

    CENTRAL_WORKSPACE = "central_global_workspace"
    PERCEPTION = "perception_specialist"
    MEMORY = "memory_retrieval_specialist"
    PLANNING = "planning_reasoning_specialist"
    METACOGNITION = "metacognition_introspection_specialist"


@dataclass
class WorkspaceMessage:
    """Message structure for inter-module communication"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType = MessageType.SYSTEM_EVENT
    content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    source: Optional[SpecialistRole] = None
    target: Optional[SpecialistRole] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    confidence: float = 1.0
    priority: int = 5  # 1-10, higher is more urgent
    context: List[str] = field(default_factory=list)  # Previous message IDs
    requires_integration: bool = True  # Should go through central workspace

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "type": self.type.value,
            "content": self.content,
            "metadata": self.metadata,
            "source": self.source.value if self.source else None,
            "target": self.target.value if self.target else None,
            "timestamp": self.timestamp.isoformat(),
            "confidence": self.confidence,
            "priority": self.priority,
            "context": self.context,
            "requires_integration": self.requires_integration,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkspaceMessage":
        """Create from dictionary"""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            type=MessageType(data["type"]),
            content=data["content"],
            metadata=data.get("metadata", {}),
            source=SpecialistRole(data["source"]) if data.get("source") else None,
            target=SpecialistRole(data["target"]) if data.get("target") else None,
            timestamp=datetime.fromisoformat(data["timestamp"])
            if "timestamp" in data
            else datetime.utcnow(),
            confidence=data.get("confidence", 1.0),
            priority=data.get("priority", 5),
            context=data.get("context", []),
            requires_integration=data.get("requires_integration", True),
        )


@dataclass
class SpecialistResponse:
    """Response from a specialist module"""

    message_id: str  # ID of the message being responded to
    role: SpecialistRole
    content: str
    confidence: float
    processing_time_ms: float
    tokens_generated: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_workspace_message(
        self, target: Optional[SpecialistRole] = None
    ) -> WorkspaceMessage:
        """Convert to WorkspaceMessage for routing"""
        return WorkspaceMessage(
            type=MessageType.WORKSPACE_BROADCAST
            if target is None
            else MessageType.SYSTEM_EVENT,
            content=self.content,
            source=self.role,
            target=target,
            confidence=self.confidence,
            metadata={
                **self.metadata,
                "processing_time_ms": self.processing_time_ms,
                "tokens_generated": self.tokens_generated,
            },
            context=[self.message_id],
        )


@dataclass
class ConsciousnessState:
    """Represents the current state of the GWT consciousness system"""

    timestamp: datetime = field(default_factory=datetime.utcnow)
    workspace_content: List[WorkspaceMessage] = field(default_factory=list)
    active_specialists: List[SpecialistRole] = field(default_factory=list)
    working_memory: Dict[str, Any] = field(default_factory=dict)
    attention_focus: Optional[str] = None  # Current focus of attention
    integration_coherence: float = 0.0  # 0-1, measure of thought integration
    consciousness_level: float = 0.0  # 0-1, measure of "awareness"
    recent_broadcasts: List[str] = field(default_factory=list)  # Recent message IDs

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "workspace_content": [msg.to_dict() for msg in self.workspace_content],
            "active_specialists": [role.value for role in self.active_specialists],
            "working_memory": self.working_memory,
            "attention_focus": self.attention_focus,
            "integration_coherence": self.integration_coherence,
            "consciousness_level": self.consciousness_level,
            "recent_broadcasts": self.recent_broadcasts,
        }


@dataclass
class ModelMetrics:
    """Performance metrics for a model instance"""

    model_name: str
    role: SpecialistRole
    tokens_per_second: float
    requests_processed: int
    average_latency_ms: float
    p99_latency_ms: float
    gpu_utilization: float
    vram_used_gb: float
    error_count: int
    last_updated: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "model_name": self.model_name,
            "role": self.role.value,
            "tokens_per_second": self.tokens_per_second,
            "requests_processed": self.requests_processed,
            "average_latency_ms": self.average_latency_ms,
            "p99_latency_ms": self.p99_latency_ms,
            "gpu_utilization": self.gpu_utilization,
            "vram_used_gb": self.vram_used_gb,
            "error_count": self.error_count,
            "last_updated": self.last_updated.isoformat(),
        }
