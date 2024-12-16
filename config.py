import logging
import os
from typing import Dict
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self._load_config()
            self.initialized = True

    def _load_config(self):
        # Load environment variables from .env file
        load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

        # Application paths
        self.CODE_PATH = "./"
        self.CODE_FILE = 'output.txt'
        self.DATA_FOLDER = './data'
        self.CHROMA_DB_DIR = "./chroma_db"
        self.LOG_FILE = os.path.join(os.path.dirname(__file__), "app.log")

        # API Keys and Endpoints
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.GROQ_API_BASE = os.getenv("GROQ_API_BASE", "https://api.groq.com/openai/v1")

        # LLM Configuration
        self.LLM_MODEL = os.getenv("LLM_MODEL")
        self.MAX_TOKENS = int(os.getenv("MAX_TOKENS"))
        self.TEMPERATURE = float(os.getenv("TEMPERATURE"))

        # Chunking Configuration
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
        self.CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))

        # Server Configuration
        self.PORT = int(os.getenv("PORT"))
        self.HOST = os.getenv("HOST")

        # File handling configuration
        self.UPLOAD_DIR = "./uploads"
        self.CHROMA_DB_DIR = "./chroma_db"

        logger.info(f"Config loaded: {self.__dict__}")

    
