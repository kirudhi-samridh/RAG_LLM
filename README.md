# Q and A - AI

# Table of Contents
- [Overview](#overview) 
- [Requirements](#requirements)
- [Installation and Usage](#installation-and-usage)
- [Project Structure](#project-structure)
- [Code Explanation](#code-explanation)

# Overview
This project is a Q&A application using Streamlit and the LangChain framework, integrated with OpenAI's and Groq's language models. The application allows users to:
- Upload PDF files
- Embed them into a vector database
- Perform similarity search (cosine similarity) on vector database to get matching documents
- Query the language model with question and retrieved matching documents as context for completion
- Display the response from the Language model for the query
- Keep track of the history of queries and their corresponding answers

# Requirements
- Python 3.11+
- Poetry for dependency management
- OpenAI API Key
- Groq API Key

# Installation and Usage
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd RAG_LLM
   ```

2. **Environment Setup**
   - Copy the `.env.dev` file to `.env`
   - Add your API keys and configure other settings:

3. **Install Dependencies**
   ```bash
   poetry shell
   poetry install
   ```

4. **Run the Application**
   ```bash
   poetry run streamlit run app.py
   ```

# Project Structure
```
RAG_LLM/
├── app.py                # Main application file
├── config.py             # Configuration management
├── pyproject.toml        # Project dependencies and metadata
├── .env.dev              # Environment variables
├── utils/
│   ├── __init__.py
│   ├── logging_utils.py  # Logging configuration
│   └── file_utils.py     # File operations
├── services/
│   ├── __init__.py
│   ├── pdf_service.py    # PDF processing service
│   └── llm_service.py    # LLM interaction service
└── ui/
    ├── __init__.py
    └── chat_ui.py        # UI components
```

# Code Explanation
1. **Configuration Management** (`config.py`)
   - Implements a Singleton pattern for configuration management
   - Loads environment variables from `.env` file
   - Provides centralized access to application settings
   - Includes configuration for LLM, chunking, and server settings

2. **PDF Processing Service** (`services/pdf_service.py`)
   - Handles PDF document loading and processing
   - Manages document chunking using RecursiveCharacterTextSplitter
   - Creates and manages vector embeddings using OpenAI
   - Stores embeddings in ChromaDB

3. **LLM Service** (`services/llm_service.py`)
   - Manages interactions with language models (Groq/OpenAI)
   - Performs similarity search in the vector database
   - Handles question-answering chain setup
   - Maintains chat history

4. **UI Components** (`ui/chat_ui.py`)
   - Manages Streamlit UI components
   - Handles session state management
   - Controls chat history display
   - Manages sidebar and chat interface

5. **Utility Functions**
   - **Logging** (`utils/logging_utils.py`): Configures application logging
   - **File Operations** (`utils/file_utils.py`): Handles file system operations

6. **Main Application** (`app.py`)
   - Orchestrates all components
   - Manages the main application flow
   - Handles user interactions
   - Coordinates between services

The application follows a modular microservices architecture, making it easy to maintain and extend. Each component has a specific responsibility and communicates with others through well-defined interfaces.