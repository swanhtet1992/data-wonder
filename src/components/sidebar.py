"""Sidebar component for navigation and information."""
import streamlit as st
from ..config import APP_TITLE, ABOUT_TEXT

def render_sidebar() -> str:
    """Render the sidebar and return the selected page."""
    with st.sidebar:
        st.title(APP_TITLE)
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["Generate Data", "Dataset History"],
            key="navigation"
        )
        
        # Information section
        st.markdown("---")
        st.markdown(ABOUT_TEXT)
        
        return page