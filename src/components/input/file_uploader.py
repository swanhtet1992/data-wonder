"""File upload handling component."""
import streamlit as st
from ...utils.file_handlers import load_file
from ...utils.state_management import set_state
from ...config import ALLOWED_EXTENSIONS
from .preview import render_data_preview

def render_file_uploader() -> None:
    """Render the file upload section."""
    st.subheader("📁 Upload Your Dataset")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=ALLOWED_EXTENSIONS,
        help="Upload your existing dataset"
    )
    
    if uploaded_file:
        try:
            data = load_file(uploaded_file)
            set_state('uploaded_data', data)
            set_state('input_type', 'dataset')
            
            st.success("✅ File uploaded successfully!")
            render_data_preview(data)
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}") 