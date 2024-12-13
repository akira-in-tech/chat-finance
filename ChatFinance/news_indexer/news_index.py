import os

import config

os.environ['OPENAI_API_KEY'] = config.OPENAI_API_KEY
# from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
# new version replaces GPTSimpleVectorIndex with GPTVectorStoreIndex

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader(config.NEWS_DATA).load_data()

index = VectorStoreIndex.from_documents(documents)

# llama index 0.6 replaces index.save_to_disk() with index.storage_context.persist()
# json files will be stored in a storage/ directory instead of index_new.json
# index.save_to_disk('index_news.json')

index.storage_context.persist(config.INDEX_PERSIST_DIR)
import pymongo
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
db_name = os.getenv("MONGODB_DATABASE")
collection_name = os.getenv("MONGODB_COLLECTION")
index_persist_dir = os.getenv("INDEX_PERSIST_DIR", "./index_storage")

# Validate required variables
if not db_name or not collection_name:
    raise ValueError("MONGODB_DATABASE or MONGODB_COLLECTION is not set. Please check your .env file.")
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")

# MongoDB Connection
client = pymongo.MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

# Debugging: Confirm connection
print(f"Connected to database: {db_name}, collection: {collection_name}")

# Fetch enriched documents from MongoDB
documents = []
for doc in collection.find({"indexed": False}):
    try:
        content = f"{doc.get('body', '')} Key Phrases: {', '.join(doc.get('key_phrases', []))}. Sentiment: {doc.get('sentiment', 'N/A')} (Score: {doc.get('sentiment_score', 0)})."
        documents.append({"text": content, "metadata": {"url": doc.get('url'), "doc_name": doc.get('doc_name')}})
    except KeyError as e:
        print(f"Document missing key {e}. Skipping...")

# Create or Load Index
if not os.path.exists(index_persist_dir):
    print("Creating a new index...")
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(index_persist_dir)
else:
    print("Loading existing index...")
    storage_context = StorageContext.from_defaults(persist_dir=index_persist_dir)
    index = load_index_from_storage(storage_context)

# Update MongoDB Indexed Status
for doc in documents:
    collection.update_one({"doc_name": doc['metadata']['doc_name']}, {"$set": {"indexed": True}})

print("Indexing completed.")

