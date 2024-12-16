import os
import logging
import traceback
import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from config import Config

config = Config()

def query_llm(question, db_dir):
    """Query the language model with the provided question."""
    logger = logging.getLogger(__name__)
    try:
        llm = ChatGroq(
            api_key=config.GROQ_API_KEY,
            model_name=config.LLM_MODEL,
            max_tokens=config.MAX_TOKENS,
            temperature=config.TEMPERATURE
        )
        chain = load_qa_chain(llm, chain_type="stuff")

        embeddings = OpenAIEmbeddings(openai_api_key = config.OPENAI_API_KEY)
        persist_directory = os.path.join(config.CHROMA_DB_DIR, db_dir)
        db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

        matching_docs = db.similarity_search(question)
        openai_ans = chain.run(input_documents=matching_docs, question=question)

        st.session_state["matching_docs"].append(matching_docs)
        st.session_state["history"].append({"question": question, "answer": openai_ans})

    except Exception as e:
        st.error("Error querying LLM.")
        st.write(traceback.format_exc())
        logger.error(f"Error querying LLM: {traceback.format_exc()}") 