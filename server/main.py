from analysis.open_info_extraction import OpenInformationExtraction
from analysis.sentence_similarity import SentenceSimilarity
from analysis.evidence_alignment import EvidenceAlignment
from webcrawling.search_articles import Search_articles
from webcrawling.rappler_scraper import RapplerScraper
from webcrawling.article_scraper import ArticleScraper
from tokenization.english import Eng_Tokenization_NLP
from llm.fact_checker_agent import FactCheckerAgent
from clasification.check import classify_input
from analysis.utils import generate_graph

from typing import Generator
from time import time
import spacy


ACCEPT_LIST = ["news claim", "statement", "question"]
news = "Vice President Sara Duterte stated that there is nothing wrong with sharing AI videos."
# news = "Firm owned by Bong Go’s kin once worked with Discayas for Davao projects"
# news = "All persons who received a COVID-19 vaccine may develop diseases such as cancer and vision loss."
nlp = spacy.load("en_core_web_sm")


def love_in_paradise(claim, use_llm=False) -> Generator[dict, None, None]:
    """
    Algorithm for verifying if a claim is true or not using online sources.

    This is a generator that yields a dictionary containing its current process
    until the whole algorithm is finished.
    """

    # Data to return to server
    results = {
        "verdict": None,
        "justification": None,
        "confidence": None,
        "sources": [],
        "currentProcess": None,
        "progress": 0.0,
    }

    results["currentProcess"] = "Checking if claim is verifiable"
    results["progress"] = 1 / 8
    yield results

    # Take claim input
    claim_input = claim

    # Tokenize
    tokenizer = Eng_Tokenization_NLP()
    tokenizer.tokenizationProcess(word_list=claim_input.split())
    print("Finished tokenization.")

    # Classify input if it is verifiable or not
    webcrawler = Search_articles()
    try:
        input_classification = classify_input(claim_input)
        if input_classification in ACCEPT_LIST:

            results["currentProcess"] = "Searching the web"
            results["progress"] = 2 / 8
            yield results

            print(f"Input is a {input_classification}; proceeding to tokenization.")
            search_query = " ".join(
                tokenizer.pos_tokens["PROPN"] + tokenizer.pos_tokens["NOUN"]
            )

            # Search articles/ Web crawling
            print("Search Terms: " + search_query + "\n")
            articles = webcrawler.search_news(
                search_query,
                exclude_terms="opinion",
                results_amt=5,
            )
        else:
            print("Input is not considered a news claim!")
            results["justification"] = "Input is not considered a news claim!"
            yield results
            return
    except Exception as e:
        print((f"News claim has missing some missing key elements: {e}"))
        results["justification"] = (
            f"News claim has missing some missing key elements: {e}"
        )
        yield results
        return

    results["currentProcess"] = "Retrieving data from articles"
    results["progress"] = 3 / 8
    yield results

    # Scrape each article
    # rappler_scraper = RapplerScraper()
    # news_data = rappler_scraper.scrape_urls(articles)

    articleScraper = ArticleScraper()
    news_data = articleScraper.article_scraper(articles)

    # !! TODO: text processing of article content here !!

    print("Scraped Articles ==================================")
    for url, data in news_data.items():
        print(url)
        print(data["headline"])
        # print(data["content"])
        # return data["content"]

    results["currentProcess"] = "Searching for relevant information"
    results["progress"] = 4 / 8
    yield results

    # SEMANTIC SENTENCE SEARCH
    # Filtering out the most relevant data
    print("Finding relevant data:")
    sentence_similarity = SentenceSimilarity(nlp)
    sentence_similarity.set_main_sentence(claim_input)
    relevant_sentences = {}
    for url, data in news_data.items():
        ss = sentence_similarity.find_similar_sentences(data["content"])
        print(data["headline"])
        if ss == []:
            print("No similar sentences found.")
        else:
            print("SCORE | SENTENCE")
            for sentence, score in ss:
                print(f"{score:.4f} | {sentence}")
                if url not in relevant_sentences.keys():
                    relevant_sentences[url] = [sentence]
                else:
                    relevant_sentences[url].append(sentence)
        print()

    results["currentProcess"] = "Extracting information"
    results["progress"] = 5 / 8
    yield results

    # Information Extraction
    # ===============================================================
    try:
        triples = {}
        """
        triples = {
            url: [(triple), (triple)],
        }
        """
        only_triples = []
        info_ext = OpenInformationExtraction()
        for url, sentences in relevant_sentences.items():
            url_triples = []
            for sent in sentences:
                gen_triples = info_ext.generate_triples(sent)
                if gen_triples:
                    url_triples.extend(gen_triples)
            if url_triples != []:
                triples[url] = url_triples
                only_triples.extend(url_triples)
        claim_triple = info_ext.generate_triples(claim_input)

        # generate_graph(only_triples)

        results["currentProcess"] = "Comparing evidence to claim"
        results["progress"] = 6 / 8
        yield results

        # CLAIM-EVIDENCE ALIGNMENT & ENTAILMENT SCORING
        # ===============================================================
        # Given a list of the most relevant sentences from articles, evaluate them against the claim
        # -> evidences = {"agree", "disagree", "neutral"}
        evidence_alignment = EvidenceAlignment()
        relevant_evidence = []
        # get related triples
        subjects = []
        for ct in claim_triple:
            subjects.append(ct[0])
            subjects.append(ct[2])

        print("subjects: ", subjects)
        print("Relevant evidences:")
        for source, url_triple in triples.items():
            for tri in url_triple:
                if list(set(subjects) & set(tri)):
                    # print(f"urls in tri: {tri}")
                    relevant_evidence.append(" ".join(tri))
        # print(f"evidences: {relevant_evidence}")

        if subjects == [] or relevant_evidence == []:
            results["justification"] = "This news claim seems to be low on information"
            yield results
            return
        else:
            alignments = evidence_alignment.calculate_entailment(
                claim_input, relevant_evidence
            )
            evidence_count = {
                "neutral": 0,
                "entailment": 0,
                "contradiction": 0,
            }
            evidence_values = {
                "neutral": 0,
                "entailment": 0,
                "contradiction": 0,
            }
            for label, score in alignments:
                evidence_count[label] += 1
                evidence_values[label] += score.item()
            print("Evidences found:")
            print(evidence_count)
            print(evidence_values)
    except Exception as e:
        results["justification"] = f"Error in algo here: {e}"
        yield results
        return

    # AGGREGATION
    # ===============================================================
    # More agree-ing evidences: higher confidence, -> True
    # Few agree-ing evidences: low confidence,-> Likely True
    # Divisive, 50-50 agree/disagree: Unsure, Need more information
    # Few disagree-ing confidence: low confidence, -> Likely False
    # More disagree-ing confidence: high confidence, -> False

    results["currentProcess"] = "Finalizing score"
    results["progress"] = 7 / 8
    yield results

    entailment = evidence_values["entailment"]
    contradiction = evidence_values["contradiction"]

    # Score calculation
    score = (entailment - contradiction) / (entailment + contradiction + 1)
    confidence = abs(score) * 100
    print(f"Confidence Level: {confidence:.1f}%")

    # Verdict Assigment
    THRESHOLD1 = 0.3
    THRESHOLD2 = 0.45
    if -THRESHOLD1 < score < THRESHOLD1:
        verdict = "UNSURE"
    elif score <= -THRESHOLD2:
        verdict = "FALSE"
    elif score <= -THRESHOLD1:
        verdict = "LIKELY FALSE"
    elif score >= THRESHOLD2:
        verdict = "TRUE"
    elif score >= THRESHOLD1:
        verdict = "LIKELY TRUE"

    print(f"Claim: {claim_input}")
    print(f"VERDICT: {verdict}")

    # JUSTIFICATION GENERATION
    # ===============================================================
    # Use a template sentence for justification
    # Some things to display:
    # - Verdict
    # - Justification
    # - Top evidences
    # - Sources

    if use_llm:
        print("==============================")
        print("LLM Response:")
        fca = FactCheckerAgent(claim=claim_input, knowledge=str(relevant_sentences))
        agent_response = fca.verify()
        if agent_response:
            results["verdict"] = agent_response[0]
            results["justification"] = agent_response[1]
            results["sources"] = list(relevant_sentences.keys())
        else:
            # No data from LLM API
            results["justification"] = "Error: No response from LLM"
            yield results
            return

    else:
        # Manual method
        results["verdict"] = verdict
        results["justification"] = "No justification yet"
        results["confidence"] = confidence
        results["sources"] = list(triples.keys())

    results["currentProcess"] = "Complete"
    results["progress"] = 8 / 8
    yield results
    return


# if __name__ == "__main__":
#     # New way to run code:
#     lip = love_in_paradise(news)
#     for result in lip:
#         print(result)
