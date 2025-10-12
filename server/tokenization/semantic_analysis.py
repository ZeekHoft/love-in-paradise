



import spacy
import re
from util import tokenized, list_pos, target


nlp = spacy.load("en_core_web_sm")
text = ("The president of Britain was caught cleaning his brothers toilet").split()



class Eng_Tokenization_NLP(object):
    

    def lexical_analysis(self, s):
        for i in s:
            tokenized.append(i)

        combined_words = " ".join(tokenized).replace("-", "_")
        doc = nlp(re.sub('[^A-Za-z0-9_]+', ' ', combined_words))
        for tokens in doc:

            if tokens.pos_ in target:
                global elements
                # elements = (f"{tokens.text.replace("_", "-")}") # just values of it
                elements = (f"{tokens.pos_} {tokens.text.replace("_", "-")}") #POS and the words of it
                self.syntax_analysis(elements)
            list_pos.append(tokens.pos_)




    def syntax_analysis(self, x):
        print(f"{x}")



sol = Eng_Tokenization_NLP()
print(sol.lexical_analysis(text))





