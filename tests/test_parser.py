import pytest

from asciidigraphs.graph import Edge, Graph, Node
from asciidigraphs.parser import parse
from asciidigraphs.positions import Pos


def test_parse_single_horizontal_bar():
    a = Node("a", Pos(0, 0))
    b = Node("b", Pos(4, 0))
    assert parse("(a)-(b)") == Graph(
        nodes=(a, b), edges=(Edge(a, "-", b), Edge(b, "-", a))
    )


def test_parse_single_right_arrow():
    a = Node("a", Pos(0, 0))
    b = Node("b", Pos(4, 0))
    assert parse("(a)>(b)") == Graph(nodes=(a, b), edges=(Edge(a, ">", b),))


def test_parse_single_left_arrow():
    a = Node("a", Pos(0, 0))
    b = Node("b", Pos(4, 0))
    assert parse("(a)<(b)") == Graph(nodes=(a, b), edges=(Edge(b, "<", a),))


def test_parse_single_vertical_bar():
    a = Node("a", Pos(4, 1))
    b = Node("b", Pos(4, 3))
    assert (
        parse(
            """
    (a)
     |
    (b)
"""
        )
        == Graph(nodes=(a, b), edges=(Edge(a, "|", b), Edge(b, "|", a)))
    )


def test_parse_single_down_arrow():
    a = Node("a", Pos(4, 1))
    b = Node("b", Pos(4, 3))
    assert (
        parse(
            """
    (a)
     v
    (b)
"""
        )
        == Graph(nodes=(a, b), edges=(Edge(a, "v", b),))
    )


def test_parse_single_up_arrow():
    a = Node("a", Pos(4, 1))
    b = Node("b", Pos(4, 3))
    assert (
        parse(
            """
    (a)
     ^
    (b)
"""
        )
        == Graph(nodes=(a, b), edges=(Edge(b, "^", a),))
    )


def test_parse_single_upward_bar():
    a = Node("a", Pos(6, 1))
    b = Node("b", Pos(4, 3))
    assert (
        parse(
            """
      (a)
      /
    (b)
"""
        )
        == Graph(nodes=(a, b), edges=(Edge(a, "/", b), Edge(b, "/", a)))
    )


def test_parse_single_downward_bar():
    a = Node("a", Pos(4, 1))
    b = Node("b", Pos(6, 3))
    assert (
        parse(
            r"""
    (a)
      \
      (b)
"""
        )
        == Graph(nodes=(a, b), edges=(Edge(a, "\\", b), Edge(b, "\\", a)))
    )


def test_parse_single_vertical_crossing():
    a = Node("a", Pos(6, 1))
    b = Node("b", Pos(6, 3))
    c = Node("c", Pos(4, 2))
    d = Node("d", Pos(8, 2))
    assert (
        parse(
            """
      (a)
    (c)+(d)
      (b)
"""
        )
        == Graph(
            nodes=(a, b, c, d),
            edges=(Edge(a, "+", b), Edge(b, "+", a), Edge(c, "+", d), Edge(d, "+", c)),
        )
    )


def test_parse_single_diagonal_crossing():
    a = Node("a", Pos(4, 1))
    b = Node("b", Pos(8, 3))
    c = Node("c", Pos(8, 1))
    d = Node("d", Pos(4, 3))
    assert (
        parse(
            """
    (a) (c)
       X
    (d) (b)
"""
        )
        == Graph(
            nodes=(a, b, c, d),
            edges=(Edge(a, "X", b), Edge(b, "X", a), Edge(c, "X", d), Edge(d, "X", c)),
        )
    )


@pytest.mark.parametrize("__", ("--", "<>"))
def test_parse_extended_horizontal(__):
    a = Node("a", Pos(0, 0))
    b = Node("b", Pos(5, 0))
    assert parse(f"(a){__}(b)") == Graph(
        nodes=(a, b), edges=(Edge(a, __, b), Edge(b, __[::-1], a))
    )


def test_parse_extended_right_arrow():
    a = Node("a", Pos(0, 0))
    b = Node("b", Pos(5, 0))
    assert parse("(a)->(b)") == Graph(nodes=(a, b), edges=(Edge(a, "->", b),))


def test_parse_extended_left_arrow():
    a = Node("a", Pos(0, 0))
    b = Node("b", Pos(5, 0))
    assert parse("(a)<-(b)") == Graph(nodes=(a, b), edges=(Edge(b, "-<", a),))


@pytest.mark.parametrize("__", ("||", "^v"))
def test_parse_extended_vertical(__):
    a = Node("a", Pos(4, 1))
    b = Node("b", Pos(4, 4))
    assert (
        parse(
            f"""
    (a)
     {__[0]}
     {__[1:]}
    (b)
"""
        )
        == Graph(nodes=(a, b), edges=(Edge(a, __, b), Edge(b, __[::-1], a)))
    )


def test_parse_extended_down_arrow():
    a = Node("a", Pos(4, 1))
    b = Node("b", Pos(4, 4))
    assert (
        parse(
            """
    (a)
     |
     v
    (b)
"""
        )
        == Graph(nodes=(a, b), edges=(Edge(a, "|v", b),))
    )


def test_parse_extended_up_arrow():
    a = Node("a", Pos(4, 1))
    b = Node("b", Pos(4, 4))
    assert (
        parse(
            """
    (a)
     ^
     |
    (b)
"""
        )
        == Graph(nodes=(a, b), edges=(Edge(b, "|^", a),))
    )


def test_parse_extended_upward_bar():
    a = Node("a", Pos(5, 1))
    b = Node("b", Pos(4, 4))
    assert (
        parse(
            """
     (a)
      /
     /
    (b)
"""
        )
        == Graph(nodes=(a, b), edges=(Edge(a, "//", b), Edge(b, "//", a)))
    )


def test_parse_extended_downward_bar():
    a = Node("a", Pos(4, 1))
    b = Node("b", Pos(5, 4))
    assert (
        parse(
            r"""
    (a)
     \
      \
     (b)
"""
        )
        == Graph(nodes=(a, b), edges=(Edge(a, "\\\\", b), Edge(b, "\\\\", a)))
    )


def test_parse_extended_vertical_crossing():
    a = Node("a", Pos(7, 1))
    b = Node("b", Pos(7, 6))
    c = Node("c", Pos(4, 3))
    d = Node("d", Pos(11, 3))
    assert (
        parse(
            """
       (a)
        |
    (c)-+--(d)
        |
        |
       (b)
"""
        )
        == Graph(
            nodes=(a, b, c, d),
            edges=(
                Edge(a, "|+||", b),
                Edge(b, "||+|", a),
                Edge(c, "-+--", d),
                Edge(d, "--+-", c),
            ),
        )
    )


def test_parse_extended_diagonal_crossing():
    a = Node("a", Pos(4, 1))
    b = Node("b", Pos(11, 7))
    c = Node("c", Pos(11, 1))
    d = Node("d", Pos(4, 7))
    assert (
        parse(
            r"""
    (a)    (c)
      \    /
       \ --
        X
       / --
      /    \
    (d)    (b)
"""
        )
        == Graph(
            nodes=(a, b, c, d),
            edges=(
                Edge(a, "\\\\X--\\", b),
                Edge(b, "\\--X\\\\", a),
                Edge(c, "/--X//", d),
                Edge(d, "//X--/", c),
            ),
        )
    )


def test_parse_bundle():
    a = Node("a", Pos(8, 1))
    b = Node("b", Pos(11, 1))
    c = Node("c", Pos(14, 1))
    d = Node("d", Pos(11, 3))
    e = Node("e", Pos(8, 8))
    f = Node("f", Pos(11, 8))
    g = Node("g", Pos(14, 8))
    assert (
        parse(
            r"""
        (a)(b)(c)
          \ | /
           (d)
           ^^^
          / | \
         /  |  \
        v   v   v
        (e)(f)(g)
"""
        )
        == Graph(
            nodes=(a, b, c, d, e, f, g),
            edges=(
                Edge(a, "\\", d),
                Edge(b, "|", d),
                Edge(c, "/", d),
                Edge(d, "/", c),
                Edge(d, "\\", a),
                Edge(d, "^//v", e),
                Edge(d, "^\\\\v", g),
                Edge(d, "^||v", f),
                Edge(d, "|", b),
                Edge(e, "v//^", d),
                Edge(f, "v||^", d),
                Edge(g, "v\\\\^", d),
            ),
        )
    )


def test_parse_spiral():
    a = Node("a", Pos(4, 1))
    b = Node("b", Pos(8, 5))
    assert (
        parse(
            r"""
    (a)----
      -    \
     / \    |
    |   \   |
    |   (b) |
     \     /
      -----
"""
        )
        == Graph(
            nodes=(a, b),
            edges=(
                Edge(a, "----\\|||/-----\\||/-\\\\", b),
                Edge(b, "\\\\-/||\\-----/|||\\----", a),
            ),
        )
    )


def test_parse_urban_grid():
    _1 = Node("1", Pos(4, 1))
    _2 = Node("2", Pos(11, 1))
    _3 = Node("3", Pos(19, 1))
    _4 = Node("4", Pos(28, 1))
    _5 = Node("5", Pos(36, 1))
    _6 = Node("6", Pos(44, 1))
    _7 = Node("7", Pos(4, 5))
    _8 = Node("8", Pos(44, 5))
    _9 = Node("9", Pos(4, 9))
    _10 = Node("10", Pos(10, 9))
    _11 = Node("11", Pos(18, 9))
    _12 = Node("12", Pos(27, 9))
    _13 = Node("13", Pos(35, 9))
    _14 = Node("14", Pos(43, 9))
    assert (
        parse(
            """
    (1)----(2)-----(3)------(4)-----(5)-----(6)
     ^      |       |        |       ^       |
     |      |       |        |       |       |
     |      |       |        |       |       |
    (7)-----+-------+--------+-------+------(8)
     |      |       |        |       |       |
     |      |       |        |       |       |
     |      |       |        |       |       |
    (9)---(10)----(11)<----(12)----(13)----(14)
"""
        )
        == Graph(
            nodes=(_1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14),
            edges=(
                Edge(_1, "----", _2),
                Edge(_2, "----", _1),
                Edge(_2, "-----", _3),
                Edge(_2, "|||+|||", _10),
                Edge(_3, "-----", _2),
                Edge(_3, "------", _4),
                Edge(_3, "|||+|||", _11),
                Edge(_4, "-----", _5),
                Edge(_4, "------", _3),
                Edge(_4, "|||+|||", _12),
                Edge(_5, "-----", _4),
                Edge(_5, "-----", _6),
                Edge(_6, "-----", _5),
                Edge(_6, "|||", _8),
                Edge(_7, "-----+-------+--------+-------+------", _8),
                Edge(_7, "||^", _1),
                Edge(_7, "|||", _9),
                Edge(_8, "------+-------+--------+-------+-----", _7),
                Edge(_8, "|||", _14),
                Edge(_8, "|||", _6),
                Edge(_9, "---", _10),
                Edge(_9, "|||", _7),
                Edge(_10, "---", _9),
                Edge(_10, "----", _11),
                Edge(_10, "|||+|||", _2),
                Edge(_11, "----", _10),
                Edge(_11, "|||+|||", _3),
                Edge(_12, "----", _13),
                Edge(_12, "----<", _11),
                Edge(_12, "|||+|||", _4),
                Edge(_13, "----", _12),
                Edge(_13, "----", _14),
                Edge(_13, "|||+||^", _5),
                Edge(_14, "----", _13),
                Edge(_14, "|||", _8),
            ),
        )
    )


def test_parse_multiple_planes():
    a = Node("a", Pos(0, 0, 0))
    b = Node("b", Pos(5, 0, 0))
    c = Node("c", Pos(5, 0, 1))
    assert parse("(a)->(b)", "(a)->(c)") == Graph(
        nodes=(a, b, c), edges=(Edge(a, "->", b), Edge(a, "->", c))
    )
