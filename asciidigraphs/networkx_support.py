import networkx


def to_networkx(graph, nx_graph_factory=networkx.DiGraph):
    nx_graph = nx_graph_factory()
    nx_graph.add_nodes_from((node.symbol for node in graph.nodes))
    nx_graph.add_edges_from((e.from_node.symbol, e.to_node.symbol) for e in graph.edges)
    return nx_graph
