import newspaper
import requests
from time import sleep

class ArticleScraper:
    def article_scraper(self, article_links):
        links_data = {}
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            )
        }

        for url in article_links:
            try:
                sleep(1)  # Avoid rate limiting
                
                # First, check if the URL is even reachable
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code != 200:
                    print(f"Skipping {url}: status code {r.status_code}")
                    continue

                # Create article with custom config (longer timeout, user-agent)
                config = newspaper.Config()
                config.browser_user_agent = headers["User-Agent"]
                config.request_timeout = 15  # ⬅ longer timeout
                config.memoize_articles = False

                article = newspaper.Article(url=url, language="en", config=config)
                article.download()
                article.parse()

                if not article.text.strip():
                    print(f"⚠ Empty content for {url}")
                    continue

                links_data[url] = {
                    "headline": article.title.strip() if article.title else "Untitled",
                    "content": article.text.strip(),
                    "link": url,
                }

            except newspaper.article.ArticleException as e:
                print(f"❌ Newspaper failed for {url}: {e}")
            except requests.exceptions.RequestException as e:
                print(f"❌ Request failed for {url}: {e}")
            except Exception as e:
                print(f"⚠ Unexpected error for {url}: {e}")

        if not links_data:
            print("⚠ Problem occurred in scraping data")
        return links_data
