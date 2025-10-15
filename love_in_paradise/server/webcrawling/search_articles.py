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


def search_news(
    search_query,
    date_restrict="",
    exact_terms="",
    exclude_terms="",
    or_terms="",
    results_amt=10,
):
    """
    Returns a list of news article URLs based on search query parameters.
    """
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

    if results_amt > 100:
        print("Search results can not be more than 100")
        results_amt = 100

    start = 1  # first item in page 1 (page 2 is 11)
    num = 10 if results_amt > 10 else results_amt  # cap at 10

    while results_amt > 0:
        params["num"] = num
        params["start"] = start
        response = requests.get(url=URL, params=params)
        results = response.json()

        if "items" in results:
            for result in results["items"]:
                article_url = result["link"]
                article_urls.append(article_url)
        else:
            print("no items in results")
            break

        results_amt -= num
        start += 10
        num = 10 if results_amt > 10 else results_amt

    return article_urls
