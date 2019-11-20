from collections import namedtuple

Node = namedtuple("Node", "symbol pos")

Edge = namedtuple("Edge", "from_node symbol to_node")


class Graph(namedtuple("Graph", "nodes edges")):
    def __new__(cls, nodes, edges):
        # noinspection PyArgumentList
        return super().__new__(cls, tuple(sorted(nodes)), tuple(sorted(edges)))
