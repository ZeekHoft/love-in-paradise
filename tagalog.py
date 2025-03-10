
# import spacy
# import re

# # Load the Tagalog NLP model
# nlp = spacy.load("tl_calamancy_md")

# text = "Pangulo ng Pilipinas, nag-anunsyo ng bagong batas para sa edukasyon."
# doc = nlp(re.sub('[^A-Za-z0-9]+', ' ', text))

# for token in doc:
#     if token.pos_ in ["NOUN", "VERB", "PROPN", "ADJ"]:
#         print(token.text)
#     # print(f"Word: {token.text}, POS: {token.pos_}, Lemma: {token.lemma_}")


# # text = "well-known actress dies"


# # for i in text:
# #     seperate = text.split("-")
# #     combined = '-'.join(seperate)
# #     print(combined)



import spacy
import re
nlp = spacy.load("tl_calamancy_md")
text = "Pangulo ng Pilipinas, nag-anunsyo ng bagong batas para sa edukasyon.".split()
tokenized = []

class Tokenization_NLP(object):
    
    def tokenization_process(self, s):
        for i in s:
            tokenized.append(i)
        print(tokenized)
    

        combined_words = " ".join(tokenized).replace("-", "_")
        doc = nlp(re.sub('[^A-Za-z0-9_]+', ' ', combined_words))


        for tokens in doc:
            if tokens.pos_ in ["NOUN", "VERB", "PROPN", "ADJ"]:
                print(tokens.text.replace("_", "-"))


        

sol = Tokenization_NLP()
print(sol.tokenization_process(text))
