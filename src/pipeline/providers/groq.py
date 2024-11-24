"""Groq LLM provider implementation."""
import os
from typing import Optional
from groq import AsyncGroq
from .base import LLMProvider

class GroqProvider(LLMProvider):
    """Groq-based LLM provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama2-70b-4096"):
        """Initialize Groq provider."""
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API key not provided")
        
        self.model = model
        self.client = AsyncGroq(api_key=self.api_key)
    
    async def generate(self, 
                      prompt: str, 
                      temperature: float = 0.7,
                      max_tokens: Optional[int] = None,
                      **kwargs) -> str:
        """Generate text using Groq."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    async def generate_batch(self,
                           prompts: list[str],
                           temperature: float = 0.7,
                           max_tokens: Optional[int] = None,
                           **kwargs) -> list[str]:
        """Generate multiple responses using Groq."""
        # Implement batching logic - could use asyncio.gather for parallel requests
        responses = []
        for prompt in prompts:
            response = await self.generate(
                prompt, 
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            responses.append(response)
        return responses
    
    def validate_connection(self) -> bool:
        """Validate Groq connection."""
        try:
            # Simple validation - could be enhanced
            return bool(self.api_key and self.client)
        except Exception:
            return False 