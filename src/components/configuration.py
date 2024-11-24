"""Configuration component for data generation settings."""
import streamlit as st
from ..config import DATA_TYPES, MIN_SAMPLES, MAX_SAMPLES, DEFAULT_SAMPLES

def render_configuration_section() -> tuple[str, int]:
    """Render the configuration section and return settings."""
    st.header("⚙️ Configure Generation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        data_type = st.selectbox(
            "Type of Data to Generate",
            DATA_TYPES,
            help="Select the type of data you want to generate"
        )
    
    with col2:
        num_samples = st.number_input(
            "Number of Samples",
            min_value=MIN_SAMPLES,
            max_value=MAX_SAMPLES,
            value=DEFAULT_SAMPLES,
            help="How many synthetic samples to generate"
        )
    
    return data_type, num_samples 