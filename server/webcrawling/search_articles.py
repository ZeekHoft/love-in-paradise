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

    def search_news(
        self,
        search_query,
        date_restrict="",
        exact_terms="",
        exclude_terms="",
        or_terms="",
        results_amt=20,  # Changed default from 10 to 20
    ):
        """
        Returns a list of news article URLs based on search query parameters.
        Supports pagination to get more than 10 results.
        """
        article_urls = []
        
        if results_amt > 100:
            print("Search results can not be more than 100")
            results_amt = 100
        
        start = 1  # First item in page 1 (page 2 starts at 11)
        num = 10 if results_amt > 10 else results_amt  # Cap at 10 per request
        
        while results_amt > 0:
            params = {
                "q": search_query,
                "key": API_KEY,
                "cx": SEARCH_ENGINE_ID,
                "dateRestrict": date_restrict,  # dwmy[number]
                "exactTerms": exact_terms,
                "excludeTerms": exclude_terms,
                "num": num,
                "start": start,
                "orTerms": or_terms,
            }
            
            try:
                response = requests.get(url=URL, params=params, timeout=10)
                
                # Debug info
                print(f"API Request: start={start}, num={num}")
                print(f"API Response Status: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"API Error: Status {response.status_code}")
                    print(f"Response: {response.text[:500]}")
                    break
                
                results = response.json()
                
                # Check for errors
                if "error" in results:
                    print(f"Google API Error: {results['error']}")
                    if "message" in results["error"]:
                        print(f"Error message: {results['error']['message']}")
                    break
                
                # Debug search info
                if "searchInformation" in results:
                    total = results["searchInformation"].get("totalResults", "0")
                    print(f"Total results available: {total}")
                
                # Extract URLs
                if "items" in results:
                    for result in results["items"]:
                        article_url = result["link"]
                        article_urls.append(article_url)
                    print(f"Found {len(results['items'])} articles in this batch")
                else:
                    print("No items in results - search may have no matches")
                    break
                
                # Move to next page
                results_amt -= num
                start += 10
                num = 10 if results_amt > 10 else results_amt
                
            except requests.exceptions.Timeout:
                print("Request timeout - API took too long to respond")
                break
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                break
        
        print(f"Total articles collected: {len(article_urls)}")
        return article_urls


# Standalone function wrapper for easier importing
def search_news(
    search_query,
    date_restrict="",
    exact_terms="",
    exclude_terms="",
    or_terms="",
    results_amt=20,
):
    """
    Convenience function that wraps Search_articles.search_news()
    Returns a list of news article URLs based on search query parameters.
    """
    searcher = Search_articles()
    return searcher.search_news(
        search_query=search_query,
        date_restrict=date_restrict,
        exact_terms=exact_terms,
        exclude_terms=exclude_terms,
        or_terms=or_terms,
        results_amt=results_amt,
    )


# Test code (uncomment to test)
# if __name__ == "__main__":
#     results = search_news("earthquakes Philippines", results_amt=20)
#     print(f"\nFinal results: {len(results)} URLs")
#     for url in results:
#         print(url)