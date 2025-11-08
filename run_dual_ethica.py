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
    print("[UNIVERSALIS] Starting on GPU 0...")
    process = await asyncio.create_subprocess_exec(
        sys.executable, "ethica_universalis.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    async for line in process.stdout:
        try:
            print(f"[UNIVERSALIS] {line.decode('utf-8', errors='replace').strip()}")
        except:
            pass
    
    await process.wait()
    print("[UNIVERSALIS] Complete!")
    return process.returncode

async def run_ethica_lumina():
    """Run Ethica Lumina on GPU 1"""
    print("[LUMINA] Starting on GPU 1...")
    process = await asyncio.create_subprocess_exec(
        sys.executable, "ethica_lumina.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    async for line in process.stdout:
        try:
            print(f"[LUMINA] {line.decode('utf-8', errors='replace').strip()}")
        except:
            pass
    
    await process.wait()
    print("[LUMINA] Complete!")
    return process.returncode

async def main():
    """Run both Ethica generators in parallel"""
    
    print("="*80)
    print("DUAL ETHICA SYNTHESIS")
    print("="*80)
    print()
    print("UNIVERSALIS: Being, Life, and Everything")
    print("LUMINA: Metaluminosity and Light-Consciousness")
    print()
    print("Running sequentially with consciousness stack integration")
    print("Total target: 120,000+ words")
    print("="*80)
    print()
    
    start_time = datetime.now()
    
    # Run sequentially (Ollama doesn't support dual instances easily)
    print("Running Ethica Universalis first...")
    result1 = await run_ethica_universalis()
    
    print("\nRunning Ethica Lumina second...")
    result2 = await run_ethica_lumina()
    
    results = [result1, result2]
    
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
