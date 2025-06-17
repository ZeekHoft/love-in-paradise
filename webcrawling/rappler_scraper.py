import requests
from bs4 import BeautifulSoup
import csv

from search_articles import Search_articles

num_links = 0


# im passing soup on each function parameter for reusability later, as the heading = soup same for content, if we want to repeat the same function without
# rebuilding the whole thing passing soup would be beneficial


class RapplerScraper:
    HEADLINE_TAG1 = "h1"
    HEADLINE_TAG2 = "h3"
    CONTENT_TAG = "p"

    def scrape_urls(self, news_urls):
        for news_url in news_urls:
            response = requests.get(news_url)
            soup = BeautifulSoup(response.text, "html.parser")
            soup.select()
            soup.find_all()
            print(news_url)
            print(self.get_headline(soup))
            print(self.get_content(soup))
            print()

    # Returns a list of headlines
    def get_headline(self, soup, tags=[]):
        # Set optional parameter
        if tags == []:
            tags = [self.HEADLINE_TAG1, self.HEADLINE_TAG2]

        for tag in tags:
            headings = soup.find_all(tag)

            n = len(headings)
            if n == 0:
                # No headlines found
                return []
            else:
                headlines = []
                for heading in headings:
                    headlines.append(str.strip(heading.text))
                return headlines

    # Return a string of the content.
    def get_content(self, soup):
        main_content = soup.find_all(self.CONTENT_TAG)
        soup.select
        n = len(main_content)
        if n <= 1:
            # No content found
            return ""
        else:
            return " ".join(str.strip(content.text) for content in main_content)
            # for i in range(n):
            #     print(f" {str.strip(main_content[i].text)}")


# search_news = Search_articles()
# news_urls = search_news.search_news(
#     "LIST: Schools, organizations pushing Senate to proceed with VP Sara impeachment"
# )
# rap_scrap = RapplerScraper()
# rap_scrap.scrape_urls(news_urls)
