# -*- encoding:utf-8 -*-
from yams.hand import Hand

__author__ = 'vfarcette'


import pytest
from yams.yams_error import YamsError
from yams.hand_values_counter import YamsCounter


class _ScoreSheet(object):
    """Score sheet mock"""
    def __getattr__(self, item):
        return 0

@pytest.fixture
def yams_counter():
    return YamsCounter()

@pytest.fixture
def sheet_mock():
    return _ScoreSheet()

@pytest.fixture
def hand_sheet():
    return Hand(), _ScoreSheet()


# Programming tests

def test_singleton_behaviour():
    y1 = YamsCounter()
    y2 = YamsCounter()
    assert id(y1) == id(y2), 'All YamsCounter instance should be the same.'


# Behavior tests

def test_access_to_attributes_raises(yams_counter):
    with pytest.raises(NotImplementedError):
        _ = yams_counter.Yams
    with pytest.raises(NotImplementedError):
        _ = yams_counter.undefined

def test_call_allowed(yams_counter, hand_sheet):
    yams_counter(hand_sheet)


# Values tests

def test_values_results_and_score_name_are_identical(yams_counter, hand_sheet):
    names = YamsCounter.score_names()
    result = yams_counter(hand_sheet)
    assert len(set(names) ^ set(result.keys())) == 0, 'YamsCounter.score_names() and yams_counter(hand_sheet).keys() ' \
                                                      'should contains the same items.'

# Scoring tests

def test_as(yams_counter, sheet_mock):
    assert yams_counter(((1, 1, 3, 4, 5), sheet_mock))['As'] == 2, 'As : It should score 2.'
    assert yams_counter(((1, 1, 1, 1, 5), sheet_mock))['As'] == 4, 'As : It should score 4.'

def test_deux(yams_counter, sheet_mock):
    assert yams_counter(((2, 1, 3, 2, 5), sheet_mock))['Deux'] == 4, 'Deux : It should score 4.'
    assert yams_counter(((2, 1, 2, 2, 5), sheet_mock))['Deux'] == 6, 'Deux : It should score 6.'

def test_trois(yams_counter, sheet_mock):
    assert yams_counter(((1, 1, 3, 4, 5), sheet_mock))['Trois'] == 3, 'Trois : It should score 3.'
    assert yams_counter(((3, 1, 3, 4, 5), sheet_mock))['Trois'] == 6, 'Trois : It should score 6.'

def test_quatre(yams_counter, sheet_mock):
    assert yams_counter(((1, 1, 3, 4, 5), sheet_mock))['Quatre'] == 4, 'Quatre : It should score 4.'
    assert yams_counter(((1, 4, 3, 4, 4), sheet_mock))['Quatre'] == 12, 'Quatre : It should score 12.'

def test_cinq(yams_counter, sheet_mock):
    assert yams_counter(((1, 1, 5, 4, 5), sheet_mock))['Cinq'] == 10, 'Cinq : It should score 10.'
    assert yams_counter(((5, 1, 5, 4, 5), sheet_mock))['Cinq'] == 15, 'Cinq : It should score 15.'

def test_six(yams_counter, sheet_mock):
    assert yams_counter(((1, 1, 3, 4, 5), sheet_mock))['Six'] == 0, 'Six : It should score 0.'
    assert yams_counter(((6, 6, 6, 6, 5), sheet_mock))['Six'] == 24, 'Six : It should score 24.'

def test_mini(yams_counter, sheet_mock):
    assert yams_counter(((1, 1, 3, 4, 5), sheet_mock))['Mini'] == 14, 'Mini : It should score 14.'

def test_maxi(yams_counter, sheet_mock):
    assert yams_counter(((1, 1, 3, 4, 5), sheet_mock))['Maxi'] == 14, 'Maxi : It should score 14.'

def test_double_paire(yams_counter, sheet_mock):
    assert yams_counter(((1, 1, 3, 3, 5), sheet_mock))['DoublePaire'] == 10, 'DoublePaire : It should score 10.'
    assert yams_counter(((1, 1, 1, 1, 5), sheet_mock))['DoublePaire'] == 10, 'DoublePaire : It should score 10.'
    assert yams_counter(((1, 1, 1, 1, 1), sheet_mock))['DoublePaire'] == 10, 'DoublePaire : It should score 10.'
    assert yams_counter(((1, 1, 3, 2, 5), sheet_mock))['DoublePaire'] == 0, 'DoublePaire : It should score 0.'

def test_full(yams_counter, sheet_mock):
    assert yams_counter(((1, 1, 3, 3, 3), sheet_mock))['Full'] == 20, 'Full : It should score 20.'
    assert yams_counter(((1, 1, 3, 3, 5), sheet_mock))['Full'] == 0, 'Full : It should score 0.'

def test_carre(yams_counter, sheet_mock):
    assert yams_counter(((1, 1, 1, 1, 5), sheet_mock))['Carre'] == 40, 'Carre : It should score 40.'
    assert yams_counter(((1, 1, 3, 4, 5), sheet_mock))['Carre'] == 0, 'Carre : It should score 0.'

def test_suite(yams_counter, sheet_mock):
    assert yams_counter(((1, 2, 3, 4, 5), sheet_mock))['Suite'] == 40, 'Suite : It should score 40.'
    assert yams_counter(((2, 3, 4, 5, 6), sheet_mock))['Suite'] == 40, 'Suite : It should score 40.'
    assert yams_counter(((2, 3, 4, 5, 5), sheet_mock))['Suite'] == 0, 'Suite : It should score 0.'

def test_yams(yams_counter, sheet_mock):
    assert yams_counter(((1, 1, 1, 1, 1), sheet_mock))['Yams'] == 50, 'Yams : It should score 50.'
    assert yams_counter(((1, 1, 1, 1, 2), sheet_mock))['Yams'] == 00, 'Yams : It should score 0.'

def test_moins_de_11(yams_counter, sheet_mock):
    assert yams_counter(((1, 1, 3, 2, 1), sheet_mock))['MoinsDe11'] == 35, 'MoinsDe11 : It should score 35.'
    assert yams_counter(((3, 1, 3, 2, 2), sheet_mock))['MoinsDe11'] == 20, 'MoinsDe11 : It should score 20.'
    assert yams_counter(((1, 1, 1, 1, 1), sheet_mock))['MoinsDe11'] == 50, 'MoinsDe11 : It should score 50.'
