"""Component for viewing document chunks and generating questions."""
import streamlit as st
from typing import List, Dict, Any
from .chunk_organizer import render_organized_chunks
from .question_generator_view import render_question_generation_view
from src.pipeline.generators.question_generator import QuestionGenerator
from src.pipeline.generators.answer_generator import AnswerGenerator

def render_chunk_viewer(chunks: List[Dict[str, Any]], metadata: Dict[str, Any], question_gen: QuestionGenerator, answer_gen: AnswerGenerator) -> None:
    """Render a viewer for document chunks and metadata."""
    # Create tabs for chunks and questions
    tab1, tab2 = st.tabs(["📄 Document Chunks", "❓ Generated Questions"])
    
    with tab1:
        render_organized_chunks(chunks, metadata)
    
    with tab2:
        render_question_generation_view(chunks, metadata, question_gen, answer_gen)