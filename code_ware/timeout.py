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

if __name__ == '__main__':
    past = time.time()
    try:
        task()
    except func_timeout.exceptions.FunctionTimedOut:
        print(f'task func_timeout,costs {round((time.time()-past)*1000,2)} MS')

