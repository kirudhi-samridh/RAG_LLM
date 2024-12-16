import streamlit as st
from pathlib import Path
from services.pdf_service import PDFService
from utils.file_utils import FileManager

pdf_service = PDFService()
file_manager = FileManager()

def init_session_state():
    """Initialize session state variables."""
    if 'history' not in st.session_state:
        st.session_state["history"] = []
    if 'matching_docs' not in st.session_state:
        st.session_state["matching_docs"] = []
    if 'selected_question' not in st.session_state:
        st.session_state['selected_question'] = None

def display_chat():
    """Display the most recent chat from the session state."""
    if len(st.session_state["history"]) != 0:
        st.write(f"**Q:** {st.session_state['history'][-1]['question']}")
        st.write(f"**A:** {st.session_state['history'][-1]['answer']}")

def display_history(i):
    """Display the history of a specific question."""
    st.write(f"**Q:** {st.session_state['history'][i]['question']}")
    st.write(f"**A:** {st.session_state['history'][i]['answer']}")

def display_sidebar():
    """Display the chat history and file upload in the sidebar."""
    # Chat history at the top
    st.sidebar.header("Chat History")
    history_container = st.sidebar.container()
    with history_container:
        for i in range(len(st.session_state["history"])):
            with st.expander(f"{st.session_state['history'][i]['question'][:20]}..."):
                st.write(f"**Q:** {st.session_state['history'][i]['question']}")
                display_button = st.button("Display", key=f"display_button_{i}")
                if display_button:
                    st.session_state["selected_question"] = i
    
    # Add file upload at the bottom of sidebar
    st.sidebar.markdown("---")  # Separator
    upload_container = st.sidebar.container()   
    with upload_container:
        with st.expander("Upload a PDF file"):
            uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=['pdf'], key="file_uploader")
            if uploaded_file:
                # Check if document is already processed
                if pdf_service.embedding_exists(uploaded_file.name.replace(".pdf", "")):
                    st.sidebar.warning(f"'{uploaded_file.name}' has already been processed.")
                else:
                    # Save and process new file
                    if st.sidebar.button("Process PDF", key="process"):
                        with st.spinner("Processing PDF..."):
                            file_path = file_manager.save_uploaded_file(uploaded_file)
                            if file_path:
                                success = pdf_service.process_pdf(file_path)
                                if success:
                                    st.sidebar.success(f"'{uploaded_file.name}' processed successfully!")
                                else:
                                    # remove file from uploads folder
                                    file_manager.remove_file(file_path)

def display():
    """Display the chat history or the most recent chat."""
    display_sidebar()
    if st.session_state["selected_question"] is not None:
        display_history(st.session_state["selected_question"])
    else:
        display_chat() 