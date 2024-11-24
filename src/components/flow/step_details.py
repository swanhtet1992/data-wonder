"""Detailed step visualization components."""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any

def render_analysis_details(analysis_data: Dict[str, Any]):
    """Render analysis step details with visualizations."""
    if not analysis_data:
        return
    
    st.subheader("Analysis Results")
    
    # Example visualization
    fig = go.Figure(data=[
        go.Bar(name='Frequency', x=analysis_data.get('categories', []), 
               y=analysis_data.get('frequencies', []))
    ])
    
    st.plotly_chart(fig)
    
    if 'patterns' in analysis_data:
        st.subheader("Detected Patterns")
        for pattern in analysis_data['patterns']:
            st.write(f"- {pattern}")

def render_planning_details(plan_data: Dict[str, Any]):
    """Render planning step details with Mermaid diagram."""
    if not plan_data:
        return
    
    st.subheader("Generation Plan")
    
    # Create Mermaid diagram
    mermaid_code = """
    graph TD
        A[Input Analysis] --> B[Pattern Extraction]
        B --> C[Template Generation]
        C --> D[Data Generation]
        D --> E[Validation]
    """
    
    st.markdown(f"```mermaid{mermaid_code}```")
    
    if 'steps' in plan_data:
        st.subheader("Planned Steps")
        for step in plan_data['steps']:
            st.write(f"- {step}") 