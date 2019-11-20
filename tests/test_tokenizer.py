from asciidigraphs.positions import Pos
from asciidigraphs.tokenizer import tokenize
from asciidigraphs.tokens import EdgeToken, NodeToken


def test_tokenize():
    assert (
        tokenize(
            """
    (a)-(b)
         |
        (c)
"""
        )
        == (
            (
                NodeToken("a", Pos(4, 1)),
                NodeToken("a", Pos(5, 1)),
                NodeToken("a", Pos(6, 1)),
                NodeToken("b", Pos(8, 1)),
                NodeToken("b", Pos(9, 1)),
                NodeToken("b", Pos(10, 1)),
                NodeToken("c", Pos(8, 3)),
                NodeToken("c", Pos(9, 3)),
                NodeToken("c", Pos(10, 3)),
            ),
            (EdgeToken("-", Pos(7, 1)), EdgeToken("|", Pos(9, 2))),
        )
    )
