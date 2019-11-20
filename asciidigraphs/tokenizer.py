import re

from asciidigraphs import tokens
from asciidigraphs.positions import Pos


def tokenize(*planes):
    node_tokens = []
    edge_tokens = []
    for z, plane in enumerate(planes):
        for y, row in enumerate(plane.splitlines()):
            for match in _iterate_tokens(row):
                token_class = getattr(tokens, match.lastgroup)
                if token_class is not tokens.NodeToken:
                    edge_tokens.append(
                        token_class(match.group(), Pos(match.start(0), y, z))
                    )
                    continue
                for x in range(match.start(0), match.end(0)):
                    node_tokens.append(token_class(match.group()[1:-1], Pos(x, y, z)))
    return tuple(node_tokens), tuple(edge_tokens)


_iterate_tokens = re.compile(
    "|".join(
        f"(?P<{token_class.__name__}>{token_class.pattern})"
        for token_class in tokens.token_classes
    )
).finditer
