"""
Ray distributed worker pool for parallel specialist processing

Enables 10-14 concurrent specialist workers across GPUs
"""

import asyncio
import logging
from typing import Dict, Any, List
import ray
from ray.util.queue import Queue

from gwt_engine.core.types import (
    WorkspaceMessage,
    SpecialistResponse,
    SpecialistRole,
)
from gwt_engine.inference.vllm_client import VLLMClient
from gwt_engine.specialists import (
    PerceptionSpecialist,
    MemorySpecialist,
    PlanningSpecialist,
    MetacognitionSpecialist,
)
from gwt_engine.config.loader import get_models_config

logger = logging.getLogger(__name__)


@ray.remote
class SpecialistWorker:
    """
    Ray actor for specialist module processing

    Each worker runs independently and can process requests concurrently
    """

    def __init__(
        self,
        specialist_type: str,
        worker_id: int,
        vllm_base_url: str,
        model_name: str,
    ):
        self.specialist_type = specialist_type
        self.worker_id = worker_id

        # Initialize vLLM client
        role_mapping = {
            "perception": SpecialistRole.PERCEPTION,
            "memory": SpecialistRole.MEMORY,
            "planning": SpecialistRole.PLANNING,
            "metacognition": SpecialistRole.METACOGNITION,
        }

        self.role = role_mapping[specialist_type]
        self.vllm_client = VLLMClient(
            base_url=vllm_base_url, model_name=model_name, role=self.role
        )

        # Initialize specialist
        specialist_classes = {
            "perception": PerceptionSpecialist,
            "memory": MemorySpecialist,
            "planning": PlanningSpecialist,
            "metacognition": MetacognitionSpecialist,
        }

        self.specialist = specialist_classes[specialist_type](self.vllm_client)

        logger.info(
            f"Worker {specialist_type}-{worker_id} initialized on {vllm_base_url}"
        )

    async def process(
        self, message_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a message and return specialist response"""
        try:
            message = WorkspaceMessage.from_dict(message_dict)
            response = await self.specialist.process_with_timing(message)

            return {
                "message_id": response.message_id,
                "role": response.role.value,
                "content": response.content,
                "confidence": response.confidence,
                "processing_time_ms": response.processing_time_ms,
                "tokens_generated": response.tokens_generated,
                "metadata": response.metadata,
                "worker_id": self.worker_id,
            }

        except Exception as e:
            logger.error(
                f"Worker {self.specialist_type}-{self.worker_id} failed: {e}"
            )
            raise

    def get_metrics(self) -> Dict[str, Any]:
        """Get worker metrics"""
        return {
            "specialist_type": self.specialist_type,
            "worker_id": self.worker_id,
            **self.specialist.get_metrics(),
        }


class WorkerPool:
    """
    Manages pool of Ray workers for parallel specialist processing

    Distributes work across multiple GPU-backed workers for maximum throughput
    """

    def __init__(self):
        self.workers: Dict[str, List[ray.ObjectRef]] = {
            "perception": [],
            "memory": [],
            "planning": [],
            "metacognition": [],
        }
        self.worker_count = 0
        self.round_robin_indices: Dict[str, int] = {
            "perception": 0,
            "memory": 0,
            "planning": 0,
            "metacognition": 0,
        }

    async def initialize(self):
        """Initialize Ray and create worker pool"""

        # Initialize Ray
        if not ray.is_initialized():
            ray.init(
                namespace="gwt_engine",
                dashboard_host="0.0.0.0",
                dashboard_port=8265,
                num_cpus=32,
                num_gpus=2,
            )

        config = get_models_config()
        vllm_instances = config["vllm_instances"]

        # Worker configuration based on models.yaml
        worker_configs = [
            # Perception workers (GPU 1)
            {
                "type": "perception",
                "count": 3,
                "url": f"http://localhost:{vllm_instances['gpu1_specialists_server']['port']}",
                "model": "mistral-small-22b",
            },
            # Memory workers (GPU 2)
            {
                "type": "memory",
                "count": 3,
                "url": f"http://localhost:{vllm_instances['gpu2_specialists_server']['port']}",
                "model": "qwen-2.5-coder-32b",
            },
            # Planning workers (GPU 2)
            {
                "type": "planning",
                "count": 6,
                "url": f"http://localhost:{vllm_instances['gpu2_specialists_server']['port']}",
                "model": "llama-3.1-8b",
            },
            # Metacognition workers (GPU 2)
            {
                "type": "metacognition",
                "count": 4,
                "url": f"http://localhost:{vllm_instances['gpu2_specialists_server']['port']}",
                "model": "gemma-2-9b",
            },
        ]

        # Create workers
        for worker_config in worker_configs:
            specialist_type = worker_config["type"]
            count = worker_config["count"]
            url = worker_config["url"]
            model = worker_config["model"]

            for i in range(count):
                worker = SpecialistWorker.remote(
                    specialist_type=specialist_type,
                    worker_id=i,
                    vllm_base_url=url,
                    model_name=model,
                )
                self.workers[specialist_type].append(worker)
                self.worker_count += 1

        logger.info(
            f"WorkerPool initialized with {self.worker_count} total workers: "
            f"{len(self.workers['perception'])} perception, "
            f"{len(self.workers['memory'])} memory, "
            f"{len(self.workers['planning'])} planning, "
            f"{len(self.workers['metacognition'])} metacognition"
        )

    async def submit_task(
        self, specialist_type: str, message: WorkspaceMessage
    ) -> ray.ObjectRef:
        """
        Submit task to a worker using round-robin load balancing

        Args:
            specialist_type: Type of specialist (perception, memory, planning, metacognition)
            message: Message to process

        Returns:
            Ray ObjectRef for the result
        """
        if specialist_type not in self.workers:
            raise ValueError(f"Unknown specialist type: {specialist_type}")

        workers = self.workers[specialist_type]
        if not workers:
            raise RuntimeError(f"No workers available for {specialist_type}")

        # Round-robin worker selection
        idx = self.round_robin_indices[specialist_type]
        worker = workers[idx]
        self.round_robin_indices[specialist_type] = (idx + 1) % len(workers)

        # Submit task
        result_ref = worker.process.remote(message.to_dict())

        logger.debug(f"Task submitted to {specialist_type} worker {idx}")

        return result_ref

    async def process_parallel(
        self, tasks: List[tuple[str, WorkspaceMessage]]
    ) -> List[SpecialistResponse]:
        """
        Process multiple tasks in parallel

        Args:
            tasks: List of (specialist_type, message) tuples

        Returns:
            List of SpecialistResponse objects
        """
        # Submit all tasks
        task_refs = []
        for specialist_type, message in tasks:
            ref = await self.submit_task(specialist_type, message)
            task_refs.append(ref)

        # Wait for all results
        results = await asyncio.gather(*[ref for ref in task_refs])

        # Convert to SpecialistResponse objects
        responses = []
        for result_dict in results:
            response = SpecialistResponse(
                message_id=result_dict["message_id"],
                role=SpecialistRole(result_dict["role"]),
                content=result_dict["content"],
                confidence=result_dict["confidence"],
                processing_time_ms=result_dict["processing_time_ms"],
                tokens_generated=result_dict["tokens_generated"],
                metadata=result_dict["metadata"],
            )
            responses.append(response)

        return responses

    async def get_all_metrics(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get metrics from all workers"""
        metrics = {
            "perception": [],
            "memory": [],
            "planning": [],
            "metacognition": [],
        }

        for specialist_type, workers in self.workers.items():
            worker_metrics = ray.get([worker.get_metrics.remote() for worker in workers])
            metrics[specialist_type] = worker_metrics

        return metrics

    async def shutdown(self):
        """Shutdown worker pool and Ray"""
        logger.info("Shutting down worker pool...")
        if ray.is_initialized():
            ray.shutdown()
        logger.info("Worker pool shutdown complete")


class RedisMessageQueue:
    """
    Redis-based message queue for inter-worker communication

    Enables asynchronous message passing between specialists and workspace
    """

    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379):
        import redis.asyncio as aioredis

        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_client = None
        self.pubsub = None

    async def connect(self):
        """Connect to Redis"""
        import redis.asyncio as aioredis

        self.redis_client = aioredis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            decode_responses=True,
        )

        self.pubsub = self.redis_client.pubsub()

        logger.info(f"Connected to Redis at {self.redis_host}:{self.redis_port}")

    async def publish(self, channel: str, message: Dict[str, Any]):
        """Publish message to channel"""
        import json

        if not self.redis_client:
            raise RuntimeError("Redis client not connected")

        await self.redis_client.publish(channel, json.dumps(message))

        logger.debug(f"Published to {channel}: {str(message)[:100]}...")

    async def subscribe(self, channels: List[str]):
        """Subscribe to channels"""
        if not self.pubsub:
            raise RuntimeError("Redis pubsub not initialized")

        await self.pubsub.subscribe(*channels)

        logger.info(f"Subscribed to channels: {channels}")

    async def listen(self):
        """Listen for messages (async generator)"""
        if not self.pubsub:
            raise RuntimeError("Redis pubsub not initialized")

        async for message in self.pubsub.listen():
            if message["type"] == "message":
                import json

                yield json.loads(message["data"])

    async def close(self):
        """Close Redis connection"""
        if self.pubsub:
            await self.pubsub.close()
        if self.redis_client:
            await self.redis_client.close()

        logger.info("Redis connection closed")
