import requests

API_KEY = open("API_KEY").read()
SEARCH_ENGINE_ID = open("SEARCH_ENGINE_ID").read()
URL = "https://www.googleapis.com/customsearch/v1"


# Returns a list of urls of news articles based on search query
def search_articles(
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
