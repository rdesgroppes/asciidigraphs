from collections import namedtuple
from enum import unique, IntEnum

from asciidigraphs.positions import (
    DOWN,
    DOWN_LEFT,
    DOWN_RIGHT,
    LEFT,
    RIGHT,
    UP,
    UP_LEFT,
    UP_RIGHT,
)

_EDGE_CHARS = {
    "-": (LEFT, RIGHT),
    "/": (UP_RIGHT, DOWN_LEFT),
    "<": (RIGHT, LEFT),
    ">": (LEFT, RIGHT),
    "\\": (UP_LEFT, DOWN_RIGHT),
    "^": (DOWN, UP),
    "v": (UP, DOWN),
    "|": (UP, DOWN),
}
_EDGE_CHARS["+"] = _EDGE_CHARS["-"] + _EDGE_CHARS["|"]
_EDGE_CHARS["X"] = _EDGE_CHARS["/"] + _EDGE_CHARS["\\"]


class NodeToken(namedtuple("NodeToken", "symbol pos")):
    pattern = r"\([^)]*\)"

    def transition_from(self, *_):
        yield Direction.ANY, self


@unique
class Direction(IntEnum):
    ANY = 0
    BACKWARD = 1
    FORWARD = 2


class EdgeToken(namedtuple("EdgeToken", "symbol pos")):
    pattern = r"[|-]"

    @property
    def slots(self):
        return frozenset(self.pos + offset for offset in _EDGE_CHARS[self.symbol])

    def transition_from(self, other, token_map):
        yield self.direction_from(other), self
        # noinspection PyTypeChecker
        yield from self.next_from(other, token_map).transition_from(self, token_map)

    def direction_from(self, other):
        return Direction.ANY

    def next_from(self, other, token_map):
        next_slots = list(self.slots)
        next_slots.remove(
            other.pos if other.pos in next_slots else other.position_to(self)
        )
        assert len(next_slots) == 1, next_slots
        next_slot = next_slots.pop()
        return token_map.get(next_slot) or self._diagonal_to(next_slot, token_map)

    def _diagonal_to(self, next_slot, token_map):
        adjacent_positions = (
            next_slot + adjacent_offset
            for adjacent_offset in {
                DOWN: (LEFT, RIGHT),
                LEFT: (DOWN, UP),
                RIGHT: (DOWN, UP),
                UP: (LEFT, RIGHT),
            }[next_slot - self.pos]
        )

        diagonal_tokens = [
            token
            for token in (token_map.get(pos) for pos in adjacent_positions)
            if isinstance(token, DiagonalEdgeToken) and self.pos in token.slots
        ]
        assert len(diagonal_tokens) == 1, diagonal_tokens
        return diagonal_tokens.pop()


class ArrowEdgeToken(EdgeToken):
    pattern = r"[<>^v]"

    def direction_from(self, other):
        return dict(
            zip(_EDGE_CHARS[self.symbol], (Direction.BACKWARD, Direction.FORWARD))
        )[self.pos - (other.pos if other.pos in self.slots else other.position_to(self))]


class DiagonalEdgeToken(EdgeToken):
    pattern = r"[/\\]"

    def position_to(self, other):
        adjacent_positions = {
            other.pos + adjacent_offset
            for adjacent_offset in {
                DOWN_LEFT: (DOWN, LEFT),
                DOWN_RIGHT: (DOWN, RIGHT),
                UP_LEFT: (UP, LEFT),
                UP_RIGHT: (UP, RIGHT),
            }[self.pos - other.pos]
        }.intersection(other.slots)
        assert len(adjacent_positions) == 1, adjacent_positions
        return adjacent_positions.pop()


class CrossingMixin:
    def next_from(self, other, token_map):
        # noinspection PyUnresolvedReferences
        return token_map[self.pos + (self.pos - other.pos)]


class DiagonalCrossingEdgeToken(CrossingMixin, DiagonalEdgeToken):
    pattern = r"X"


class VerticalCrossingEdgeToken(CrossingMixin, EdgeToken):
    pattern = r"\+"


token_classes = (
    ArrowEdgeToken,
    DiagonalCrossingEdgeToken,
    DiagonalEdgeToken,
    EdgeToken,
    NodeToken,
    VerticalCrossingEdgeToken,
)
