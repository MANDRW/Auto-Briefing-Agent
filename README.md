# Auto-Briefing-Agent
Auto-Briefing-Agent is a Dockerized FastAPI service that scrapes headlines from Hacker News, deduplicates them, and prepares them for a newsletter/LLM-powered briefing pipeline.

It supports scheduled scraping and sending daily briefings via email using LLMs (e.g., Gemini) and Gmail credentials.

## Features
- **Scrapes top stories from Hacker News**
- **Deduplicates articles using a SQLite database**
- **Prepares content for LLM-based summarization**
- **Sends briefings via email using Gmail SMTP**
- **Fully containerized with Docker**

## Project Structure

```
.
├── app/
│   ├── main.py         # FastAPI application
│   ├── scraper.py      # Hacker News scrapers
│   ├── models.py       # DB models
│   └── database.py     # DB setup
├── tests/              # API & logic tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

```
## Prerequisites

Before running the application, ensure you have the following:
  
1. A Google Gemini API key  
2. Gmail credentials

---

## Installation

### Clone the Repository

```
git clone https://github.com/MANDRW/Auto-Briefing-Agent.git
cd Auto-Briefing-Agent
```
### Running with Docker
Build and start the services:
```
docker compose up --build
```

### Starting n8n
Open n8n in your browser:
```
http://localhost:5678/workflow/
```
## Importing the Workflow

1. Open the **n8n UI**
2. Click **Import Workflow**
3. Import the provided `workflow.json` file
4. Configure the required credentials:
   - Gemini API credentials
   - Gmail credentials
5. Set the recipient email address
6. Save and activate the workflow


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

##


