
# import spacy

# nlp = spacy.load("en_core_web_sm")

# text = "The president of North Korea has made cure for cancer"
# doc = nlp(text)

# # Extract meaningful words (nouns, verbs, named entities)
# keywords = [token.text for token in doc if token.pos_ in ["NOUN", "VERB", "PROPN"]]

# print(keywords) 

import spacy
import re

# Load the Tagalog NLP model
nlp = spacy.load("tl_calamancy_md")

text = "Pangulo ng Pilipinas, nag-anunsyo ng bagong batas para sa edukasyon."
doc = nlp(re.sub('[^A-Za-z0-9]+', ' ', text))

for token in doc:
    if token.pos_ in ["NOUN", "VERB", "PROPN", "ADJ"]:
        print(token.text)
    # print(f"Word: {token.text}, POS: {token.pos_}, Lemma: {token.lemma_}")

