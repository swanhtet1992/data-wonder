"""Main application entry point for the Synthetic Data Generator."""
import streamlit as st
from llama_stack_client import LlamaStackClient
from src.utils.state_management import initialize_session_state, get_state
from src.components.sidebar import render_sidebar
from src.components.input import render_input_section
from src.components.configuration import render_configuration_section
from src.components.flow.flow_visualizer import render_flow_visualization
from src.components.flow.step_manager import StepManager, StepStatus
from src.components.history import render_history_page
from src.pipeline.processors.document_processor import DocumentProcessor
from src.pipeline.generators.question_generator import QuestionGenerator
from src.pipeline.generators.answer_generator import AnswerGenerator
from src.config import APP_TITLE, APP_ICON, LAYOUT
import asyncio

def initialize_components():
    """Initialize all pipeline components."""
    try:
        # Initialize client if not already done
        if 'llama_client' not in st.session_state:
            client = LlamaStackClient(base_url="http://localhost:5001")
            st.session_state.llama_client = client
            
            # Initialize processor and memory bank
            processor = DocumentProcessor(client)
            asyncio.run(processor.initialize_memory_bank("default-bank"))
            
            # Store components in session state
            st.session_state.document_processor = processor
            st.session_state.question_generator = QuestionGenerator(client)
            st.session_state.answer_generator = AnswerGenerator(client)
            st.session_state.step_manager = StepManager()
            
            st.success("✅ Components initialized successfully!")
        
        # Verify all components are present
        required_components = [
            'llama_client',
            'document_processor',
            'question_generator',
            'answer_generator',
            'step_manager'
        ]
        
        missing_components = [comp for comp in required_components 
                            if comp not in st.session_state]
        
        if missing_components:
            st.error(f"❌ Missing components: {', '.join(missing_components)}")
            st.stop()
            
    except Exception as e:
        st.error(f"❌ Initialization failed: {str(e)}")
        st.exception(e)  # Show full traceback in development
        st.stop()

def main():
    """Main application entry point."""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=LAYOUT
    )
    
    # Initialize state and components
    initialize_session_state()
    initialize_components()
    
    # Verify components before proceeding
    if not all(comp in st.session_state for comp in [
        'document_processor',
        'question_generator',
        'answer_generator'
    ]):
        st.error("❌ Application not properly initialized")
        st.stop()
        return
    
    page = render_sidebar()
    
    if page == "Generate Data":
        render_input_section(
            processor=st.session_state.document_processor,
            question_gen=st.session_state.question_generator,
            answer_gen=st.session_state.answer_generator
        )
        
        # Check if data is ready for processing
        input_ready = (get_state('uploaded_data') is not None or 
                      get_state('prompt_input') is not None)
        
        if input_ready:
            data_type, num_samples = render_configuration_section()
            
            if st.button("Process Document", type="primary"):
                step_manager = st.session_state.step_manager
                
                if get_state('input_type') == 'dataset':
                    step_manager.update_step_status("upload", StepStatus.COMPLETED, 1.0)
                    step_manager.update_step_status("process", StepStatus.RUNNING, 0.0)
                else:
                    step_manager.update_step_status("prompt", StepStatus.COMPLETED, 1.0)
                    step_manager.update_step_status("process", StepStatus.RUNNING, 0.0)
            
            # Render flow visualization
            render_flow_visualization()
    
    else:  # Dataset History page
        render_history_page()

if __name__ == "__main__":
    main() 