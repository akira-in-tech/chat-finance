# ChatFinance

An AI-powered financial news chatbot built with Flask, OpenAI GPT, and LlamaIndex. Users can ask questions about financial news and receive intelligent, context-aware answers backed by a RAG (Retrieval-Augmented Generation) pipeline.

## Features

- Natural language Q&A over financial news articles
- Sentiment analysis on news content
- User authentication with session management
- MongoDB-backed news crawl status tracking
- Flask REST API backend with a responsive frontend

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask, Flask-Login |
| AI / RAG | OpenAI GPT, LlamaIndex, HuggingFace Transformers |
| Database | MongoDB |
| Frontend | HTML, CSS, JavaScript |

## Getting Started

### Prerequisites

- Python 3.9+
- MongoDB running locally or a connection URI
- OpenAI API key

### Installation

```bash
cd ChatFinance/APIs
pip install -r requirements.txt
```

Create a `.env` file (see `.env.example`):

```bash
cp .env.example .env
# Fill in your OPENAI_API_KEY and MONGODB_URI
```

Run the server:

```bash
python app.py
```

## Project Structure

```
ChatFinance/
├── APIs/
│   ├── app.py          # Flask application entry point
│   ├── config.py       # Configuration and paths
│   ├── models.py       # MongoDB user model
│   ├── requirements.txt
│   └── static/         # CSS, JS, images
│   └── templates/      # HTML templates
└── Frontend/           # Static frontend assets
```

## License

MIT License — see [LICENSE](LICENSE)
