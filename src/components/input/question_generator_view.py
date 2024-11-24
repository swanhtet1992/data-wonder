"""Question generation and display component."""
import streamlit as st
from typing import List, Dict, Any
from ...utils.state_management import get_state, set_state
from ...pipeline.generators.question_generator import QuestionGenerator
from ...pipeline.generators.answer_generator import AnswerGenerator
import pandas as pd

def render_question_generation_view(
    chunks: List[Dict[str, Any]], 
    metadata: Dict[str, Any],
    question_gen: QuestionGenerator,
    answer_gen: AnswerGenerator
) -> None:
    """Render the question generation and display view."""
    
    # Get current state
    current_questions = get_state('current_questions') or []
    current_answers = get_state('current_answers') or []
    
    # Simple stats
    st.caption(f"Generated {len(current_questions)} questions, {len(current_answers)} answers")
    
    # Search filter
    search = st.text_input("🔍 Search questions and answers", key="qa_search")
    
    # Prepare data for table
    data = []
    for i, q in enumerate(current_questions):
        answer = current_answers[i] if i < len(current_answers) else None
        row = {
            "Q#": f"Q{i+1}",
            "Question": q.get('question', ''),
            "Answer": answer.get('answer', "⏳ Generating...") if answer else "⏳ Generating...",
            "Type": q.get('type', '').title(),
            "Difficulty": q.get('difficulty', '').title(),
            "Confidence": f"{answer.get('confidence', 0):.2f}" if answer else "-"
        }
        
        # Apply search filter
        if search:
            if not any(search.lower() in str(v).lower() for v in row.values()):
                continue
        
        data.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Render table with fixed height
    st.dataframe(
        df,
        use_container_width=True,
        height=400,  # Fixed height
        column_config={
            "Q#": st.column_config.Column(width=50),
            "Question": st.column_config.TextColumn(width=300),
            "Answer": st.column_config.TextColumn(width=300),
            "Type": st.column_config.Column(width=100),
            "Difficulty": st.column_config.Column(width=100),
            "Confidence": st.column_config.Column(width=100)
        },
        hide_index=True
    )