"""Document processing pipeline for RAG preparation."""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import asyncio

from llama_stack_client import LlamaStackClient
from llama_stack_client.types.memory_insert_params import Document

@dataclass
class ChunkConfig:
    """Configuration for document chunking."""
    chunk_size_tokens: int = 512
    overlap_tokens: int = 64
    embedding_model: str = "all-MiniLM-L6-v2"

class DocumentProcessor:
    """Handles document processing for RAG preparation."""
    
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
    
    async def process_document(self, 
                             content: str, 
                             metadata: Optional[Dict[str, Any]] = None,
                             progress_callback: Optional[callable] = None) -> None:
        """Process a document and store in memory bank."""
        if not self._memory_bank_id:
            raise RuntimeError("Memory bank not initialized")
            
        if progress_callback:
            progress_callback(0.2, "Preparing document...")
        
        # Create document object
        doc = Document(
            document_id=f"doc-{len(content)}", # TODO: Use a better ID strategy
            content=content,
            metadata=metadata or {},
        )
        
        if progress_callback:
            progress_callback(0.5, "Storing document...")
            
        # Store in memory bank
        try:
            self.client.memory.insert(
                bank_id=self._memory_bank_id,
                documents=[doc],
            )
            
            if progress_callback:
                progress_callback(1.0, "Document processed successfully!")
                
        except Exception as e:
            raise RuntimeError(f"Failed to store document: {str(e)}") 