from clasification.check import classify_input
from tokenization.english import Eng_Tokenization_NLP
from tokenization.util import pos_tokens
from webcrawling.search_articles import Search_articles
from webcrawling.rappler_scraper import RapplerScraper
from analysis.sentence_similarity import SentenceSimilarity
from time import time


ACCEPT_LIST = ["news claim", "statement"]
durations = []


def main():
    time_overall = time()
    # Take claim input
    claim_input = "Vice President Sara Duterte stated that there is nothing wrong with sharing AI-generated videos."

    time_section = time()
    # Classify input if it is verifiable or not
    input_classification = classify_input(claim_input)
    if input_classification in ACCEPT_LIST:
        print(f"Input is a {input_classification}; proceeding to tokenization.")
    else:
        print("Input is not considered a news claim!")
        return
    durations.append(time() - time_section)

    # Tokenize
    time_section = time()
    tokenizer = Eng_Tokenization_NLP()
    tokenizer.tokenizationProcess(word_list=claim_input.split())
    durations.append(time() - time_section)
    print("Finished tokenization.")

    # Search articles/ Web crawling
    time_section = time()
    webcrawler = Search_articles()
    search_query = " ".join(pos_tokens["PROPN"] + pos_tokens["NOUN"])
    print("Search Terms: " + search_query + "\n")

    articles = webcrawler.search_news(
        search_query,
        exclude_terms="opinion",
        results_amt=3,
    )
    durations.append(time() - time_section)
    print("List of articles: " + str(articles) + "\n")

    # Scrape each article
    time_section = time()
    rappler_scraper = RapplerScraper()
    news_data = rappler_scraper.scrape_urls(articles)
    durations.append(time() - time_section)
    print("Headlines")
    for url, data in news_data.items():
        print(data["headline"])
        # print(data["content"])
    print()

    # Sentence similarity
    print("Finding relevant data:")
    time_section = time()
    sentence_similarity = SentenceSimilarity()
    sentence_similarity.set_main_sentence(claim_input)
    for url, data in news_data.items():
        ss = sentence_similarity.find_similar_sentences(data["content"])
        most_similar_sentence = ss[0]
        print(most_similar_sentence)
        print("--from " + url + "\n")
    durations.append(time() - time_section)
    durations.append(time() - time_overall)


def display_time():
    print(f"Classification: {durations[0]} seconds")
    print(f"Tokenization: {durations[1]} seconds")
    print(f"Searching: {durations[2]} seconds")
    print(f"Page Scraping: {durations[3]} seconds")
    print(f"Sentence Similarity: {durations[4]} seconds")
    print(f"Overall program execution: {durations[5]} seconds")


if __name__ == "__main__":
    main()
    display_time()
