OPENAI_API_KEY = "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"
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to persist the index
INDEX_PERSIST_DIR = os.path.join(BASE_DIR, "../index_persist")

# Path to the directory containing HTML news files
NEWS_DATA = os.path.join(BASE_DIR, "../news_crawler/news_data")
