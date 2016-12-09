# -*- encoding:utf-8 -*-

__author__ = 'vfarcette'


class GetAttr(object):

    def __init__(self):
        self.__values = {'un': 1, 'deux': 2, 'trois': 3}

    def __getattr__(self, item):
        return self.__values[item]

    def __setattr__(self, key, value):
        print(self, key, key.__class__, value)
        # raise NotImplementedError('You cant do that ! On purpose...')
        return super().__setattr__(key, value)


if __name__ == '__main__':
    g = GetAttr()
    print(g.un)
    g.un = 'UN'

    def decorateur(func):
        # @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
