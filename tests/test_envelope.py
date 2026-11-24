import pytest

from gantryctl.envelope import FLEET, Gantry, check_lift


def test_no_derate_inside_start():
    g = FLEET["panamax"]
    assert g.swl_at(10.0) == 40.0
    assert g.swl_at(24.0) == 40.0


def test_derate_is_linear_past_start():
    g = FLEET["panamax"]
    assert g.swl_at(34.0) == pytest.approx(35.5)


def test_outreach_beyond_max_raises():
    with pytest.raises(ValueError, match="exceeds"):
        FLEET["panamax"].swl_at(40.0)


def test_negative_outreach_raises():
    with pytest.raises(ValueError, match="negative"):
        FLEET["panamax"].swl_at(-1.0)


def test_unknown_gantry_raises():
    with pytest.raises(KeyError):
        check_lift("feeder", 10.0, 10.0)


def test_unsafe_lift_reports_negative_margin():
    v = check_lift("postpanamax", 50.0, 60.0)
    assert v["safe"] is False
    assert v["margin_t"] < 0


def test_safe_lift_reports_positive_margin():
    v = check_lift("neopanamax", 45.0, 60.0)
    assert v["safe"] is True
    assert v["margin_t"] > 0


def test_custom_gantry_roundtrip():
    g = Gantry("test", 50.0, 40.0, 20.0, 1.0)
    assert g.swl_at(30.0) == 40.0
