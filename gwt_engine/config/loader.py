"""Configuration loader for YAML files"""

import os
from pathlib import Path
from typing import Dict, Any
import yaml


class ConfigLoader:
    """Loads and manages configuration files"""

    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = Path(__file__).parent
        self.config_dir = Path(config_dir)
        self._models_config = None
        self._system_config = None

    def load_models_config(self) -> Dict[str, Any]:
        """Load models.yaml configuration"""
        if self._models_config is None:
            config_path = self.config_dir / "models.yaml"
            with open(config_path, "r") as f:
                self._models_config = yaml.safe_load(f)
        return self._models_config

    def load_system_config(self) -> Dict[str, Any]:
        """Load system.yaml configuration"""
        if self._system_config is None:
            config_path = self.config_dir / "system.yaml"
            with open(config_path, "r") as f:
                self._system_config = yaml.safe_load(f)
        return self._system_config

    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """Get configuration for a specific model"""
        models_config = self.load_models_config()
        if model_name not in models_config.get("models", {}):
            raise ValueError(f"Model '{model_name}' not found in configuration")
        return models_config["models"][model_name]

    def get_vllm_instance_config(self, instance_name: str) -> Dict[str, Any]:
        """Get vLLM instance configuration"""
        models_config = self.load_models_config()
        instances = models_config.get("vllm_instances", {})
        if instance_name not in instances:
            raise ValueError(f"vLLM instance '{instance_name}' not found")
        return instances[instance_name]

    def get_hardware_config(self) -> Dict[str, Any]:
        """Get hardware configuration"""
        return self.load_models_config().get("hardware", {})

    def get_redis_config(self) -> Dict[str, Any]:
        """Get Redis configuration"""
        return self.load_system_config().get("redis", {})

    def get_ray_config(self) -> Dict[str, Any]:
        """Get Ray configuration"""
        return self.load_system_config().get("ray", {})


# Global configuration instance
_config_loader = ConfigLoader()


def load_config(config_dir: str = None) -> ConfigLoader:
    """Initialize and return configuration loader"""
    global _config_loader
    if config_dir:
        _config_loader = ConfigLoader(config_dir)
    return _config_loader


def get_model_config(model_name: str) -> Dict[str, Any]:
    """Get configuration for a specific model"""
    return _config_loader.get_model_config(model_name)


def get_system_config() -> Dict[str, Any]:
    """Get system configuration"""
    return _config_loader.load_system_config()


def get_models_config() -> Dict[str, Any]:
    """Get models configuration"""
    return _config_loader.load_models_config()
