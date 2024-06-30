import traceback
import os
import streamlit as st 
import logging
import openai
import time
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain

# Define constants
CODE_PATH = "./"
CODE_FILE = 'output.txt'
DATA_FOLDER = './data'
CHROMA_DB_DIR = "./chroma_db"
LOG_FILE = __file__.replace(".py", ".log")

# Setup logging configuration
def setup_logging(log_file):
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%H:%M:%S",
        filename=log_file,
        filemode='a',
    )

setup_logging(LOG_FILE)

# Initialize session state variables if not already present
if 'history' not in st.session_state:
    st.session_state["history"] = []
if 'matching_docs' not in st.session_state:
    st.session_state["matching_docs"] = []
if 'selected_question' not in st.session_state:
    st.session_state['selected_question'] = None

# List files in a directory
def list_files_in_directory(directory):
    """List files in the specified directory."""
    if os.path.exists(directory):
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return []

# List directories in a directory
def list_dirs_in_directory(directory):
    """List directories in the specified directory."""
    if os.path.exists(directory):
        return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    return []

# Get list of files and directories for selection
files_select = list_files_in_directory(DATA_FOLDER)
dir_select = list_dirs_in_directory(CHROMA_DB_DIR)

# Read and process the selected PDF file
def read_pdf(file_path):
    """Read and process the selected PDF file."""
    try:
        print("Print-time - Read PDF Started ", time.localtime())
        loader = PyPDFLoader(file_path)
        data = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(data)

        embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
        db_dir = os.path.splitext(os.path.basename(file_path))[0]
        persist_directory = os.path.join(CHROMA_DB_DIR, db_dir)

        vectordb = Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory=persist_directory)
        vectordb.persist()
        
        st.success("PDF read and encoded successfully!")
    except Exception as e:
        st.error("Error reading PDF.")
        st.code(repr(e))
        logging.error(f"Error reading PDF: {traceback.format_exc()}")

# Query the language model with the provided question
def query_llm(question, db_dir):
    """Query the language model with the provided question."""
    logger = logging.getLogger(__name__)
    try:
        llm = ChatGroq(
            model_name='llama3-70b-8192',
            max_tokens=3048,
            temperature=0.1
        )
        chain = load_qa_chain(llm, chain_type="stuff")

        embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
        persist_directory = os.path.join(CHROMA_DB_DIR, db_dir)
        db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

        matching_docs = db.similarity_search(question)
        openai_ans = chain.run(input_documents=matching_docs, question=question)

        st.session_state["matching_docs"].append(matching_docs)
        st.session_state["history"].append({"question": question, "answer": openai_ans})

        # Uncomment this line if you want to display chat immediately after querying
        # display_chat()

    except Exception as e:
        st.error("Error querying LLM.")
        st.write(traceback.format_exc())
        logger.error(f"Error querying LLM: {traceback.format_exc()}")

# Display the most recent chat
def display_chat():
    """Display the most recent chat from the session state."""
    if len(st.session_state["history"]) != 0:
        st.write(f"**Q:** {st.session_state['history'][-1]['question']}")
        st.write(f"**A:** {st.session_state['history'][-1]['answer']}")

# Display the history of a specific question
def display_history(i):
    """Display the history of a specific question."""
    st.write(f"**Q:** {st.session_state['history'][i]['question']}")
    st.write(f"**A:** {st.session_state['history'][i]['answer']}")

# Display the chat history in the sidebar
def display_sidebar():
    """Display the chat history in the sidebar."""
    st.sidebar.header("Chat History")
    for i in range(len(st.session_state["history"])):
        with st.sidebar.expander(f"{st.session_state['history'][i]['question'][:20]}"):
            st.write(f"**Q:** {st.session_state['history'][i]['question']}")
            display_button = st.button("Display", key=f"display_button_{i}")
            if display_button:
                st.session_state["selected_question"] = i

# Display the chat history or the most recent chat
def display():
    """Display the chat history or the most recent chat."""
    display_sidebar()
    if st.session_state["selected_question"] is not None:
        display_history(st.session_state["selected_question"])
    else:
        display_chat()

# Main Streamlit app
st.header("Q and A - AI")

# Dropdown to select a file
uploaded_file = st.selectbox("Select a file", files_select)

# Dropdown to select a database directory
db_dir = st.selectbox("Select a DB", dir_select)

# Button to embed the selected PDF file
if st.button("Embed", key="encode"):
    read_pdf(os.path.join(DATA_FOLDER, uploaded_file))

# Chat input for entering a question
question = st.chat_input("Enter your question:")

# If a question is entered, query the LLM and update session state
if question:
    st.session_state["selected_question"] = None
    query_llm(question, db_dir)

# Display the chat or history
display()
