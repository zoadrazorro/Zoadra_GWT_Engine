"""
THE MYSTERY MACHINE
===================
Stochastic memory retrieval using Brownian noise for serendipitous discovery.
"""

import numpy as np
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import math

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class BrownianSeed:
    """A seed generated from Brownian noise"""
    value: float
    index: int
    drift: float
    volatility: float
    timestamp: float


class MysteryMachine:
    """Stochastic memory retrieval using Brownian motion"""
    
    def __init__(
        self,
        memory_file: str = "./philosophical_memory.json",
        drift: float = 0.0,
        volatility: float = 1.0,
        seed: Optional[int] = None
    ):
        self.memory_file = Path(memory_file)
        self.memories = []
        self.drift = drift
        self.volatility = volatility
        self.rng = np.random.default_rng(seed)
        self.position = 0.0
        self.walk_history = [0.0]
        self._load_memories()
        logger.info(f"Mystery Machine: {len(self.memories)} memories loaded")
    
    def _load_memories(self):
        """Load memories from JSON"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.memories = data.get("memories", [])
        except Exception as e:
            logger.error(f"Failed to load: {e}")
            self.memories = []
    
    def brownian_step(self, dt: float = 1.0) -> float:
        """Generate Brownian motion step: dX = drift*dt + volatility*sqrt(dt)*Z"""
        z = self.rng.standard_normal()
        return self.drift * dt + self.volatility * math.sqrt(dt) * z
    
    def walk(self, steps: int = 1) -> List[float]:
        """Perform random walk"""
        positions = []
        for _ in range(steps):
            self.position += self.brownian_step()
            self.walk_history.append(self.position)
            positions.append(self.position)
        return positions
    
    def position_to_index(self, position: float) -> int:
        """Convert position to memory index using sigmoid"""
        if not self.memories:
            return 0
        normalized = 1 / (1 + math.exp(-position / 10))
        return int(normalized * len(self.memories)) % len(self.memories)
    
    def generate_seed(self, steps: int = 10) -> BrownianSeed:
        """Generate seed by walking"""
        positions = self.walk(steps)
        final_position = positions[-1]
        index = self.position_to_index(final_position)
        return BrownianSeed(
            value=final_position,
            index=index,
            drift=self.drift,
            volatility=self.volatility,
            timestamp=len(self.walk_history)
        )
    
    def retrieve_by_seed(self, seed: BrownianSeed) -> Optional[Dict[str, Any]]:
        """Retrieve memory using seed"""
        if not self.memories or seed.index >= len(self.memories):
            return None
        return self.memories[seed.index]
    
    def mysterious_retrieval(
        self,
        num_memories: int = 5,
        walk_steps: int = 10
    ) -> List[Dict[str, Any]]:
        """Retrieve memories through random walks"""
        discovered = []
        logger.info(f"Beginning mysterious retrieval: {num_memories} memories")
        
        for i in range(num_memories):
            seed = self.generate_seed(steps=walk_steps)
            memory = self.retrieve_by_seed(seed)
            if memory:
                discovered.append(memory)
                logger.info(f"  Step {i+1}: pos={seed.value:.2f} -> idx={seed.index}")
        
        logger.info(f"Discovered {len(discovered)} memories")
        return discovered
    
    def quantum_superposition_retrieval(
        self,
        num_memories: int = 10,
        collapse_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """Quantum superposition - multiple walks collapse to memories"""
        logger.info(f"Quantum superposition retrieval...")
        
        superposition_states = []
        for _ in range(num_memories):
            seed = self.generate_seed(steps=self.rng.integers(5, 20))
            amplitude = abs(math.sin(seed.value))
            superposition_states.append({
                'seed': seed,
                'amplitude': amplitude
            })
        
        collapsed_memories = []
        for state in superposition_states:
            if state['amplitude'] > collapse_threshold:
                memory = self.retrieve_by_seed(state['seed'])
                if memory:
                    collapsed_memories.append(memory)
                    logger.info(f"  Collapsed: amp={state['amplitude']:.3f} -> idx={state['seed'].index}")
        
        logger.info(f"{len(collapsed_memories)} states collapsed")
        return collapsed_memories
    
    def fractal_memory_dive(
        self,
        depth: int = 5,
        branching_factor: int = 3
    ) -> Dict[str, Any]:
        """Recursive fractal exploration"""
        logger.info(f"Fractal dive: depth={depth}, branching={branching_factor}")
        
        def dive(current_depth: int, parent_position: float) -> List:
            if current_depth >= depth:
                return None
            
            branches = []
            for _ in range(branching_factor):
                self.position = parent_position
                seed = self.generate_seed(steps=3)
                memory = self.retrieve_by_seed(seed)
                
                if memory:
                    subtree = dive(current_depth + 1, seed.value)
                    branches.append({
                        'memory': memory,
                        'seed_value': seed.value,
                        'index': seed.index,
                        'children': subtree
                    })
            
            return branches if branches else None
        
        root_seed = self.generate_seed(steps=10)
        root_memory = self.retrieve_by_seed(root_seed)
        
        tree = {
            'root': {
                'memory': root_memory,
                'seed_value': root_seed.value,
                'index': root_seed.index
            },
            'branches': dive(0, root_seed.value)
        }
        
        logger.info(f"Fractal exploration complete")
        return tree
    
    def reset_walk(self, position: float = 0.0):
        """Reset walk to position"""
        self.position = position
        self.walk_history = [position]
    
    def get_walk_statistics(self) -> Dict[str, float]:
        """Get statistics about the random walk"""
        if len(self.walk_history) < 2:
            return {}
        
        positions = np.array(self.walk_history)
        return {
            'mean': float(np.mean(positions)),
            'std': float(np.std(positions)),
            'min': float(np.min(positions)),
            'max': float(np.max(positions)),
            'steps': len(positions),
            'current_position': self.position
        }


def demo_mystery_machine():
    """Demonstrate the Mystery Machine"""
    print("=" * 80)
    print("THE MYSTERY MACHINE - STOCHASTIC MEMORY RETRIEVAL")
    print("=" * 80)
    
    machine = MysteryMachine(drift=0.1, volatility=2.0)
    
    print("\n1. MYSTERIOUS RETRIEVAL (Random Walk)")
    print("-" * 80)
    memories = machine.mysterious_retrieval(num_memories=5, walk_steps=10)
    for i, mem in enumerate(memories, 1):
        content = mem.get('content', '')[:100]
        print(f"{i}. {content}...")
    
    print("\n2. QUANTUM SUPERPOSITION")
    print("-" * 80)
    machine.reset_walk()
    quantum_memories = machine.quantum_superposition_retrieval(num_memories=10)
    print(f"Collapsed {len(quantum_memories)} memories from superposition")
    
    print("\n3. FRACTAL MEMORY DIVE")
    print("-" * 80)
    machine.reset_walk()
    tree = machine.fractal_memory_dive(depth=3, branching_factor=2)
    print(f"Root: Index {tree['root']['index']}")
    
    print("\n4. WALK STATISTICS")
    print("-" * 80)
    stats = machine.get_walk_statistics()
    for key, value in stats.items():
        print(f"{key}: {value:.2f}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    demo_mystery_machine()
