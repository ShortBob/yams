# -*- encoding:utf-8 -*-

__author__ = 'vfarcette'

from yams.objects.dice import DiceError, Dice, Hand


if __name__ == '__main__':
    d = Dice()
    print("{!r}".format(d))
    h = Hand()
    print(h)
    print(repr(h))
