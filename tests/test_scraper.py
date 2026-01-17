import pytest
from unittest.mock import Mock, patch
from app.scraper import HackerNewsScraper, USER_AGENT, REQUEST_DELAY


def test_scraper_initialization():
    scraper = HackerNewsScraper()
    assert scraper.delay == REQUEST_DELAY
    assert scraper.session.headers['User-Agent'] == USER_AGENT


def test_scraper_custom_delay():
    scraper = HackerNewsScraper(delay=5.0)
    assert scraper.delay == 5.0


@patch('app.scraper.requests.Session.get')
def test_scrape_top_articles_logic(mock_get):

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"""
    <html>
        <body>
            <table>
                <tr class="athing">
                    <td class="title">
                        <span class="titleline">
                            <a href="https://example.com/ai-news">Super AI Project</a>
                        </span>
                    </td>
                </tr>
                <tr class="athing">
                    <td class="title">
                        <span class="titleline">
                            <a href="item?id=12345">Show HN: Local Link</a>
                        </span>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """
    mock_get.return_value = mock_response

    scraper = HackerNewsScraper(delay=0)
    articles = scraper.scrape_top_articles(limit=2)

    assert len(articles) == 2
    assert articles[0]['title'] == "Super AI Project"
    assert articles[0]['url'] == "https://example.com/ai-news"

    assert articles[1]['url'] == "https://news.ycombinator.com/item?id=12345"