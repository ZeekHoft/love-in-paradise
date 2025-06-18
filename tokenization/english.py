import spacy
import re
from .util import tokenized, list_pos, target, pos_tokens


nlp = spacy.load("en_core_web_sm")
text = ("The president of Britain was caught cleaning his brothers toilet").split()


# Enlgish tokenization class. Needs en_core_web_sm installed first.
class Eng_Tokenization_NLP(object):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def invalidNewsForChecking(self):
        print("Not a valid news to be checked")

    def validNewsForChecking(self):
        print("Valid news to be checked")

    def tokenizationProcess(self, word_list):
        for word in word_list:
            tokenized.append(word)

        combined_words = " ".join(tokenized).replace("-", "_")
        doc = self.nlp(re.sub("[^A-Za-z0-9_]+", " ", combined_words))
        for tokens in doc:
            # uncomment the code to check what other Parts of speech you want to add

            # print(f"tokenzzz: {tokens.pos_}")
            current_word = tokens.text.replace("_", "-")
            if tokens.pos_ in target:
                global elements
                elements = f"{tokens.pos_} {current_word}"
                # print(elements)
            list_pos.append(tokens.pos_)

            if tokens.pos_ not in pos_tokens.keys():
                pos_tokens[tokens.pos_] = [
                    current_word,
                ]
            else:
                pos_tokens[tokens.pos_].append(current_word)

        # self.checkValidation()

    def isValidNews(self):
        if all(items in list_pos for items in target):
            # self.validNewsForChecking()
            return True
        else:
            # self.invalidNewsForChecking()
            return False


# sol = Eng_Tokenization_NLP()
# print(sol.tokenizationProcess(text))
