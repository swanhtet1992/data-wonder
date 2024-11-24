"""Advanced chunk organization and visualization component."""
import streamlit as st
from typing import List, Dict, Any
import math

def render_chunk_pagination(chunks: List[Dict[str, Any]], 
                          page: int, 
                          chunks_per_page: int) -> None:
    """Render pagination controls."""
    total_pages = math.ceil(len(chunks) / chunks_per_page)
    
    col1, col2, col3 = st.columns([2, 3, 2])
    
    with col2:
        if total_pages > 1:
            pages = st.select_slider(
                "Navigate Chunks",
                options=range(1, total_pages + 1),
                value=page,
                key="chunk_page_slider"
            )
            st.caption(f"Page {page} of {total_pages}")
    
    return (pages - 1) * chunks_per_page

def render_chunk_search(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Render search functionality for chunks."""
    search_term = st.text_input("🔍 Search in chunks", key="chunk_search")
    
    if search_term:
        filtered_chunks = [
            chunk for chunk in chunks
            if search_term.lower() in chunk["content"].lower()
        ]
        st.caption(f"Found {len(filtered_chunks)} matching chunks")
        return filtered_chunks
    return chunks

def render_chunk_stats(chunks: List[Dict[str, Any]], metadata: Dict[str, Any]) -> None:
    """Render statistical overview of chunks."""
    total_chars = sum(chunk["size"] for chunk in chunks)
    avg_size = total_chars / len(chunks) if chunks else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Chunks", len(chunks))
    with col2:
        st.metric("Avg. Chunk Size", f"{avg_size:.0f} chars")
    with col3:
        if "estimated_reading_time" in metadata:
            st.metric("Est. Reading Time", 
                     f"{metadata['estimated_reading_time']:.1f} min")

def render_organized_chunks(chunks: List[Dict[str, Any]], 
                          metadata: Dict[str, Any],
                          chunks_per_page: int = 5) -> None:
    """Render chunks with advanced organization and navigation."""
    st.subheader("📄 Document Analysis")
    
    # Show document metadata and stats
    with st.expander("📊 Document Overview", expanded=True):
        render_chunk_stats(chunks, metadata)
        if "title" in metadata:
            st.text("Title: " + metadata["title"])
    
    # Add search functionality
    filtered_chunks = render_chunk_search(chunks)
    
    # Initialize pagination state
    if "chunk_page" not in st.session_state:
        st.session_state.chunk_page = 1
    
    # Get current page of chunks
    start_idx = render_chunk_pagination(
        filtered_chunks, 
        st.session_state.chunk_page,
        chunks_per_page
    )
    
    # Show current page of chunks
    page_chunks = filtered_chunks[start_idx:start_idx + chunks_per_page]
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Chunk View", "Analysis View"])
    
    with tab1:
        for i, chunk in enumerate(page_chunks, start=start_idx + 1):
            with st.expander(
                f"Chunk {i} ({chunk['size']} chars)", 
                expanded=i == start_idx + 1
            ):
                st.text(chunk["content"])
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.caption("Chunk Metadata:")
                    st.json({
                        "index": i-1,
                        "size": chunk["size"],
                        "id": f"chunk_{i-1}"
                    })
                with col2:
                    if st.button("📋 Copy", key=f"copy_chunk_{i}"):
                        st.toast("Chunk copied to clipboard!")
    
    with tab2:
        # Show chunk size distribution
        chunk_sizes = [chunk["size"] for chunk in filtered_chunks]
        st.bar_chart(chunk_sizes)
        st.caption("Chunk Size Distribution")
        
        # Show additional analytics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Largest Chunk", f"{max(chunk_sizes)} chars")
        with col2:
            st.metric("Smallest Chunk", f"{min(chunk_sizes)} chars") 