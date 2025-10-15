import networkx as nx
from pyvis.network import Network


def get_relevant_triples(main_triple, triples):
    subject = main_triple[0]
    results = []
    for tri in triples:
        if subject in tri:
            results.append(tri)
    # print("Results:", results)
    return results


def triple_to_sentence(triple):
    return " ".join(triple)


# Create Networkx Knowledge Graph and visualization on html
def generate_graph(list_triples, filename="graph.html"):
    knowledge_graph = nx.Graph()
    net = Network()
    for triple in list_triples:

        knowledge_graph.add_nodes_from([triple[0], triple[2]])
        knowledge_graph.add_edge(triple[0], triple[2], relation=triple[1])

        net.add_node(triple[0])
        net.add_node(triple[2])
        net.add_edge(triple[0], triple[2], title=triple[1])
    net.write_html(filename, notebook=False, open_browser=False)
    return knowledge_graph
