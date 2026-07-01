from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ==========================
# LLM
# ==========================

LLM_PROVIDER = config(
    "LLM_PROVIDER",
    default="gemini"
)

LLM_MODEL = config(
    "LLM_MODEL",
    default="gemini-2.5-flash"
)

GOOGLE_API_KEY = config(
    "GOOGLE_API_KEY"
)

# ==========================
# Embeddings
# ==========================

EMBEDDING_MODEL = config(
    "EMBEDDING_MODEL"
)

# ==========================
# Chroma
# ==========================

CHROMA_DB_PATH = BASE_DIR / config(
    "CHROMA_DB_PATH"
)

# ==========================
# RAG
# ==========================

TOP_K_RESULTS = config(
    "TOP_K_RESULTS",
    cast=int,
    default=5
)

CHUNK_SIZE = config(
    "CHUNK_SIZE",
    cast=int,
    default=500
)

CHUNK_OVERLAP = config(
    "CHUNK_OVERLAP",
    cast=int,
    default=50
)

# ==========================
# Cache
# ==========================

CACHE_TIMEOUT = config(
    "CACHE_TIMEOUT",
    cast=int,
    default=300
)