import pytest

from pymad_hzb.DateTools import is_date


def test____is_date___no_date____expectFalse():
    assert is_date('boe') == False


def test___is_date___int___expectFalse():
    with pytest.raises(TypeError):
        is_date(10)


def test___is_date____valid_date____expectTrue():
    assert is_date('2018-10-04') == True


def test___is_date____valid_date2____expectTrue():
    assert is_date('04-10-2018') == True
