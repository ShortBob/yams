# -*- encoding:utf-8 -*-

__author__ = 'vfarcette'


from collections import OrderedDict
from yams.definition import SCORE_SHEET_DEF
from yams.hand_values_counter import YamsCounter


class NullInt(object):

    def __int__(self):
        return 0

    @staticmethod
    def __check_other_operand_type(other):
        if not isinstance(other, (int, float)):
            raise ValueError('operand {} have to be int or float'.format(other))

    def __add__(self, other):
        self.__class__.__check_other_operand_type(other)
        return other

    def __radd__(self, other):
        self.__class__.__check_other_operand_type(other)
        return other


class EmptyValue(NullInt):
    pass


class CrossedOutValue(NullInt):
    pass


class ScoreColumnUsage(object):
    pass


class ScoreColumn(object):

    def __init__(self, col_usage: ScoreColumnUsage):
        self._value_score = OrderedDict()
        for line in SCORE_SHEET_DEF:
            self._value_score[line.name] = EmptyValue()


class ScoreSheet(object):
    pass
