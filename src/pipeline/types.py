"""Shared type definitions for pipeline components."""
from typing import TypeVar, Protocol, Dict, Any, List, Optional, Callable, AsyncGenerator, Union
from dataclasses import dataclass
from datetime import datetime

# Type definitions
DocumentContent = TypeVar('DocumentContent', str, bytes)
ProgressCallback = Callable[[float, str], None]

@dataclass
class ProcessingMetadata:
    """Metadata for document processing."""
    processed_at: datetime
    char_count: int
    estimated_reading_time: float
    title: Optional[str] = None
    source: Optional[str] = None
    
@dataclass
class ProcessingConfig:
    """Configuration for document processing."""
    chunk_size_tokens: int = 512
    overlap_tokens: int = 64
    embedding_model: str = "all-MiniLM-L6-v2"
    min_chunk_size: int = 100
    max_chunk_size: int = 2000

@dataclass
class GenerationConfig:
    """Configuration for question generation."""
    questions_per_chunk: int = 3
    temperature: float = 0.7
    max_tokens: int = 1000
    quality_threshold: float = 0.7
    difficulty_levels: List[str] = None
    question_types: List[str] = None
    
    def __post_init__(self):
        if self.difficulty_levels is None:
            self.difficulty_levels = ["basic", "intermediate", "advanced"]
        if self.question_types is None:
            self.question_types = ["factual", "conceptual", "analytical"]

@dataclass
class DocumentChunk:
    """Represents a chunk of processed document."""
    content: str
    index: int
    size: int
    metadata: Dict[str, Any]

@dataclass
class Question:
    """Represents a generated question."""
    question: str
    explanation: str
    difficulty: str
    type: str
    chunk_index: int
    metadata: Dict[str, Any]

@dataclass
class Answer:
    """Represents a generated answer."""
    answer: str
    explanation: str
    metadata: Dict[str, Any]

class PipelineResult:
    """Result from pipeline processing."""
    def __init__(self):
        self.chunks: List[DocumentChunk] = []
        self.questions: List[Question] = []
        self.metadata: ProcessingMetadata = None
        self.errors: List[str] = [] 