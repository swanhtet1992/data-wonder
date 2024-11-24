"""Configuration settings for the Synthetic Data Generator."""
from typing import List, Dict

# App settings
APP_TITLE = "🤖 Synthetic Data Generator"
APP_ICON = "🤖"
LAYOUT = "wide"

# Data generation settings
DATA_TYPES = ["Q&A Pairs", "FAQs", "Structured JSON"]
MIN_SAMPLES = 1
MAX_SAMPLES = 1000
DEFAULT_SAMPLES = 10

# Progress steps
GENERATION_STEPS = ["Data Extraction", "Planning", "Generation", "Validation"]

# File settings
ALLOWED_EXTENSIONS = ["csv", "txt", "md", "rst"]
OUTPUT_DIR = "generated_datasets"

# Processing settings
DEFAULT_CHUNK_SIZE = 2000
DEFAULT_OVERLAP = 64
DEFAULT_MIN_CHUNK_SIZE = 100

# Memory bank settings
DEFAULT_MEMORY_BANK = "knowledge_base"
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# About text
ABOUT_TEXT = """
### About
This app helps you generate synthetic data from your existing datasets.

### How to use:
1. Upload your dataset
2. Configure generation settings
3. Generate synthetic data
4. Download results
""" 

# Prompt templates
PROMPT_TEMPLATES = {
    "Q&A Generation": """Generate a Q&A dataset about [topic].
Include:
- Diverse question types (what, why, how)
- Varying complexity levels
- Clear and concise answers
- [Specific requirements]""",

    "Conversation Dataset": """Create a dataset of conversations between [participants].
Format:
- Natural dialogue flow
- Multiple turns
- Different scenarios
- [Specific characteristics]""",

    "Technical Documentation": """Generate technical documentation examples for [subject].
Include:
- API descriptions
- Usage examples
- Error scenarios
- [Technical details]""",
}

# Input validation
MAX_PROMPT_LENGTH = 4000
MIN_PROMPT_LENGTH = 10 