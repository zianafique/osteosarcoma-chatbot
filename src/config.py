import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ========== API CONFIGURATION ==========
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"

# ========== VECTOR DATABASE CONFIGURATION ==========
CHROMA_PERSIST_DIR = "data/chroma_db"

# ========== EMBEDDING CONFIGURATION ==========
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ========== TEXT PROCESSING CONFIGURATION ==========
CHUNK_SIZE = 1000  # Characters per chunk
CHUNK_OVERLAP = 200  # Overlap between chunks for context
TOP_K_RESULTS = 3  # Number of context chunks to retrieve

# ========== FILE PATHS ==========
PDF_DIR = "pdfs"
