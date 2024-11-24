"""Console-like progress view component."""
import streamlit as st
from datetime import datetime
from typing import Optional
import time

class ConsoleView:
    """Console-like view for progress updates."""
    
    def __init__(self, height: int = 300):
        """Initialize console view with fixed height."""
        self.height = height
        if 'console_messages' not in st.session_state:
            st.session_state.console_messages = []
        
        # Create fixed container for console
        self.container = st.empty()
        self._render_console()
    
    def _render_console(self):
        """Render the console with current messages."""
        console_html = f"""
        <div style="
            height: {self.height}px;
            overflow-y: auto;
            background-color: #1E1E1E;
            color: #CCCCCC;
            padding: 10px;
            font-family: 'Courier New', monospace;
            border-radius: 5px;
            margin: 10px 0;
        ">
            {'<br>'.join(st.session_state.console_messages)}
        </div>
        """
        self.container.markdown(console_html, unsafe_allow_html=True)
    
    def log(self, message: str, level: str = 'info'):
        """Add a new message to the console."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        # Define colors for different message levels
        colors = {
            'info': '#CCCCCC',
            'success': '#4CAF50',
            'error': '#F44336',
            'warning': '#FFC107',
            'progress': '#2196F3'
        }
        
        # Create formatted message
        formatted_msg = f'<span style="color: {colors.get(level, "#CCCCCC")}">[{timestamp}] {message}</span>'
        
        # Add to message history
        st.session_state.console_messages.append(formatted_msg)
        
        # Keep only last 100 messages
        if len(st.session_state.console_messages) > 100:
            st.session_state.console_messages = st.session_state.console_messages[-100:]
        
        # Update display
        self._render_console() 