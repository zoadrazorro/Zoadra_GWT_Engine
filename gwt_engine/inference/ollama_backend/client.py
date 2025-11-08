"""
Ollama client for multi-instance consciousness simulation

Uses multiple Ollama instances (one per GPU) to maximize parallelism
despite Ollama's lower per-instance throughput vs vLLM.
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
import httpx
from dataclasses import dataclass
import logging

from gwt_engine.core.types import SpecialistRole
from gwt_engine.config.loader import get_models_config

logger = logging.getLogger(__name__)


@dataclass
class OllamaGenerationRequest:
    """Request for Ollama text generation"""

    prompt: str
    model: str
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    stop: Optional[List[str]] = None
    stream: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "prompt": self.prompt,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "stop": self.stop,
            "stream": self.stream,
        }


@dataclass
class OllamaGenerationResponse:
    """Response from Ollama generation"""

    text: str
    tokens_generated: int
    finish_reason: str
    latency_ms: float
    tokens_per_second: float
    model: str


class OllamaClient:
    """
    Client for communicating with Ollama servers

    Supports multiple Ollama instances running on different GPUs
    """

    def __init__(
        self,
        base_url: str,
        model_name: str,
        role: SpecialistRole,
        timeout: float = 1800.0,  # 30 minutes for large models
    ):
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name
        self.role = role
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)

        logger.info(f"OllamaClient initialized: {role.value} at {base_url}")

    async def generate(self, request: OllamaGenerationRequest) -> OllamaGenerationResponse:
        """Generate text using Ollama API"""
        start_time = time.time()

        payload = {
            "model": request.model,
            "prompt": request.prompt,
            "stream": request.stream,
            "options": {
                "num_predict": request.max_tokens,
                "temperature": request.temperature,
                "top_p": request.top_p,
                "top_k": request.top_k,
            },
        }

        if request.stop:
            payload["options"]["stop"] = request.stop

        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate", json=payload
            )
            response.raise_for_status()
            result = response.json()

            latency_ms = (time.time() - start_time) * 1000

            # Ollama response format
            text = result.get("response", "")
            tokens_generated = result.get("eval_count", len(text.split()))
            tokens_per_second = (
                tokens_generated / (latency_ms / 1000) if latency_ms > 0 else 0
            )

            return OllamaGenerationResponse(
                text=text,
                tokens_generated=tokens_generated,
                finish_reason=result.get("done_reason", "stop"),
                latency_ms=latency_ms,
                tokens_per_second=tokens_per_second,
                model=self.model_name,
            )

        except httpx.HTTPError as e:
            logger.error(f"Ollama HTTP error for {self.role.value}: {e}")
            raise RuntimeError(f"Ollama request failed: {e}")
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            raise RuntimeError(f"Ollama generation failed: {e}")

    async def generate_chat(
        self, messages: List[Dict[str, str]], request: OllamaGenerationRequest
    ) -> OllamaGenerationResponse:
        """Generate using Ollama chat endpoint"""
        start_time = time.time()

        payload = {
            "model": request.model,
            "messages": messages,
            "stream": request.stream,
            "options": {
                "num_predict": request.max_tokens,
                "temperature": request.temperature,
                "top_p": request.top_p,
                "top_k": request.top_k,
            },
        }

        try:
            response = await self.client.post(
                f"{self.base_url}/api/chat", json=payload
            )
            response.raise_for_status()
            result = response.json()

            latency_ms = (time.time() - start_time) * 1000

            text = result.get("message", {}).get("content", "")
            tokens_generated = result.get("eval_count", len(text.split()))
            tokens_per_second = (
                tokens_generated / (latency_ms / 1000) if latency_ms > 0 else 0
            )

            return OllamaGenerationResponse(
                text=text,
                tokens_generated=tokens_generated,
                finish_reason=result.get("done_reason", "stop"),
                latency_ms=latency_ms,
                tokens_per_second=tokens_per_second,
                model=self.model_name,
            )

        except httpx.HTTPError as e:
            logger.error(f"Ollama chat request failed for {self.role.value}: {e}")
            raise RuntimeError(f"Ollama chat request failed: {e}")

    async def health_check(self) -> bool:
        """Check if Ollama server is healthy"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


class OllamaClientPool:
    """
    Pool of Ollama clients for different specialist roles

    Supports multi-instance Ollama deployment (one per GPU)
    """

    def __init__(self):
        self.clients: Dict[SpecialistRole, OllamaClient] = {}
        self._initialized = False

    async def initialize(self, instance_ports: Optional[Dict[str, int]] = None):
        """
        Initialize clients based on configuration

        Args:
            instance_ports: Override ports for Ollama instances
                           {"gpu0": 11434, "gpu1": 11435, "gpu2": 11436}
        """
        if self._initialized:
            return

        # Default Ollama instance ports
        if instance_ports is None:
            instance_ports = {
                "central": 11434,  # GPU 0+1 tensor parallel
                "gpu0": 11435,     # GPU 0 specialists
                "gpu1": 11436,     # GPU 1 specialists
            }

        # Map roles to Ollama instances and models
        role_to_config = {
            SpecialistRole.CENTRAL_WORKSPACE: {
                "port": instance_ports["central"],
                "model": "llama3.1:70b-q4_K_M",
            },
            SpecialistRole.PERCEPTION: {
                "port": instance_ports["gpu0"],
                "model": "mistral-small:22b-q5_K_M",
            },
            SpecialistRole.MEMORY: {
                "port": instance_ports["gpu1"],
                "model": "qwen2.5-coder:32b-q4_K_M",
            },
            SpecialistRole.PLANNING: {
                "port": instance_ports["gpu1"],
                "model": "llama3.1:8b-q5_K_M",
            },
            SpecialistRole.METACOGNITION: {
                "port": instance_ports["gpu1"],
                "model": "gemma2:9b-q6_K_M",
            },
        }

        for role, config in role_to_config.items():
            base_url = f"http://localhost:{config['port']}"
            self.clients[role] = OllamaClient(
                base_url=base_url, model_name=config["model"], role=role
            )

        self._initialized = True
        logger.info(f"OllamaClientPool initialized with {len(self.clients)} clients")

    def get_client(self, role: SpecialistRole) -> OllamaClient:
        """Get client for a specific specialist role"""
        if not self._initialized:
            raise RuntimeError("OllamaClientPool not initialized. Call initialize() first.")
        return self.clients[role]

    async def health_check_all(self) -> Dict[SpecialistRole, bool]:
        """Check health of all Ollama instances"""
        results = {}
        for role, client in self.clients.items():
            results[role] = await client.health_check()
        return results

    async def close_all(self):
        """Close all clients"""
        for client in self.clients.values():
            await client.close()
        logger.info("All Ollama clients closed")
