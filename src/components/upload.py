"""Upload component for handling file uploads."""
import streamlit as st
from ..utils.file_handlers import load_file
from ..utils.state_management import set_state
from ..config import ALLOWED_EXTENSIONS

def render_upload_section() -> None:
    """Render the file upload section."""
    st.header("📤 Upload Your Data")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV or TXT file",
        type=ALLOWED_EXTENSIONS,
        help="Upload your existing dataset"
    )
    
    if uploaded_file:
        try:
            data = load_file(uploaded_file)
            set_state('uploaded_data', data)
            st.success("File uploaded successfully!")
            
            st.subheader("Data Preview")
            st.dataframe(data.head())
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}") 