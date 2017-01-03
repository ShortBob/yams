# -*- encoding:utf-8 -*-

__author__ = 'vfarcette'

from functools import wraps
from collections import OrderedDict, Counter, namedtuple

from tools.singleton_meta import Singleton

from yams.dice import Hand
from yams.yams_error import YamsError


ScoreLineChecker = namedtuple('ScoreLineChecker', ('name', 'num_param', 'definition'))


class YamsCounter(object, metaclass=Singleton):

    __INITIALIZED = False

    __SCORE_DEF = (
        ScoreLineChecker(
            'As',
            1,
            lambda ch: sum((v * c if v == 1 else 0 for v, c in ch))
        ),
        ScoreLineChecker(
            'Deux',
            1,
            lambda ch: sum((v * c if v == 2 else 0 for v, c in ch))
        ),
        ScoreLineChecker(
            'Trois',
            1,
            lambda ch: sum((v * c if v == 3 else 0 for v, c in ch))
        ),
        ScoreLineChecker(
            'Quatre',
            1,
            lambda ch: sum((v * c if v == 4 else 0 for v, c in ch))
        ),
        ScoreLineChecker(
            'Cinq',
            1,
            lambda ch: sum((v * c if v == 5 else 0 for v, c in ch))
        ),
        ScoreLineChecker(
            'Six',
            1,
            lambda ch: sum((v * c if v == 6 else 0 for v, c in ch))
        ),
        ScoreLineChecker(
            'Mini',
            2,
            lambda ch, ss: sum((v * c for v, c in ch)) if
            (ss.Maxi == 0 or ss.Maxi > sum((v * c for v, c in ch))) else 0
        ),
        ScoreLineChecker(
            'Maxi',
            2,
            lambda ch, ss: sum((v * c for v, c in ch)) if (ss.Mini < sum((v * c for v, c in ch))) else 0
        ),
        ScoreLineChecker(
            'DoublePaire',
            1,
            lambda ch: 10
            if len(ch) == 1 or len(ch) == 2 or (
                len(ch) == 3 and sorted(Counter((c for v, c in ch)).most_common())[-1][1] == 2) else 0
        ),
        ScoreLineChecker(
            'Full',
            1,
            lambda ch: 20 if len(ch) == 1 or (len(ch) == 2 and (ch[0][1] == 2 or ch[0][1] == 3)) else 0
        ),
        ScoreLineChecker(
            'Carre',
            1,
            lambda ch: 40 if ch[0][1] >= 4 else 0
        ),
        ScoreLineChecker(
            'Suite',
            1,
            lambda ch: 40
            if len(ch) == 5 and (
                (ch[0][0] == 1 and ch[4][0] == 5)
                or
                (ch[0][0] == 2 and ch[4][0] == 6)) else 0
        ),
        ScoreLineChecker(
            'Yams',
            1,
            lambda ch: 50 if len(ch) == 1 else 0
        ),
        ScoreLineChecker(
            'MoinsDe11',
            1,
            lambda ch: max(0, 20 + (5 * (11 - sum((v * c for v, c in ch)))))
        ),
    )

    __SCORE_DEF_DICT = OrderedDict()

    __SCORE_NAMES = []

    __CACHED_SCORE_DEF = OrderedDict()

    def __new__(cls):
        for score_line_checker in cls.__SCORE_DEF:
            cls.__SCORE_NAMES.append(score_line_checker.name)
            cls.__SCORE_DEF_DICT[score_line_checker.name] = score_line_checker
        return super().__new__(cls)

    def __init__(self):
        if not self.__class__.__INITIALIZED:
            for score in self.__class__.__SCORE_DEF_DICT.keys():
                _ = self.__getattr__(score)
            self.__class__.__INITIALIZED = True

    def __getattr__(self, attr):
        if self.__class__.__INITIALIZED:
            raise NotImplementedError('Internal objects are not made for direct access after initialisation.')

        if attr not in self.__class__.__CACHED_SCORE_DEF.keys():
            score_line_checker = self.__class__.__SCORE_DEF_DICT[attr]
            check_func = score_line_checker.definition

            if score_line_checker.num_param == 1:

                @wraps(score_line_checker)
                def wrapper(hand_n_score_wrapper):
                    (hand, *_) = hand_n_score_wrapper
                    return check_func(self.__class__._to_values(hand))

            elif score_line_checker.num_param == 2:

                @wraps(score_line_checker)
                def wrapper(hand_n_score_wrapper):
                    (hand, *opt_score_sheet) = hand_n_score_wrapper
                    values = self.__class__._to_values(hand)
                    return check_func(values, *opt_score_sheet)

            else:
                raise NotImplementedError('All {} must define 1 or 2 params in one of {}.'.format(
                    ScoreLineChecker.__name__,
                    ScoreLineChecker._fields,
                ))

            self.__class__.__CACHED_SCORE_DEF[attr] = wrapper

        return self.__class__.__CACHED_SCORE_DEF[attr]

    def __call__(self, hand_n_score_wrapper):
        score = OrderedDict()
        for hand, result in self.__class__.__CACHED_SCORE_DEF.items():
            score[hand] = result(hand_n_score_wrapper)
        return score

    @classmethod
    def score_names(cls):
        return tuple((name for name in cls.__SCORE_NAMES))

    @classmethod
    def _to_values(cls, hand):
        if isinstance(hand, Hand):
            hand = hand.values()
        elif isinstance(hand, (list, tuple)) and\
                len(hand) == 5 and\
                all(isinstance(v, int) and 1 <= v <= 6 for v in hand):
            pass
        else:
            raise YamsError(
                'Only a Hand object or list or tuple of int between 1 and 6 included '
                'is supposed to be transformed this way.'
            )
        most_common_sort = tuple(sorted(Counter(hand).most_common()))
        return most_common_sort


if __name__ == '__main__':

    class ScoreSheet(object):
        def __getattr__(self, item):
            return 0

    score_sheet_mock = ScoreSheet()

    def checker_printer(hand):
        print('Hand {} -> Results {}'.format(
            hand,
            YamsCounter()((hand, score_sheet_mock))
        ))

    checker_printer((1, 1, 1, 1, 1))
    checker_printer((1, 2, 6, 6, 6))
    checker_printer((1, 2, 2, 6, 6))
    checker_printer(Hand())
    checker_printer(Hand())
    checker_printer(Hand())
    checker_printer(Hand())
    print(YamsCounter.score_names())
