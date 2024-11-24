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
        prompt = f"""
                  You are an advanced AI system specialized in generating focused, relevant answers based on provided context. Your task is to create a single, concise answer to a given question using only the information provided.

                  First, carefully read the following context: {question['context']}

                  Now, consider this specific question: {question['question']}

                  Your goal is to generate an answer that adheres to the following guidelines:

                  1. The answer must be fully contained within and based solely on the given context.
                  2. Focus on important or relevant information from the context.
                  3. Keep the answer concise and to the point.
                  4. If the answer cannot be found in the context, clearly state that you cannot answer the question.

                  Before presenting your final answer, follow these steps:

                  1. Identify and quote the most relevant parts of the context.
                  2. List 2-3 potential answers and rate their relevance on a scale of 1-5.
                  3. For each potential answer, explain why it's relevant or not.
                  4. Choose the best answer and explain your reasoning for the final choice.
                  5. Consider how to make the chosen answer as concise as possible without losing essential information.
                  6. Assess your confidence in the answer on a scale of 0.0 to 1.0, explaining the factors that influenced your confidence level.

                  After completing your analysis, present your final answer as below:

                  <json>
                    "answer": "Your concise answer here",
                    "explanation": "Brief explanation of your reasoning",
                    "confidence": 0.0-1.0
                  </json>

                  <json> tags are required.

                  Remember to only use the given context as a source for generating the answer and to be as precise and concise as possible.
                  REMEMBER <json> TAGS ARE REQUIRED.
                  """
        return prompt
    
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