"""Preview components for uploaded data and prompts."""
import streamlit as st
import pandas as pd
from typing import Optional

def render_data_preview(data: pd.DataFrame) -> None:
    """Render a preview of uploaded data."""
    with st.expander("📊 Data Preview", expanded=True):
        st.dataframe(
            data.head(),
            use_container_width=True,
            column_config={
                "_index": st.column_config.Column(
                    "Index",
                    help="Row index",
                    width="small",
                )
            }
        )

def enhance_prompt(prompt: str) -> str:
    """Enhance the given prompt with additional context and structure."""
    # This is a placeholder - in real implementation, you might use an LLM
    enhanced = f"""Based on your input, here's an enhanced version:

Input Format:
{prompt}

Additional Context:
- Specify data structure and format
- Include validation rules
- Define edge cases
- Add example outputs

Output Requirements:
- Maintain data consistency
- Follow specified format
- Include error handling
- Validate against schema
"""
    return enhanced

def render_prompt_preview(prompt: str, template_name: str) -> None:
    """Render a preview of the prompt with enhancement option."""
    col1, col2 = st.columns([0.85, 0.15])
    
    with col1:
        st.subheader("Original Prompt")
    with col2:
        if st.button("✨ Enhance", key=f"enhance_{template_name}", 
                    help="Enhance prompt with additional context and structure"):
            enhanced_prompt = enhance_prompt(prompt)
            st.session_state[f'enhanced_prompt_{template_name}'] = enhanced_prompt
    
    # Show original prompt
    with st.expander("👁️ View Original", expanded=True):
        st.code(prompt, language="text")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Copy Original", key=f"copy_{template_name}"):
                st.toast("Original prompt copied! 📋")
        with col2:
            if st.button("🔄 Reset", key=f"reset_{template_name}"):
                if template_name != "Custom":
                    st.experimental_rerun()
    
    # Show enhanced prompt if available
    enhanced_prompt = st.session_state.get(f'enhanced_prompt_{template_name}')
    if enhanced_prompt:
        st.subheader("✨ Enhanced Prompt")
        with st.expander("🔍 View Enhanced", expanded=True):
            st.code(enhanced_prompt, language="text")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📋 Copy Enhanced", key=f"copy_enhanced_{template_name}"):
                    st.toast("Enhanced prompt copied! 📋")
            with col2:
                if st.button("↩️ Revert", key=f"revert_{template_name}"):
                    del st.session_state[f'enhanced_prompt_{template_name}']
                    st.experimental_rerun()
            with col3:
                if st.button("✨ Re-enhance", key=f"reenhance_{template_name}"):
                    enhanced_prompt = enhance_prompt(prompt)
                    st.session_state[f'enhanced_prompt_{template_name}'] = enhanced_prompt
                    st.experimental_rerun()
        
        # Show diff or comparison
        with st.expander("📊 Compare Changes", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original**")
                st.code(prompt, language="text")
            with col2:
                st.markdown("**Enhanced**")
                st.code(enhanced_prompt, language="text")