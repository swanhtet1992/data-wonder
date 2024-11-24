"""Input method selection component."""
import streamlit as st
from ...utils.state_management import set_state, get_state

def render_method_card(title: str, icon: str, description: str) -> bool:
    """Render a clickable card for input method selection."""
    card_html = f"""
        <div style="
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            background-color: white;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            height: 100%;
            &:hover {{
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }}">
            <h3 style="margin-bottom: 0.5rem; color: #0F52BA;">{icon} {title}</h3>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">{description}</p>
        </div>
    """
    return st.markdown(card_html, unsafe_allow_html=True)

def render_method_selector() -> None:
    """Render the input method selection section."""
    # Initialize input_method in session state if not present
    if 'input_method' not in st.session_state:
        st.session_state.input_method = None
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_method_card(
            "Upload Dataset",
            "📊",
            "Upload your existing dataset in CSV or TXT format"
        )
        if st.button("Choose Upload", key="btn_upload", use_container_width=True):
            set_state('input_method', 'upload')
    
    with col2:
        render_method_card(
            "Write Prompt",
            "✍️",
            "Describe the synthetic data you want to generate"
        )
        if st.button("Choose Prompt", key="btn_prompt", use_container_width=True):
            set_state('input_method', 'prompt') 