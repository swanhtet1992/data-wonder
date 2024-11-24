"""File upload handling component."""
import streamlit as st
from ...utils.file_handlers import load_file
from ...utils.state_management import set_state, get_state
from ...config import ALLOWED_EXTENSIONS
from ...pipeline.processors.document_processor import DocumentProcessor
from .preview import render_data_preview
from .chunk_viewer import render_chunk_viewer
from .console_view import ConsoleView
import asyncio

async def process_uploaded_file(processor: DocumentProcessor, content: str) -> None:
    """Process an uploaded file with progress tracking."""
    progress_bar = st.progress(0)
    console = ConsoleView(height=400)
    
    def update_progress(progress: float, message: str):
        progress_bar.progress(progress)
        console.log(message, level='progress')
    
    try:
        # Stage 1: Chunking (0-30% progress)
        console.log("Starting document processing...", level='info')
        update_progress(0.1, "Analyzing document structure...")
        
        chunks = processor._chunk_article(content)
        metadata = processor._extract_article_metadata(content)
        
        console.log(f"Document split into {len(chunks)} chunks", level='success')
        set_state('current_chunks', chunks)
        set_state('current_metadata', metadata)
        
        update_progress(0.3, "Document chunking complete")
        
        # Stage 2: Generate questions (30-65% progress)
        question_gen = get_state('question_generator')
        console.log("Starting question generation...", level='info')
        
        def question_progress(progress: float, message: str):
            overall_progress = 0.3 + (progress * 0.35)
            update_progress(overall_progress, f"Generating questions: {message}")
            #console.log(f"Question Generation: {message}", level='progress')
        
        questions = await question_gen.generate(
            context=content,
            progress_callback=question_progress
        )
        
        console.log(f"Generated {len(questions)} questions", level='success')
        set_state('current_questions', questions)
        
        # Stage 3: Generate answers (65-100% progress)
        answer_gen = get_state('answer_generator')
        console.log("Starting answer generation...", level='info')
        
        def answer_progress(progress: float, message: str):
            overall_progress = 0.65 + (progress * 0.35)
            update_progress(overall_progress, f"Generating answers: {message}")
            #console.log(f"Answer Generation: {message}", level='progress')
        
        answers = await answer_gen.generate(
            questions=questions,
            progress_callback=answer_progress
        )
        
        console.log(f"Generated {len(answers)} answers", level='success')
        set_state('current_answers', answers)
        
        update_progress(1.0, "✅ Processing complete!")
        console.log("Document processing completed successfully!", level='success')
        
    except Exception as e:
        error_msg = f"Error processing document: {str(e)}"
        console.log(error_msg, level='error')
        st.error(error_msg)
    finally:
        progress_bar.empty()

def render_file_uploader(processor: DocumentProcessor) -> None:
    """Render the file upload section."""
    # Get required components from session state
    question_gen = st.session_state.get('question_generator')
    answer_gen = st.session_state.get('answer_generator')
    
    if not question_gen or not answer_gen:
        st.error("❌ Components not properly initialized. Please refresh the page.")
        return
    
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
            if content is None:
                st.error("❌ Failed to load file content")
                return
                
            set_state('uploaded_data', content)
            set_state('input_type', 'dataset')
            
            # Show file preview
            if isinstance(content, str):
                with st.expander("📄 File Preview", expanded=True):
                    st.text(content[:1000] + ("..." if len(content) > 1000 else ""))
            else:
                render_data_preview(content)
            
            # Automatically start processing if not already done
            if not get_state('current_chunks'):
                asyncio.run(process_uploaded_file(processor, str(content)))
            
            # Show chunks and Q&A if available
            chunks = get_state('current_chunks')
            metadata = get_state('current_metadata')
            
            if chunks and metadata:
                render_chunk_viewer(chunks, metadata, question_gen, answer_gen)
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.exception(e)  # This will show the full traceback in development