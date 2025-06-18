from clasification.check import classify_input
from tokenization.english import Eng_Tokenization_NLP
from tokenization.util import pos_tokens
from webcrawling.search_articles import Search_articles
from webcrawling.rappler_scraper import RapplerScraper
from analysis.sentence_similarity import SentenceSimilarity


ACCEPT_LIST = ["news claim", "statement"]


def main():
    # Take claim input
    claim_input = "Vice President Sara Duterte stated that there is nothing wrong with sharing AI-generated videos."

    # Classify input if it is verifiable or not
    input_classification = classify_input(claim_input)
    if input_classification in ACCEPT_LIST:
        print(f"Input is a {input_classification}; proceeding to tokenization.")
    else:
        print("Input is not considered a news claim!")
        return

    # Tokenize
    tokenizer = Eng_Tokenization_NLP()
    tokenizer.tokenizationProcess(word_list=claim_input.split())
    print("Finished tokenization.")

    # Search articles/ Web crawling
    webcrawler = Search_articles()
    search_query = " ".join(pos_tokens["PROPN"] + pos_tokens["NOUN"])
    print("Search Terms: " + search_query + "\n")

    articles = webcrawler.search_news(
        search_query,
        exclude_terms="opinion",
        results_amt=3,
    )
    print("List of articles: " + str(articles) + "\n")

    # Scrape each article
    rappler_scraper = RapplerScraper()
    news_data = rappler_scraper.scrape_urls(articles)
    print("Headlines")
    for url, data in news_data.items():
        print(data["headline"])
        # print(data["content"])
    print()

    # Sentence similarity
    print("Finding relevant data:")
    sentence_similarity = SentenceSimilarity()
    sentence_similarity.set_main_sentence(claim_input)
    for url, data in news_data.items():
        ss = sentence_similarity.find_similar_sentences(data["content"])
        most_similar_sentence = ss[0]
        print(most_similar_sentence)
        print("--from " + url + "\n")


if __name__ == "__main__":
    main()
