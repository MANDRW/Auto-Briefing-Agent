import logging
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from contextlib import asynccontextmanager

from app.database import init_db, get_session
from app.models import Article
from app.scraper import HackerNewsScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Auto-Briefing-Agent API...")
    init_db()
    logger.info("API startup complete.")
    yield

    logger.info("Shutting down Auto-Briefing-Agent API...")


app = FastAPI(
    title="Auto-Briefing-Agent API",
    description="API service for scraping and deduplicating Hacker News articles",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    return {
        "message": "Auto-Briefing-Agent API",
        "version": "1.0.0",
        "endpoints": {
            "scrape": "POST /scrape - Scrape Hacker News and return new articles",
            "health": "GET /health - Health check endpoint"
        }
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/scrape", response_model=List[dict])
async def scrape_articles(session: Session = Depends(get_session)):
    logger.info("Scrape endpoint called")
    
    try:
        scraper = HackerNewsScraper()

        scraped_articles = scraper.scrape_top_articles(limit=5)
        logger.info(f"Scraped {len(scraped_articles)} articles from Hacker News")

        new_articles = []
        
        for article_data in scraped_articles:
            url = article_data['url']

            statement = select(Article).where(Article.url == url)
            existing = session.exec(statement).first()
            
            if existing:
                logger.info(f"Article with URL '{url[:50]}...' already exists, skipping")
                continue

            article = Article(
                title=article_data['title'],
                url=url,
                is_processed=False
            )
            
            session.add(article)
            session.commit()
            session.refresh(article)
            
            logger.info(f"Saved new article: {article.title[:50]}... (ID: {article.id})")
            
            new_articles.append({
                "id": article.id,
                "title": article.title,
                "url": article.url,
                "created_at": article.created_at.isoformat(),
                "is_processed": article.is_processed
            })
        
        logger.info(f"Returning {len(new_articles)} new articles")
        return new_articles
    
    except Exception as e:
        logger.error(f"Error in scrape endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")
