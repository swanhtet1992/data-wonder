"""Step manager component for handling flow visualization."""
import streamlit as st
from typing import List, Dict, Optional
from ...utils.state_management import get_state, set_state
from dataclasses import dataclass
from enum import Enum

class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    PAUSED = "paused"
    ERROR = "error"

@dataclass
class Step:
    id: str
    name: str
    description: str
    status: StepStatus
    progress: float = 0.0
    output: Optional[Dict] = None

class StepManager:
    def __init__(self):
        if 'steps' not in st.session_state:
            st.session_state.steps = self._initialize_steps()
            
    def _initialize_steps(self) -> List[Step]:
        """Initialize all steps with their default states."""
        input_type = get_state('input_type')
        
        if input_type == 'dataset':
            return [
                Step("upload", "Upload Data", "Upload and validate input data", StepStatus.PENDING),
                Step("analyze", "Analyze Examples", "Extract patterns and insights", StepStatus.PENDING),
                Step("plan", "Planning", "Plan the data generation process", StepStatus.PENDING),
                Step("generate", "Generation", "Generate synthetic data", StepStatus.PENDING),
                Step("validate", "Validation", "Validate and filter results", StepStatus.PENDING),
                Step("export", "Export", "Save and export results", StepStatus.PENDING),
            ]
        else:  # prompt-based flow
            return [
                Step("prompt", "Process Prompt", "Analyze and validate prompt", StepStatus.PENDING),
                Step("plan", "Planning", "Plan the data generation process", StepStatus.PENDING),
                Step("generate", "Generation", "Generate synthetic data", StepStatus.PENDING),
                Step("validate", "Validation", "Validate and filter results", StepStatus.PENDING),
                Step("export", "Export", "Save and export results", StepStatus.PENDING),
            ]
    
    def get_current_step(self) -> Step:
        """Get the currently active step."""
        steps = st.session_state.steps
        for step in steps:
            if step.status == StepStatus.RUNNING:
                return step
        return steps[0]
    
    def update_step_status(self, step_id: str, status: StepStatus, progress: float = None):
        """Update the status of a specific step."""
        steps = st.session_state.steps
        for step in steps:
            if step.id == step_id:
                step.status = status
                if progress is not None:
                    step.progress = progress
                break
        st.session_state.steps = steps 