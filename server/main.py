from analysis.open_info_extraction import OpenInformationExtraction
from analysis.sentence_similarity import SentenceSimilarity
from webcrawling.article_scraper import ArticleScraper
from tokenization.english import Eng_Tokenization_NLP
from llm.fact_checker_agent import FactCheckerAgent

from analysis.evidence_alignment import calculate_entailment
from webcrawling.search_articles import search_news
from clasification.check import classify_input

from typing import Generator
import numpy as np
import spacy
import traceback


ACCEPT_LIST = ["news claim", "statement", "question"]
news = "Vice President Sara Duterte stated that there is nothing wrong with sharing AI videos."
# news = "CLTG Builders worked with the Discayas for Davao projects"
# news = "Some celebrities participated in assisting Cebu earthquake victims."
# news = "A Chinese Coast Guard ship fired its water cannon at a Philippine vessel near the West Philippine Sea."
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

    try:
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
        try:
            input_classification = classify_input(claim_input)
            if input_classification in ACCEPT_LIST:

                results["currentProcess"] = "Searching the web"
                results["progress"] = 2 / 8
                yield results

                print(f"Input is a {input_classification}; proceeding to tokenization.")
                
                # Build search query from proper nouns and nouns, with fallback
                propn_tokens = tokenizer.pos_tokens.get("PROPN", [])
                noun_tokens = tokenizer.pos_tokens.get("NOUN", [])
                search_query_tokens = propn_tokens + noun_tokens
                
                # Fallback: if no proper nouns or nouns, use the original claim
                if not search_query_tokens:
                    print("Warning: No PROPN or NOUN tokens found, using full claim for search")
                    search_query = claim_input
                else:
                    search_query = " ".join(search_query_tokens)
                
                print(f"Search query: {search_query}")

                # Search articles - Request 20 results (2 API calls, allows 50 fact-checks/day)
                articles = search_news(
                    search_query,
                    results_amt=20,  # 2 API calls per fact-check = 50 fact-checks/day
                )

                print(f"Found {len(articles)} articles from search")

                if len(articles) == 0:
                    print("No news articles found related to news claim.")
                    results["justification"] = (
                        "No news articles found related to news claim."
                    )
                    yield results
                    return
                # print(articles)
            else:
                print("Input is not considered a news claim!")
                results["justification"] = "Input is not considered a news claim!"
                yield results
                return
        except KeyError as e:
            print(f"Missing POS tag in tokenization: {e}")
            traceback.print_exc()
            results["justification"] = (
                f"Unable to extract key terms from claim. Please try rephrasing."
            )
            yield results
            return
        except Exception as e:
            print((f"News claim has missing some missing key elements: {e}"))
            traceback.print_exc()
            results["justification"] = (
                f"News claim has missing some missing key elements: {e}"
            )
            yield results
            return

        results["currentProcess"] = "Retrieving data from articles"
        results["progress"] = 3 / 8
        yield results

        # Scrape each article
        articleScraper = ArticleScraper()
        news_data = articleScraper.article_scraper(articles)
        if len(news_data) == 0:
            print("Problem occurred in scraping data")
            results["justification"] = "Problem occurred in scraping data"
            yield results
            return

        """
        news_data = {
            "headline": HEADLINE,
            "content": CONTENT,
            "sentences": will be compared to claim,
            "link": url
        }
        """

        print(f"Successfully scraped {len(news_data)} articles")

        print("Scraped Articles ==================================")
        for url, data in news_data.items():
            print(url)
            print(data["headline"])

        results["currentProcess"] = "Searching for relevant information"
        results["progress"] = 4 / 8
        yield results

        # SEMANTIC SENTENCE SEARCH
        # Filtering out the most relevant data
        print("Finding relevant data:")
        sentence_similarity = SentenceSimilarity(nlp)
        sentence_similarity.set_main_sentence(claim_input)
        relevant_sentences = {}
        urls_to_remove = []
        for url, data in news_data.items():
            ss = sentence_similarity.find_similar_sentences(
                data["content"],
                cutoff_score=0.40,  # Lowered from 0.50 to catch more relevant sentences
            )
            print(data["headline"])
            if ss == []:
                print("No similar sentences found.")
                urls_to_remove.append(url)

            else:
                print("SCORE | SENTENCE")
                for sentence, score in ss:
                    print(f"{score:.4f} | {sentence}")
                    if url not in relevant_sentences.keys():
                        relevant_sentences[url] = [sentence]
                        news_data[url]["sentences"] = [sentence]
                    else:
                        relevant_sentences[url].append(sentence)
                        news_data[url]["sentences"].append(sentence)
            print()

        # Discard urls with no relevant sentences
        for key_url in urls_to_remove:
            print(f"Removed News: {news_data[key_url]['headline']}")
            news_data.pop(key_url)
        print()

        print(f"Total articles with relevant content: {len(relevant_sentences)}")

        # Information Extraction
        # ===============================================================
        # Gets subject, predicate, object triples
        info_ext = OpenInformationExtraction()
        claim_triples = info_ext.generate_triples(claim_input)
        print(f"Claim triples: {claim_triples}")

        results["currentProcess"] = "Comparing evidence to claim"
        results["progress"] = 5 / 8
        yield results

        # CLAIM-EVIDENCE ALIGNMENT & ENTAILMENT SCORING
        # ===============================================================
        # Given a list of the most relevant sentences from articles, evaluate them against the claim
        # -> evidences = {"agree", "disagree", "neutral"}

        print("Scoring each article")
        for article in news_data.values():
            # Score each article based on semantic entailment and matching triples
            score_article(
                claim=claim_input,
                article=article,
                oie=info_ext,
                claim_triples=claim_triples,
            )
        print("Done scoring\n")

        results["currentProcess"] = "Aggregating Scores"
        results["progress"] = 6 / 8
        yield results

        print("SCORE | ARTICLE")
        agree = []
        disagree = []
        urls_to_remove = []
        for url, article in news_data.items():
            score = article["score"]
            print(f"DEBUG: Article '{article['headline'][:50]}...' scored: {score}")
            if score > 0 or score < 0:
                # Fixed the f-string syntax error
                print(f"{score: .2f} | {article['headline']}")
                if score > 0:
                    agree.append(article)
                else:
                    disagree.append(article)
            elif score == 0:
                print(f"Article scored 0, removing: {article['headline'][:50]}")
                urls_to_remove.append(url)

        # Discard urls with no score
        for key_url in urls_to_remove:
            news_data.pop(key_url)

        article_scores = [a["score"] for a in news_data.values() if a["score"] != 0]
        if len(article_scores) == 0:
            print("No significant evidence found.")
            results["justification"] = "No significant evidence found."
            yield results
            return
        average_score = sum(article_scores) / len(article_scores)
        print(f"Final Score: {average_score}")

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

        # Calculate confidence based on standard deviation
        standard_deviation = np.std(article_scores)
        confidence = (1 - standard_deviation / 2) * 100
        confidence = max(0, min(100, confidence))
        print(f"Confidence Level: {confidence:.1f}%")

        # Verdict Assigment
        THRESHOLD1 = 0.3
        THRESHOLD2 = 0.45
        if -THRESHOLD1 < average_score < THRESHOLD1:
            verdict = "UNSURE"
        elif average_score <= -THRESHOLD2:
            verdict = "FALSE"
        elif average_score <= -THRESHOLD1:
            verdict = "LIKELY FALSE"
        elif average_score >= THRESHOLD2:
            verdict = "TRUE"
        elif average_score >= THRESHOLD1:
            verdict = "LIKELY TRUE"

        # JUSTIFICATION GENERATION
        if use_llm:
            # Use LLM agent
            print("==============================")
            print("LLM Response:")
            fca = FactCheckerAgent(claim=claim_input, knowledge=str(news_data))
            agent_response = fca.verify()
            if agent_response:
                results["verdict"] = agent_response[0]
                results["justification"] = agent_response[1]
                results["confidence"] = 0
            else:
                results["justification"] = "Error: No response from LLM"
                results["currentProcess"] = "Error"
                results["progress"] = 8 / 8
                yield results
                return
        else:
            # Manual justification based on top articles
            justification = ""
            if len(article_scores) >= 3:
                # Get top 3 articles in support of verdict
                reverse = average_score > 0
                top3_scores = sorted(article_scores, reverse=reverse)[:3]

                justification += (
                    "The verdict was evaluated based on the following news articles:\n"
                    + "(Listed based on relevance)\n"
                )

                listcount = 1
                for article in news_data.values():
                    if article["score"] in top3_scores:
                        # Filter alignments based on verdict type
                        if average_score > 0:
                            alignments = [
                                a
                                for a in article.get("alignments", [])
                                if a["label"] == "entailment"
                            ]
                        else:
                            alignments = [
                                a
                                for a in article.get("alignments", [])
                                if a["label"] == "contradiction"
                            ]

                        if alignments:
                            evidence = max(alignments, key=lambda x: x["score"])
                            justification += (
                                f"{listcount}. {article['headline']}\n"
                                + f"Evidence: {evidence['sentence']}\n"
                            )
                        else:
                            # Fallback if no strong evidence
                            justification += (
                                f"{listcount}. {article['headline']}\n"
                                + "Evidence: No strong evidence found\n"
                            )
                        listcount += 1
            else:
                # Handle cases with fewer than 3 articles
                justification = "The verdict was evaluated based on limited news articles:\n"
                listcount = 1
                for article in news_data.values():
                    # Filter alignments based on verdict type
                    if average_score > 0:
                        alignments = [
                            a
                            for a in article.get("alignments", [])
                            if a["label"] == "entailment"
                        ]
                    else:
                        alignments = [
                            a
                            for a in article.get("alignments", [])
                            if a["label"] == "contradiction"
                        ]

                    if alignments:
                        evidence = max(alignments, key=lambda x: x["score"])
                        justification += (
                            f"{listcount}. {article['headline']}\n"
                            + f"Evidence: {evidence['sentence']}\n"
                        )
                    else:
                        justification += (
                            f"{listcount}. {article['headline']}\n"
                            + "Evidence: No strong evidence found\n"
                        )
                    listcount += 1
                justification += "\nNote: Limited sources available. This claim needs more information for a conclusive verdict."

            results["verdict"] = verdict
            results["justification"] = justification
            results["confidence"] = confidence

        # Always include article URLs and headlines
        results["article_urls"] = list(news_data.keys())
        results["headlines"] = {
            key: value["headline"].replace('"', "'")
            for key, value in news_data.items()
        }
        results["sources"] = list(news_data.keys())
        results["currentProcess"] = "Complete"
        results["progress"] = 8 / 8
        yield results
        return
        
    except Exception as e:
        # Catch any unhandled exceptions
        print(f"Unexpected error in love_in_paradise: {e}")
        traceback.print_exc()
        results["justification"] = f"Unexpected error: {str(e)}"
        results["currentProcess"] = "Error"
        results["progress"] = 8 / 8
        yield results
        return


def score_article(
    claim: str, article: dict, oie: OpenInformationExtraction, claim_triples: list
):
    """
    Score an article based on claim
    """
    sentences = article["sentences"]

    # Triple comparison with claim
    common_count = 0
    for sentence in sentences:
        article_triples = oie.generate_triples(sentence)
        if article_triples:
            common = set(article_triples).intersection(set(claim_triples))
            common_count += len(common)

    if common_count != 0:
        print("Common triples found:", common_count)

    # Scores sentences based on entailment to claim
    # Returns list of {label, score, sentence}
    alignments = calculate_entailment(claim=claim, sentences=sentences)
    article["alignments"] = alignments

    # Debug output
    print(f"  Alignments for this article: {len(alignments)}")

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

    for alignment in alignments:
        label = alignment["label"]
        evidence_count[label] += 1
        evidence_values[label] += alignment["score"]

    entailment = evidence_values["entailment"] + common_count
    contradiction = evidence_values["contradiction"]

    print(f"  Entailment: {entailment}, Contradiction: {contradiction}")

    # Score calculation
    score = (entailment - contradiction) / (entailment + contradiction + 1)
    article["score"] = score
    print(f"  Final score: {score}")


# if __name__ == "__main__":
#     # New way to run code:
#     lip = love_in_paradise(news, use_llm=False)
#     final = None
#     for result in lip:
#         print(result["currentProcess"])
#         final = result
#     for key, val in final.items():
#         print(f"{key.title()}: {val}")