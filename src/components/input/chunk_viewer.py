"""Component for viewing document chunks."""
import streamlit as st
from typing import List, Dict, Any

def render_chunk_viewer(chunks: List[Dict[str, Any]], metadata: Dict[str, Any]) -> None:
    """Render a viewer for document chunks and metadata."""
    st.subheader("📄 Document Analysis")
    
    # Show document metadata
    with st.expander("📊 Document Metadata", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Chunks", len(chunks))
            if "char_count" in metadata:
                st.metric("Characters", metadata["char_count"])
        with col2:
            if "estimated_reading_time" in metadata:
                st.metric("Est. Reading Time", 
                         f"{metadata['estimated_reading_time']:.1f} min")
            if "title" in metadata:
                st.text("Title: " + metadata["title"])
    
    # Show chunks
    st.subheader("📝 Document Chunks")
    for i, chunk in enumerate(chunks):
        with st.expander(f"Chunk {i+1} ({chunk['size']} chars)", expanded=i==0):
            st.text(chunk["content"])
            
            # Show chunk metadata
            st.caption("Chunk Metadata:")
            st.json({
                "index": i,
                "size": chunk["size"],
                "id": f"chunk_{i}"
            }) 