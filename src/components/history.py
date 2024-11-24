"""History component for managing generated datasets."""
import streamlit as st
import pandas as pd
from ..utils.state_management import get_state

def render_history_page() -> None:
    """Render the dataset history page."""
    st.header("📚 Dataset History")
    
    history = get_state('history')
    if not history:
        st.info("No datasets generated yet.")
        return
    
    df = pd.DataFrame(history)
    st.dataframe(df) 