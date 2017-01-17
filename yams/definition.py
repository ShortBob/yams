# -*- encoding:utf-8 -*-

__author__ = 'vfarcette'


from collections import namedtuple, Counter


SUB_TOTAL_1_FLAG = 'T1'
SUB_TOTAL_2_FLAG = 'T2'
TOTAL_FLAG = 'Total'
GENERAL_TOTAL_FLAG = 'TOTAL'

TARGET_YAMS_COUNTER = 'YamsCounter'
TARGET_SCORE_COLUMN = 'ScoreColumn'
TARGET_SCORE_SHEET = 'ScoreSheet'

LineDef = namedtuple('LineDef', ('name', 'target', 'total', 'definition'))

SCORE_SHEET_DEF = (

    # First part. Count in T1
    LineDef(
        'As',
        (TARGET_YAMS_COUNTER, TARGET_SCORE_COLUMN, ),
        SUB_TOTAL_1_FLAG,
        lambda ch, _: sum((v * c for v, c in ch if v == 1))
    ),
    LineDef(
        'Deux',
        (TARGET_YAMS_COUNTER, TARGET_SCORE_COLUMN, ),
        SUB_TOTAL_1_FLAG,
        lambda ch, _: sum((v * c for v, c in ch if v == 2))
    ),
    LineDef(
        'Trois',
        (TARGET_YAMS_COUNTER, TARGET_SCORE_COLUMN, ),
        SUB_TOTAL_1_FLAG,
        lambda ch, _: sum((v * c for v, c in ch if v == 3))
    ),
    LineDef(
        'Quatre',
        (TARGET_YAMS_COUNTER, TARGET_SCORE_COLUMN, ),
        SUB_TOTAL_1_FLAG,
        lambda ch, _: sum((v * c for v, c in ch if v == 4))
    ),
    LineDef(
        'Cinq',
        (TARGET_YAMS_COUNTER, TARGET_SCORE_COLUMN, ),
        SUB_TOTAL_1_FLAG,
        lambda ch, _: sum((v * c for v, c in ch if v == 5))
    ),
    LineDef(
        'Six',
        (TARGET_YAMS_COUNTER, TARGET_SCORE_COLUMN, ),
        SUB_TOTAL_1_FLAG,
        lambda ch, _: sum((v * c for v, c in ch if v == 6))
    ),
    # T1. Count in Total
    LineDef(
        SUB_TOTAL_1_FLAG,
        (TARGET_SCORE_COLUMN, ),
        TOTAL_FLAG,
        lambda sc: sum(sc.__getattr(line.name) for line in SCORE_SHEET_DEF if line.target == SUB_TOTAL_1_FLAG)
    ),
    # Bonus. Count in Total
    LineDef(
        'Bonus',
        (TARGET_SCORE_COLUMN, ),
        TOTAL_FLAG,
        lambda sc: 30 if sc.T1 >= 60 else 0
    ),

    # Part 2. Count in T2
    LineDef(
        'Mini',
        (TARGET_YAMS_COUNTER, TARGET_SCORE_COLUMN, ),
        SUB_TOTAL_2_FLAG,
        lambda ch, ss: sum((v * c for v, c in ch)) if
        (ss.Maxi == 0 or ss.Maxi > sum((v * c for v, c in ch))) else 0
    ),
    LineDef(
        'Maxi',
        (TARGET_YAMS_COUNTER, TARGET_SCORE_COLUMN, ),
        SUB_TOTAL_2_FLAG,
        lambda ch, ss: sum((v * c for v, c in ch)) if (ss.Mini < sum((v * c for v, c in ch))) else 0
    ),
    LineDef(
        'DoublePaire',
        (TARGET_YAMS_COUNTER, TARGET_SCORE_COLUMN, ),
        SUB_TOTAL_2_FLAG,
        lambda ch, _: 10
        if len(ch) == 1 or len(ch) == 2 or (
            len(ch) == 3 and sorted(Counter((c for v, c in ch)).most_common())[-1][1] == 2) else 0
    ),
    LineDef(
        'Full',
        (TARGET_YAMS_COUNTER, TARGET_SCORE_COLUMN, ),
        SUB_TOTAL_2_FLAG,
        lambda ch, _: 20 if len(ch) == 1 or (len(ch) == 2 and (ch[0][1] == 2 or ch[0][1] == 3)) else 0
    ),
    LineDef(
        'Carre',
        (TARGET_YAMS_COUNTER, TARGET_SCORE_COLUMN, ),
        SUB_TOTAL_2_FLAG,
        lambda ch, _: 40 if ch[0][1] >= 4 else 0
    ),
    LineDef(
        'Suite',
        (TARGET_YAMS_COUNTER, TARGET_SCORE_COLUMN, ),
        SUB_TOTAL_2_FLAG,
        lambda ch, _: 40
        if len(ch) == 5 and (
            (ch[0][0] == 1 and ch[4][0] == 5)
            or
            (ch[0][0] == 2 and ch[4][0] == 6)) else 0
    ),
    LineDef(
        'Yams',
        (TARGET_YAMS_COUNTER, TARGET_SCORE_COLUMN, ),
        SUB_TOTAL_2_FLAG,
        lambda ch, _: 50 if len(ch) == 1 else 0
    ),
    LineDef(
        'MoinsDe11',
        (TARGET_YAMS_COUNTER, TARGET_SCORE_COLUMN, ),
        SUB_TOTAL_2_FLAG,
        lambda ch, _: max(0, 20 + (5 * (11 - sum((v * c for v, c in ch)))))
    ),
    # T2. Count in Total
    LineDef(
        SUB_TOTAL_2_FLAG,
        (TARGET_SCORE_COLUMN, ),
        TOTAL_FLAG,
        lambda sc: sum(sc.__getattr(line.name) for line in SCORE_SHEET_DEF if line.target == SUB_TOTAL_2_FLAG)
    ),

    # Total. Count in TOTAL (ScoreSheet)
    LineDef(
        TOTAL_FLAG,
        (TARGET_SCORE_COLUMN, TARGET_SCORE_SHEET, ),
        GENERAL_TOTAL_FLAG,
        lambda ss: sum(ss.__getattr(line.name) for line in SCORE_SHEET_DEF if line.target == TOTAL_FLAG)
    )
)
