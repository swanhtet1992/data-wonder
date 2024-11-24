"""File upload handling component."""
import streamlit as st
from ...utils.file_handlers import load_file
from ...utils.state_management import set_state, get_state
from ...config import ALLOWED_EXTENSIONS
from ...pipeline.processors.document_processor import DocumentProcessor
from .preview import render_data_preview
import asyncio

async def process_uploaded_file(processor: DocumentProcessor, content: str) -> None:
    """Process an uploaded file with progress tracking."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    def update_progress(progress: float, message: str):
        progress_bar.progress(progress)
        status_text.text(message)
    
    try:
        await processor.process_document(content, progress_callback=update_progress)
        st.success("✅ Document processed successfully!")
    except Exception as e:
        st.error(f"❌ Error processing document: {str(e)}")
    finally:
        progress_bar.empty()
        status_text.empty()

def render_file_uploader(processor: DocumentProcessor) -> None:
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
            
            # Process the document
            if st.button("Process Document"):
                asyncio.run(process_uploaded_file(processor, str(data)))
            
            render_data_preview(data)
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}") 