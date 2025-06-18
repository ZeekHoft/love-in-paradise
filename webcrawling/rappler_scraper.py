import requests
from bs4 import BeautifulSoup

# import csv

# from .search_articles import Search_articles

num_links = 0


# im passing soup on each function parameter for reusability later, as the heading = soup same for content, if we want to repeat the same function without
# rebuilding the whole thing passing soup would be beneficial
class RapplerScraper:
    HEADLINE_TAG1 = "h1"
    HEADLINE_TAG2 = "h3"
    CONTENT_TAG = "p"

    def scrape_urls(self, news_urls):
        scraped_data = {}
        for news_url in news_urls:
            response = requests.get(news_url)
            soup = BeautifulSoup(response.text, "html.parser")
            scraped_data[news_url] = {
                "headline": self.get_headline(soup)[0],
                "content": self.get_content(soup),
            }
        return scraped_data

    # Returns a list of headlines
    def get_headline(self, soup, tags=[]):
        # Set optional parameter
        if tags == []:
            tags = [self.HEADLINE_TAG1, self.HEADLINE_TAG2]

        headlines = []
        for tag in tags:
            headings = soup.find_all(tag)
            if len(headings) != 0:
                for heading in headings:
                    headlines.append(str.strip(heading.text))
        return headlines

    # Return a string of the content.
    def get_content(self, soup):
        content_containers = soup.find_all("div", class_="entry-content")
        main_content = []
        for container in content_containers:
            found_content = container.find_all(self.CONTENT_TAG)
            main_content += found_content
        if len(main_content) <= 1:
            # No content found
            return ""
        else:
            return " ".join(str.strip(content.text) for content in main_content)


# search_news = Search_articles()
# news_urls = search_news.search_news(
#     "LIST: Schools, organizations pushing Senate to proceed with VP Sara impeachment"
# )
# rap_scrap = RapplerScraper()
# print(rap_scrap.scrape_urls(news_urls))
