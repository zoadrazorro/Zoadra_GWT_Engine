"""
PARALLEL DEBATE ORCHESTRATOR
=============================
Generates multiple debate rounds simultaneously to maximize GPU usage.
Uses asyncio to run multiple Ollama requests in parallel.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from gwt_engine.specialists.cross_temporal_debate import (
    CrossTemporalDebate,
    create_debate,
    HISTORICAL_PHILOSOPHERS,
)
from gwt_engine.specialists.composer import ComposerSpecialist


class ParallelDebateOrchestrator:
    """
    Orchestrates debates with PARALLEL generation to maximize GPU usage.
    """
    
    def __init__(self):
        """Initialize with composer"""
        self.composer = ComposerSpecialist()
        print(">> Parallel Debate Orchestrator initialized")
        print(f"   Composer: {self.composer.model_name}")
        print(f"   Memories: {len(self.composer.philosophical_memories)}")
    
    async def generate_platonic_exchange(
        self,
        debate: CrossTemporalDebate,
        questioner: str,
        respondent: str,
        round_num: int
    ) -> Dict[str, Any]:
        """Generate a complete Platonic dialogue exchange"""
        
        questioner_obj = debate.philosophers[questioner]
        respondent_obj = debate.philosophers[respondent]
        
        # Generate question, response, and elenchus IN PARALLEL
        question_task = self.composer.compose(
            prompt=f"You are {questioner} ({questioner_obj.era}). "
                   f"Using the Socratic method, pose a probing question to {respondent} "
                   f"about: '{debate.topic}'. "
                   f"Draw on your concepts: {', '.join(questioner_obj.key_concepts[:3])}. "
                   f"2-3 sentences.",
            style="formal",
            section_type="body",
            constraints={"word_count": 100}
        )
        
        # Start all three generations in parallel
        question_response = await question_task
        question = question_response.content
        
        # Now generate response and elenchus in parallel
        response_task = self.composer.compose(
            prompt=f"You are {respondent} ({respondent_obj.era}). "
                   f"{questioner} asks: '{question}'. "
                   f"Respond using your concepts: {', '.join(respondent_obj.key_concepts[:3])}. "
                   f"3-4 sentences.",
            style="formal",
            section_type="body",
            constraints={"word_count": 150}
        )
        
        elenchus_task = self.composer.compose(
            prompt=f"You are {questioner}. Provide Socratic examination (elenchus) of {respondent}'s likely response. "
                   f"Probe assumptions. 2-3 sentences.",
            style="analytical",
            section_type="body",
            constraints={"word_count": 100}
        )
        
        # Wait for both
        response_result, elenchus_result = await asyncio.gather(response_task, elenchus_task)
        
        return {
            "type": "platonic_dialogue",
            "questioner": questioner,
            "respondent": respondent,
            "question": question,
            "response": response_result.content,
            "elenchus": elenchus_result.content,
            "round": round_num
        }
    
    async def generate_geometric_proposition(
        self,
        debate: CrossTemporalDebate,
        proposer: str,
        round_num: int
    ) -> Dict[str, Any]:
        """Generate a geometric proposition with proof"""
        
        proposer_obj = debate.philosophers[proposer]
        
        # Generate axioms, proposition, and proof in parallel
        axioms_task = self.composer.compose(
            prompt=f"You are {proposer}. State 3 axioms about '{debate.topic}' "
                   f"using your concepts: {', '.join(proposer_obj.key_concepts[:2])}. "
                   f"Numbered list, one sentence each.",
            style="formal",
            section_type="body",
            constraints={"word_count": 150}
        )
        
        proposition_task = self.composer.compose(
            prompt=f"You are {proposer}. State a bold PROPOSITION about '{debate.topic}'. "
                   f"One sentence starting with 'PROPOSITION:'",
            style="formal",
            section_type="body",
            constraints={"word_count": 75}
        )
        
        # Wait for both
        axioms_result, prop_result = await asyncio.gather(axioms_task, proposition_task)
        
        # Parse axioms
        axioms = [a.strip() for a in axioms_result.content.split('\n') if a.strip() and any(c.isdigit() for c in a[:3])]
        proposition = prop_result.content
        
        # Now generate proof and corollary in parallel
        proof_task = self.composer.compose(
            prompt=f"You are {proposer}. PROOF of: '{proposition}' using your axioms. "
                   f"3-4 sentences. Start with 'PROOF:'",
            style="analytical",
            section_type="body",
            constraints={"word_count": 200}
        )
        
        corollary_task = self.composer.compose(
            prompt=f"State a COROLLARY from: '{proposition}'. One sentence.",
            style="formal",
            section_type="body",
            constraints={"word_count": 75}
        )
        
        proof_result, corollary_result = await asyncio.gather(proof_task, corollary_task)
        
        return {
            "type": "geometric_proposition",
            "philosopher": proposer,
            "axioms": axioms,
            "proposition": proposition,
            "proof": proof_result.content,
            "corollary": corollary_result.content,
            "round": round_num
        }
    
    async def generate_process_occasion(
        self,
        debate: CrossTemporalDebate,
        speaker: str,
        round_num: int,
        prehensions: List[str]
    ) -> Dict[str, Any]:
        """Generate a Whiteheadian actual occasion"""
        
        speaker_obj = debate.philosophers[speaker]
        
        # Generate content and satisfaction in parallel
        content_task = self.composer.compose(
            prompt=f"You are {speaker}. Express how reality is creative process, not static substance. "
                   f"This thought prehends (grasps): {', '.join(prehensions)}. "
                   f"Use your concepts: {', '.join(speaker_obj.key_concepts[:2])}. "
                   f"3-4 sentences emphasizing becoming.",
            style="narrative",
            section_type="body",
            constraints={"word_count": 175}
        )
        
        satisfaction_task = self.composer.compose(
            prompt=f"This occasion reaches SATISFACTION (completion). "
                   f"What unified feeling emerges? One sentence.",
            style="formal",
            section_type="body",
            constraints={"word_count": 75}
        )
        
        content_result, satisfaction_result = await asyncio.gather(content_task, satisfaction_task)
        
        return {
            "type": "actual_occasion",
            "speaker": speaker,
            "content": content_result.content,
            "satisfaction": satisfaction_result.content,
            "prehensions": prehensions,
            "round": round_num
        }
    
    async def generate_round_batch(
        self,
        debate: CrossTemporalDebate,
        start_round: int,
        batch_size: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple rounds in parallel (batch)
        
        Args:
            debate: The debate instance
            start_round: Starting round number
            batch_size: Number of rounds to generate in parallel
            
        Returns:
            List of generated exchanges
        """
        
        philosophers = list(debate.philosophers.keys())
        tasks = []
        
        for i in range(batch_size):
            round_num = start_round + i
            style_idx = round_num % 3
            
            if style_idx == 0:
                # Platonic dialogue
                questioner = philosophers[round_num % len(philosophers)]
                respondent = philosophers[(round_num + 1) % len(philosophers)]
                task = self.generate_platonic_exchange(debate, questioner, respondent, round_num)
            
            elif style_idx == 1:
                # Geometric proposition
                proposer = philosophers[round_num % len(philosophers)]
                task = self.generate_geometric_proposition(debate, proposer, round_num)
            
            else:
                # Process occasion
                speaker = philosophers[round_num % len(philosophers)]
                # Get some previous speakers for prehensions
                prev_speakers = [philosophers[(round_num - j) % len(philosophers)] for j in range(1, 4)]
                task = self.generate_process_occasion(debate, speaker, round_num, prev_speakers)
            
            tasks.append(task)
        
        # Execute all tasks in parallel
        print(f"\n>> Generating rounds {start_round}-{start_round + batch_size - 1} IN PARALLEL...")
        results = await asyncio.gather(*tasks)
        print(f">> Batch complete!")
        
        return results
    
    async def run_parallel_debate(
        self,
        topic: str,
        philosopher_names: List[str],
        num_rounds: int = 30,
        batch_size: int = 6
    ) -> CrossTemporalDebate:
        """
        Run a full debate with parallel generation
        
        Args:
            topic: Debate topic
            philosopher_names: List of philosopher keys
            num_rounds: Total rounds
            batch_size: Rounds to generate in parallel (higher = more GPU usage)
            
        Returns:
            Completed debate
        """
        
        print("\n" + "="*80)
        print(">> PARALLEL DEBATE GENERATION")
        print("="*80)
        print(f"Topic: {topic}")
        print(f"Philosophers: {', '.join(philosopher_names)}")
        print(f"Total Rounds: {num_rounds}")
        print(f"Batch Size: {batch_size} (parallel generations)")
        print(f"Expected GPU Usage: HIGH (multiple concurrent requests)")
        print("="*80 + "\n")
        
        # Create debate
        debate = create_debate(topic, philosopher_names)
        
        # Generate in batches
        all_exchanges = []
        for start_round in range(0, num_rounds, batch_size):
            actual_batch_size = min(batch_size, num_rounds - start_round)
            
            batch_results = await self.generate_round_batch(
                debate,
                start_round,
                actual_batch_size
            )
            
            all_exchanges.extend(batch_results)
            
            # Save progress
            self.save_progress(debate, all_exchanges, start_round + actual_batch_size, num_rounds)
            
            print(f"Progress: {len(all_exchanges)}/{num_rounds} rounds complete")
        
        # Add exchanges to debate
        for exchange in all_exchanges:
            debate.full_transcript.append(exchange)
        
        print("\n" + "="*80)
        print(f">> DEBATE COMPLETE: {len(all_exchanges)} rounds generated")
        print("="*80)
        
        return debate
    
    def save_progress(self, debate, exchanges, completed, total):
        """Save debate progress"""
        progress = {
            "topic": debate.topic,
            "philosophers": list(debate.philosophers.keys()),
            "completed_rounds": completed,
            "total_rounds": total,
            "exchanges": exchanges,
            "timestamp": datetime.now().isoformat()
        }
        
        with open('parallel_debate_progress.json', 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2)


async def main():
    """Run parallel debate"""
    
    orchestrator = ParallelDebateOrchestrator()
    
    topic = "What is the nature of consciousness and its relationship to reality?"
    
    philosophers = [
        "plato",
        "aristotle",
        "descartes",
        "spinoza",
        "kant",
        "hegel"
    ]
    
    # Generate 30 rounds with batch size of 6 = 5 batches of 6 parallel generations
    debate = await orchestrator.run_parallel_debate(
        topic=topic,
        philosopher_names=philosophers,
        num_rounds=30,
        batch_size=6  # Increase this to max out GPU more (try 8, 10, 12)
    )
    
    # Save final debate
    output_path = "outputs/parallel_debate.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "topic": debate.topic,
            "philosophers": list(debate.philosophers.keys()),
            "rounds": len(debate.full_transcript),
            "transcript": debate.full_transcript
        }, f, indent=2)
    
    print(f"\n>> Debate saved to: {output_path}")
    print(f">> Total exchanges: {len(debate.full_transcript)}")
    
    return debate


if __name__ == "__main__":
    debate = asyncio.run(main())
