"""Prompt editing component."""
import streamlit as st
from ...utils.state_management import set_state
from ...config import PROMPT_TEMPLATES, MAX_PROMPT_LENGTH

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

def render_template_tab(template_name: str) -> None:
    """Render a single template tab."""
    col1, col2 = st.columns([0.9, 0.1])
    
    with col1:
        if template_name == "Custom":
            prompt = st.text_area(
                "Enter your custom prompt",
                height=150,
                help="Describe what kind of synthetic data you want to generate",
                placeholder="Example: Generate a dataset of customer service conversations...",
                key=f"prompt_{template_name}"
            )
        else:
            prompt = st.text_area(
                "Customize the template",
                value=PROMPT_TEMPLATES[template_name],
                height=150,
                help="Modify the template according to your needs",
                key=f"prompt_{template_name}"
            )
    
    # Only show enhance button for custom prompts
    if template_name == "Custom":
        with col2:
            if st.button("✨", key="enhance_button", help="Enhance your prompt"):
                enhanced = enhance_prompt(prompt)
                st.session_state[f'enhanced_prompt_{template_name}'] = enhanced
    
    if prompt.strip():
        set_state('prompt_input', prompt)
        set_state('input_type', 'prompt')
        
        # Show character count and tips in columns
        col1, col2 = st.columns([1, 1])
        with col1:
            st.caption(f"📝 Characters: {len(prompt)}/{MAX_PROMPT_LENGTH}")
        with col2:
            if len(prompt) > MAX_PROMPT_LENGTH:
                st.warning("⚠️ Prompt is too long")
        
        # Show enhanced prompt section if available
        if template_name == "Custom" and st.session_state.get(f'enhanced_prompt_{template_name}'):
            st.markdown("---")
            st.subheader("✨ Enhanced Prompt")
            
            enhanced_prompt = st.text_area(
                "Edit enhanced prompt",
                value=st.session_state[f'enhanced_prompt_{template_name}'],
                height=250,
                help="You can further edit the enhanced prompt",
                key=f"enhanced_{template_name}"
            )
            
            # Update the stored enhanced prompt if edited
            if enhanced_prompt != st.session_state[f'enhanced_prompt_{template_name}']:
                st.session_state[f'enhanced_prompt_{template_name}'] = enhanced_prompt
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Re-enhance", key=f"reenhance_{template_name}"):
                    enhanced = enhance_prompt(prompt)
                    st.session_state[f'enhanced_prompt_{template_name}'] = enhanced
                    st.experimental_rerun()
            with col2:
                if st.button("↩️ Reset", key=f"reset_enhanced_{template_name}"):
                    del st.session_state[f'enhanced_prompt_{template_name}']
                    st.experimental_rerun()

def render_prompt_editor() -> None:
    """Render the prompt input section."""
    st.subheader("✍️ Write Your Prompt")
    
    templates = ["Custom"] + list(PROMPT_TEMPLATES.keys())
    tabs = st.tabs(templates)
    
    for idx, tab in enumerate(tabs):
        with tab:
            template_name = templates[idx]
            render_template_tab(template_name)