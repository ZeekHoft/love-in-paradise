





# import requests
# from bs4 import BeautifulSoup
# https://edition.cnn.com
# https://realpython.github.io/fake-jobs/



# URL = "https://edition.cnn.com"
# page = requests.get(URL)

# print(page.text) #outputs the whole page of


# soup = BeautifulSoup(page.content, "html.parser")

# results = soup.find(class_ ="layout__wrapper layout-homepage__wrapper")

# print(results.encode("utf-8"))
# # job_cards = results.find("div", class_="card-content")

# # for job_card in job_cards:
# #     title_element = job_cards.find("h2", class_="title")
# #     company_element = job_cards.find("h3", class_="company")
# #     location_element = job_cards.find("p", class_="location")
# #     print(title_element)
# #     print(company_element)
# #     print(location_element)


import requests
from bs4 import BeautifulSoup


URL = "https://lite.cnn.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


response = requests.get(URL, headers=HEADERS)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    headlines = soup.find_all("h3", class_ = "gd-c-promo-heading__title get-pics-bold nw-o-link-split__text")[:10]
    for index, headline in enumerate(headlines, 1):
        print(f"{index}. {headline.text.strip()}")

else:
    print("failed" + response.status_code)



