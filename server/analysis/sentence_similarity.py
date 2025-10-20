import re
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

CUTTOFF_SCORE = 0.25


class SentenceSimilarity:
    """
    For searching sentences similar to the claim in a document.
    """

    def __init__(self, nlp):
        self.model = SentenceTransformer("distiluse-base-multilingual-cased-v1")
        self.nlp = nlp  # Spacy NLP model

    # Set and encode main sentence that will be used for comparison.
    def set_main_sentence(self, main_sentence):
        self.ms_encoding = self.model.encode(main_sentence)

    # Searches for the most relevent/similar sentences using a base sentence
    def find_similar_sentences(self, content, cutoff_score=0.25):

        # Separate content into list of sentences
        doc = self.nlp(content)
        tokenized_sentences = []
        for sent in doc.sents:
            sentences_found = re.split(r"\n+", sent.text)
            tokenized_sentences += [s for s in sentences_found if s != ""]

        # Encode sentences
        ts_encoding = self.model.encode(tokenized_sentences)

        similarities = {}

        # Calculate cosine similarity for each sentence
        for i in range(len(tokenized_sentences)):
            cosine_similarity = cos_sim(self.ms_encoding, ts_encoding[i])
            similarities[tokenized_sentences[i]] = cosine_similarity[0][0].item()

        sorted_score = sorted(
            similarities.items(), key=lambda item: item[1], reverse=True
        )

        # Find most related sentences
        top_sentences = [
            (sentence, score)
            for sentence, score in sorted_score
            if score >= cutoff_score
        ]

        return top_sentences
