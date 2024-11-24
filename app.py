"""Main application entry point for the Synthetic Data Generator."""
import streamlit as st
from src.utils.state_management import initialize_session_state, get_state
from src.components.sidebar import render_sidebar
from src.components.input import render_input_section
from src.components.configuration import render_configuration_section
from src.components.flow.flow_visualizer import render_flow_visualization
from src.components.flow.step_manager import StepManager, StepStatus
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
        render_input_section()
        
        # Check if either data is uploaded or prompt is provided
        input_ready = (get_state('uploaded_data') is not None or 
                      get_state('prompt_input') is not None)
        
        if input_ready:
            # Initialize step manager if not already done
            if 'step_manager' not in st.session_state:
                st.session_state.step_manager = StepManager()
            
            data_type, num_samples = render_configuration_section()
            
            if st.button("Generate Synthetic Data", type="primary"):
                # Start the generation process
                step_manager = st.session_state.step_manager
                
                if get_state('input_type') == 'dataset':
                    step_manager.update_step_status("upload", StepStatus.COMPLETED, 1.0)
                    step_manager.update_step_status("analyze", StepStatus.RUNNING, 0.0)
                else:
                    step_manager.update_step_status("prompt", StepStatus.COMPLETED, 1.0)
                    step_manager.update_step_status("plan", StepStatus.RUNNING, 0.0)
            
            # Render the flow visualization
            render_flow_visualization()
    
    else:  # Dataset History page
        render_history_page()

if __name__ == "__main__":
    main() 