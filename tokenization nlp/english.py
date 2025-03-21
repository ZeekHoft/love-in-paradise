



import spacy
import re
from time import sleep


nlp = spacy.load("en_core_web_sm")
text = ("Ceasefire shatters as Israel pounds Gaza with wave of deadly strikes ").split()
# text = "is water wet?".split()

tokenized = []
list_pos = []
target = ["NOUN", "VERB", "PROPN", "ADJ"]


class Tokenization_NLP(object):
    
    def invalidNewsForChecking(self):
        print ("Not a valid news to be checked")
    
    def validNewsForChecking(self):
        print ("Valid news to be checked")


    def tokenizationProcess(self, s):
        for i in s:
            tokenized.append(i)
        # print(f"tokenized: {tokenized}")

        combined_words = " ".join(tokenized).replace("-", "_")
        doc = nlp(re.sub('[^A-Za-z0-9_]+', ' ', combined_words))
        for tokens in doc:
            if tokens.pos_ in target:
                global elements
                elements = (f"{tokens.pos_} {tokens.text.replace("_", "-")}")
                print(elements)
            list_pos.append(tokens.pos_)
        self.checkValidation()




    def checkValidation(self):
        if all(items in list_pos for items in target):
            self.validNewsForChecking()
        else:
            self.invalidNewsForChecking()
        

sol = Tokenization_NLP()
print(sol.tokenizationProcess(text))
