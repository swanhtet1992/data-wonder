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
            # Split context into chunks if it's not already chunked
            if not isinstance(context, list):
                chunks = [context]
            else:
                chunks = context

            all_questions = []
            total_chunks = len(chunks)

            for i, chunk in enumerate(chunks):
                if progress_callback:
                    progress = i / total_chunks
                    progress_callback(progress, f"Generating questions for chunk {i+1}/{total_chunks}")

                messages = [
                    UserMessage(content=self._build_prompt(chunk), role="user")
                ]
                
                response = self.client.inference.chat_completion(
                    model_id="meta-llama/Llama-3.1-70B-Instruct",
                    messages=messages,
                )

                chunk_questions = self._parse_response(response.completion_message.content, chunk)
                
                # Add chunk index to each question
                for q in chunk_questions:
                    q['chunk_index'] = i
                
                all_questions.extend(chunk_questions)

            if progress_callback:
                progress_callback(1.0, f"Generated {len(all_questions)} questions!")
            
            return all_questions
                
        except Exception as e:
            raise ValueError(f"Failed to generate questions: {str(e)}")
        
    def _build_prompt(self, context: str) -> str:
        """Build prompt for question generation."""
        prompt = f"""You are a question generation AI tasked with creating 2-3 focused questions based on provided context. Here's the context you'll be working with:
                <context>
                {context}
                </context>

                Your goal is to generate 2-3 questions that can be fully answered using the information in the context above. Follow these guidelines:

                1. Ensure each question is self-contained and understandable without the context.
                2. The answers must be fully contained within the given context.
                3. Focus on important or relevant information from the context.
                4. Avoid using phrases like "provided context" in the questions.
                5. Keep questions concise, using no more than 15 words each.
                6. Generate a mix of different difficulty levels and question types.

                Format your response as JSON with <json> tags:
                <json>
                  {{"questions": [
                      {{
                          "question": "First question text",
                          "difficulty": "basic/intermediate/advanced",
                          "type": "factual/conceptual/analytical"
                      }},
                      {{
                          "question": "Second question text",
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