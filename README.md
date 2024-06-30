# Q and A - AI

# Table of Contents
- [Overview](#overview) 
- [Requirements](#requirements)
- [Installation and Usage](#installation-and-usage)
- [Code Explanation](#code-explanation)

# Overview
This project is a Q&A application using Streamlit and the LangChain framework, integrated with OpenAI's language models. The application allows users to,
- upload PDF files
- embed them into a vector database
- perform similarity search (cosine similarity) on vector database to get matching documents
- query the language model with question and retrieved matching documents as context for completion.
- The application displays the response from the Language model for the query.
- The application also keeps track of the history of queries and their corresponding answers, which can be displayed.

# Requirements
- Python 3.7+
- OpenAI API Key
- Groq API key

# Installation and Usage
- Python virtual environment can be used.
- Install Miniconda from https://docs.anaconda.com/miniconda/miniconda-install/
- Add OpenAI API key (OPENAI_API_KEY = "your_api_key") and Groq API key (GROQ_API_KEY = "your_api_key") to System Environment Variables
- Prepare Your Data
    - Place your dataset (PDF files) inside a directory named data.
    - Ensure the chroma_db directory exists in the project root for storing the vector database.
- Create a virtual environment:
    - Replace "project-dir" with your project directory and "env-name" with your environment name
       
  ```
  conda create --prefix "project-dir"\"env-name" python
  ```
- Activate the virtual environment:
    - Replace "project-dir" with your project directory and "env-name" with your environment name
  
  ```
  conda activate "project-dir"\"env-name"
  ```
- Install the Libraries:
  ```
  pip install "packages"
  ```
  - replace "packages" with packages in requirements.txt
- Run:
  ```
  streamlit run app.py
  ```
- Deactivate the Environment:
  ```
  deactivate
  ```

# Code Explanation
1. Setup Logging
    - setup_logging(log_file): This function sets up the logging configuration for the application. It defines the logging level, format, date format, filename, and file mode. This helps in capturing logs for debugging and monitoring purposes.

2. Session State Initialization
   - Session state variables are used to maintain the state of the application between user interactions.
   - The following session state variables are initialized if they do not already exist.
      - history: Stores the history of questions and answers.
      - matching_docs: Stores the documents that match the query.
      - selected_question: Stores the index of the selected question from the history.

4. List Files and Directories
    - list_files_in_directory(directory): This function lists all the files in the specified directory. It checks if the directory exists and returns a list of files.
    - list_dirs_in_directory(directory): This function lists all the directories in the specified directory. It checks if the directory exists and returns a list of directories.
    - These functions are used to populate the dropdowns for selecting a PDF file and a database directory.

5. Read and Process PDF
    - read_pdf(file_path): This function reads and processes the selected PDF file. It uses PyPDFLoader to load the PDF content and RecursiveCharacterTextSplitter to split the content into chunks. The chunks are then embedded using OpenAIEmbeddings and stored in a Chroma vector database. If successful, a success message is displayed; otherwise, an error message is shown.

6. Query the Language Model
    - query_llm(question, db_dir): This function queries the language model with the provided question. It initializes the language model using ChatGroq and loads a question-answering chain. It then performs a similarity search on the vector database to find matching documents and queries the language model with question and matching documents as context. The response along with question is appended to the history and matching documents to the matching_docs session state variables. If an error occurs, an error message is displayed.

7. Display Chat
    - display_chat(): This function displays the most recent chat (question and answer) from the session state. It checks if the history is not empty and writes the most recent question and answer to the Streamlit interface.

8. Display History
    - display_history(i): This function displays the history of a specific question. It takes an index i as a parameter and writes the question and answer corresponding to that index from the session state to the Streamlit interface.

9. Display Sidebar
    - display_sidebar(): This function displays the chat history in the sidebar. It iterates through the history and creates an expander for each question. Each expander contains a button to display the details of the question and answer from history. If the display button is clicked, the corresponding question index is stored in the selected_question session state variable.

10. Display Function
    - display(): This function determines whether to display the selected question's history or the most recent chat. It first calls display_sidebar() to show the chat history in the sidebar. Then, it checks if a question is selected (selected_question is not None) and displays the corresponding history using display_history(i). If no question is selected, it displays the most recent chat using display_chat().

11. Main Streamlit App
    - st.header("Q and A - AI"): This sets the header for the Streamlit application.
    - uploaded_file = st.selectbox("Select a file", files_select): This creates a dropdown for selecting a PDF file from the list of files in the ./data directory.
    - db_dir = st.selectbox("Select a DB", dir_select): This creates a dropdown for selecting a database directory from the list of directories in the ./chroma_db directory.
    - st.button("Embed", key="encode"): This button triggers the read_pdf(file_path) function to read and process the selected PDF file and store embedding in chroma db.
    - question = st.chat_input("Enter your question:"): This creates a chat input box for entering a question. If a question is entered, query_llm(question, db_dir) is called to similarity search in vector db to get relevant docs, query the language model and update the session state.
    - Finally, display() is called to display the chat or history based on the session state.
