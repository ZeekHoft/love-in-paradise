from stanza.server import CoreNLPClient, StartServer

"""
import stanza
stanza.install_corenlp()
"""

PROPERTIES = {
    "openie.resolve_coref": True,
}


class OpenInformationExtraction:
    """
    Uses Stanza/Stanford OpenIE for extracting relations from text sentences.
    """

    def generate_triples(self, text):
        # Returns a triple for each sentence
        triples = []
        with CoreNLPClient(
            annotators=["openie", "coref"],
            start_server=StartServer.TRY_START,
            properties=PROPERTIES,
            be_quiet=True,
        ) as client:
            annotation = client.annotate(text)
            for sentence in annotation.sentence:
                for data in sentence.openieTriple:
                    triple = (data.subject, data.relation, data.object)
                    # print("|-", triple)
                    triples.append(triple)
        return triples
