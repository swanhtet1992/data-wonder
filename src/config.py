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
ALLOWED_EXTENSIONS = ["csv", "txt"]
OUTPUT_DIR = "generated_datasets"

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