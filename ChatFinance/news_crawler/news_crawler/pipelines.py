from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import datetime
import os
from pathlib import Path
import pymongo
import spacy
import uuid
from dotenv import load_dotenv

load_dotenv()

class NewsCrawlerPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        cls.mongodb_uri = crawler.settings.get("MONGODB_URI", "mongodb://localhost:27017/")
        cls.db_name = crawler.settings.get("MONGODB_DATABASE", "financial_news")
        cls.collection_name = crawler.settings.get("MONGODB_COLLECTION", "news_crawl_status")
        cls.file_dir = os.getenv("NEWS_DATA_DIR")
        if not cls.file_dir:
            raise ValueError("File directory path not found in .env file. Please define NEWS_DATA_DIR.")
        cls.nlp = spacy.load("en_core_web_sm")  # Load spaCy model

        # Initialize FinBERT sentiment analysis pipeline
        tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
        model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
        cls.sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def process_item(self, item, spider):
        url = item['url']
        query = {"url": url}
        doc = self.collection.find_one(query)
        if doc:
            raise DropItem(f"Already crawled {item['url']}.")

        # NLP Enrichment
        doc_text = item['body'].decode('utf-8')
        spacy_doc = self.nlp(doc_text)
        key_phrases = [chunk.text for chunk in spacy_doc.noun_chunks]

        # FinBERT Sentiment Analysis
        sentiment_result = self.sentiment_analyzer(doc_text[:512])  # Limit input to first 512 tokens
        sentiment = sentiment_result[0]["label"]  # 'Positive', 'Negative', or 'Neutral'
        sentiment_score = sentiment_result[0]["score"]

        item['key_phrases'] = key_phrases
        item['sentiment'] = sentiment
        item['sentiment_score'] = sentiment_score

        # Save enriched HTML file
        doc_uuid = str(uuid.uuid4())
        doc_path = os.path.join(self.file_dir, f"{doc_uuid}.html")
        try:
            Path(doc_path).write_bytes(item['body'])
        except:
            raise DropItem(f"Write doc failed {item['url']}.")

        # Write metadata and enrichment to MongoDB
        current_time = datetime.datetime.utcnow()
        update_doc = {
            "url": url,
            "doc_name": doc_uuid,
            "key_phrases": key_phrases,
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "last_modified": current_time,
            "created_at": current_time,
            "indexed": False
        }
        self.collection.insert_one(update_doc)
        return item

    def close_spider(self, spider):
        self.client.close()
