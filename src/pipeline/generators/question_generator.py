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
        prompt = f"""You are a question generation AI tasked with creating a single, focused question based on provided context. Here's the context you'll be working with:
                <context>
                {context}
                </context>

                Your goal is to generate one question that can be fully answered using the information in the context above. Follow these guidelines:

                1. Ensure the question is self-contained and understandable without the context.
                2. The answer must be fully contained within the given context.
                3. Focus on important or relevant information from the context.
                4. Avoid using phrases like "provided context" in the question.
                5. Keep the question concise, using no more than 10 words.
                6. Use abbreviations where appropriate to keep the question concise.

                Before generating the final question, follow these steps:

                1. Identify and list 3-5 key pieces of information from the context.
                2. Based on these key points, brainstorm 3 potential questions.
                3. For each potential question, evaluate how well it meets the guidelines above.
                4. Choose the best question that adheres to all guidelines, or refine one of the questions to meet all criteria.
                
                Include difficulty (basic/intermediate/advanced) and type (factual/conceptual/analytical).

                After completing your thought proces, write your final question as below:
                <json>
                  {{"questions": [
                      {{
                          "question": "question text",
                          "difficulty": "basic/intermediate/advanced",
                          "type": "factual/conceptual/analytical"
                      }}
                  ]}}
                </json>

                REMEMBER <json> TAGS ARE REQUIRED.
                """

        return prompt
    def _parse_response(self, response: str, context: str) -> List[Dict[str, Any]]:
        print(f"Response: {response}")
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