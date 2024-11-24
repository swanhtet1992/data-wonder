"""Component for viewing document chunks."""
import streamlit as st
from typing import List, Dict, Any
from .chunk_organizer import render_organized_chunks

def render_chunk_viewer(chunks: List[Dict[str, Any]], metadata: Dict[str, Any]) -> None:
    """Render a viewer for document chunks and metadata."""
    render_organized_chunks(chunks, metadata)