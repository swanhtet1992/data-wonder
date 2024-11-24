"""Tests for QA Generator component."""
import pytest
from typing import Dict, Any
from src.pipeline.generators.qa_generator import QAGenerator

@pytest.mark.asyncio
async def test_qa_generator_synthetic(
    qa_generator: QAGenerator,
    sample_text: str,
    sample_config: Dict[str, Any]
):
    """Test synthetic data generation."""
    # Test non-streaming generation
    results = await qa_generator.generate(
        input_data=sample_text,
        config=sample_config,
        stream=False
    )
    
    assert isinstance(results, list)
    assert len(results) > 0
    assert all('question' in pair and 'answer' in pair for pair in results)

@pytest.mark.asyncio
async def test_qa_generator_streaming(
    qa_generator: QAGenerator,
    sample_text: str,
    sample_config: Dict[str, Any]
):
    """Test streaming generation."""
    results = []
    async for pair in await qa_generator.generate(
        input_data=sample_text,
        config=sample_config,
        stream=True
    ):
        results.append(pair)
        assert isinstance(pair, dict)
        assert 'question' in pair
        assert 'answer' in pair

    assert len(results) > 0

@pytest.mark.asyncio
async def test_qa_generator_progress_callback(
    qa_generator: QAGenerator,
    sample_text: str,
    sample_config: Dict[str, Any]
):
    """Test progress callback functionality."""
    progress_updates = []
    
    def progress_callback(progress: float, message: str):
        progress_updates.append((progress, message))
    
    await qa_generator.generate(
        input_data=sample_text,
        config=sample_config,
        progress_callback=progress_callback
    )
    
    assert len(progress_updates) > 0
    assert progress_updates[-1][0] == 1.0  # Final progress should be 100%

def test_qa_generator_validate_config(qa_generator: QAGenerator):
    """Test configuration validation."""
    # Valid config
    valid_config = {
        "num_pairs": 5,
        "temperature": 0.7,
        "max_tokens": 1000,
        "quality_threshold": 0.8,
        "generation_type": "synthetic"
    }
    assert qa_generator.validate_config(valid_config) is True
    
    # Invalid config - missing field
    invalid_config = {
        "num_pairs": 5,
        "temperature": 0.7
    }
    assert qa_generator.validate_config(invalid_config) is False
    
    # Invalid config - wrong value type
    invalid_config = {
        "num_pairs": "5",  # should be int
        "temperature": 0.7,
        "max_tokens": 1000,
        "quality_threshold": 0.8,
        "generation_type": "synthetic"
    }
    assert qa_generator.validate_config(invalid_config) is False

def test_qa_generator_validate_input(qa_generator: QAGenerator):
    """Test input validation."""
    assert qa_generator.validate_input("Valid input text") is True
    assert qa_generator.validate_input("") is False
    assert qa_generator.validate_input(None) is False
    assert qa_generator.validate_input(123) is False 