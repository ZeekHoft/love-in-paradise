from time import sleep
import newspaper

# import validators

# list_of_urls = [
#             "https://www.bworldonline.com/top-stories/2025/09/05/696236/philippine-banks-npl-ratio-rises-to-8-month-high-in-july",
#             "https://www.bworldonline.com/top-stories/2025/09/05/695808/ng-outstanding-debt-surges-to-record-p17-56-trillion-as-of-end-july",
#             "https://www.bworldonline.com/top-stories/2025/09/05/696273/new-law-allows-foreign-investors-to-lease-land-in-the-philippines-for-up-to-99-years",
#             "https://www.bworldonline.com/top-stories/2025/09/05/696136/philippine-inflation-quickens-to-1-5-in-august"
#             ]


# Parse through each url and display its content
class ArticleScraper:
    def article_scraper(self, article_links, delay=1.0):
        links_data = {}

        try:

            sleep(delay)  # delay to avoid limit rates

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

            print(
                f"Successfully scraped {len(links_data)} out of {len(article_links)} articles"
            )
            return links_data
            # return "\n".join(article_content)
        except Exception as e:
            # Return empty dict instead of string
            print(f"Error in article scraper: {e}")
            return {}


# news = ArticleScraper()
# print(news.article_scraper(list_of_urls))
