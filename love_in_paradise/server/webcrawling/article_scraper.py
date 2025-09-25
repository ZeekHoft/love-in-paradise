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
    def article_scraper(self, article_links):
        try:
            from time import sleep

            sleep(1)  # delay to avoid limit rates
            article_content = []
            links_data = {}
            # add valid URL detector
            for url in article_links:
                url_i = newspaper.Article(url="%s" % (url), language="en")
                url_i.download()
                url_i.parse()
                # content = f"TITLE:{url_i.title} CONTENT: {url_i.text}"
                # article_content.append(content)

                links_data[url] = {
                    "headline": url_i.title,
                    "content": url_i.text,
                }

            return links_data
            # return "\n".join(article_content)
        except Exception as e:
            return f"Error scraping article: {e}"



# news = ArticleScraper()
# print(news.article_scraper(list_of_urls))
