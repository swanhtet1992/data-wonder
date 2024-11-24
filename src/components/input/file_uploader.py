"""File upload handling component."""
import streamlit as st
from ...utils.file_handlers import load_file
from ...utils.state_management import set_state, get_state
from ...config import ALLOWED_EXTENSIONS
from ...pipeline.processors.document_processor import DocumentProcessor
from .preview import render_data_preview
from .chunk_viewer import render_chunk_viewer
import asyncio

async def process_uploaded_file(processor: DocumentProcessor, content: str) -> None:
    """Process an uploaded file with progress tracking."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    def update_progress(progress: float, message: str):
        progress_bar.progress(progress)
        status_text.text(message)
    
    try:
        # Store chunks in session state for visualization
        chunks = processor._chunk_article(content)
        metadata = processor._extract_article_metadata(content)
        
        set_state('current_chunks', chunks)
        set_state('current_metadata', metadata)
        
        # Process the document
        await processor.process_document(
            content, 
            metadata=metadata,
            progress_callback=update_progress
        )
        
        st.success("✅ Document processed successfully!")
        
    except Exception as e:
        st.error(f"❌ Error processing document: {str(e)}")
    finally:
        progress_bar.empty()
        status_text.empty()

def render_file_uploader(processor: DocumentProcessor) -> None:
    """Render the file upload section."""
    st.subheader("📁 Upload Your Dataset")
    
    # Add configuration options
    with st.expander("⚙️ Processing Configuration"):
        with st.form(key="processing_config"):
            col1, col2 = st.columns(2)
            
            with col1:
                chunk_size = st.slider(
                    "Maximum Chunk Size (characters)",
                    min_value=500,
                    max_value=5000,
                    value=2000,
                    step=100,
                    help="Maximum size of each document chunk"
                )
            
            with col2:
                overlap = st.slider(
                    "Chunk Overlap (tokens)",
                    min_value=0,
                    max_value=128,
                    value=64,
                    step=8,
                    help="Number of overlapping tokens between chunks"
                )
            
            chunks_per_page = st.slider(
                "Chunks per Page",
                min_value=3,
                max_value=20,
                value=5,
                step=1,
                help="Number of chunks to show per page"
            )
            
            submit_config = st.form_submit_button("Apply Configuration")
            
            if submit_config:
                processor.config.max_chunk_size = chunk_size
                processor.config.overlap_tokens = overlap
                set_state('chunks_per_page', chunks_per_page)
                st.success("✅ Configuration updated!")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=ALLOWED_EXTENSIONS,
        help="Upload your knowledge base article or dataset"
    )
    
    if uploaded_file:
        try:
            # Load and preview file
            content = load_file(uploaded_file)
            set_state('uploaded_data', content)
            set_state('input_type', 'dataset')
            
            # Show file preview
            if isinstance(content, str):
                with st.expander("📄 File Preview", expanded=True):
                    st.text(content[:1000] + ("..." if len(content) > 1000 else ""))
            else:
                render_data_preview(content)
            
            # Process document button
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("🔄 Process Document", type="primary", use_container_width=True):
                    asyncio.run(process_uploaded_file(processor, str(content)))
            
            # Show chunks if available
            chunks = get_state('current_chunks')
            metadata = get_state('current_metadata')
            if chunks and metadata:
                render_chunk_viewer(chunks, metadata)
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")