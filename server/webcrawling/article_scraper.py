import newspaper

class ArticleScraper:
    def article_scraper(self, article_links):
        links_data = {}
        
        try:
            from time import sleep
            sleep(1)  # delay to avoid limit rates
            
            # add valid URL detector
            for url in article_links:
                try:
                    url_i = newspaper.Article(url="%s" % (url), language="en")
                    url_i.download()
                    url_i.parse()

                    # Only add if we got valid content
                    if url_i.title and url_i.text:
                        links_data[url] = {
                            "headline": url_i.title,
                            "content": url_i.text,
                        }
                    else:
                        print(f"Skipping {url} - no content extracted")
                        
                except Exception as e:
                    # Log error but continue with other articles
                    print(f"Error scraping {url}: {e}")
                    continue
            
            print(f"Successfully scraped {len(links_data)} out of {len(article_links)} articles")
            return links_data
            
        except Exception as e:
            # Return empty dict instead of string
            print(f"Error in article scraper: {e}")
            return {}