"""Tests for LlamaStack Provider component."""
import pytest
from src.pipeline.providers.llama import LlamaStackProvider

@pytest.mark.asyncio
async def test_provider_initialization(mock_llama_client):
    """Test provider initialization."""
    provider = LlamaStackProvider(host="mock", port=1234)
    provider.client = mock_llama_client
    
    await provider.initialize()
    assert provider.model_id == "llama2-7b"

@pytest.mark.asyncio
async def test_provider_generate(llama_provider):
    """Test text generation."""
    response = await llama_provider.generate(
        prompt="Test prompt",
        temperature=0.7
    )
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.asyncio
async def test_provider_generate_stream(llama_provider):
    """Test streaming generation."""
    chunks = []
    async for chunk in await llama_provider.generate(
        prompt="Test prompt",
        temperature=0.7,
        stream=True
    ):
        chunks.append(chunk)
        assert isinstance(chunk, str)
    
    assert len(chunks) > 0

@pytest.mark.asyncio
async def test_provider_generate_batch(llama_provider):
    """Test batch generation."""
    prompts = ["Test 1", "Test 2", "Test 3"]
    responses = await llama_provider.generate_batch(
        prompts=prompts,
        temperature=0.7
    )
    
    assert isinstance(responses, list)
    assert len(responses) == len(prompts)
    assert all(isinstance(r, str) for r in responses)

@pytest.mark.asyncio
async def test_provider_validate_connection(llama_provider):
    """Test connection validation."""
    assert await llama_provider.validate_connection() is True 