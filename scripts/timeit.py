# -*- coding: utf-8 -*-
from time import time

def timeit(method):
    # function to compute execution time -> implemented as a decorator
    def timed(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 0.01666)
        else:
            print('%r  %2.2f min' % \
                  (method.__name__, (te - ts) * 0.01666))
        return result
    return timed
