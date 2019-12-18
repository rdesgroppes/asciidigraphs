#!/usr/bin/env -S pipenv run python
import networkx as nx
from matplotlib import pyplot

from asciidigraphs.networkx_support import to_networkx
from asciidigraphs.parser import parse

if __name__ == "__main__":
    graph = parse(
        r"""
    (a)-->(b)---(c)---------(d)-----(e)<--(f)
     ^     |     |           ^         \ /
     |     |     |           |          X
     |     |     v           |         / \
    (g)----+----(h)-------->(i)-----(j)-->(k)
       \   |      ^        / | \         /
        \  |       \      v  |  \       /
         \ |        (l)<-(m) |   \     /
          vv        /      \ |    \   /
          (n)-----(o)<------(p)    (q)
""",
        r"""
    (a)
       \
        ------------(under)-----(ground)-(j)
""",
    )
    nx_graph = to_networkx(graph)
    pos_by_node_symbol = {node.symbol: (node.pos.x, -node.pos.y) for node in graph.nodes}
    nx.draw_networkx(nx_graph, node_color="#add8e6", pos=pos_by_node_symbol)
    nx.draw_networkx_edge_labels(
        nx_graph,
        pos=pos_by_node_symbol,
        edge_labels={
            (e.from_node.symbol, e.to_node.symbol): (
                e.to_node.pos - e.from_node.pos
            ).distance
            for e in graph.edges
        },
    )
    pyplot.show()
