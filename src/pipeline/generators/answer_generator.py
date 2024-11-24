"""Answer generation for questions."""
from typing import List, Dict, Any, Optional, Callable
from llama_stack_client import LlamaStackClient
from llama_stack_client.types import UserMessage, SystemMessage
import json
import os

class AnswerGenerator:
    """Generates answers for questions."""
    
    def __init__(self, client: LlamaStackClient):
        """Initialize with LlamaStack client."""
        self.client = client
    
    async def generate(self,
                      questions: List[Dict[str, Any]],
                      progress_callback: Optional[Callable] = None) -> List[Dict[str, Any]]:
        """Generate answers for questions."""
        answers = []
        total = len(questions)
        
        try:
            for i, question in enumerate(questions):
                if progress_callback:
                    progress = i / total
                    progress_callback(progress, f"Generating answer {i+1}/{total}")
                
                messages = [
                    UserMessage(content=self._build_prompt(question), role="user")
                ]
                
                response = self.client.inference.chat_completion(
                    model_id="meta-llama/Llama-3.2-3B-Instruct",
                    messages=messages
                )
                
                answer = self._parse_response(response.completion_message.content)
                answers.append(answer)
            
            if progress_callback:
                progress_callback(1.0, "All answers generated!")
            
            return answers
            
        except Exception as e:
            raise ValueError(f"Failed to generate answers: {str(e)}")
    
    def _build_prompt(self, question: Dict[str, Any]) -> str:
        """Build prompt for answer generation."""
        return f"""Answer this question based on the given context.
        Format as complete JSON object and wrap in <json> tags:
        <json>
        {{
            "answer": "detailed answer here",
            "explanation": "reasoning or additional context",
            "confidence": 0.0-1.0
        }}
        </json>

        Context: {question['context']}
        Question: {question['question']}"""
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse response into answer."""
        try:
            # Get content between <json> tags
            content = response.split("<json>")[1].split("</json>")[0].strip()
            
            # Extract fields
            answer = content.split('"answer": "')[1].split('",')[0]
            explanation = content.split('"explanation": "')[1].split('",')[0]
            confidence = float(content.split('"confidence": ')[1].split('}')[0])
            
            return {
                "answer": answer,
                "explanation": explanation,
                "confidence": confidence
            }
        except Exception as e:
            raise ValueError(f"Failed to parse answer: {str(e)}") 