"""Input components for the Synthetic Data Generator."""
import streamlit as st
from .method_selector import render_method_selector
from .file_uploader import render_file_uploader
from .prompt_editor import render_prompt_editor
from ...pipeline.processors.document_processor import DocumentProcessor
from ...pipeline.generators.question_generator import QuestionGenerator
from ...pipeline.generators.answer_generator import AnswerGenerator

def render_input_section(processor: DocumentProcessor,
                         question_gen: QuestionGenerator,
                         answer_gen: AnswerGenerator) -> None:
    """
    Render the complete input section.
    
    Args:
        processor: Document processor instance for handling inputs
        question_gen: Question generator instance for generating questions
        answer_gen: Answer generator instance for generating answers
    """
    st.header("📤 Input Data")
    
    render_method_selector()
    st.markdown("---")
    
    input_method = st.session_state.get('input_method')
    if input_method == 'upload':
        render_file_uploader(processor)
    elif input_method == 'prompt':
        render_prompt_editor(question_gen, answer_gen) 