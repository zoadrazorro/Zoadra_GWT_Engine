"""
CURRICULUM RAG SYSTEM
=====================
Retrieval-Augmented Generation over the full university curriculum.
92 texts across all disciplines for comprehensive knowledge retrieval.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict


class CurriculumRAG:
    """
    RAG system for querying the full university curriculum.
    """
    
    def __init__(self, curriculum_dir: str = "./university_curriculum"):
        """
        Initialize RAG with curriculum texts
        
        Args:
            curriculum_dir: Directory containing curriculum texts
        """
        self.curriculum_dir = Path(curriculum_dir)
        self.manifest_path = self.curriculum_dir / "curriculum_manifest.json"
        
        # Load manifest
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            self.manifest = json.load(f)
        
        self.total_texts = self.manifest['total_texts']
        self.categories = self.manifest['categories']
        self.completed = self.manifest['completed']
        
        # Build text index
        self.text_index = {}
        self.category_index = defaultdict(list)
        self._build_index()
        
        print(f"CurriculumRAG initialized:")
        print(f"  Total texts: {self.total_texts}")
        print(f"  Categories: {len(self.categories)}")
        print(f"  Indexed: {len(self.text_index)} texts")
    
    def _build_index(self):
        """Build searchable index of all texts"""
        
        # Map text IDs to categories
        text_to_category = {}
        
        # Read category files to map texts
        for category_name in self.categories.keys():
            category_file = self.curriculum_dir / f"{category_name.lower().replace(' ', '_')}.txt"
            if category_file.exists():
                with open(category_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract text IDs from content
                    for text_id in self.completed:
                        if text_id in content.lower():
                            text_to_category[text_id] = category_name
                            self.category_index[category_name].append(text_id)
        
        # Load each text (search in subdirectories)
        for text_id in self.completed:
            # Try finding the file in any subdirectory
            found = False
            for subdir in self.curriculum_dir.iterdir():
                if subdir.is_dir():
                    text_file = subdir / f"{text_id}.txt"
                    if text_file.exists():
                        try:
                            with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                
                                self.text_index[text_id] = {
                                    'content': content,
                                    'word_count': len(content.split()),
                                    'category': text_to_category.get(text_id, subdir.name),
                                    'path': str(text_file)
                                }
                                found = True
                                break
                        except Exception as e:
                            print(f"  [WARNING] Could not load {text_id}: {e}")
                            continue
    
    def search_by_keywords(self, keywords: List[str], max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search texts by keywords
        
        Args:
            keywords: List of keywords to search for
            max_results: Maximum number of results
            
        Returns:
            List of matching texts with relevance scores
        """
        results = []
        
        for text_id, data in self.text_index.items():
            content_lower = data['content'].lower()
            
            # Count keyword matches
            matches = sum(1 for kw in keywords if kw.lower() in content_lower)
            
            if matches > 0:
                # Calculate relevance score
                relevance = matches / len(keywords)
                
                # Extract context around keywords
                contexts = []
                for kw in keywords:
                    if kw.lower() in content_lower:
                        idx = content_lower.find(kw.lower())
                        start = max(0, idx - 200)
                        end = min(len(data['content']), idx + 200)
                        context = data['content'][start:end]
                        contexts.append(context)
                
                results.append({
                    'text_id': text_id,
                    'category': data['category'],
                    'relevance': relevance,
                    'matches': matches,
                    'word_count': data['word_count'],
                    'contexts': contexts[:3],  # Top 3 contexts
                    'path': data['path']
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance'], reverse=True)
        
        return results[:max_results]
    
    def search_by_category(self, category: str) -> List[str]:
        """
        Get all texts in a category
        
        Args:
            category: Category name
            
        Returns:
            List of text IDs
        """
        return self.category_index.get(category, [])
    
    def get_text_content(self, text_id: str, max_chars: int = None) -> str:
        """
        Get full content of a text
        
        Args:
            text_id: Text identifier
            max_chars: Maximum characters to return (None = all)
            
        Returns:
            Text content
        """
        if text_id not in self.text_index:
            return f"Text '{text_id}' not found"
        
        content = self.text_index[text_id]['content']
        
        if max_chars:
            return content[:max_chars]
        
        return content
    
    def query_for_context(self, query: str, max_texts: int = 5, context_chars: int = 1000) -> List[Dict[str, Any]]:
        """
        Query curriculum for relevant context
        
        Args:
            query: Natural language query
            max_texts: Maximum texts to return
            context_chars: Characters of context per text
            
        Returns:
            List of relevant text excerpts
        """
        # Extract keywords from query
        keywords = [word.lower() for word in re.findall(r'\b\w+\b', query) if len(word) > 3]
        
        # Search
        results = self.search_by_keywords(keywords, max_results=max_texts)
        
        # Format for context
        context_results = []
        for result in results:
            context_results.append({
                'source': result['text_id'],
                'category': result['category'],
                'relevance': result['relevance'],
                'excerpt': result['contexts'][0] if result['contexts'] else '',
                'full_text_available': True
            })
        
        return context_results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get curriculum statistics"""
        total_words = sum(data['word_count'] for data in self.text_index.values())
        
        category_stats = {}
        for category, texts in self.category_index.items():
            category_words = sum(
                self.text_index[text_id]['word_count'] 
                for text_id in texts 
                if text_id in self.text_index
            )
            category_stats[category] = {
                'texts': len(texts),
                'words': category_words
            }
        
        return {
            'total_texts': len(self.text_index),
            'total_words': total_words,
            'categories': len(self.category_index),
            'category_breakdown': category_stats
        }


def demo_curriculum_rag():
    """Demo the curriculum RAG system"""
    
    rag = CurriculumRAG()
    
    print("\n" + "="*80)
    print("CURRICULUM RAG DEMO")
    print("="*80)
    
    # Statistics
    stats = rag.get_statistics()
    print(f"\nTotal Words: {stats['total_words']:,}")
    print(f"Total Texts: {stats['total_texts']}")
    
    # Example queries
    queries = [
        "consciousness and mind",
        "ethics and morality",
        "nature and evolution",
        "democracy and government"
    ]
    
    for query in queries:
        print(f"\n{'='*80}")
        print(f"Query: {query}")
        print("="*80)
        
        results = rag.query_for_context(query, max_texts=3)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['source']} ({result['category']})")
            print(f"   Relevance: {result['relevance']:.2%}")
            print(f"   Excerpt: {result['excerpt'][:200]}...")


if __name__ == "__main__":
    demo_curriculum_rag()
