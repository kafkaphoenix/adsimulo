from adsimulo.utils import clamp


def test_clamp_ok():
    upper_limit = 2
    lower_limit = -1
    ok_value = 0.5

    assert clamp(upper_limit) == 1
    assert clamp(lower_limit) == 0
    assert clamp(ok_value) == ok_value
