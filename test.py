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


class My0Int(object):

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
        self.__check_other_operand_type(other)
        return other

if __name__ == '__main__':
    # g = GetAttr()
    # print(g.un)
    # g.un = 'UN'
    #
    # def decorateur(func):
    #     # @wraps(func)
    #     def wrapper(*args, **kwargs):
    #         return func(*args, **kwargs)
    #     return wrapper

    my0 = My0Int()
    print(my0 + 1)
    print(1 + my0)
