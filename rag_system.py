#!/usr/bin/env python3
"""
RAG System for MS AI Program Site
Indexes site content and provides AI responses using OpenRouter
"""

import os
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib
from typing import List, Dict, Any
import re
from datetime import datetime

class MSRAGSystem:
    def __init__(self):
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.indexed_content = {}
        self.content_chunks = []
        
    def extract_text_from_html(self, html_content: str) -> str:
        """Extract clean text from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk.strip())
        
        return chunks
    
    def index_site_content(self):
        """Index all site content for RAG"""
        print("🔍 Indexing site content...")
        
        # Define content sources
        content_sources = {
            'index': 'index.html',
            'white_paper': 'white-paper.html',
            'course_catalog': 'course-catalog.html',
            'faculty': 'faculty.html',
            'application_form': 'msai_application_form.html'
        }
        
        for source_name, filename in content_sources.items():
            file_path = Path(filename)
            if file_path.exists():
                print(f"   📄 Indexing {filename}...")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Extract text
                text_content = self.extract_text_from_html(html_content)
                
                # Create chunks
                chunks = self.chunk_text(text_content)
                
                # Store content
                self.indexed_content[source_name] = {
                    'filename': filename,
                    'full_text': text_content,
                    'chunks': chunks,
                    'chunk_count': len(chunks)
                }
                
                # Add chunks to global list
                for i, chunk in enumerate(chunks):
                    chunk_id = f"{source_name}_{i}"
                    self.content_chunks.append({
                        'id': chunk_id,
                        'source': source_name,
                        'content': chunk,
                        'chunk_index': i
                    })
                
                print(f"   ✅ Indexed {len(chunks)} chunks from {filename}")
            else:
                print(f"   ⚠️  File not found: {filename}")
        
        print(f"📊 Total chunks indexed: {len(self.content_chunks)}")
        return self.content_chunks
    
    def search_relevant_chunks(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for relevant content chunks using simple keyword matching"""
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        scored_chunks = []
        
        for chunk in self.content_chunks:
            content_lower = chunk['content'].lower()
            content_words = set(content_lower.split())
            
            # Calculate simple relevance score
            word_matches = len(query_words.intersection(content_words))
            total_words = len(query_words)
            relevance_score = word_matches / total_words if total_words > 0 else 0
            
            # Boost score for exact phrase matches
            if query_lower in content_lower:
                relevance_score += 0.5
            
            if relevance_score > 0:
                scored_chunks.append({
                    **chunk,
                    'relevance_score': relevance_score
                })
        
        # Sort by relevance and return top_k
        scored_chunks.sort(key=lambda x: x['relevance_score'], reverse=True)
        return scored_chunks[:top_k]
    
    def get_openrouter_response(self, query: str, context_chunks: List[Dict]) -> str:
        """Get AI response from OpenRouter with context"""
        if not self.openrouter_api_key:
            return "Error: OpenRouter API key not found. Please set OPENROUTER_API_KEY environment variable."
        
        # Prepare context
        context_text = "\n\n".join([
            f"Source: {chunk['source']}\nContent: {chunk['content']}"
            for chunk in context_chunks
        ])
        
        # Create prompt
        system_prompt = """You are AurAI, the AI assistant for the MS AI Program at AURNOVA University. You help prospective students, current students, and faculty with questions about the program.

Use the provided context to answer questions accurately. If the context doesn't contain enough information, say so and suggest contacting the admissions office.

Be helpful, professional, and encouraging. Emphasize the program's unique features like:
- AI tutoring for non-CS backgrounds
- Co-evolutionary learning with personal AI companions
- 24/7 AI teaching assistants
- Comprehensive curriculum
- Industry partnerships

Always maintain a positive, supportive tone."""

        user_prompt = f"""Context about the MS AI Program:

{context_text}

Question: {query}

Please provide a helpful, accurate response based on the context above."""

        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.openrouter_api_key, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            return f"Error calling OpenRouter API: {str(e)}"
        except KeyError as e:
            return f"Error parsing OpenRouter response: {str(e)}"
    
    def query(self, question: str) -> Dict[str, Any]:
        """Main query function that combines RAG with OpenRouter"""
        print(f"🤖 Processing query: {question}")
        
        # Search for relevant chunks
        relevant_chunks = self.search_relevant_chunks(question, top_k=5)
        
        if not relevant_chunks:
            return {
                'answer': "I couldn't find relevant information in our knowledge base. Please try rephrasing your question or contact our admissions office directly.",
                'sources': [],
                'chunks_used': 0
            }
        
        # Get AI response
        ai_response = self.get_openrouter_response(question, relevant_chunks)
        
        # Prepare sources
        sources = list(set([chunk['source'] for chunk in relevant_chunks]))
        
        return {
            'answer': ai_response,
            'sources': sources,
            'chunks_used': len(relevant_chunks),
            'relevance_scores': [chunk['relevance_score'] for chunk in relevant_chunks]
        }
    
    def save_index(self, filename: str = "rag_index.json"):
        """Save the indexed content for future use"""
        index_data = {
            'timestamp': datetime.now().isoformat(),
            'content_chunks': self.content_chunks,
            'indexed_sources': list(self.indexed_content.keys())
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2)
        
        print(f"💾 Index saved to {filename}")
    
    def load_index(self, filename: str = "rag_index.json"):
        """Load previously saved index"""
        if Path(filename).exists():
            with open(filename, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            self.content_chunks = index_data['content_chunks']
            print(f"📂 Loaded index with {len(self.content_chunks)} chunks")
            return True
        return False

def main():
    """Test the RAG system"""
    rag = MSRAGSystem()
    
    # Check for API key
    if not rag.openrouter_api_key:
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        print("Please set your OpenRouter API key:")
        print("export OPENROUTER_API_KEY='your-api-key-here'")
        return
    
    # Try to load existing index, otherwise create new one
    if not rag.load_index():
        print("🔄 Creating new index...")
        rag.index_site_content()
        rag.save_index()
    
    # Test queries
    test_queries = [
        "What is the MS AI program about?",
        "How much does the program cost?",
        "Do I need a computer science background?",
        "What are the admission requirements?",
        "Tell me about the AI tutoring system",
        "What courses are required?",
        "How long is the program?",
        "What are the career outcomes?"
    ]
    
    print("\n🧪 Testing RAG system with sample queries...")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n❓ Query: {query}")
        result = rag.query(query)
        print(f"📝 Answer: {result['answer'][:200]}...")
        print(f"📚 Sources: {', '.join(result['sources'])}")
        print(f"🔍 Chunks used: {result['chunks_used']}")
        print("-" * 40)

if __name__ == "__main__":
    main()