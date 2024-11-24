"""Session state management utilities."""
import streamlit as st
from typing import Any, Optional

def initialize_session_state() -> None:
    """Initialize all session state variables."""
    defaults = {
        'uploaded_data': None,
        'generated_data': None,
        'generation_step': 0,
        'history': []
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def get_state(key: str) -> Any:
    """Get a value from session state."""
    return st.session_state.get(key)

def set_state(key: str, value: Any) -> None:
    """Set a value in session state."""
    st.session_state[key] = value 