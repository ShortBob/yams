# -*- encoding:utf-8 -*-

__author__ = 'vfarcette'


from random import randint
from yams.yams_error import YamsError


class DiceError(YamsError):
    pass


class Dice(object):

    __MIN_VALUE = 1
    __MAX_VALUE = 6

    def __init__(self):
        self._value = self.__class__._rand()
        self._locked = False

    def value(self):
        return self._value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._value == other._value
        return False

    def lock(self):
        if self._locked:
            raise DiceError('Dice is already locked !')
        self._locked = True

    def unlock(self):
        if not self._locked:
            raise DiceError('Dice is already unlocked !')
        self._locked = False

    def is_locked(self):
        return self._locked

    def roll(self):
        if self._locked:
            raise DiceError('Impossible to roll a locked Dice.')
        self._value = self.__class__._rand()

    @classmethod
    def possible_values(cls):
        return tuple((v for v in range(cls.__MIN_VALUE, cls.__MAX_VALUE + 1)))

    @classmethod
    def _rand(cls):
        return randint(cls.__MIN_VALUE, cls.__MAX_VALUE)

    def __str__(self):
        return 'D' + str(self._value)

    def __repr__(self):
        return '<{clazz} val={value} {lock_state}>'.format(
            clazz=self.__class__.__name__,
            value=self._value,
            lock_state='locked' if self._locked else 'free',
        )
