import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the repository root .env file, regardless of cwd.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

@dataclass
class Config:
    """Configuration settings for the RAG system"""
    # Zhipu/Z.ai API settings
    ZAI_API_KEY: str = os.getenv("ZAI_API_KEY", "")
    ZAI_MODEL: str = os.getenv("ZAI_MODEL", "glm-4.7-flash")
    
    # Embedding model settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Document processing settings
    CHUNK_SIZE: int = 800       # Size of text chunks for vector storage
    CHUNK_OVERLAP: int = 100     # Characters to overlap between chunks
    MAX_RESULTS: int = 5         # Maximum search results to return
    MAX_HISTORY: int = 2         # Number of conversation messages to remember
    
    # Database paths
    CHROMA_PATH: str = "./chroma_db"  # ChromaDB storage location

config = Config()


