"""Document processing pipeline for article/knowledge base data."""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import asyncio
import hashlib
import re
from datetime import datetime

from llama_stack_client import LlamaStackClient
from llama_stack_client.types.memory_insert_params import Document

@dataclass
class ChunkConfig:
    """Configuration for document chunking."""
    chunk_size_tokens: int = 512
    overlap_tokens: int = 64
    embedding_model: str = "all-MiniLM-L6-v2"
    min_chunk_size: int = 100  # Minimum characters per chunk
    max_chunk_size: int = 2000  # Maximum characters per chunk

class DocumentProcessor:
    """Handles document processing for knowledge base articles."""
    
    def __init__(self, client: LlamaStackClient, config: Optional[ChunkConfig] = None):
        """Initialize processor with LlamaStack client."""
        self.client = client
        self.config = config or ChunkConfig()
        self._memory_bank_id = None
    
    async def initialize_memory_bank(self, bank_id: str) -> None:
        """Initialize or get existing memory bank."""
        try:
            # Get first available memory provider
            providers = self.client.providers.list()
            provider_id = providers["memory"][0].provider_id
            
            # Register memory bank
            self.client.memory_banks.register(
                memory_bank_id=bank_id,
                params={
                    "embedding_model": self.config.embedding_model,
                    "chunk_size_in_tokens": self.config.chunk_size_tokens,
                    "overlap_size_in_tokens": self.config.overlap_tokens,
                },
                provider_id=provider_id,
            )
            
            self._memory_bank_id = bank_id
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize memory bank: {str(e)}")
    
    def _extract_article_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from article content."""
        metadata = {
            "processed_at": datetime.utcnow().isoformat(),
            "char_count": len(content),
            "estimated_reading_time": len(content.split()) / 200  # Assuming 200 wpm
        }
        
        # Try to extract title from first line
        lines = content.split('\n')
        if lines:
            potential_title = lines[0].strip()
            if len(potential_title) < 200:  # Reasonable title length
                metadata["title"] = potential_title
        
        return metadata
    
    def _generate_document_id(self, content: str, chunk_index: int = 0) -> str:
        """Generate a stable document ID based on content hash."""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        return f"article-{timestamp}-{content_hash}-chunk{chunk_index}"
    
    def _chunk_article(self, content: str) -> List[Dict[str, Any]]:
        """Split article into semantic chunks."""
        chunks = []
        
        # Split into paragraphs first
        paragraphs = re.split(r'\n\s*\n', content)
        
        current_chunk = []
        current_size = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            para_size = len(para)
            
            # If paragraph itself exceeds max size, split it
            if para_size > self.config.max_chunk_size:
                # Add current chunk if it exists
                if current_chunk:
                    chunks.append({
                        "content": "\n\n".join(current_chunk),
                        "size": current_size
                    })
                    current_chunk = []
                    current_size = 0
                
                # Split large paragraph
                sentences = re.split(r'(?<=[.!?])\s+', para)
                temp_chunk = []
                temp_size = 0
                
                for sentence in sentences:
                    if temp_size + len(sentence) > self.config.max_chunk_size:
                        if temp_chunk:
                            chunks.append({
                                "content": " ".join(temp_chunk),
                                "size": temp_size
                            })
                        temp_chunk = [sentence]
                        temp_size = len(sentence)
                    else:
                        temp_chunk.append(sentence)
                        temp_size += len(sentence)
                
                if temp_chunk:
                    chunks.append({
                        "content": " ".join(temp_chunk),
                        "size": temp_size
                    })
                    
            # Normal paragraph handling
            elif current_size + para_size > self.config.max_chunk_size:
                chunks.append({
                    "content": "\n\n".join(current_chunk),
                    "size": current_size
                })
                current_chunk = [para]
                current_size = para_size
            else:
                current_chunk.append(para)
                current_size += para_size
        
        # Add final chunk
        if current_chunk:
            chunks.append({
                "content": "\n\n".join(current_chunk),
                "size": current_size
            })
        
        return chunks
    
    async def process_document(self, 
                             content: str, 
                             metadata: Optional[Dict[str, Any]] = None,
                             progress_callback: Optional[callable] = None) -> None:
        """Process an article and store in memory bank."""
        if not self._memory_bank_id:
            raise RuntimeError("Memory bank not initialized")
            
        if progress_callback:
            progress_callback(0.1, "Extracting metadata...")
        
        # Extract and merge metadata
        article_metadata = self._extract_article_metadata(content)
        if metadata:
            article_metadata.update(metadata)
            
        if progress_callback:
            progress_callback(0.2, "Chunking article...")
        
        # Chunk the article
        chunks = self._chunk_article(content)
        total_chunks = len(chunks)
        
        if progress_callback:
            progress_callback(0.3, f"Processing {total_chunks} chunks...")
        
        # Process each chunk
        for i, chunk in enumerate(chunks):
            doc = Document(
                document_id=self._generate_document_id(chunk["content"], i),
                content=chunk["content"],
                metadata={
                    **article_metadata,
                    "chunk_index": i,
                    "total_chunks": total_chunks,
                    "chunk_size": chunk["size"]
                }
            )
            
            try:
                self.client.memory.insert(
                    bank_id=self._memory_bank_id,
                    documents=[doc],
                )
                
                if progress_callback:
                    progress = 0.3 + (0.7 * (i + 1) / total_chunks)
                    progress_callback(progress, f"Processed chunk {i + 1}/{total_chunks}")
                    
            except Exception as e:
                raise RuntimeError(f"Failed to store chunk {i}: {str(e)}")
        
        if progress_callback:
            progress_callback(1.0, "Article processed successfully!")