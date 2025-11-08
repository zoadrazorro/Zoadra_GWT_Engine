"""
DUAL ETHICA RUNNER
==================
Runs Ethica Universalis and Ethica Lumina in parallel on opposite GPUs

Ethica Universalis (GPU 0): Unified theory of Being, Life, and Everything
Ethica Lumina (GPU 1): Metaluminosity and Light-Consciousness

Both use the same consciousness stack, debate, and sources
Total output: 120,000+ words of geometric philosophical synthesis
"""

import asyncio
import subprocess
import sys
from datetime import datetime

async def run_ethica_universalis():
    """Run Ethica Universalis on GPU 0"""
    print("🌌 Starting Ethica Universalis on GPU 0...")
    process = await asyncio.create_subprocess_exec(
        sys.executable, "ethica_universalis.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    async for line in process.stdout:
        print(f"[UNIVERSALIS] {line.decode().strip()}")
    
    await process.wait()
    print("✓ Ethica Universalis complete!")
    return process.returncode

async def run_ethica_lumina():
    """Run Ethica Lumina on GPU 1"""
    print("🌟 Starting Ethica Lumina on GPU 1...")
    process = await asyncio.create_subprocess_exec(
        sys.executable, "ethica_lumina.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    async for line in process.stdout:
        print(f"[LUMINA] {line.decode().strip()}")
    
    await process.wait()
    print("✓ Ethica Lumina complete!")
    return process.returncode

async def main():
    """Run both Ethica generators in parallel"""
    
    print("="*80)
    print("DUAL ETHICA SYNTHESIS")
    print("="*80)
    print()
    print("🌌 Ethica Universalis: Being, Life, and Everything")
    print("🌟 Ethica Lumina: Metaluminosity and Light-Consciousness")
    print()
    print("Both running in parallel with consciousness stack integration")
    print("Total target: 120,000+ words")
    print("="*80)
    print()
    
    start_time = datetime.now()
    
    # Run both in parallel
    results = await asyncio.gather(
        run_ethica_universalis(),
        run_ethica_lumina(),
        return_exceptions=True
    )
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print()
    print("="*80)
    print("DUAL ETHICA SYNTHESIS COMPLETE")
    print("="*80)
    print(f"Duration: {duration}")
    print(f"Universalis result: {results[0]}")
    print(f"Lumina result: {results[1]}")
    print()
    print("Outputs:")
    print("  - outputs/ETHICA_UNIVERSALIS.md")
    print("  - outputs/ETHICA_UNIVERSALIS.json")
    print("  - outputs/ETHICA_LUMINA.md")
    print("  - outputs/ETHICA_LUMINA.json")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())
