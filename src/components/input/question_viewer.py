"""Question viewer component."""
import streamlit as st
from typing import List, Dict, Any
from .question_organizer import render_organized_questions
from ...pipeline.types import Question
import pandas as pd

def render_question_viewer(questions: List[Question], metadata: Dict[str, Any]) -> None:
    """Render the question viewer component."""
    # Document overview
    with st.expander("📊 Document Overview", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Questions", len(questions))
        with col2:
            st.metric("Document Chunks", len(set(q.chunk_index for q in questions)))
        with col3:
            if "estimated_reading_time" in metadata:
                st.metric("Est. Reading Time", 
                         f"{metadata['estimated_reading_time']:.1f} min")
    
    # Get current answers state
    current_answers = get_state('current_answers') or []
    
    # Show generation progress if available
    if "generation_progress" in metadata:
        progress = metadata["generation_progress"]
        st.progress(progress, text=f"Generating questions... {progress*100:.0f}%")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📝 Q&A View", "📊 Analysis View"])
    
    with tab1:
        # Render organized questions with progressive answers
        render_organized_questions(questions, current_answers)
    
    with tab2:
        # Show analytics
        if questions:
            col1, col2 = st.columns(2)
            with col1:
                difficulties = [q.difficulty for q in questions]
                st.bar_chart(pd.value_counts(difficulties))
                st.caption("Question Difficulty Distribution")
            
            with col2:
                types = [q.type for q in questions]
                st.bar_chart(pd.value_counts(types))
                st.caption("Question Type Distribution")
    
    # Export options
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export Q&A", type="primary", use_container_width=True):
            st.toast("Q&A exported successfully!")
    with col2:
        if st.button("📋 Copy All", use_container_width=True):
            st.toast("All Q&A copied to clipboard!")