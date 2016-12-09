# -*- encoding:utf-8 -*-

__author__ = 'vfarcette'


"""
Add a simple console logger.
Use logging.getLogger('name') to get an extra one.
"""


import logging
from os import curdir
from os import path

__HAS_BEEN_SET = False
__LOGGERS = {}


def configure(include_console=True):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M',
        filename=path.join(curdir, 'yams.log'),
        filemode='w',
        )
    if include_console:
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(
            logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        )
        logging.getLogger('').addHandler(console)
    global __HAS_BEEN_SET
    __HAS_BEEN_SET = True


def get_logger(logger_name=''):
    if logger_name not in __LOGGERS:
        __LOGGERS[logger_name] = logging.getLogger(name=logger_name)
    return __LOGGERS[logger_name]
