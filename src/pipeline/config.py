"""Pipeline configuration."""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from .providers.interfaces import ProviderConfig

@dataclass
class PipelineConfig:
    """Configuration for the entire pipeline."""
    
    # Provider configurations
    llm_provider: ProviderConfig = field(default_factory=ProviderConfig)
    memory_provider: ProviderConfig = field(default_factory=ProviderConfig)
    embedding_provider: ProviderConfig = field(default_factory=ProviderConfig)
    
    # Processing settings
    chunk_size_tokens: int = 512
    overlap_tokens: int = 64
    min_chunk_size: int = 100
    max_chunk_size: int = 2000
    
    # Generation settings
    questions_per_chunk: int = 3
    temperature: float = 0.7
    max_tokens: int = 1000
    quality_threshold: float = 0.7
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'PipelineConfig':
        """Create config from dictionary."""
        return cls(**config_dict) 