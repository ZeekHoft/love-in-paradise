import requests
import os

api_file_path = os.path.join(os.path.dirname(__file__), "API_KEY")
sei_file_path = os.path.join(os.path.dirname(__file__), "SEARCH_ENGINE_ID")

try:
    with open(api_file_path, "r") as f:
        API_KEY = f.read().strip()
    with open(sei_file_path, "r") as f:
        SEARCH_ENGINE_ID = f.read().strip()
except FileNotFoundError as e:
    print(f"file not found: {e}")


URL = "https://www.googleapis.com/customsearch/v1"


class Search_articles(object):




# Returns a list of urls of news articles based on search query
    def search_news(self,
        search_query,
        date_restrict="",
        exact_terms="",
        exclude_terms="",
        results_amt=10,
    ):
        article_urls = []
        params = {
            "q": search_query,
            "key": API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "dateRestrict": date_restrict,  # dwmy[number]
            "exactTerms": exact_terms,
            "excludeTerms": exclude_terms,
            "num": results_amt,
            # "orTerms": "",
        }

        response = requests.get(url=URL, params=params)
        results = response.json()

        if "items" in results:
            for result in results["items"]:
                article_url = result["link"]
                article_urls.append(article_url)

        return article_urls


# res = Search_articles()
# values = (res.search_news("Will new US sanctions on ICC judges be felt in Duterte case?"))

# for i in values:
#     print(i)

# results = search_news("Will new US sanctions on ICC judges be felt in Duterte case?")
# results = search_news("Will new US sanctions on ICC judges be felt in Duterte case?")
# for i in results:
#     print(i)
