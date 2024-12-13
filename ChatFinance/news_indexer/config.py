
OPENAI_API_KEY = "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"
# OPENAI_API_KEY = "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"


import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# # Update this to local path.
# INDEX_PERSIST_DIR = "../index_persist"
# # Update this to local path.
# NEWS_DATA = "../news_crawler/news_data"

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Path to persist the index
INDEX_PERSIST_DIR = os.path.join(BASE_DIR, "../index_persist")

# Path to the directory containing HTML news files
NEWS_DATA = os.path.join(BASE_DIR, "../news_crawler/news_data")

# Path configurations
INDEX_PERSIST_DIR = os.getenv("INDEX_PERSIST_DIR")
NEWS_DATA = os.getenv("NEWS_DATA_DIR")

if not INDEX_PERSIST_DIR or not NEWS_DATA:
    raise ValueError("File paths not found in .env file. Please define INDEX_PERSIST_DIR and NEWS_DATA_DIR.")

