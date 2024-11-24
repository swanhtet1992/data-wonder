"""Input components for the Synthetic Data Generator."""
import streamlit as st
from .method_selector import render_method_selector
from .file_uploader import render_file_uploader
from .prompt_editor import render_prompt_editor
from ...pipeline.processors.document_processor import DocumentProcessor

def render_input_section(processor: DocumentProcessor) -> None:
    """
    Render the complete input section.
    
    Args:
        processor: Document processor instance for handling inputs
    """
    st.header("📤 Input Data")
    
    render_method_selector()
    st.markdown("---")
    
    input_method = st.session_state.get('input_method')
    if input_method == 'upload':
        render_file_uploader(processor)
    elif input_method == 'prompt':
        render_prompt_editor() 