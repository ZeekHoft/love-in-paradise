import requests
from bs4 import BeautifulSoup
import csv


num_links = 0
news_urls = [
    "https://www.rappler.com/philippines/new-us-sanctions-icc-judges-effect-duterte/",
    "https://www.rappler.com/philippines/duterte-request-disqualify-judges-icc-plenary/",
    "https://www.rappler.com/newsbreak/explainers/leila-sadat-expert-confident-charges-confirmation-duterte-icc/",
    "https://www.rappler.com/newsbreak/fact-check/rodrigo-duterte-recycled-items-statue-ai-generated/",
    "https://www.rappler.com/world/asia-pacific/thailand-cambodia-border-row-tensions-updates-june-6-2025/",
    "https://www.rappler.com/plus-membership-program/exclusive-content/sui-generis-win-canada-courts-2025/",
    "https://www.rappler.com/sports/nba/g00641685-pelicans/",
    "https://www.rappler.com/sports/nba/g44870615-oklahoma-city-thunder/",
    "https://www.rappler.com/sports/nba/g39262543-sacramento-kings/"
]

headlline_tag = "h1"
content_tag = "p"

for i in news_urls:
    response = requests.get(i)
    soup = BeautifulSoup(response.text, "html.parser")
    #HEADLINE
    def headeline():
        heading = soup.find_all(headlline_tag)  
        n=len(heading)
        if n <= 1:
            print(f"No headline of {headlline_tag} found")
        else:
            for i in range(n):
                print(str.strip(heading[i].text))

    #CONTENT
    def content():
        heading = soup.find_all(content_tag)
        n=len(heading)
        if n <= 1:
            print(f"No content of {content_tag} found")
        else:
            for i in range(n):
                print(F" {str.strip(heading[i].text)}")

    headeline()
    content()
 