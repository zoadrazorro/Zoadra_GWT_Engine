"""vLLM client for interfacing with model servers"""

import asyncio
import time
from typing import Dict, List, Optional, Any
import httpx
from dataclasses import dataclass

from gwt_engine.config.loader import get_model_config, get_models_config
from gwt_engine.core.types import SpecialistRole


@dataclass
class GenerationRequest:
    """Request for text generation"""

    prompt: str
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    stop: Optional[List[str]] = None
    stream: bool = False
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0


@dataclass
class GenerationResponse:
    """Response from text generation"""

    text: str
    tokens_generated: int
    finish_reason: str
    latency_ms: float
    tokens_per_second: float
    model: str


class VLLMClient:
    """Client for communicating with vLLM servers"""

    def __init__(
        self,
        base_url: str,
        model_name: str,
        role: SpecialistRole,
        timeout: float = 300.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name
        self.role = role
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)

        # Load model configuration
        self.config = get_model_config(
            {
                SpecialistRole.CENTRAL_WORKSPACE: "central_workspace",
                SpecialistRole.PERCEPTION: "perception",
                SpecialistRole.MEMORY: "memory",
                SpecialistRole.PLANNING: "planning",
                SpecialistRole.METACOGNITION: "metacognition",
            }[role]
        )

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate text using vLLM server"""
        start_time = time.time()

        payload = {
            "model": self.model_name,
            "prompt": request.prompt,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "top_k": request.top_k,
            "stream": request.stream,
            "presence_penalty": request.presence_penalty,
            "frequency_penalty": request.frequency_penalty,
        }

        if request.stop:
            payload["stop"] = request.stop

        try:
            response = await self.client.post(
                f"{self.base_url}/v1/completions", json=payload
            )
            response.raise_for_status()
            result = response.json()

            latency_ms = (time.time() - start_time) * 1000
            tokens_generated = result["usage"]["completion_tokens"]
            tokens_per_second = (
                tokens_generated / (latency_ms / 1000) if latency_ms > 0 else 0
            )

            return GenerationResponse(
                text=result["choices"][0]["text"],
                tokens_generated=tokens_generated,
                finish_reason=result["choices"][0]["finish_reason"],
                latency_ms=latency_ms,
                tokens_per_second=tokens_per_second,
                model=self.model_name,
            )

        except httpx.HTTPError as e:
            raise RuntimeError(f"vLLM request failed: {e}")

    async def generate_chat(
        self, messages: List[Dict[str, str]], request: GenerationRequest
    ) -> GenerationResponse:
        """Generate using chat completion endpoint"""
        start_time = time.time()

        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "stream": request.stream,
        }

        try:
            response = await self.client.post(
                f"{self.base_url}/v1/chat/completions", json=payload
            )
            response.raise_for_status()
            result = response.json()

            latency_ms = (time.time() - start_time) * 1000
            tokens_generated = result["usage"]["completion_tokens"]
            tokens_per_second = (
                tokens_generated / (latency_ms / 1000) if latency_ms > 0 else 0
            )

            return GenerationResponse(
                text=result["choices"][0]["message"]["content"],
                tokens_generated=tokens_generated,
                finish_reason=result["choices"][0]["finish_reason"],
                latency_ms=latency_ms,
                tokens_per_second=tokens_per_second,
                model=self.model_name,
            )

        except httpx.HTTPError as e:
            raise RuntimeError(f"vLLM chat request failed: {e}")

    async def health_check(self) -> bool:
        """Check if vLLM server is healthy"""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


class VLLMClientPool:
    """Pool of vLLM clients for different specialist roles"""

    def __init__(self):
        self.clients: Dict[SpecialistRole, VLLMClient] = {}
        self._initialized = False

    async def initialize(self):
        """Initialize clients based on configuration"""
        if self._initialized:
            return

        models_config = get_models_config()
        vllm_instances = models_config["vllm_instances"]

        # Map roles to vLLM server endpoints
        role_to_server = {
            SpecialistRole.CENTRAL_WORKSPACE: (
                f"http://localhost:{vllm_instances['central_workspace_server']['port']}",
                "llama-3.1-70b",
            ),
            SpecialistRole.PERCEPTION: (
                f"http://localhost:{vllm_instances['gpu1_specialists_server']['port']}",
                "mistral-small-22b",
            ),
            SpecialistRole.MEMORY: (
                f"http://localhost:{vllm_instances['gpu2_specialists_server']['port']}",
                "qwen-2.5-coder-32b",
            ),
            SpecialistRole.PLANNING: (
                f"http://localhost:{vllm_instances['gpu2_specialists_server']['port']}",
                "llama-3.1-8b",
            ),
            SpecialistRole.METACOGNITION: (
                f"http://localhost:{vllm_instances['gpu2_specialists_server']['port']}",
                "gemma-2-9b",
            ),
        }

        for role, (base_url, model_name) in role_to_server.items():
            self.clients[role] = VLLMClient(
                base_url=base_url, model_name=model_name, role=role
            )

        self._initialized = True

    def get_client(self, role: SpecialistRole) -> VLLMClient:
        """Get client for a specific specialist role"""
        if not self._initialized:
            raise RuntimeError("VLLMClientPool not initialized. Call initialize() first.")
        return self.clients[role]

    async def health_check_all(self) -> Dict[SpecialistRole, bool]:
        """Check health of all vLLM servers"""
        results = {}
        for role, client in self.clients.items():
            results[role] = await client.health_check()
        return results

    async def close_all(self):
        """Close all clients"""
        for client in self.clients.values():
            await client.close()
