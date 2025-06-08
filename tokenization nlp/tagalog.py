


import spacy
import re

from util import tokenized, list_pos, target

nlp = spacy.load("tl_calamancy_md")
text = ("Pangulo ng Pilipinas, nag-anunsyo ng bagong batas para sa edukasyon.").split()




class Tag_Tokenization_NLP(object):
    
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
        

sol = Tag_Tokenization_NLP()
print(sol.tokenizationProcess(text))





