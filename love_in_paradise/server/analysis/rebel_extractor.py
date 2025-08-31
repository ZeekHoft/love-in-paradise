from transformers import pipeline
import spacy
import rebel_spacy_component


class REBELExtractor:
    """
    Uses REBEL-large model for relation extraction.
    More resource intensive than Stanford OpenIE.
    """

    def __init__(self, nlp=None):
        if nlp is None:
            self.nlp = spacy.load("en_core_web_sm")
        else:
            self.nlp = nlp

        self.nlp.add_pipe(
            "rebel",
            after="senter",
            config={
                # "device": 0,  # Number of the GPU, -1 if want to use CPU
                "model_name": "Babelscape/rebel-large",
            },  # Model used, will default to 'Babelscape/rebel-large' if not given
        )

    def extract_relations(self, sentence):
        doc = self.nlp(sentence)
        # doc_list = self.nlp.pipe([input_sentence])
        triples = []
        for value, rel_dict in doc._.rel.items():
            print(f"{value}: {rel_dict}")
            triples.append(
                (
                    rel_dict["head_span"].text,
                    rel_dict["relation"],
                    rel_dict["tail_span"].text,
                )
            )
        return triples
