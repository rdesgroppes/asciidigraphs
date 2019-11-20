from collections import namedtuple


class Offset(namedtuple("Offset", "dx dy dz")):
    def __new__(cls, dx, dy, dz=0):
        # noinspection PyArgumentList
        return super().__new__(cls, dx, dy, dz)


DOWN = Offset(dx=0, dy=1)
DOWN_LEFT = Offset(dx=-1, dy=1)
DOWN_RIGHT = Offset(dx=1, dy=1)
LEFT = Offset(dx=-1, dy=0)
RIGHT = Offset(dx=1, dy=0)
UP = Offset(dx=0, dy=-1)
UP_LEFT = Offset(dx=-1, dy=-1)
UP_RIGHT = Offset(dx=1, dy=-1)


class Pos(namedtuple("Pos", "x y z")):
    def __new__(cls, x, y, z=0):
        # noinspection PyArgumentList
        return super().__new__(cls, x, y, z)

    def __add__(self, offset):
        return type(self)(self.x + offset.dx, self.y + offset.dy, self.z + offset.dz)

    def __sub__(self, other):
        return Offset(self.x - other.x, self.y - other.y, self.z - other.z)
