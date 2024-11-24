"""Test configuration and fixtures."""
import pytest
import asyncio
from typing import AsyncGenerator, Dict, Any
from llama_stack_client import LlamaStackClient
from src.pipeline.providers.llama import LlamaStackProvider
from src.pipeline.generators.qa_generator import QAGenerator

@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def mock_llama_client(mocker):
    """Create a mocked LlamaStack client."""
    mock_client = mocker.Mock(spec=LlamaStackClient)
    
    # Mock models list
    mock_client.models.list.return_value = [
        mocker.Mock(identifier="llama2-7b")
    ]
    
    # Mock chat completion
    mock_completion = mocker.Mock()
    mock_completion.completion_message.content = '{"question": "Test?", "answer": "Answer"}'
    mock_client.inference.chat_completion.return_value = mock_completion
    
    return mock_client

@pytest.fixture
async def llama_provider(mock_llama_client):
    """Create a LlamaStack provider with mocked client."""
    provider = LlamaStackProvider(host="mock", port=1234)
    provider.client = mock_llama_client
    await provider.initialize()
    return provider

@pytest.fixture
def qa_generator(llama_provider):
    """Create a QA Generator instance."""
    return QAGenerator(provider=llama_provider)

@pytest.fixture
def sample_text():
    """Sample input text for testing."""
    return """
    The Python programming language was created by Guido van Rossum and was 
    released in 1991. Python is known for its simplicity and readability, 
    following the principle of "explicit is better than implicit".
    """

@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        "num_pairs": 3,
        "temperature": 0.7,
        "max_tokens": 1000,
        "quality_threshold": 0.8,
        "generation_type": "synthetic"
    } 