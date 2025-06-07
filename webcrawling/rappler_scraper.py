import requests
from bs4 import BeautifulSoup
import csv

from search_articles import search_news
news_urls = (search_news("LIST: Schools, organizations pushing Senate to proceed with VP Sara impeachment"))
for i in news_urls:
    print(i)

num_links = 0

headline_tag1 = "h1"
headline_tag2 = "h3"
content_tag = "p"

#im passing soup on each function parameter for reusability later, as the heading = soup same for content, if we want to repeat the same function without
#rebuilding the whole thing passing soup would be beneficial
for i in news_urls:
    response = requests.get(i)
    soup = BeautifulSoup(response.text, "html.parser")
    #HEADLINE
    def headeline(soup, tags = [headline_tag1, headline_tag2]):
        for tag in tags:
            heading = soup.find_all(tag)  
            n=len(heading)
            if n == 0:
                print(f"No headline of {tag} found")
            else:
                for i in range(n):
                    print(str.strip(heading[i].text))

    #CONTENT
    def content(soup):
        main_content = soup.find_all(content_tag)
        n=len(main_content)
        if n <= 1:
            print(f"No content of {content_tag} found")
        else:
            for i in range(n):
                print(F" {str.strip(main_content[i].text)}")

    headeline(soup)
    content(soup)
 