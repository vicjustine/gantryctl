from gantryctl.schedule import Berth, Move


def test_empty_berth_is_zero():
    b = Berth("empty")
    assert b.critical_path_minutes() == 0
    assert b.balance_score() == 0.0


def test_critical_path_is_busiest_gantry():
    b = Berth("B2")
    b.add(Move("MSCU1", "panamax", 25))
    b.add(Move("MSCU2", "panamax", 35))
    b.add(Move("MSCU3", "neopanamax", 40))
    assert b.critical_path_minutes() == 60


def test_single_gantry_is_fully_imbalanced():
    b = Berth("B3")
    b.add(Move("X", "panamax", 10))
    assert b.balance_score() == 1.0


def test_even_split_is_balanced():
    b = Berth("B4")
    b.add(Move("X", "panamax", 30))
    b.add(Move("Y", "neopanamax", 30))
    assert b.balance_score() == 0.0
