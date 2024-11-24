"""Flow visualization component."""
import streamlit as st
from .step_manager import StepStatus, Step
import time

def render_step(step: Step, is_active: bool = False):
    """Render an individual step with its status and progress."""
    col1, col2 = st.columns([0.2, 0.8])
    
    with col1:
        if step.status == StepStatus.RUNNING:
            st.spinner("")
        elif step.status == StepStatus.COMPLETED:
            st.success("✓")
        elif step.status == StepStatus.ERROR:
            st.error("×")
        elif step.status == StepStatus.PAUSED:
            st.warning("⏸")
        else:
            st.text("○")
    
    with col2:
        expander = st.expander(
            f"{step.name} ({step.progress:.0%})", 
            expanded=is_active
        )
        with expander:
            st.write(step.description)
            if step.progress > 0:
                st.progress(step.progress)
            
            if step.output:
                st.json(step.output)
            
            if is_active and step.status == StepStatus.RUNNING:
                if st.button("Pause", key=f"pause_{step.id}"):
                    return "pause"
            elif is_active and step.status == StepStatus.PAUSED:
                if st.button("Resume", key=f"resume_{step.id}"):
                    return "resume"
    
    return None

def render_flow_visualization():
    """Render the complete flow visualization."""
    st.header("Generation Progress")
    
    steps = st.session_state.steps
    current_step = None
    
    for step in steps:
        if step.status == StepStatus.RUNNING:
            current_step = step
            break
    
    # Render connection lines between steps
    for idx, step in enumerate(steps):
        is_active = step == current_step
        action = render_step(step, is_active)
        
        if action == "pause":
            step.status = StepStatus.PAUSED
        elif action == "resume":
            step.status = StepStatus.RUNNING
        
        if idx < len(steps) - 1:
            st.markdown("<div style='border-left: 2px solid #ccc; margin-left: 10%; height: 20px'></div>", 
                       unsafe_allow_html=True) 