# -*- encoding:utf-8 -*-

__author__ = 'vfarcette'


import pytest
from objects.yams_error import YamsError
from objects.dice import Hand
from objects.hand_values import _to_values,  check_hand


def test_to_values_accept_hand():
    _to_values(Hand())


def test_to_values_accept_list_of_tuple():
    _to_values((1, 2, 3, 4, 5))
    _to_values([1, 2, 3, 4, 5])


def test_to_values_refuses_some_list_or_tuple():
    with pytest.raises(YamsError):
        _to_values(())
    with pytest.raises(YamsError):
        _to_values([])
    with pytest.raises(YamsError):
        _to_values((0, 1, 2, 3, 4))
    with pytest.raises(YamsError):
        _to_values([1, 2, 3, 4, 7])


def test_hand_checking_with_static_values():
    assert check_hand((1, 1, 1, 1, 1)) == 'Yams'
    assert check_hand((1, 1, 1, 1, 2)) == 'Carre'
    assert check_hand((1, 2, 3, 4, 5)) == 'Suite'
    assert check_hand((2, 3, 4, 5, 6)) == 'Suite'
    assert check_hand((2, 2, 3, 3, 3)) == 'Full'


def test_hand_checking_with_actual_hand():
    h = Hand()
    assert isinstance(check_hand(h), str) == True, 'The return type of a successful checking should be `str`.'
