"""Q&A pair generator implementation."""
from typing import Any, Dict, List, Optional, AsyncGenerator, Union
import json
from .base import DataGenerator, ProgressCallback

class QAGenerator(DataGenerator):
    """Generator for question-answer pairs."""
    
    DEFAULT_CONFIG = {
        "num_pairs": 5,
        "temperature": 0.7,
        "max_tokens": 2000,
        "quality_threshold": 0.7,
        "generation_type": "synthetic",  # or "traditional"
    }
    
    async def generate(self,
                      input_data: str,
                      config: Dict[str, Any],
                      stream: bool = False,
                      progress_callback: Optional[ProgressCallback] = None
                      ) -> Union[List[Dict[str, Any]], AsyncGenerator[Dict[str, Any], None]]:
        """Generate Q&A pairs from input text."""
        if not self.validate_input(input_data):
            raise ValueError("Invalid input data")
        
        # Merge with default config
        full_config = {**self.DEFAULT_CONFIG, **config}
        if not self.validate_config(full_config):
            raise ValueError("Invalid configuration")
        
        await self._report_progress(0.1, "Starting generation...", progress_callback)
        
        if full_config["generation_type"] == "synthetic":
            return await self._generate_synthetic(input_data, full_config, stream, progress_callback)
        else:
            return await self._generate_traditional(input_data, full_config, stream, progress_callback)
    
    async def _generate_synthetic(self,
                                input_data: str,
                                config: Dict[str, Any],
                                stream: bool,
                                progress_callback: Optional[ProgressCallback]
                                ) -> Union[List[Dict[str, Any]], AsyncGenerator[Dict[str, Any], None]]:
        """Generate using llama-stack's synthetic data generation."""
        synthetic_config = {
            "format": "qa_pairs",
            "num_samples": config["num_pairs"],
            "temperature": config["temperature"],
            "max_tokens": config["max_tokens"],
            "quality_threshold": config["quality_threshold"]
        }
        
        prompt = self._create_synthetic_prompt(input_data, config["num_pairs"])
        
        await self._report_progress(0.3, "Generating synthetic data...", progress_callback)
        
        if stream:
            async def stream_generator():
                response = await self.provider.generate_synthetic_data(prompt, synthetic_config)
                for idx, pair in enumerate(response.get("qa_pairs", [])):
                    progress = 0.3 + (0.7 * (idx + 1) / config["num_pairs"])
                    await self._report_progress(
                        progress,
                        f"Generated pair {idx + 1}/{config['num_pairs']}",
                        progress_callback
                    )
                    yield pair
            return stream_generator()
        else:
            response = await self.provider.generate_synthetic_data(prompt, synthetic_config)
            await self._report_progress(1.0, "Generation complete!", progress_callback)
            return response.get("qa_pairs", [])
    
    async def _generate_traditional(self,
                                  input_data: str,
                                  config: Dict[str, Any],
                                  stream: bool,
                                  progress_callback: Optional[ProgressCallback]
                                  ) -> Union[List[Dict[str, Any]], AsyncGenerator[Dict[str, Any], None]]:
        """Generate using traditional prompt-based approach."""
        prompt = self._create_generation_prompt(input_data, config["num_pairs"])
        
        await self._report_progress(0.3, "Generating Q&A pairs...", progress_callback)
        
        if stream:
            async def stream_generator():
                async for chunk in self.provider.generate(
                    prompt=prompt,
                    temperature=config["temperature"],
                    max_tokens=config["max_tokens"],
                    stream=True
                ):
                    try:
                        qa_pair = json.loads(chunk)
                        yield qa_pair
                    except json.JSONDecodeError:
                        continue
            return stream_generator()
        else:
            response = await self.provider.generate(
                prompt=prompt,
                temperature=config["temperature"],
                max_tokens=config["max_tokens"]
            )
            await self._report_progress(1.0, "Generation complete!", progress_callback)
            return self._parse_response(response)
    
    def _create_synthetic_prompt(self, text: str, num_pairs: int) -> str:
        """Create prompt for synthetic data generation."""
        return f"""Generate {num_pairs} high-quality question-answer pairs from this text.
        Each pair should test understanding of key concepts.
        
        Text: {text}
        
        Requirements:
        - Questions should be diverse and engaging
        - Answers should be accurate and comprehensive
        - Include both factual and analytical questions
        - Ensure natural language and proper grammar
        """
    
    def _create_generation_prompt(self, text: str, num_pairs: int) -> str:
        """Create prompt for traditional generation."""
        return f"""Given the following text, generate {num_pairs} question-answer pairs.
        Return the pairs in JSON format with 'question' and 'answer' fields.
        
        Text: {text}
        
        Generate detailed, diverse questions that test understanding of the text.
        Format the response as a JSON array of objects like this:
        [
            {{"question": "...", "answer": "..."}},
            {{"question": "...", "answer": "..."}}
        ]
        """
    
    def _parse_response(self, response: str) -> List[Dict[str, str]]:
        """Parse and validate the generated response."""
        try:
            qa_pairs = json.loads(response)
            # Validate format
            for pair in qa_pairs:
                if not isinstance(pair, dict) or \
                   'question' not in pair or \
                   'answer' not in pair:
                    raise ValueError("Invalid Q&A pair format")
            return qa_pairs
        except json.JSONDecodeError:
            raise ValueError("Generated response is not valid JSON")
    
    def validate_input(self, input_data: Any) -> bool:
        """Validate input text."""
        return isinstance(input_data, str) and len(input_data.strip()) > 0
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate generation configuration."""
        required_keys = {"num_pairs", "temperature", "max_tokens", "quality_threshold", "generation_type"}
        if not all(key in config for key in required_keys):
            return False
        
        return (
            isinstance(config["num_pairs"], int) and 
            0 < config["num_pairs"] <= 100 and
            0 <= config["temperature"] <= 1 and
            isinstance(config["max_tokens"], int) and
            0 <= config["quality_threshold"] <= 1 and
            config["generation_type"] in {"synthetic", "traditional"}
        )