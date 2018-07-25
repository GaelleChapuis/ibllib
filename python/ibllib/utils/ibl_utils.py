# -*- coding: utf-8 -*-
# @Author: nico
# @Date:   2018-02-13 18:10:50
# @Last Modified by:   nico
# @Last Modified time: 2018-02-15 13:38:29
import collections
import time


def timing(f):
    """
    Timing decorator will print time took in milliseconds
    """
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f, (time2-time1)*1000.0))
        return ret

    return wrap


def iflatten(x):
    result = []
    for el in x:
        if isinstance(el, collections.Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


def flat_gen(x):
    def iselement(e):
        return not(isinstance(e, collections.Iterable) and not isinstance(e,
                                                                          str))
    for el in x:
        if iselement(el):
            yield el
        else:
            yield from flat_gen(el)  # python >= 3.3
            # for sub in flatten(el):
            #     yield sub


def flatten(x):
    return list(flat_gen(x))


if __name__ == '__main__':
    x = [1, 2, 3, [1, 2]]
    result = []
    for el in x:
        if isinstance(el, collections.Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)