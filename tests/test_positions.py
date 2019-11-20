from asciidigraphs.positions import Offset, Pos


def test_new_offset_with_default_z():
    assert Offset(1, 2) == Offset(dx=1, dy=2, dz=0)


def test_new_pos_with_default_z():
    assert Pos(1, 2) == Pos(x=1, y=2, z=0)


def test_add_offset_to_pos():
    assert Pos(1, 2, 3) + Offset(10, 20, 30) == Pos(11, 22, 33)


def test_subtract_pos_from_pos():
    assert Pos(1, 2, 3) - Pos(3, 2, 1) == Offset(-2, 0, 2)
