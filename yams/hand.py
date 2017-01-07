# -*- encoding:utf-8 -*-

from collections import OrderedDict
from yams.dice import Dice
from yams.yams_error import YamsError

__author__ = 'vfarcette'


class HandError(YamsError):
    pass


class Hand(object):

    __DICE_COUNT = 5
    (*__DICE_INDEXES,) = (n for n in range(1, __DICE_COUNT + 1))
    __INITIAL_ROLL_REMAINING = 3

    def __init__(self):
        self._dices = self.__class__._new_dices()
        self._rolls_remaining = self.__class__.__INITIAL_ROLL_REMAINING

    def lock(self, *indexes):
        self.__class__._check_indexes(indexes)
        for i in indexes:
            self._dices[i].lock()

    def unlock(self, *indexes):
        self.__class__._check_indexes(indexes)
        for i in indexes:
            self._dices[i].unlock()

    def roll(self):
        if self._rolls_remaining == 0:
            raise HandError('The Hand has reached is maximum rolls count.')
        else:
            for d in self._dices.values():
                if not d.is_locked():
                    d.roll()
            self._rolls_remaining -= 1

    def values(self):
        result_builder = (d.value() for d in self._dices.values())
        return tuple(result_builder)

    @classmethod
    def _check_indexes(cls, indexes):
        for i in indexes:
            if not isinstance(i, int):
                raise HandError('Given indexes have to be `int` but was {}'.format(type(i)))
            if i not in cls.__DICE_INDEXES:
                raise HandError('Given indexes have to be one of {}'.format(cls.__DICE_INDEXES))

    @classmethod
    def _new_dices(cls):
        dices_gen = (Dice() for x in range(cls.__DICE_COUNT))
        dices_dict = OrderedDict()
        for index, dice in zip(cls.__DICE_INDEXES, dices_gen):
            dices_dict[index] = dice
        return dices_dict

    def __repr__(self):
        representation = '<Hand {}>'
        inner = []
        for index, dice in self._dices.items():
            inner.append('{}:{}'.format(index, repr(dice)))
        return representation.format(' '.join(inner))

    def __str__(self):
        return ' '.join((str(d) for d in self._dices.values()))
