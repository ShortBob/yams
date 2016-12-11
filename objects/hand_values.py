# -*- encoding:utf-8 -*-

__author__ = 'vfarcette'

from functools import wraps
from collections import OrderedDict, Counter
from objects.yams_error import YamsError
from objects.dice import Hand
from tools.singleton_meta import Singleton


class YamsCounter(object, metaclass=Singleton):

    __INITIALIZED = False

    __SCORE_DEF = (

        (
            'Yams',
            lambda ch: 50 if len(ch) == 1 else 0
        ),
        (
            'Carre',
            lambda ch: 40 if ch[0][1] >= 4 else 0
        ),
        (
            'Suite',
            lambda ch:
            40 if len(ch) == 5 and ((ch[0][0] == 1 and ch[4][0] == 5) or (ch[0][0] == 2 and ch[4][0] == 6)) else 0
        ),
        (
            'Full',
            lambda ch: 20 if len(ch) == 2 and (ch[0][1] == 2 or ch[0][1] == 3) else 0
        ),
        (
            'MoinsDe11',
            lambda ch: 30 if sum((v * c for v, c in ch)) else 0
        ),
        (
            'Rien',
            lambda _: 0
        ),
    )

    __SCORE_DEF_DICT = OrderedDict()

    __SCORE_NAMES = []

    __CACHED_SCORE_DEF = OrderedDict()

    def __new__(cls):
        for score_name, score_lambda in cls.__SCORE_DEF:
            cls.__SCORE_NAMES.append(score_name)
            cls.__SCORE_DEF_DICT[score_name] = score_lambda
        return super().__new__(cls)

    def __init__(self):
        if not self.__INITIALIZED:
            for score in self.__class__.__SCORE_DEF_DICT.keys():
                _ = self.__getattr__(score)
            self.__INITIALIZED = True

    def __getattr__(self, attr):
        if attr not in self.__class__.__CACHED_SCORE_DEF.keys():
            try:
                hand_def = self.__class__.__SCORE_DEF_DICT[attr]

                @wraps(hand_def)
                def wrapper(hand):
                    return hand_def(self.__class__._to_values(hand))

                self.__class__.__CACHED_SCORE_DEF[attr] = wrapper
            except KeyError as e:
                raise AttributeError(e, "'YamsCounter' has no attribute '{}'".format(attr))
        return self.__class__.__CACHED_SCORE_DEF[attr]

    def __call__(self, hand_like):
        score = OrderedDict()
        for hand, result in self.__class__.__CACHED_SCORE_DEF.items():
            score[hand] = result(hand_like)
        return score

    @classmethod
    def score_names(cls):
        gen = (name for name, _ in cls.__SCORE_DEF)
        return tuple(gen)

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
        return tuple(sorted(Counter(hand).most_common()))



counter = YamsCounter()
counter_yams = counter.Yams((1, 1, 1, 1, 1))
print(counter_yams)
print(counter.Yams(Hand()))
print(counter(Hand()))
print(counter((1, 1, 1, 1, 1)))
print(counter.score_names())

counter_2 = YamsCounter()
print(counter_2.Yams((1, 1, 1, 1, 1)))
print(counter_2.Yams(Hand()))
print(counter_2(Hand()))
print(counter_2((1, 1, 1, 1, 1)))

print(YamsCounter.score_names())

