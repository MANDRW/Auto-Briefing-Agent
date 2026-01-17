import time
import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

logger = logging.getLogger(__name__)

USER_AGENT = "Auto-Briefing-Agent/1.0 (Educational/Research Purpose)"
REQUEST_DELAY = 30


class HackerNewsScraper:

    def __init__(self, delay: float = REQUEST_DELAY):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENT
        })

    def scrape_top_articles(self, limit: int = 5) -> List[Dict[str, str]]:
        logger.info(f"Starting scrape of top {limit} articles from Hacker News")

        try:
            time.sleep(self.delay)

            response = self.session.get('https://news.ycombinator.com', timeout=10)
            response.raise_for_status()

            logger.info(f"Successfully fetched Hacker News page (Status: {response.status_code})")

            soup = BeautifulSoup(response.content, 'html.parser')

            articles = []
            article_rows = soup.find_all('tr', class_='athing')

            for idx, row in enumerate(article_rows[:limit]):
                try:
                    title_container = row.find(class_='titleline')
                    if not title_container:
                        continue

                    title_link = title_container.find('a')

                    if title_link:
                        title = title_link.get_text(strip=True)
                        url = title_link.get('href', '')

                        if url.startswith('item?'):
                            url = f"https://news.ycombinator.com/{url}"
                        elif not url.startswith('http'):
                            url = f"https://news.ycombinator.com/{url}"

                        articles.append({
                            'title': title,
                            'url': url
                        })
                        logger.info(f"Scraped article {idx + 1}: {title[:50]}...")

                except Exception as e:
                    logger.warning(f"Error parsing article {idx + 1}: {e}")
                    continue

            logger.info(f"Successfully scraped {len(articles)} articles")
            return articles

        except requests.RequestException as e:
            logger.error(f"Error fetching Hacker News: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during scraping: {e}")
            raise