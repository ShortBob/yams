# -*- encoding:utf-8 -*-

__author__ = 'vfarcette'


import pytest
from objects.dice import Dice, DiceError, Hand, HandError

# Dice object tests

@pytest.fixture
def d():
    return Dice()


def test_value_is_an_int(d):
    assert isinstance(d.value(), int) == True, 'A Dice value is an int.'


def test_dice_is_unlocked_at_creation(d):
    assert d.is_locked() == False, 'Dice is supposed to be unlocked at creation.'


def test_unlocked_dice_can_be_locked(d):
    d.lock()
    assert d.is_locked() == True, 'Locking a Dice makes it locked.'


def test_try_to_unlock_an_unlocked_dice_fails(d):
    with pytest.raises(DiceError):
        d.unlock()


def test_lock_and_unlock_makes_dice_unlocked(d):
    d.lock()
    d.unlock()
    assert d.is_locked() == False, 'Lock, then unlock... Dice should be unlocked.'


def test_locked_dice_can_not_be_locked_twice(d):
    d.lock()
    with pytest.raises(DiceError):
        d.lock()


def test_unlocked_dice_can_roll(d):
    d.roll()


def test_locked_dice_can_not_roll(d):
    d.lock()
    with pytest.raises(DiceError):
        d.roll()


def test_dice_possible_values():
    assert Dice.possible_values() == (1, 2, 3, 4, 5, 6), 'Possible values should be 6 `int` between 1 and 6 included'

# Hand object tests

@pytest.fixture
def h():
    return Hand()


def test_hand_lock_do_not_admit_non_int(h):
    with pytest.raises(HandError):
        h.lock('')


def test_hand_lock_admit_empty_arguments(h):
    h.lock()


def test_hand_roll_is_allowed_when_all_dices_are_locked(h):
    h.lock(1, 2, 3, 4, 5)
    h.roll()


def test_hand_give_values_as_list_of_five_int(h):
    assert type(h.values()) == tuple, 'Values of a hand should be a tuple.'
    assert len(h.values()) == 5, 'There should be five values in a Hand.'
    for v in h.values():
        assert isinstance(v, int) == True, 'Values of a hand should be int.'


def test_try_to_roll_hand_more_than_three_times_raise_exception(h):
    h.roll()
    h.roll()
    h.roll()
    with pytest.raises(HandError):
        h.roll()
