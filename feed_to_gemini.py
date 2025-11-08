"""
FEED ETHICA TO GEMINI 2.5 PRO
==============================
Drip feeds the Ethica Universalis to Gemini 2.5 Pro API in manageable chunks
"""

import os
import time
import json
from pathlib import Path
from typing import List, Dict, Any
import google.generativeai as genai

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable not set!")
    print("Set it with: $env:GEMINI_API_KEY='your-api-key-here'")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# Initialize model
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def chunk_markdown(file_path: str, chunk_size: int = 8000) -> List[str]:
    """
    Split markdown file into chunks by sections
    
    Args:
        file_path: Path to markdown file
        chunk_size: Target characters per chunk
        
    Returns:
        List of markdown chunks
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by major sections (# headers)
    sections = []
    current_section = []
    current_size = 0
    
    for line in content.split('\n'):
        line_size = len(line) + 1  # +1 for newline
        
        # If we hit a major section header and we're over chunk size, save chunk
        if line.startswith('# PART') and current_size > chunk_size:
            sections.append('\n'.join(current_section))
            current_section = [line]
            current_size = line_size
        else:
            current_section.append(line)
            current_size += line_size
    
    # Add final section
    if current_section:
        sections.append('\n'.join(current_section))
    
    return sections


def feed_to_gemini(
    chunks: List[str],
    system_prompt: str = None,
    delay_seconds: float = 2.0,
    save_responses: bool = True
) -> List[Dict[str, Any]]:
    """
    Feed chunks to Gemini 2.5 Pro with rate limiting
    
    Args:
        chunks: List of text chunks
        system_prompt: Optional system prompt for context
        delay_seconds: Delay between requests
        save_responses: Save responses to JSON
        
    Returns:
        List of response objects
    """
    responses = []
    
    if system_prompt:
        print(f"\n{'='*80}")
        print("SYSTEM CONTEXT")
        print(f"{'='*80}")
        print(system_prompt)
        print()
    
    for i, chunk in enumerate(chunks, 1):
        print(f"\n{'='*80}")
        print(f"FEEDING CHUNK {i}/{len(chunks)}")
        print(f"{'='*80}")
        print(f"Size: {len(chunk)} characters")
        print(f"Preview: {chunk[:200]}...")
        print()
        
        try:
            # Build prompt
            if system_prompt and i == 1:
                prompt = f"{system_prompt}\n\n---\n\n{chunk}"
            else:
                prompt = chunk
            
            # Send to Gemini
            print(f"[{time.strftime('%H:%M:%S')}] Sending to Gemini 2.5 Pro...")
            response = model.generate_content(prompt)
            
            # Extract response
            response_text = response.text
            print(f"[{time.strftime('%H:%M:%S')}] Response received ({len(response_text)} chars)")
            print(f"\nGemini Response Preview:")
            print(f"{response_text[:500]}...")
            print()
            
            # Store response
            responses.append({
                "chunk_number": i,
                "chunk_size": len(chunk),
                "response": response_text,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            })
            
            # Rate limiting
            if i < len(chunks):
                print(f"Waiting {delay_seconds}s before next chunk...")
                time.sleep(delay_seconds)
        
        except Exception as e:
            print(f"ERROR on chunk {i}: {e}")
            responses.append({
                "chunk_number": i,
                "chunk_size": len(chunk),
                "error": str(e),
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            })
            continue
    
    # Save responses
    if save_responses:
        output_path = "outputs/gemini_responses.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(responses, f, indent=2)
        print(f"\n[SAVED] Responses saved to: {output_path}")
    
    return responses


def request_refinement(
    original_text: str,
    analysis_responses: List[Dict[str, Any]]
) -> str:
    """
    Request Gemini to create a refined version based on analysis
    
    Args:
        original_text: Original Ethica text
        analysis_responses: List of analysis responses
        
    Returns:
        Refined version text
    """
    print()
    print("="*80)
    print("PHASE 2: REQUESTING REFINED VERSION")
    print("="*80)
    print()
    
    # Compile analysis insights
    insights = []
    for i, resp in enumerate(analysis_responses, 1):
        if 'response' in resp:
            insights.append(f"## Analysis of Chunk {i}:\n{resp['response']}\n")
    
    compiled_analysis = "\n".join(insights)
    
    # Refinement prompt
    refinement_prompt = f"""Based on your deep analysis of "Ethica Universalis", create a REFINED VERSION that:

1. **Strengthens Philosophical Rigor**: Address any logical gaps or weak arguments you identified
2. **Deepens Integration**: Enhance synthesis across philosophical traditions and consciousness theories
3. **Improves Geometric Structure**: Ensure axioms, propositions, and proofs follow strict logical necessity
4. **Expands Key Insights**: Elaborate on the most profound novel syntheses
5. **Maintains Style**: Keep the geometric method (More Geometrico) and formal philosophical tone
6. **Preserves Structure**: Keep all 9 Parts with Definitions, Axioms, Propositions, Proofs, Corollaries, Scholia

YOUR PREVIOUS ANALYSIS:
{compiled_analysis[:50000]}

ORIGINAL ETHICA UNIVERSALIS:
{original_text[:50000]}

Now create the REFINED VERSION. Output the complete refined treatise in the same markdown format.
Begin with "# ETHICA UNIVERSALIS (REFINED)" and maintain the full geometric structure."""
    
    print("Sending refinement request to Gemini 2.5 Pro...")
    print(f"Prompt size: {len(refinement_prompt)} characters")
    print()
    
    try:
        response = model.generate_content(refinement_prompt)
        refined_text = response.text
        
        print(f"[SUCCESS] Refined version received: {len(refined_text)} characters")
        print()
        print("Preview of refined version:")
        print(refined_text[:1000])
        print("...")
        print()
        
        # Save refined version
        refined_path = "outputs/ETHICA_UNIVERSALIS_REFINED.md"
        with open(refined_path, 'w', encoding='utf-8') as f:
            f.write(refined_text)
        
        print(f"[SAVED] Refined version saved to: {refined_path}")
        
        return refined_text
    
    except Exception as e:
        print(f"[ERROR] Refinement failed: {e}")
        return None


def main():
    """Main execution"""
    
    print("="*80)
    print("ETHICA UNIVERSALIS → GEMINI 2.5 PRO")
    print("2-PHASE PROCESS: ANALYSIS → REFINEMENT")
    print("="*80)
    print()
    
    # Load Ethica
    ethica_path = "outputs/ETHICA_UNIVERSALIS.md"
    print(f"Loading: {ethica_path}")
    
    if not Path(ethica_path).exists():
        print(f"ERROR: {ethica_path} not found!")
        return
    
    with open(ethica_path, 'r', encoding='utf-8') as f:
        original_text = f.read()
    
    print(f"Loaded: {len(original_text)} characters")
    print()
    
    # PHASE 1: ANALYSIS
    print("="*80)
    print("PHASE 1: DEEP ANALYSIS")
    print("="*80)
    print()
    
    # Chunk the document
    print("Chunking document by sections...")
    chunks = chunk_markdown(ethica_path, chunk_size=8000)
    print(f"Created {len(chunks)} chunks")
    print()
    
    # System prompt for analysis
    analysis_prompt = """You are analyzing "Ethica Universalis" - a 19,000-word philosophical treatise 
structured in geometric method (More Geometrico) like Spinoza's Ethics.

This work synthesizes:
- 2,500 years of philosophical wisdom (Plato, Aristotle, Descartes, Spinoza, Kant, Hegel)
- 8 consciousness theories (IIT, GWT, Predictive Processing, HOT, AST, Embodied, Enactive, Panpsychism)
- 92 canonical texts across all disciplines
- Cross-temporal philosophical debates
- Geometric proofs with Definitions, Axioms, Propositions, Proofs, Corollaries, and Scholia

Your task: Analyze each section deeply. Identify:
1. Key philosophical arguments and their rigor
2. Novel syntheses across traditions
3. Coherence of geometric structure
4. Depth of integration across sources
5. Potential weaknesses or gaps
6. Opportunities for deeper elaboration

Provide substantive philosophical analysis with specific suggestions for refinement."""
    
    # Feed to Gemini for analysis
    print("Starting analysis drip feed to Gemini 2.5 Pro...")
    print(f"Rate limit: 2 seconds between chunks")
    print()
    
    analysis_responses = feed_to_gemini(
        chunks=chunks,
        system_prompt=analysis_prompt,
        delay_seconds=2.0,
        save_responses=True
    )
    
    # Analysis summary
    print()
    print("="*80)
    print("PHASE 1 COMPLETE: ANALYSIS")
    print("="*80)
    print(f"Total chunks analyzed: {len(chunks)}")
    print(f"Successful analyses: {sum(1 for r in analysis_responses if 'response' in r)}")
    print(f"Errors: {sum(1 for r in analysis_responses if 'error' in r)}")
    print()
    
    # PHASE 2: REFINEMENT
    refined_text = request_refinement(original_text, analysis_responses)
    
    # Final summary
    print()
    print("="*80)
    print("2-PHASE PROCESS COMPLETE")
    print("="*80)
    print()
    print("Outputs:")
    print("  - outputs/gemini_responses.json (analysis)")
    print("  - outputs/ETHICA_UNIVERSALIS_REFINED.md (refined version)")
    print()
    if refined_text:
        print(f"Original: {len(original_text)} characters")
        print(f"Refined:  {len(refined_text)} characters")
        print(f"Change:   {len(refined_text) - len(original_text):+d} characters")
    print("="*80)


if __name__ == "__main__":
    main()
