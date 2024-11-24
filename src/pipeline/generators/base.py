"""Base class for data generators."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, AsyncGenerator, Callable, Union
from ..providers.base import LLMProvider

ProgressCallback = Callable[[float, str], None]

class DataGenerator(ABC):
    """Abstract base class for data generators."""
    
    def __init__(self, provider: LLMProvider):
        """Initialize generator with LLM provider."""
        self.provider = provider
    
    @abstractmethod
    async def generate(self, 
                      input_data: Any,
                      config: Dict[str, Any],
                      stream: bool = False,
                      progress_callback: Optional[ProgressCallback] = None
                      ) -> Union[List[Dict[str, Any]], AsyncGenerator[Dict[str, Any], None]]:
        """
        Generate synthetic data.
        
        Args:
            input_data: Input data to base generation on
            config: Configuration for generation
            stream: Whether to stream results
            progress_callback: Optional callback for progress updates
            
        Returns:
            Either a list of generated items or an async generator for streaming
        """
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data format."""
        pass
    
    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate generation configuration."""
        pass
    
    async def _report_progress(self, 
                             progress: float, 
                             message: str,
                             callback: Optional[ProgressCallback] = None) -> None:
        """Report generation progress if callback is provided."""
        if callback:
            callback(progress, message)
    