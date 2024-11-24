"""Progress tracking component."""
import streamlit as st
from ..utils.state_management import get_state
from ..config import GENERATION_STEPS

def render_progress_section() -> None:
    """Render the progress tracking section."""
    st.header("🔄 Generation Progress")
    
    current_step = get_state('generation_step')
    
    # Progress bar
    progress_bar = st.progress(current_step / len(GENERATION_STEPS))
    
    # Step indicator
    columns = st.columns(len(GENERATION_STEPS))
    
    for idx, (col, step) in enumerate(zip(columns, GENERATION_STEPS)):
        with col:
            if idx < current_step:
                st.success(step)
            elif idx == current_step:
                st.info(step)
            else:
                st.text(step) 