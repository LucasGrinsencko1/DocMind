
import html

import streamlit as st

from streamlit_pdf_viewer import pdf_viewer

from src.pdf_processor import extract_text_from_pdf
from src.rag_pipeline import create_chunks, create_vector_store, get_answer


# Page configuration
st.set_page_config(
    page_title="DocMind | Intelligent Document Assistant",
    page_icon="📄",
    layout="wide"
)


# Custom design system
st.markdown(
    """
    <style>
    /* Global layout */
    .stApp {
        background: linear-gradient(135deg, #0B1120 0%, #101827 55%, #111B30 100%);
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0D1525;
        border-right: 1px solid rgba(148, 163, 184, 0.12);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 1rem;
    }

    /* Typography */
    h1, h2, h3, p, label {
        color: #E8EDF7;
    }

    h1 {
        letter-spacing: -1.5px;
        font-weight: 750 !important;
    }

    h2, h3 {
        letter-spacing: -0.5px;
    }

    .stCaption, [data-testid="stCaptionContainer"] {
        color: #94A3B8 !important;
    }

    /* Brand */
    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0.5rem 0 1rem 0;
    }

    .brand-icon {
        width: 44px;
        height: 44px;
        border-radius: 13px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #3157A4, #7555C7);
        color: white;
        font-size: 23px;
        box-shadow: 0 5px 20px rgba(78, 105, 210, 0.25);
    }

    .brand-name {
        color: #F1F5FF;
        font-size: 23px;
        font-weight: 750;
        letter-spacing: -0.8px;
    }

    .brand-subtitle {
        color: #8190A8;
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 1.5px;
    }

    /* Hero section */
    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.5rem 2.4rem;
        border-radius: 22px;
        background: linear-gradient(120deg, #172746 0%, #20294B 55%, #30254D 100%);
        border: 1px solid rgba(151, 170, 220, 0.18);
        margin: 1rem 0 1.5rem 0;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 250px;
        height: 250px;
        right: -65px;
        top: -100px;
        border-radius: 50%;
        background: rgba(111, 130, 255, 0.12);
        filter: blur(5px);
    }

    .hero-label {
        color: #A9BCFF;
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 14px;
    }

    .hero-title {
        color: #FFFFFF;
        font-size: clamp(32px, 4vw, 46px);
        font-weight: 800;
        letter-spacing: -2px;
        line-height: 1.12;
        margin-bottom: 14px;
    }

    .hero-title span {
        color: #A8B9FF;
    }

    .hero-description {
        color: #C0CBE0;
        font-size: 15px;
        line-height: 1.7;
        max-width: 650px;
        margin-bottom: 0;
    }

    /* Feature cards */
    .feature-card {
        height: 100%;
        min-height: 145px;
        padding: 1.25rem;
        border-radius: 16px;
        background: rgba(24, 37, 59, 0.82);
        border: 1px solid rgba(148, 163, 184, 0.13);
    }

    .feature-icon {
        font-size: 23px;
        margin-bottom: 12px;
    }

    .feature-title {
        color: #E9EEFA;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .feature-description {
        color: #91A1B9;
        font-size: 12px;
        line-height: 1.6;
    }

    /* Section labels */
    .section-label {
        color: #AAB8D0;
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin: 1.5rem 0 0.8rem 0;
    }

    /* Status */
    .status-card {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 14px 16px;
        border-radius: 13px;
        background: rgba(22, 42, 56, 0.75);
        border: 1px solid rgba(52, 211, 153, 0.2);
        margin: 1rem 0;
    }

    .status-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #34D399;
        box-shadow: 0 0 12px rgba(52, 211, 153, 0.65);
    }

    .status-text {
        color: #D1FAE5;
        font-size: 13px;
        font-weight: 650;
    }

    .document-name {
        color: #AAB8D0;
        font-size: 12px;
        margin-top: 3px;
        overflow-wrap: anywhere;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(125, 150, 230, 0.3);
        background: linear-gradient(110deg, #3559A8, #6652B5);
        color: #FFFFFF;
        font-weight: 650;
        min-height: 43px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #9DB5FF;
        background: linear-gradient(110deg, #426BC1, #7964CF);
        box-shadow: 0 5px 18px rgba(83, 103, 200, 0.2);
        transform: translateY(-1px);
    }

    .stButton > button:disabled {
        background: #263248;
        color: #718096;
        border-color: #344155;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(24, 37, 59, 0.55);
        border: 1px dashed rgba(137, 158, 208, 0.35);
        border-radius: 13px;
        padding: 10px;
    }

    [data-testid="stFileUploader"] section {
        background: transparent;
    }

    /* Chat */
    [data-testid="stChatMessage"] {
        background: rgba(24, 37, 59, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.11);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }

    [data-testid="stChatInput"] {
        border-color: rgba(137, 158, 208, 0.35);
    }

    [data-testid="stChatInput"] textarea {
        color: #E8EDF7;
    }

    /* Dividers */
    hr {
        border-color: rgba(148, 163, 184, 0.13) !important;
    }

    /* Footer */
    .footer {
        color: #64748B;
        font-size: 11px;
        text-align: center;
        padding-top: 2rem;
        letter-spacing: 0.5px;
    }

    /* Keep Streamlit toolbar and hide Deploy button */
    [data-testid="stDeployButton"] {
        display: none;
    }

    /* Make the toolbar transparent */
    [data-testid="stHeader"] {
        background: transparent;
    }

    
    /* Dynamic theme support */
    .stApp {
        background: var(--background-color) !important;
        color: var(--text-color);
    }

    [data-testid="stSidebar"] {
        background: var(--secondary-background-color) !important;
    }

    h1, h2, h3, p, label,
    .stMarkdown,
    .stMarkdown p {
        color: var(--text-color);
    }

    /* Brand */
    .brand-name {
        color: var(--text-color);
    }

    .brand-subtitle {
        color: var(--text-color);
        opacity: 0.65;
    }

    /* Hero */
    .hero {
        background: linear-gradient(
            120deg,
            color-mix(in srgb, var(--primary-color) 15%, var(--secondary-background-color)),
            var(--secondary-background-color)
        );
        border-color: var(--border-color);
    }

    .hero-title {
        color: var(--text-color);
    }

    .hero-title span {
        color: var(--primary-color);
    }

    .hero-description {
        color: var(--text-color);
        opacity: 0.78;
    }

    .hero-label,
    .section-label {
        color: var(--primary-color);
    }

    /* Feature cards */
    .feature-card {
        background: var(--secondary-background-color);
        border-color: var(--border-color);
    }

    .feature-title {
        color: var(--text-color);
    }

    .feature-description {
        color: var(--text-color);
        opacity: 0.7;
    }

    /* Document status */
    .status-card {
        background: var(--secondary-background-color);
        border-color: var(--border-color);
    }

    .status-text {
        color: var(--text-color);
    }

    .document-name {
        color: var(--text-color);
        opacity: 0.7;
    }

    /* Chat */
    [data-testid="stChatMessage"] {
        background: var(--secondary-background-color);
        border-color: var(--border-color);
    }

    [data-testid="stChatInput"] {
        background: var(--secondary-background-color);
        border-color: var(--border-color);
    }

    [data-testid="stChatInput"] textarea {
        color: var(--text-color);
    }

    /* Upload */
    [data-testid="stFileUploader"] {
        background: var(--secondary-background-color);
        border-color: var(--border-color);
    }

    /* Footer */
    .footer {
        color: var(--text-color);
        opacity: 0.55;
    }

    
    /* Light theme refinements */
    [data-testid="stAppViewContainer"] {
        background: var(--background-color);
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid var(--border-color);
    }

    /* Active document highlight */
    .status-card {
        background: #E1EAF9 !important;
        border: 1px solid #91ACDE !important;
        box-shadow: 0 2px 8px rgba(54, 91, 155, 0.08);
    }

    .status-text {
        color: #244578 !important;
    }

    .document-name {
        color: #536D95 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# Initialize application state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None

# Sidebar: document management
with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">▤</div>
            <div>
                <div class="brand-name">DocMind</div>
                <div class="brand-subtitle">INTELLIGENT DOCUMENT AI</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Your intelligent workspace for document analysis.")

    st.divider()

    st.markdown(
        '<div class="section-label">DOCUMENT MANAGEMENT</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"],
        help="Select a PDF file to analyze with DocMind."
    )

    if st.button(
        "Process Document",
        use_container_width=True,
        disabled=uploaded_file is None
    ):

        try:
            with st.spinner("Processing your document..."):

                # Extract text from the PDF
                pages = extract_text_from_pdf(uploaded_file)

                if not pages:
                    raise ValueError(
                        "No text could be extracted from this PDF."
                    )

                # Split the document into chunks
                chunks = create_chunks(pages)

                # Create a new vector database collection
                vector_store = create_vector_store(chunks)

                # Store the reference to the previous vector store
                previous_vector_store = st.session_state.vector_store

                # Update the active document
                st.session_state.vector_store = vector_store
                st.session_state.document_name = uploaded_file.name
                st.session_state.pdf_bytes = uploaded_file.getvalue()

                # Delete the previous collection after successful processing
                if previous_vector_store is not None:
                    try:
                        previous_vector_store.delete_collection()
                    except Exception as error:
                        print(
                            f"[CHROMA] Failed to delete previous collection: {error}"
                        )

                # Clear the conversation history for the new document
                st.session_state.messages = []

            st.success("Document processed successfully!")

        except Exception as error:
            st.error(f"Failed to process document: {error}")

    st.divider()

    st.markdown(
        '<div class="section-label">ACTIVE DOCUMENT</div>',
        unsafe_allow_html=True
    )

    if st.session_state.vector_store is not None:

        safe_document_name = html.escape(
            st.session_state.document_name or "Untitled document"
        )

        st.markdown(
            f"""
            <div class="status-card">
                <div class="status-dot"></div>
                <div>
                    <div class="status-text">Document ready</div>
                    <div class="document-name">{safe_document_name}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption("You can now ask questions about this document.")

    else:
        st.info("No active document. Upload a PDF to get started.")

    st.divider()

    st.markdown(
        """
        <div style="color:#71829B; font-size:11px; line-height:1.8;">
            <strong style="color:#AAB8D0;">DOCMIND</strong><br>
            AI-powered document intelligence.<br><br>
            Powered by Google Gemini and ChromaDB.
        </div>
        """,
        unsafe_allow_html=True
    )


# Main area: application header
st.markdown(
    """
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:5px;">
        <span style="color:#A9BFFF; font-size:12px; font-weight:750; letter-spacing:1.8px;">
            DOCMIND WORKSPACE
        </span>
        <span style="background:#193A38; color:#6EE7B7; padding:4px 9px;
                     border-radius:20px; font-size:10px; font-weight:700;">
            AI POWERED
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("Document Intelligence")

st.markdown(
    '<p style="color:#94A3B8; margin-top:-12px;">'
    'Understand your documents. Find answers. Discover insights.'
    '</p>',
    unsafe_allow_html=True
)

st.divider()


# Initial application state
if st.session_state.vector_store is None:

    st.markdown(
        """
        <div class="hero">
            <div class="hero-label">YOUR AI DOCUMENT ASSISTANT</div>
            <div class="hero-title">
                Your documents.<br>
                <span>Understood.</span>
            </div>
            <p class="hero-description">
                Turn static documents into interactive knowledge.
                Upload a PDF, ask questions and get intelligent answers
                grounded in your document's content.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-label">WHAT YOU CAN DO WITH DOCMIND</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">AI Understanding</div>
                <div class="feature-description">
                    Ask natural language questions and receive
                    context-aware answers from your documents.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🔎</div>
                <div class="feature-title">Semantic Search</div>
                <div class="feature-description">
                    Retrieve relevant information based on meaning
                    and context, not just exact keywords.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📑</div>
                <div class="feature-title">Source References</div>
                <div class="feature-description">
                    Identify the pages used to generate answers
                    and trace information back to its source.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div style="margin-top:28px; padding:17px 20px; border-radius:13px;
                    background:rgba(35,52,81,0.55);
                    border:1px solid rgba(148,163,184,0.13);">
            <div style="color:#DCE6FA; font-size:13px; font-weight:700;">
                Getting started
            </div>
            <div style="color:#94A3B8; font-size:12px; margin-top:6px; line-height:1.7;">
                Upload a PDF using the sidebar, process the document,
                and start exploring its content through an AI-powered conversation.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



else:

    # Active document workspace
    safe_document_name = html.escape(
        st.session_state.document_name or "Untitled document"
    )

    st.markdown(
        f"""
        <div class="status-card">
            <div class="status-dot"></div>
            <div>
                <div class="status-text">Workspace ready</div>
                <div class="document-name">Currently analyzing: {safe_document_name}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Split workspace into PDF preview and AI chat
    pdf_column, chat_column = st.columns([1, 1], gap="large")

    with pdf_column:

        st.markdown("### Document Preview")

        if st.session_state.pdf_bytes:
            pdf_viewer(
                input=st.session_state.pdf_bytes,
                width="100%",
                height=700,
                zoom_level="auto",
                viewer_align="center",
                show_page_separator=True
            )
        else:
            st.info("PDF preview is unavailable.")

    with chat_column:

        st.markdown("### AI Assistant")

        # Create a fixed-height chat history area
        chat_history = st.container(
            height=700,
            border=False
        )

        with chat_history:

            if not st.session_state.messages:

                st.markdown(
                    """
                    <p style="color:#94A3B8; font-size:14px;">
                        Your document has been processed. Ask a question
                        to begin exploring its content.
                    </p>
                    """,
                    unsafe_allow_html=True
                )

                suggestions = [
                    "Summarize this document.",
                    "What are the most important points?",
                    "What conclusions can be drawn from the document?"
                ]

                for suggestion in suggestions:

                    st.markdown(
                        f"""
                        <div style="padding:12px; margin-bottom:10px;
                                    border-radius:12px;
                                    background:rgba(24,37,59,0.65);
                                    border:1px solid rgba(148,163,184,0.13);
                                    color:#B8C5D8; font-size:12px;">
                            {html.escape(suggestion)}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # Display conversation history
            for message in st.session_state.messages:

                with st.chat_message(message["role"]):

                    st.markdown(message["content"])

                    if message["role"] == "assistant" and message.get("sources"):

                        source_pages = ", ".join(
                            map(str, message["sources"])
                        )

                        st.caption(f"Sources: Pages {source_pages}")

        # Question input field
        question = st.chat_input(
            "Ask anything about your document..."
        )

        if question:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with chat_history:

                with st.chat_message("user"):
                    st.markdown(question)

                # Generate an answer using the RAG pipeline
                with st.chat_message("assistant"):

                    with st.spinner("Analyzing your document..."):

                        try:
                            answer, sources = get_answer(
                                question,
                                st.session_state.vector_store
                            )

                            st.markdown(answer)

                            if sources:

                                source_pages = ", ".join(
                                    map(str, sources)
                                )

                                st.caption(f"Sources: Pages {source_pages}")

                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": answer,
                                    "sources": sources
                                }
                            )

                        except Exception as error:
                            st.error(f"Failed to generate answer: {error}")
