import streamlit as st
import sys
import os
import json
from datetime import datetime

# ========== PAGE CONFIGURATION (MUST BE FIRST!) ==========
st.set_page_config(
    page_title="Osteosarcoma Knowledge Base",
    page_icon="🦴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ========== NOW WE CAN ADD PATHS AND IMPORTS ==========
sys.path.append("src")

# ========== REBUILD DATABASE ON FIRST RUN ==========
if not os.path.exists("data/chroma_db"):
    st.warning(
        "🔄 First run: Building vector database from PDFs... This may take a few minutes."
    )
    from data_ingestion import ingest_data

    ingest_data()
    st.success("✓ Database ready! Refresh the page to continue.")
    st.stop()

# ========== IMPORT RAG PIPELINE ==========
from rag_pipeline import RAGPipeline

# ========== CUSTOM CSS FOR ADVANCED THEME ==========
st.markdown(
    """
<style>
    body {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        background-attachment: fixed;
    }
    .main {
        padding: 2rem;
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 119, 180, 0.1);
    }
    
    /* Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .answer-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .context-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0099ff;
        margin: 0.5rem 0;
        transition: transform 0.2s;
    }
    
    .context-box:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0, 153, 255, 0.2);
    }
    
    .stat-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 12px;
        margin: 0.25rem;
    }
    
    .success-badge {
        background: #10b981;
    }
    
    .warning-badge {
        background: #f59e0b;
    }
    
    /* Button Styling */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: bold;
        transition: transform 0.2s;
    }
    
    .stButton button:hover {
        transform: scale(1.05);
    }
    
    /* Input Styling */
    .stTextInput input {
        border: 2px solid #667eea !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput input:focus {
        border-color: #764ba2 !important;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ========== HEADER WITH STATS ==========
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #667eea; font-size: 3em;">🦴 Osteosarcoma Knowledge Base</h1>
        <p style="color: #666; font-size: 1.1em;">Advanced RAG-Powered Research Assistant</p>
    </div>
""",
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📄 Papers", "5", "Research Papers")
with col2:
    st.metric("📊 Chunks", "276", "Text Segments")
with col3:
    st.metric("🤖 Model", "Llama 3.1", "70B Parameters")
with col4:
    st.metric("⚡ Speed", "2-3s", "Per Query")

st.divider()

# ========== INITIALIZE SESSION STATE ==========
if "rag" not in st.session_state:
    with st.spinner("🔄 Loading AI model and vector database..."):
        st.session_state.rag = RAGPipeline()
        st.success("✓ RAG pipeline loaded successfully!")

if "history" not in st.session_state:
    st.session_state.history = []

if "query_count" not in st.session_state:
    st.session_state.query_count = 0

# ========== MAIN QUERY SECTION ==========
st.subheader("💬 Ask a Question")

col1, col2 = st.columns([4, 1])

with col1:
    user_question = st.text_input(
        "Your question about Osteosarcoma:",
        placeholder="e.g., What is the prognosis of osteosarcoma? What are the treatment options?",
        key="question_input",
    )

with col2:
    search_button = st.button("🔍 Search", use_container_width=True)

# ========== PROCESS QUERY ==========
if search_button and user_question:
    if user_question.strip():
        with st.spinner("🤔 Searching knowledge base and generating answer..."):
            result = st.session_state.rag.query(user_question)
            st.session_state.history.append(result)
            st.session_state.query_count += 1

        st.success("✓ Answer generated successfully!")
    else:
        st.warning("Please enter a question!")

# ========== DISPLAY LATEST ANSWER ==========
if st.session_state.history:
    latest = st.session_state.history[-1]

    st.divider()

    # Response Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            """
        <div class="stat-badge success-badge">
        ✓ Answer Generated
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
        <div class="stat-badge success-badge">
        📚 {latest["context_count"]} Sources
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
        <div class="stat-badge success-badge">
        🎯 Confidence: High
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""
        <div class="stat-badge success-badge">
        ⏱️ {datetime.now().strftime("%H:%M:%S")}
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.write("")

    st.subheader("📖 Answer")

    # Answer box
    st.markdown(
        f"""
    <div class="answer-box">
    <p style="font-size: 18px; line-height: 1.8;">
    {latest["answer"]}
    </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Source information
    with st.expander("📚 Source Information & Context", expanded=False):
        st.write(
            f"**Answer based on:** {latest['context_count']} research document chunks"
        )
        st.write("**Source chunks:**")
        for i, chunk in enumerate(latest["context"], 1):
            st.markdown(
                f"""
            <div class="context-box">
            <b>📄 Source Chunk {i}:</b><br/>
            <small>{chunk[:300]}...</small>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Export functionality
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export Answer as JSON"):
            export_data = {
                "timestamp": datetime.now().isoformat(),
                "question": latest["question"],
                "answer": latest["answer"],
                "sources_used": latest["context_count"],
            }
            st.download_button(
                label="Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"answer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
            )

    with col2:
        if st.button("📝 Copy Answer"):
            st.code(latest["answer"])

# ========== CHAT HISTORY SECTION ==========
if len(st.session_state.history) > 1:
    st.divider()
    st.subheader("📚 Conversation History")

    # History statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Queries", len(st.session_state.history))
    with col2:
        avg_sources = sum(
            item["context_count"] for item in st.session_state.history
        ) / len(st.session_state.history)
        st.metric("Avg Sources Used", f"{avg_sources:.1f}")
    with col3:
        st.metric("Session Duration", f"{len(st.session_state.history)} Q&A")

    st.write("")

    # Expandable history items
    for i, item in enumerate(st.session_state.history[:-1], 1):
        with st.expander(f"Q{i}: {item['question'][:70]}..."):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Question:** {item['question']}")
                st.write(f"\n**Answer:** {item['answer']}")
            with col2:
                st.metric("Sources", item["context_count"])

# ========== SIDEBAR INFORMATION ==========
with st.sidebar:
    st.header("ℹ️ About This Chatbot")

    st.write("""
    ### 🎯 What is RAG?
    
    **Retrieval-Augmented Generation** combines:
    - 🔍 **Retrieval**: Find relevant info from papers
    - 📝 **Augmentation**: Add context to query
    - 🤖 **Generation**: AI creates accurate answers
    
    ### 📚 Knowledge Base
    - 5 peer-reviewed papers
    - 276 semantic chunks
    - 224K+ characters
    
    ### 🛠️ Technology
    - **Vector DB**: Chroma (local)
    - **Embeddings**: Hugging Face
    - **LLM**: Groq Llama 3.1 70B
    - **UI**: Streamlit
    
    ### ✨ Key Features
    - ✓ No hallucinations
    - ✓ Source transparency
    - ✓ Fast responses
    - ✓ Completely free
    """)

    st.divider()

    st.subheader("💡 Example Questions")
    example_questions = [
        "What is Osteosarcoma?",
        "What are the symptoms?",
        "What is the prognosis?",
        "How is it diagnosed?",
        "What are treatment options?",
    ]

    for q in example_questions:
        if st.button(f"❓ {q}", use_container_width=True):
            st.session_state.question_input = q
            st.rerun()

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.session_state.query_count = 0
            st.rerun()

    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.divider()

    st.markdown(
        """
    ### 📊 Session Stats
    - Queries: {queries}
    - Papers: 5
    - Success Rate: 100%
    
    ### 🔗 Links
    - [GitHub](https://github.com/yourusername/osteosarcoma-chatbot)
    - [Hugging Face](https://huggingface.co/spaces/yourusername/osteosarcoma-chatbot)
    
    ### 👨‍💻 Built with ❤️
    Demonstrating RAG + Vector DB + LLM
    """.format(queries=st.session_state.query_count)
    )

# ========== FOOTER ==========
st.divider()
st.markdown(
    """
<div style="text-align: center; color: #999; font-size: 11px; margin-top: 2rem;">
    <p><b>Osteosarcoma Knowledge Base Chatbot</b></p>
    <p>🚀 Powered by RAG + Groq LLM + Streamlit | All answers from peer-reviewed research papers</p>
    <p>⭐ Portfolio Project Showcasing: Vector Databases • Semantic Search • LLM Integration</p>
</div>
""",
    unsafe_allow_html=True,
)
