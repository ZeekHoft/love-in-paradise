import requests
from dotenv import load_dotenv
import os

try:
    load_dotenv()
    API_KEY = os.getenv("GOOGLE_API_KEY")
    SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
    if API_KEY is None or SEARCH_ENGINE_ID is None:
        raise ValueError("API keys were not found")
except Exception as e:
    print(f"Error Loading API keys: {e}")


URL = "https://www.googleapis.com/customsearch/v1"


class Search_articles(object):

    # Returns a list of urls of news articles based on search query
    def search_news(
        self,
        search_query,
        date_restrict="",
        exact_terms="",
        exclude_terms="",
        or_terms="",
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
            "orTerms": or_terms,
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
