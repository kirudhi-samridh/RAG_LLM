import streamlit as st
from pathlib import Path
from config import Config
from utils.logging_utils import setup_logging
from utils.file_utils import FileManager
from services.pdf_service import PDFService
from services.llm_service import query_llm
from ui.chat_ui import init_session_state, display

# Initialize configuration and services
config = Config()
setup_logging(config.LOG_FILE)
file_manager = FileManager()
pdf_service = PDFService()

# Initialize session state
init_session_state()

# Main Streamlit app
st.header("Q and A - AI")

# Select processed file for querying
processed_files = file_manager.list_processed_files()
if processed_files:
    selected_file = st.selectbox(
        "Select a processed file to query",
        processed_files,
        format_func=lambda x: Path(x).stem
    )

    # Chat input for entering a question
    question = st.chat_input("Enter your question:")

    # If a question is entered, query the LLM and update session state
    if question:
        st.session_state["selected_question"] = None
        query_llm(question, Path(selected_file).stem)

    # Display the chat or history
    display()
else:
    st.info("No processed files available. Please upload and process a PDF file.")
