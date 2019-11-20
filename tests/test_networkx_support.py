from asciidigraphs.networkx_support import to_networkx
from asciidigraphs.parser import parse


def test_to_networkx():
    nx_graph = to_networkx(parse("(a)<-(b)"))
    assert tuple(nx_graph.nodes) == ("a", "b")
    assert tuple(nx_graph.edges) == (("b", "a"),)
