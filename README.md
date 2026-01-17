# Auto-Briefing-Agent

A robust, Dockerized API service using FastAPI that scrapes news titles from Hacker News (news.ycombinator.com), deduplicates them using a database, and prepares them for an LLM pipeline.

## Features

- **FastAPI** web framework for high-performance API endpoints
- **SQLModel** with SQLite for efficient data storage and deduplication
- **BeautifulSoup** for web scraping with ethical considerations
- **Docker** containerization for easy deployment
- **Structured logging** for monitoring and debugging
- **Robots.txt compliance** with request delays and custom User-Agent

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and endpoints
│   ├── scraper.py       # Hacker News scraping logic
│   ├── models.py        # Database models (Article)
│   └── database.py      # Database connection and session management
├── tests/
│   ├── __init__.py
│   ├── test_main.py     # API endpoint tests
│   └── test_scraper.py  # Scraper tests
├── Dockerfile           # Production-ready container definition
├── docker-compose.yml   # Docker Compose configuration
├── requirements.txt    # Python dependencies
└── README.md

```

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and run the service:**
   ```bash
   docker-compose up --build
   ```

2. **The API will be available at:**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t auto-briefing-agent .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 -v $(pwd)/articles.db:/app/articles.db auto-briefing-agent
   ```

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Run tests:**
   ```bash
   pytest tests/
   ```

## API Endpoints

### POST `/scrape`

Scrapes the top 5 articles from Hacker News and returns only new articles (deduplicated by URL).

**Request:**
```bash
curl -X POST http://localhost:8000/scrape
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Article Title",
    "url": "https://example.com/article",
    "created_at": "2024-01-01T12:00:00",
    "is_processed": false
  }
]
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### GET `/`

Root endpoint with API information.

## Database Schema

The `Article` table contains:
- `id`: Primary key (auto-increment)
- `title`: Article title (indexed)
- `url`: Article URL (unique, indexed)
- `created_at`: Timestamp of when the article was scraped
- `is_processed`: Boolean flag for LLM pipeline processing status

## Ethical Scraping

The scraper implements several ethical practices:

1. **Custom User-Agent**: Identifies the bot with contact information
2. **Request Delays**: 2-second delay between requests to respect robots.txt
3. **Error Handling**: Graceful handling of network errors and parsing issues
4. **Logging**: Comprehensive logging of all scraping activities

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Structure

- **main.py**: FastAPI application with endpoint definitions
- **scraper.py**: HackerNewsScraper class with scraping logic
- **models.py**: SQLModel Article model definition
- **database.py**: Database initialization and session management

## License

This project is for educational/research purposes.
