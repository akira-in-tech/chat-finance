import os

os.environ['OPENAI_API_KEY'] = "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"


from flask import Flask
from flask_login import LoginManager
from flask import request
from flask_cors import CORS
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage, GPTVectorStoreIndex

import config


from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from llama_index.core import StorageContext, VectorStoreIndex, SimpleDirectoryReader, load_index_from_storage
from dotenv import load_dotenv
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import datetime

from pymongo import MongoClient
from flask_bcrypt import Bcrypt

from models import User

load_dotenv()


app = Flask(__name__)
CORS(app)

# mongodb connection
client = MongoClient("mongodb://localhost:27017/")
db = client["financialnews"] # database
users_collection = db['users'] # table
user_model = User(db)

#initialize flask bcrypt
bcrypt = Bcrypt()

index = None

def initialize_index():
    global index
    storage_context = StorageContext.from_defaults(persist_dir=config.INDEX_PERSIST_DIR)
    if os.path.exists(config.INDEX_PERSIST_DIR):#index_dir):
        index = load_index_from_storage(storage_context)            
    else:
        documents = SimpleDirectoryReader(config.NEWS_DATA).load_data()
        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
        storage_context.persist(config.INDEX_PERSIST_DIR)
        

# Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

INDEX_PERSIST_DIR = os.getenv("INDEX_PERSIST_DIR")
NEWS_DATA_DIR = os.getenv("NEWS_DATA_DIR")

index = None

# Initialize FinBERT Sentiment Analysis Pipeline
finbert_model_name = "yiyanghkust/finbert-tone"
tokenizer = AutoTokenizer.from_pretrained(finbert_model_name)
model = AutoModelForSequenceClassification.from_pretrained(finbert_model_name)
sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Initialize or Load Index
def initialize_index():
    global index
    if os.path.exists(INDEX_PERSIST_DIR):
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_PERSIST_DIR)
        index = load_index_from_storage(storage_context)
    else:
        documents = SimpleDirectoryReader(NEWS_DATA_DIR).load_data()
        # Perform sentiment analysis on the documents when loading them
        for doc in documents:
            sentiment, sentiment_score = analyze_sentiment(doc["text"])
            doc.metadata["sentiment"] = sentiment
            doc.metadata["sentiment_score"] = sentiment_score
            doc.metadata["created_at"] = datetime.datetime.now().isoformat()  # Adding timestamp (optional)
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(INDEX_PERSIST_DIR)

# Function to perform sentiment analysis on text
def analyze_sentiment(text):
    result = sentiment_analyzer(text)
    return result[0]['label'], result[0]['score']  # Return sentiment label (Positive/Negative/Neutral) and confidence score


# home
@app.route("/")
def home():
    return render_template('login.html')

# Route for the home page (index.html)
@app.route('/search')
def index():
    return render_template('index.html')

@app.route("/results")
def results():
    return render_template('results.html')

# query
@app.route("/query", methods=["GET"])
def query_index():
    query_text = request.args.get("text", None)
    if query_text is None:
        return jsonify({"error": "No text found. Please include a ?text=blah parameter in the URL."}), 400
    
    # Query your index
    query_engine = index.as_query_engine()
    response = query_engine.query(query_text)

    # Analyze sentiment
    sentiment, sentiment_score = analyze_sentiment(str(response))

    return jsonify({
        "response": str(response),
        "sentiment": sentiment,
        "sentiment_score": sentiment_score
    }), 200



# register 
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"success": False, "message": "username and password required!"}), 400
    result = user_model.create_user(username, password)
    return jsonify(result)

# login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({'success': False, "message": "username and password are required!"}), 400
    result = user_model.authenticate_user(username, password)
    return jsonify(result)



# @app.route("/")
# def home():
#     return "Get insights from financial news!"

if __name__ == "__main__":
    initialize_index()
    app.run(host="0.0.0.0", port=5600)