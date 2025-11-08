"""
Ollama Client for GWT Engine
Replaces vLLM with Ollama for Windows compatibility
"""

import asyncio
import logging
from typing import Dict, Any, Optional
import httpx

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for Ollama API"""
    
    def __init__(self, model_name: str, base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=120.0)
        
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate completion from Ollama"""
        
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                }
            }
            
            if system:
                payload["system"] = system
                
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "text": result.get("response", ""),
                "model": self.model_name,
                "done": result.get("done", False),
                "total_duration": result.get("total_duration", 0),
                "eval_count": result.get("eval_count", 0),
            }
            
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            raise
            
    async def health_check(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False
            
    async def close(self):
        """Close the client"""
        await self.client.aclose()


class OllamaClientPool:
    """Pool of Ollama clients for different specialist roles"""
    
    def __init__(self):
        self.clients: Dict[str, OllamaClient] = {}
        self.model_mapping = {
            "central_workspace": "qwen2.5:32b",  # UPGRADED: 32B for maximum integration power
            "perception": "qwen2.5:14b",         # UPGRADED: 14B for better perception
            "memory": "qwen2.5:14b",             # 14B for memory
            "planning": "qwen2.5:7b",            # 7B for fast planning
            "metacognition": "qwen2.5:7b",       # 7B for fast metacognition
        }
        
    async def initialize(self):
        """Initialize all clients"""
        logger.info("Initializing Ollama client pool...")
        
        for role, model in self.model_mapping.items():
            self.clients[role] = OllamaClient(model)
            logger.info(f"Created client for {role}: {model}")
            
        # Health check
        health_checks = await self.health_check_all()
        if not all(health_checks.values()):
            logger.warning("Some Ollama models may not be available")
            
        logger.info("Ollama client pool initialized")
        
    def get_client(self, role: str) -> OllamaClient:
        """Get client for a specific role"""
        if role not in self.clients:
            raise ValueError(f"No client for role: {role}")
        return self.clients[role]
        
    async def health_check_all(self) -> Dict[str, bool]:
        """Check health of all clients"""
        results = {}
        for role, client in self.clients.items():
            results[role] = await client.health_check()
        return results
        
    async def close_all(self):
        """Close all clients"""
        for client in self.clients.values():
            await client.close()
