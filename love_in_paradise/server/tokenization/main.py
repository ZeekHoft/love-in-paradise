


from english import Eng_Tokenization_NLP
from tagalog import Tag_Tokenization_NLP
from util import tokenized, list_pos, target

from langdetect import detect
# text = ("Pangulo ng Pilipinas, nag-anunsyo ng bagong batas para sa edukasyon.")
text = ("Ceasefire shatters as Israel pounds Gaza with wave of deadly strikes.")


value = detect(text)
if value == "tl":
    new_text = text.split()
    solution = Tag_Tokenization_NLP()
    print(solution.tokenizationProcess(new_text))


elif value == "en":
    new_text = text.split()
    solution = Eng_Tokenization_NLP()
    print(solution.tokenizationProcess(new_text))


else:
    print("Invalid Language unsupported")




