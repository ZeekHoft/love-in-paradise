
import spacy
import re

nlp = spacy.load("tl_calamancy_md")


text = "Pangulo ng Pilipinas, nag-anunsyo ng bagong batas para sa edukasyon.".split()
tokenized = []
for i in text:
    tokenized.append(i)
print(tokenized)


combined_words = " ".join(tokenized).replace("-", "_")
doc = nlp(re.sub('[^A-Za-z0-9_]+', ' ', combined_words))


for tokens in doc:
    if tokens.pos_ in ["NOUN", "VERB", "PROPN", "ADJ"]:
        print(tokens.text.replace("_", "-"))



