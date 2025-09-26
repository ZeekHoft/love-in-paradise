from stanza.server import CoreNLPClient, StartServer
import os

"""
import stanza
stanza.install_corenlp()
"""

# Get the relative filepath of property file
# Should be forward slash instead of backslash provided by os.path
props_filepath = os.path.relpath(os.path.join(os.path.dirname(__file__), "corenlp.props")).replace("\\", "/")


class OpenInformationExtraction:
    """
    Uses Stanza/Stanford OpenIE for extracting relations from text sentences.
    """
    nlp_client = None

    def __init__(self):
        self.nlp_client = CoreNLPClient(
            start_server=StartServer.TRY_START,
            properties=props_filepath,
        )

    def generate_triples(self, text):
        # Returns a triple for each sentence
        triples = []

        annotation = self.nlp_client.annotate(text)
        for sentence in annotation.sentence:
            for data in sentence.openieTriple:
                triple = (data.subject, data.relation, data.object)
                # print("|-", triple)
                triples.append(triple)
        return triples
    
    def dispose(self):
        if self.nlp_client is not None:
            self.nlp_client.stop()