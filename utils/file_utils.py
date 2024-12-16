import os
from pathlib import Path
import streamlit as st
from typing import List, Optional
from config import Config

config = Config()
class FileManager:
    def __init__(self, upload_dir: str = config.UPLOAD_DIR):
        self.upload_dir = Path(upload_dir)
        self._ensure_upload_dir()
        self.chroma_db_dir = Path(config.CHROMA_DB_DIR)
        self._ensure_chroma_db_dir()

    def _ensure_upload_dir(self):
        """Create upload directory if it doesn't exist."""
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def _ensure_chroma_db_dir(self):
        """Create ChromaDB directory if it doesn't exist."""
        self.chroma_db_dir.mkdir(parents=True, exist_ok=True)

    def save_uploaded_file(self, uploaded_file) -> Optional[Path]:
        """Save an uploaded file and return its path."""
        if uploaded_file is None:
            return None
        
        file_path = self.upload_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    
    def remove_file(self, file_path: Path):
        """Remove a file from the upload directory."""
        if file_path.exists():
            file_path.unlink()

    def list_processed_files(self) -> List[str]:
        """List all processed files in the ChromaDB directory."""
        if not self.chroma_db_dir.exists():
            return []
        return [f.name for f in self.chroma_db_dir.glob("*")]

    def get_file_path(self, filename: str) -> Path:
        """Get the full path for a filename."""
        return self.upload_dir / filename 