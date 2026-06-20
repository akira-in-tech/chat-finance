import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INDEX_PERSIST_DIR = os.getenv("INDEX_PERSIST_DIR", os.path.join(BASE_DIR, "../index_persist"))
NEWS_DATA = os.getenv("NEWS_DATA_DIR", os.path.join(BASE_DIR, "../news_crawler/news_data"))
