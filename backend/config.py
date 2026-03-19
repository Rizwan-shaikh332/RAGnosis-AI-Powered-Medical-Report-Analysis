import os
import pathlib
from dotenv import load_dotenv

# Load .env or .ENV (Windows is case-insensitive but dotenv looks for lowercase)
_base = pathlib.Path(__file__).parent
for _name in ('.env', '.ENV', '.Env'):
    _p = _base / _name
    if _p.exists():
        load_dotenv(dotenv_path=_p)
        break

class Config:
    # MongoDB
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/ragnosis")
    DB_NAME = os.getenv("DB_NAME", "ragnosis")

    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-production")
    JWT_EXPIRY_HOURS = 24

    # Groq
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # Upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}

    # Models
    SUMMARIZER_MODEL = "facebook/bart-large-cnn"
    BIOBERT_MODEL = "dmis-lab/biobert-base-cased-v1.1"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    FAISS_INDEX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models", "faiss_index")
    KNOWLEDGE_BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datasets", "medical_knowledge_base.jsonl")

    # CORS
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # Tesseract OCR (optional custom path for non-standard installations)
    TESSERACT_CMD = os.getenv("TESSERACT_CMD", None)
