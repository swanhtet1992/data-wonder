"""Question organization and display component."""
import streamlit as st
from typing import List, Dict, Any
import pandas as pd
from ...pipeline.types import Question

def render_question_filters() -> Dict[str, List[str]]:
    """Render filter controls for questions."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        difficulties = st.multiselect(
            "Filter by Difficulty",
            options=["basic", "intermediate", "advanced"],
            default=["basic", "intermediate", "advanced"],
            key="difficulty_filter"
        )
    
    with col2:
        types = st.multiselect(
            "Filter by Type",
            options=["factual", "conceptual", "analytical"],
            default=["factual", "conceptual", "analytical"],
            key="type_filter"
        )
    
    with col3:
        quality_threshold = st.slider(
            "Minimum Quality Score",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            key="quality_filter"
        )
    
    return {
        "difficulties": difficulties,
        "types": types,
        "quality_threshold": quality_threshold
    }

def render_question_stats(questions: List[Question]) -> None:
    """Render statistical overview of questions."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Questions", len(questions))
    
    with col2:
        avg_quality = sum(q.quality_score for q in questions) / len(questions) if questions else 0
        st.metric("Average Quality", f"{avg_quality:.2f}")
    
    with col3:
        difficulty_dist = {d: sum(1 for q in questions if q.difficulty == d) 
                         for d in ["basic", "intermediate", "advanced"]}
        most_common = max(difficulty_dist.items(), key=lambda x: x[1])[0]
        st.metric("Most Common Difficulty", most_common.title())
    
    with col4:
        type_dist = {t: sum(1 for q in questions if q.type == t)
                    for t in ["factual", "conceptual", "analytical"]}
        most_common = max(type_dist.items(), key=lambda x: x[1])[0]
        st.metric("Most Common Type", most_common.title())

def render_question_card(question: Question, index: int) -> None:
    """Render a single question card."""
    with st.expander(f"Q{index + 1}: {question.question}", expanded=index == 0):
        st.markdown("**Answer:**")
        st.write(question.answer)
        
        if question.explanation:
            st.markdown("**Explanation:**")
            st.write(question.explanation)
        
        # Metadata and quality score
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.caption(f"Difficulty: {question.difficulty.title()}")
        with col2:
            st.caption(f"Type: {question.type.title()}")
        with col3:
            st.caption(f"Quality: {question.quality_score:.2f}")
        with col4:
            st.caption(f"Chunk: {question.chunk_index + 1}")
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("📋 Copy", key=f"copy_q_{index}"):
                st.toast("Question copied to clipboard!")
        with col2:
            if st.button("⭐ Favorite", key=f"fav_q_{index}"):
                st.toast("Added to favorites!")

def render_organized_questions(questions: List[Question], current_answers: List[Dict[str, Any]] = None) -> None:
    """Render questions with organization options."""
    st.subheader("🤔 Generated Questions")
    
    # Render filters
    filters = render_question_filters()
    
    # Apply filters
    filtered_questions = [
        q for q in questions
        if (q.difficulty in filters["difficulties"] and
            q.type in filters["types"] and
            q.quality_score >= filters["quality_threshold"])
    ]
    
    # Show statistics
    render_question_stats(filtered_questions)
    
    # Organization options
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox(
            "Sort Questions By",
            ["Chunk Index", "Difficulty", "Type", "Quality Score"],
            key="question_sort"
        )
    
    with col2:
        view_mode = st.radio(
            "View Mode",
            ["Cards", "Table"],
            horizontal=True,
            key="question_view_mode"
        )
    
    # Sort questions
    sorted_questions = sort_questions(filtered_questions, sort_by)
    
    if view_mode == "Cards":
        # Render as expandable cards with progressive answers
        for i, question in enumerate(sorted_questions):
            with st.expander(f"Q{i+1}: {question.question}", expanded=i==0):
                render_question_card_content(question, i, current_answers)
    else:
        # Render as table with answer status
        render_questions_table(sorted_questions, current_answers)

def render_question_card_content(question: Question, index: int, current_answers: List[Dict[str, Any]] = None) -> None:
    """Render content for a single question card."""
    st.markdown("**Question:**")
    st.write(question.question)
    
    # Show answer if available
    if current_answers and index < len(current_answers):
        answer = current_answers[index]
        st.markdown("**Answer:**")
        st.write(answer['content'])
        
        if 'explanation' in answer:
            st.markdown("**Explanation:**")
            st.write(answer['explanation'])
        
        if 'confidence' in answer:
            st.metric("Confidence", f"{answer['confidence']:.2f}")
    else:
        with st.spinner("Generating answer..."):
            st.info("Answer will appear here soon...")
    
    # Metadata and quality score
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"Difficulty: {question.difficulty.title()}")
    with col2:
        st.caption(f"Type: {question.type.title()}")
    with col3:
        st.caption(f"Quality: {question.quality_score:.2f}")

def render_questions_table(questions: List[Question], current_answers: List[Dict[str, Any]] = None) -> None:
    """Render questions and answers in table format."""
    data = []
    for i, q in enumerate(questions):
        answer_status = "Pending..."
        answer_content = ""
        confidence = None
        
        if current_answers and i < len(current_answers):
            answer_content = current_answers[i]['content']
            answer_status = "Complete"
            confidence = current_answers[i].get('confidence', 0.0)
        
        data.append({
            "Question": q.question,
            "Answer": answer_content or answer_status,
            "Difficulty": q.difficulty.title(),
            "Type": q.type.title(),
            "Quality": f"{q.quality_score:.2f}",
            "Confidence": confidence if confidence is not None else "N/A"
        })
    
    df = pd.DataFrame(data)
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "Question": st.column_config.TextColumn(
                "Question",
                width="large"
            ),
            "Answer": st.column_config.TextColumn(
                "Answer",
                width="large"
            ),
            "Confidence": st.column_config.NumberColumn(
                "Confidence",
                format="%.2f"
            )
        }
    ) 