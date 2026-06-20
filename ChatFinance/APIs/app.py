import os
import datetime

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

from models import User

load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB
mongo_client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
db = mongo_client["financialnews"]
user_model = User(db)
bcrypt = Bcrypt()

# Environment config
INDEX_PERSIST_DIR = os.getenv("INDEX_PERSIST_DIR")
NEWS_DATA_DIR = os.getenv("NEWS_DATA_DIR")

# FinBERT sentiment pipeline
finbert_model_name = "yiyanghkust/finbert-tone"
tokenizer = AutoTokenizer.from_pretrained(finbert_model_name)
model = AutoModelForSequenceClassification.from_pretrained(finbert_model_name)
sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

rag_index = None


def initialize_index():
    global rag_index
    if os.path.exists(INDEX_PERSIST_DIR):
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_PERSIST_DIR)
        rag_index = load_index_from_storage(storage_context)
    else:
        documents = SimpleDirectoryReader(NEWS_DATA_DIR).load_data()
        for doc in documents:
            sentiment, sentiment_score = analyze_sentiment(doc["text"])
            doc.metadata["sentiment"] = sentiment
            doc.metadata["sentiment_score"] = sentiment_score
            doc.metadata["created_at"] = datetime.datetime.now().isoformat()
        rag_index = VectorStoreIndex.from_documents(documents)
        rag_index.storage_context.persist(INDEX_PERSIST_DIR)


def analyze_sentiment(text):
    result = sentiment_analyzer(text)
    return result[0]['label'], result[0]['score']


@app.route("/")
def home():
    return render_template('login.html')


@app.route('/search')
def search_page():
    return render_template('index.html')


@app.route("/results")
def results():
    return render_template('results.html')


@app.route("/query", methods=["GET"])
def query_index():
    query_text = request.args.get("text")
    if not query_text:
        return jsonify({"error": "No text found. Please include a ?text=blah parameter in the URL."}), 400

    query_engine = rag_index.as_query_engine()
    response = query_engine.query(query_text)
    sentiment, sentiment_score = analyze_sentiment(str(response))

    return jsonify({
        "response": str(response),
        "sentiment": sentiment,
        "sentiment_score": sentiment_score
    }), 200


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"success": False, "message": "username and password required!"}), 400
    return jsonify(user_model.create_user(username, password))


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"success": False, "message": "username and password are required!"}), 400
    return jsonify(user_model.authenticate_user(username, password))


if __name__ == "__main__":
    initialize_index()
    app.run(host="0.0.0.0", port=5600)
