from collections import ChainMap

from asciidigraphs.graph import Edge, Graph, Node
from asciidigraphs.tokenizer import tokenize
from asciidigraphs.tokens import Direction


def parse(*planes):
    node_tokens, edge_tokens = tokenize(*planes)
    nodes_by_symbol = _get_nodes_by_symbol(node_tokens)
    return Graph(
        nodes_by_symbol.values(),
        _generate_edges(edge_tokens, {t.pos: t for t in node_tokens}, nodes_by_symbol),
    )


def _get_nodes_by_symbol(node_tokens):
    nodes = {}
    for token in node_tokens:
        node = nodes.get(token.symbol)
        if node is None or token.pos[::-1] < node.pos[::-1]:
            nodes[token.symbol] = Node(*token)
    return nodes


def _generate_edges(edge_tokens, node_token_map, nodes_by_symbol):
    token_map = ChainMap({t.pos: t for t in edge_tokens}, node_token_map)
    for edge_token in edge_tokens:
        for head_node_token in filter(None, map(node_token_map.get, edge_token.slots)):
            directions, tail_tokens = zip(
                *edge_token.transition_from(head_node_token, token_map)
            )
            if max(directions) is not Direction.BACKWARD:
                yield Edge(
                    nodes_by_symbol[head_node_token.symbol],
                    "".join(token.symbol for token in tail_tokens[:-1]),
                    nodes_by_symbol[tail_tokens[-1].symbol],
                )
