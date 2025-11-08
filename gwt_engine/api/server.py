"""
FastAPI server for GWT Engine

Provides REST API for consciousness simulation interaction
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from gwt_engine.core.types import (
    WorkspaceMessage,
    MessageType,
    ConsciousnessState,
)
from gwt_engine.core.workspace import CentralWorkspace
from gwt_engine.inference.ollama_client import OllamaClientPool
from gwt_engine.specialists import (
    PerceptionSpecialist,
    MemorySpecialist,
    PlanningSpecialist,
    MetacognitionSpecialist,
)
from gwt_engine.orchestration.gwt_graph import GWTWorkflow
# Ray workers optional (not available on Windows Python 3.14)
try:
    from gwt_engine.orchestration.ray_workers import WorkerPool
except ImportError:
    WorkerPool = None
from gwt_engine.config.loader import get_system_config

# Multi-Theory Consciousness Framework
from gwt_engine.theories.multi_theory_orchestrator import MultiTheoryOrchestrator

logger = logging.getLogger(__name__)


# Request/Response Models
class ProcessRequest(BaseModel):
    """Request to process input through GWT"""

    content: str = Field(..., description="Input content to process")
    message_type: str = Field(
        default="perception", description="Type of message (perception, memory_query, etc.)"
    )
    priority: int = Field(default=5, ge=1, le=10, description="Priority (1-10)")


class ProcessResponse(BaseModel):
    """Response from GWT processing"""

    workspace_broadcast: str
    consciousness_level: float
    integration_coherence: float
    active_specialists: List[str]
    processing_time_ms: float


class ConsciousnessProbeResponse(BaseModel):
    """Response from consciousness probe"""

    introspection: str
    consciousness_level: float
    integration_coherence: float
    workspace_content_count: int


class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    vllm_servers: Dict[str, bool]
    worker_count: int
    uptime_seconds: float


class MetricsResponse(BaseModel):
    """System metrics response"""

    workspace_metrics: Dict[str, Any]
    specialist_metrics: Dict[str, Any]
    worker_pool_metrics: Optional[Dict[str, Any]] = None


# Global state
app_state = {
    "vllm_pool": None,
    "central_workspace": None,
    "specialists": {},
    "workflow": None,
    "worker_pool": None,
    "multi_theory_orchestrator": None,  # NEW: Multi-theory framework
    "start_time": None,
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    import time

    logger.info("Starting GWT Engine...")
    app_state["start_time"] = time.time()

    # Initialize Ollama client pool
    app_state["vllm_pool"] = OllamaClientPool()
    await app_state["vllm_pool"].initialize()
    logger.info("Ollama client pool initialized")

    # Initialize Central Workspace
    workspace_client = app_state["vllm_pool"].get_client("central_workspace")
    app_state["central_workspace"] = CentralWorkspace(workspace_client)
    logger.info("Central Workspace initialized")

    # Initialize Specialists
    app_state["specialists"] = {
        "perception": PerceptionSpecialist(
            app_state["vllm_pool"].get_client("perception")
        ),
        "memory": MemorySpecialist(
            app_state["vllm_pool"].get_client("memory")
        ),
        "planning": PlanningSpecialist(
            app_state["vllm_pool"].get_client("planning")
        ),
        "metacognition": MetacognitionSpecialist(
            app_state["vllm_pool"].get_client("metacognition")
        ),
    }
    logger.info("Specialist modules initialized")

    # Initialize LangGraph workflow
    app_state["workflow"] = GWTWorkflow(
        central_workspace=app_state["central_workspace"],
        perception=app_state["specialists"]["perception"],
        memory=app_state["specialists"]["memory"],
        planning=app_state["specialists"]["planning"],
        metacognition=app_state["specialists"]["metacognition"],
    )
    await app_state["workflow"].compile()
    logger.info("LangGraph workflow compiled")

    # Initialize Multi-Theory Orchestrator
    app_state["multi_theory_orchestrator"] = MultiTheoryOrchestrator(
        central_workspace=app_state["central_workspace"],
        specialists=app_state["specialists"],
        ollama_pool=app_state["vllm_pool"],
    )
    logger.info("Multi-Theory Orchestrator initialized - 8 consciousness theories active!")

    # Initialize Ray worker pool (optional, for high-throughput mode)
    # app_state["worker_pool"] = WorkerPool()
    # await app_state["worker_pool"].initialize()
    # logger.info("Ray worker pool initialized")

    logger.info("GWT Engine ready with Multi-Theory Consciousness Framework!")

    yield

    # Cleanup
    logger.info("Shutting down GWT Engine...")
    await app_state["vllm_pool"].close_all()

    if app_state["worker_pool"]:
        await app_state["worker_pool"].shutdown()

    logger.info("GWT Engine shutdown complete")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""

    app = FastAPI(
        title="GWT Consciousness Engine",
        description="Global Workspace Theory consciousness simulation API",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS middleware
    config = get_system_config()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config["api"]["cors_origins"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "name": "GWT Consciousness Engine",
            "version": "0.1.0",
            "status": "operational",
        }

    @app.get("/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint"""
        import time

        # Check vLLM servers
        vllm_health = await app_state["vllm_pool"].health_check_all()

        uptime = time.time() - app_state["start_time"]

        return HealthResponse(
            status="healthy" if all(vllm_health.values()) else "degraded",
            vllm_servers=vllm_health,  # Already strings from Ollama client
            worker_count=app_state["worker_pool"].worker_count
            if app_state["worker_pool"]
            else 0,
            uptime_seconds=uptime,
        )

    @app.post("/process", response_model=ProcessResponse)
    async def process_input(request: ProcessRequest):
        """
        Process input through GWT consciousness simulation

        This is the main endpoint for interacting with the consciousness engine
        """
        import time

        start_time = time.time()

        try:
            # Map string to MessageType enum
            message_type_map = {
                "perception": MessageType.PERCEPTION,
                "memory_query": MessageType.MEMORY_QUERY,
                "planning_request": MessageType.PLANNING_REQUEST,
                "metacognition_probe": MessageType.METACOGNITION_PROBE,
                "consciousness_probe": MessageType.CONSCIOUSNESS_PROBE,
            }

            message_type = message_type_map.get(
                request.message_type, MessageType.PERCEPTION
            )

            # Process through workflow
            consciousness_state = await app_state["workflow"].process_input(
                request.content, message_type
            )

            processing_time = (time.time() - start_time) * 1000

            # Get workspace broadcast
            workspace_broadcast = (
                consciousness_state.workspace_content[-1].content
                if consciousness_state.workspace_content
                else ""
            )

            return ProcessResponse(
                workspace_broadcast=workspace_broadcast,
                consciousness_level=consciousness_state.consciousness_level,
                integration_coherence=consciousness_state.integration_coherence,
                active_specialists=[
                    role.value for role in consciousness_state.active_specialists
                ],
                processing_time_ms=processing_time,
            )

        except Exception as e:
            logger.error(f"Processing failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/process/multi-theory")
    async def process_multi_theory(request: ProcessRequest):
        """
        Process input through ALL 8 consciousness theories
        
        Returns unified consciousness score (0-100) plus individual theory metrics:
        - GWT: Integration & broadcasting
        - IIT: Φ (integrated information)
        - Predictive Processing: Precision & free energy
        - Attention Schema Theory: Self-model accuracy
        - Higher-Order Thought: Meta-representation
        - LIDA: Cognitive cycle timing
        - CLARION: Implicit/explicit rule extraction
        """
        import time
        
        start_time = time.time()
        
        try:
            # Process through multi-theory orchestrator
            result = await app_state["multi_theory_orchestrator"].process_with_all_theories(
                request.content
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            # Extract theory metrics
            theories = result.get("theories", {})
            outputs = result.get("outputs", {})
            
            # Interpret score
            score = result.get("consciousness_score", 0)
            if score < 20:
                level = "unconscious"
            elif score < 40:
                level = "minimal"
            elif score < 70:
                level = "moderate"
            else:
                level = "high"
            
            return {
                "consciousness_score": score,  # 0-100
                "consciousness_level": level,
                "processing_time_ms": processing_time,
                "theories": {
                    "gwt": theories.get("gwt", {}),
                    "iit": theories.get("iit", {}),
                    "predictive": theories.get("predictive_processing", {}),
                    "attention_schema": theories.get("attention_schema", {}),
                    "higher_order_thought": theories.get("higher_order_thought", {}),
                    "lida": theories.get("lida", {}),
                    "clarion": theories.get("clarion", {}),
                },
                "outputs": {
                    "workspace_broadcast": outputs.get("workspace_broadcast", ""),
                    "prediction": outputs.get("prediction", ""),
                    "attention_schema": outputs.get("attention_schema", ""),
                    "higher_order_thought": outputs.get("higher_order_thought", ""),
                },
                "interpretation": {
                    "0-20": "Unconscious",
                    "20-40": "Minimal consciousness",
                    "40-70": "Moderate consciousness (animal-level)",
                    "70-100": "High consciousness (human-level)",
                }
            }
            
        except Exception as e:
            logger.error(f"Multi-theory processing failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/consciousness/probe", response_model=ConsciousnessProbeResponse)
    async def probe_consciousness():
        """
        Probe current consciousness state

        Returns introspective reflection on current state
        """
        try:
            # Get current consciousness state
            consciousness_state = (
                await app_state["central_workspace"].get_consciousness_state()
            )

            # Generate metacognitive probe
            metacog_specialist = app_state["specialists"]["metacognition"]
            probe_response = await metacog_specialist.probe_consciousness(
                consciousness_state
            )

            return ConsciousnessProbeResponse(
                introspection=probe_response.content,
                consciousness_level=consciousness_state.consciousness_level,
                integration_coherence=consciousness_state.integration_coherence,
                workspace_content_count=len(consciousness_state.workspace_content),
            )

        except Exception as e:
            logger.error(f"Consciousness probe failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/consciousness/state")
    async def get_consciousness_state():
        """Get current consciousness state (detailed)"""
        try:
            state = await app_state["central_workspace"].get_consciousness_state()
            return state.to_dict()

        except Exception as e:
            logger.error(f"Failed to get consciousness state: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/metrics", response_model=MetricsResponse)
    async def get_metrics():
        """Get system metrics"""
        try:
            workflow_metrics = app_state["workflow"].get_workflow_metrics()

            worker_metrics = None
            if app_state["worker_pool"]:
                worker_metrics = await app_state["worker_pool"].get_all_metrics()

            return MetricsResponse(
                workspace_metrics=workflow_metrics["workspace"],
                specialist_metrics=workflow_metrics["specialists"],
                worker_pool_metrics=worker_metrics,
            )

        except Exception as e:
            logger.error(f"Failed to get metrics: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/specialists/{specialist_name}/process")
    async def process_specialist(specialist_name: str, request: ProcessRequest):
        """Process input through a specific specialist directly"""
        if specialist_name not in app_state["specialists"]:
            raise HTTPException(status_code=404, detail="Specialist not found")

        try:
            specialist = app_state["specialists"][specialist_name]

            message = WorkspaceMessage(
                content=request.content,
                type=MessageType.PERCEPTION,
                priority=request.priority,
            )

            response = await specialist.process_with_timing(message)

            return {
                "content": response.content,
                "confidence": response.confidence,
                "processing_time_ms": response.processing_time_ms,
                "tokens_generated": response.tokens_generated,
            }

        except Exception as e:
            logger.error(f"Specialist processing failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    return app


def main():
    """Main entry point for running the server"""
    import uvicorn

    config = get_system_config()
    api_config = config["api"]

    uvicorn.run(
        "gwt_engine.api.server:create_app",
        factory=True,
        host=api_config["host"],
        port=api_config["port"],
        reload=api_config["reload"],
        log_level=api_config["log_level"],
    )


if __name__ == "__main__":
    main()
