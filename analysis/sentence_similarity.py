from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


"""
This class needs punkt_tab to be installed first
Run the below code in the Python interpreter:
    import nltk
    nltk.download("punkt_tab")
"""

CUTTOFF_SCORE = 0.25


class SentenceSimilarity:
    def __init__(self):
        self.model = SentenceTransformer("distiluse-base-multilingual-cased-v1")

    # Set and encode main sentence that will be used for comparison.
    def set_main_sentence(self, main_sentence):
        self.ms_encoding = self.model.encode(main_sentence)

    # Searches for the most relevent/similar sentences using a base sentence
    def find_similar_sentences(self, content):

        # Separate content into list of sentences
        tokenized_sentences = sent_tokenize(content)

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
            if score >= CUTTOFF_SCORE
        ]

        return top_sentences
