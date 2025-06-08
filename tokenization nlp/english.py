



import spacy
import re
from util import tokenized, list_pos, target


nlp = spacy.load("en_core_web_sm")
text = ("The president of Britain was caught cleaning his brothers toilet").split()



class Eng_Tokenization_NLP(object):
    
    def invalidNewsForChecking(self):
        print ("Not a valid news to be checked")
    
    def validNewsForChecking(self):
        print ("Valid news to be checked")


    def tokenizationProcess(self, s):
        for i in s:
            tokenized.append(i)

        combined_words = " ".join(tokenized).replace("-", "_")
        doc = nlp(re.sub('[^A-Za-z0-9_]+', ' ', combined_words))
        for tokens in doc:
            #uncomment the code to check what other Parts of speech you want to add 
            
            # print(f"tokenzzz: {tokens.pos_}")

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
        

sol = Eng_Tokenization_NLP()
print(sol.tokenizationProcess(text))
