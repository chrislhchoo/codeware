#!/usr/bin/env python
# -*- coding: utf-8 -*-

from func_timeout import func_set_timeout
import time, datetime
import func_timeout


@func_set_timeout(1)
def task():
    while True:
        print('hello world')
        time.sleep(1)


def performance(func):
    def wrapper(*args, **kwargs):
        past = time.time()
        func(*args, **kwargs)
        timediff = round((time.time() - past) * 1000, 2)
        print(timediff)

    return wrapper


@performance
def add(adding):
    r = 0
    for i in range(adding):
        r += i


@performance
def beep(adding):
    r = 0
    for i in range(adding):
        r += i
    for i in range(adding):
        r += i


if __name__ == '__main__':
    past = time.time()
    try:
        task()
    except func_timeout.exceptions.FunctionTimedOut:
        print(f'task func_timeout,costs {round((time.time()-past)*1000,2)} MS')
    beep(10000000)
