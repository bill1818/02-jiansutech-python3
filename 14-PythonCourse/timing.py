#coding:utf-8

'''
  tilename: timing.py
'''

import time

def timing_func(func):
    def wrapper():
        start = time.time()
        func()
        stop = time.time()
        return (stop - start)

    return wrapper

@timing_func
def test_list_append():
    lst = []
    for i in range(0,10000):
        lst.append(i)

@timing_fun
def test_list_compre():
    [i for i in range(0, 100000)]
a = test_list_append()
c = test_list_compre()
print("test list append time:", a)
print("test list comprehension time:", c)
print("append/compre:", round(a/c, 3))


