import os
import time
import logging
import traceback
from pathlib import Path
import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from config import Config

class PDFService:
    def __init__(self):
        self.config = Config()
        self.embeddings = OpenAIEmbeddings()

    def embedding_exists(self, file_name: str) -> bool:
        """Check if embeddings for a file exist."""
        persist_directory = Path(self.config.CHROMA_DB_DIR) / file_name
        return persist_directory.exists()

    def process_pdf(self, file_path: Path) -> bool:
        """Process a PDF file and create embeddings."""
        try:
            print(f"Processing PDF Started at {time.localtime()}")
            loader = PyPDFLoader(str(file_path))
            data = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.config.CHUNK_SIZE,
                chunk_overlap=self.config.CHUNK_OVERLAP
            )
            texts = text_splitter.split_documents(data)

            db_dir = file_path.stem
            persist_directory = Path(self.config.CHROMA_DB_DIR) / db_dir

            vectordb = Chroma.from_documents(
                documents=texts,
                embedding=self.embeddings,
                persist_directory=str(persist_directory)
            )
            vectordb.persist()
            
            st.success("PDF processed and encoded successfully!")
            return True

        except Exception as e:
            st.error("Error processing PDF.")
            st.code(repr(e))
            logging.error(f"Error processing PDF: {traceback.format_exc()}")
            return False