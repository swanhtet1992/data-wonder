"""Base class for LLM providers using llama-stack."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, AsyncGenerator, Union
from llama_stack_client import LlamaStackClient
from llama_stack_client.types import UserMessage

class LLMProvider(ABC):
    """Abstract base class for LLM providers using llama-stack."""
    
    def __init__(self, client: LlamaStackClient):
        """Initialize provider with llama-stack client."""
        self.client = client
        self._model_id = None
    
    @property
    def model_id(self) -> Optional[str]:
        """Get the current model ID."""
        return self._model_id
    
    @model_id.setter
    def model_id(self, value: str):
        """Set the model ID."""
        self._model_id = value
    
    async def list_models(self) -> list[str]:
        """List available models."""
        models_response = self.client.models.list()
        return [model.identifier for model in models_response]
    
    @abstractmethod
    async def generate(self, 
                      prompt: str, 
                      temperature: float = 0.7,
                      max_tokens: Optional[int] = None,
                      stream: bool = False,
                      **kwargs) -> Union[str, AsyncGenerator[str, None]]:
        """Generate text from the LLM."""
        pass
    
    @abstractmethod
    async def generate_batch(self,
                           prompts: list[str],
                           temperature: float = 0.7,
                           max_tokens: Optional[int] = None,
                           **kwargs) -> list[str]:
        """Generate multiple responses in batch."""
        pass
    
    @abstractmethod
    async def validate_connection(self) -> bool:
        """Validate that the provider connection is working."""
        pass 