"""Llama Stack provider implementation."""
import os
from typing import Optional, Union, AsyncGenerator
from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.inference.event_logger import EventLogger
from llama_stack_client.types import UserMessage
from .base import LLMProvider

class LlamaStackProvider(LLMProvider):
    """Llama Stack-based provider."""
    
    def __init__(self, 
                 host: str = "localhost",
                 port: int = 5001,
                 model_id: Optional[str] = None):
        """Initialize Llama Stack provider."""
        client = LlamaStackClient(base_url=f"http://{host}:{port}")
        super().__init__(client)
        
        if model_id:
            self.model_id = model_id
    
    async def initialize(self):
        """Initialize the provider and select model if needed."""
        if not self.model_id:
            # Get first available model if none specified
            models = await self.list_models()
            if not models:
                raise ValueError("No models available in the Llama Stack server")
            self.model_id = models[0]
    
    async def generate(self, 
                      prompt: str, 
                      temperature: float = 0.7,
                      max_tokens: Optional[int] = None,
                      stream: bool = False,
                      **kwargs) -> Union[str, AsyncGenerator[str, None]]:
        """Generate text using Llama Stack."""
        await self.initialize()
        
        message = UserMessage(content=prompt, role="user")
        
        response = self.client.inference.chat_completion(
            messages=[message],
            model_id=self.model_id,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            **kwargs
        )
        
        if not stream:
            return response.completion_message.content
        else:
            async for log in EventLogger().log(response):
                yield log.content
    
    async def generate_batch(self,
                           prompts: list[str],
                           temperature: float = 0.7,
                           max_tokens: Optional[int] = None,
                           **kwargs) -> list[str]:
        """Generate multiple responses using Llama Stack."""
        await self.initialize()
        
        # Use batch inference API
        messages = [UserMessage(content=prompt, role="user") for prompt in prompts]
        response = self.client.batch_inference.chat_completion(
            messages=messages,
            model_id=self.model_id,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return [msg.content for msg in response.completions]
    
    async def validate_connection(self) -> bool:
        """Validate Llama Stack connection."""
        try:
            models = await self.list_models()
            return len(models) > 0
        except Exception:
            return False
    
    async def generate_synthetic_data(self,
                                    prompt: str,
                                    config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate synthetic data using Llama Stack's dedicated API."""
        await self.initialize()
        
        response = self.client.synthetic_data_generation.generate(
            prompt=prompt,
            model_id=self.model_id,
            **config
        )
        
        return response.data 