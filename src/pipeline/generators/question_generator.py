"""Question generation from document chunks."""
from typing import List, Dict, Any, Optional, Callable
from llama_stack_client import LlamaStackClient
from llama_stack_client.types import UserMessage, SystemMessage
import json
import os

class QuestionGenerator:
    """Generates questions using LLM."""
    
    def __init__(self, client: LlamaStackClient):
        """Initialize with LlamaStack client."""
        self.client = client

    async def generate(self,
                      context: str,
                      progress_callback: Optional[Callable] = None) -> List[Dict[str, Any]]:
        """Generate questions from context."""
        try:
            if progress_callback:
                progress_callback(0.3, "Generating questions...")

            messages = [
                UserMessage(content=self._build_prompt(context), role="user")
            ]
            
            response = self.client.inference.chat_completion(
                model_id="meta-llama/Llama-3.2-3B-Instruct",
                messages=messages,
            )

            if progress_callback:
                progress_callback(0.7, "Processing questions...")
            
            questions = self._parse_response(response.completion_message.content, context)
            
            if progress_callback:
                progress_callback(1.0, "Questions generated successfully!")
            
            return questions
            
        except Exception as e:
            raise ValueError(f"Failed to generate questions: {str(e)}")
        
    def _build_prompt(self, context: str) -> str:
        """Build prompt for question generation."""
        return f"""You are an expert at generating insightful questions.
        Generate 3-5 relevant questions from this context. 
        Include difficulty (basic/intermediate/advanced) and type (factual/conceptual/analytical).
        
        Format as JSON and wrap in <json> tags:
        {{
            "questions": [
                {{
                    "question": "question text",
                    "difficulty": "basic/intermediate/advanced",
                    "type": "factual/conceptual/analytical"
                }}
            ]
        }}
        
        Context:
        {context}"""

    def _parse_response(self, response: str, context: str) -> List[Dict[str, Any]]:
        """Parse response into questions."""
        try:
            # Extract content between <json> tags
            start_tag = "<json>"
            end_tag = "</json>"
            start_index = response.find(start_tag)
            end_index = response.find(end_tag)
            
            if start_index == -1 or end_index == -1:
                raise ValueError("Response does not contain valid <json> tags")
            
            json_str = response[start_index + len(start_tag):end_index].strip()
            data = json.loads(json_str)
            
            return [
                {
                    **q,
                    "context": context,
                    "quality_score": 0.8  # Could be calculated based on metrics
                }
                for q in data["questions"]
            ]
        except Exception as e:
            raise ValueError(f"Failed to parse questions: {str(e)}")