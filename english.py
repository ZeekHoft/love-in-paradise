



import spacy
import re


nlp = spacy.load("en_core_web_sm")

text = "How the Magna Carta of Women protects Filipinas"
doc = nlp(re.sub('[^A-Za-z0-9]+', ' ', text))

for token in doc:
    if token.pos_ in ["NOUN", "VERB", "PROPN", "ADJ"]:
        print(token.text)
    # print(f"Word: {token.text}, POS: {token.pos_}, Lemma: {token.lemma_}")

