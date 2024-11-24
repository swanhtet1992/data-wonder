"""Main application entry point for the Synthetic Data Generator."""
import streamlit as st
from src.utils.state_management import initialize_session_state
from src.components.sidebar import render_sidebar
from src.components.upload import render_upload_section
from src.components.configuration import render_configuration_section
from src.components.progress import render_progress_section
from src.components.history import render_history_page
from src.config import APP_TITLE, APP_ICON, LAYOUT

def main():
    """Main application entry point."""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=LAYOUT
    )
    
    initialize_session_state()
    page = render_sidebar()
    
    if page == "Generate Data":
        render_upload_section()
        
        if st.session_state.uploaded_data is not None:
            data_type, num_samples = render_configuration_section()
            
            if st.button("Generate Synthetic Data", type="primary"):
                render_progress_section()
                st.info("Generation would happen here in the full implementation")
    
    else:  # Dataset History page
        render_history_page()

if __name__ == "__main__":
    main() 