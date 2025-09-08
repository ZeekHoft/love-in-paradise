from clasification.check import classify_input
from analysis.evidence_alignment import EvidenceAlignment
from tokenization.english import Eng_Tokenization_NLP
from webcrawling.search_articles import Search_articles
from webcrawling.rappler_scraper import RapplerScraper
from webcrawling.article_scraper import ArticleScraper
from analysis.sentence_similarity import SentenceSimilarity
from analysis.open_info_extraction import OpenInformationExtraction
from analysis.utils import generate_graph
import spacy
from time import time

# from llm.fact_checker_agent import FactCheckerAgent

ACCEPT_LIST = ["news claim", "statement", "question"]
durations = []
# news = "Vice President Sara Duterte stated that there is nothing wrong with sharing AI videos."
# news = "Firm owned by Bong Go’s kin once worked with Discayas for Davao projects"
news = "All persons who received a COVID-19 vaccine may develop diseases such as cancer and vision loss."
nlp = spacy.load("en_core_web_sm")


def love_in_paradise(claim):
    time_overall = time()
    # Take claim input
    claim_input = claim

    time_section = time()
    tokenizer = Eng_Tokenization_NLP()
    tokenizer.tokenizationProcess(word_list=claim_input.split())
    durations.append(time() - time_section)
    webcrawler = Search_articles()
    try:
        input_classification = classify_input(claim_input)
        if input_classification in ACCEPT_LIST :
            print(f"Input is a {input_classification}; proceeding to tokenization.")
            search_query = " ".join(tokenizer.pos_tokens["PROPN"] + tokenizer.pos_tokens["NOUN"])
            print("Search Terms: " + search_query + "\n")
            articles = webcrawler.search_news(
                search_query,
                exclude_terms="opinion",
                results_amt=5,
            )
        else:
            print("Input is not considered a news claim!")
            return ("Input is not considered a news claim!")
    except Exception as e:
        print((f"News claim has missing some missing key elements: {e}"))
        return (f"News claim has missing some missing key elements: {e}")


    # Classify input if it is verifiable or not
    
  
    durations.append(time() - time_section)
    # Tokenize
    time_section = time()
    
    print("Finished tokenization.")

    # *.rappler.com/*
    # Search articles/ Web crawling
    time_section = time()
   
    
    durations.append(time() - time_section)

    # Scrape each article
    time_section = time()

    # rappler_scraper = RapplerScraper()
    # news_data = rappler_scraper.scrape_urls(articles)

    articleScraper = ArticleScraper()
    news_data = articleScraper.article_scraper(articles)

    # !! Please do text processing of article content here !!

    durations.append(time() - time_section)

    print("Scraped Articles ==================================")
    for url, data in news_data.items():
        print(data["headline"])
        # print(data["content"])
        # return data["content"]

    # SEMANTIC SENTENCE SEARCH
    # Filtering out the most relevant data
    print("Finding relevant data:")
    time_section = time()
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
    durations.append(time() - time_section)

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
                    print(f"urls in tri: {tri}")
                    relevant_evidence.append(" ".join(tri))
        print(f"evidences: {relevant_evidence}")

        if subjects == [] and relevant_evidence == []:
            return "This news claim seems to be low on information"
        else:
            alignments = evidence_alignment.calculate_entailment(claim_input, relevant_evidence)
            evidence_count = {
                "neutral": 0,
                "entailment": 0,
                "contradiction": 0,
            }
            for label, score in alignments:
                evidence_count[label] += 1
            print("Evidences found:")
            print(evidence_count)





    except Exception as e:
        return (f"Error in algo here: {e}")



    # AGGREGATION
    # ===============================================================
    # More agree-ing evidences: higher confidence, -> True
    # Few agree-ing evidences: low confidence,-> Likely True
    # Divisive, 50-50 agree/disagree: Unsure, Need more information
    # Few disagree-ing confidence: low confidence, -> Likely False
    # More disagree-ing confidence: high confidence, -> False

    entailment = evidence_count["entailment"]
    contradiction = evidence_count["contradiction"]

    # Score calculation
    score = (entailment - contradiction) / (entailment + contradiction + 1)
    print(f"Score: {score}")

    # Verdict Assigment
    THRESHOLD1 = 0.2
    THRESHOLD2 = 0.4
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

    # return {"verdict": verdict, "just": "justification here"}
    return verdict



    # print("DATA PASSED INTO PROMPT")
    # for url, data in relevant_sentences.items():
    #     print(f"{url[:-10]}...:", data)

    # # print("==============================")
    # # print("LLM Response:")
    # fca = FactCheckerAgent(claim=claim_input, knowledge=str(relevant_sentences))
    # agent_response = fca.verify()
    # if agent_response:
    #     return {
    #         "claim": claim_input,
    #         "verdict": agent_response[0],
    #         "justification": agent_response[1],
    #     }

    # durations.append(time() - time_overall)


def display_time():
    print(f"Classification: {durations[0]} seconds")
    print(f"Tokenization: {durations[1]} seconds")
    print(f"Searching: {durations[2]} seconds")
    print(f"Page Scraping: {durations[3]} seconds")
    print(f"Sentence Similarity: {durations[3]} seconds")
    print(f"Overall program execution: {durations[3]} seconds")


# if __name__ == "__main__":
    # claims = [
    #     "A new disease called chikungunya is spreading in China.",
    #     "Three million Filipinos were cured by a non-surgical arthritis treatment, certified and endorsed by the Department of Health (DOH) and the Philippine Orthopedic Center (POC)",
    #     "The Pantawid Pamilyang Pilipino Program (4Ps) is being removed, with the last payout being in August 2025.",
    #     "Marcos slams Kennon Road rockshed, calls it ‘economic sabotage’",
    #     "Ukraine drone attacks spark fires at Russia’s Kursk nuclear plant, Novatek’s Ust-Luga terminal",
    #     "Most flood control contracts in Ilagan City, Isabela went to mayor’s brother",
    #     "local duck becomes mayor",
    # ]
    # results = []
    # # for claim in claims:
    # #     claim_result = love_in_paradise(claim)
    # #     if claim_result:
    # #         results.append(claim_result)
    # results.append(love_in_paradise(claims[6]))
    # for result in results:
    #     print(f"Claim: {result["claim"]}")
    #     print(f"Verdict: {result["verdict"]}")
    #     print(f"Justification: {result["justification"]}")
love_in_paradise(news)
    # display_time()
