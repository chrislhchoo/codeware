# -*- coding: utf-8 -*-
"""
*
* copyright (c) 2016, 2017 State Street Bank & Trust Co.
% Description:	Utils for Python3
"""
import re, datetime, time
from multiprocessing import Pool, cpu_count, Queue, Process
from _queue import Empty
import multiprocessing

def add(q, index,Q):
    r = 0
    try:
        args = q.get(block=False)
        #Q.put(args[0])
    except Empty:
        #print(f'{index}_Empty')
        pass
    except:
        print('else')
    print(f'{index}_QueueIsEmpty')


if __name__ == '__main__':
    multipy=1
    past ,cpus= time.time(),cpu_count()*multipy
    Q= Queue()
    for j in range(1):
        q, p = Queue(), []
        for i in range(20000):
            q.put((i, i + 1))
        diff=round(time.time()-past,2)*1000
        print(f'PutCost{diff}MS')
        past=time.time()
        for i in range(cpus):
            p.append(Process(target=add, args=(q, i,Q)))
        for i in p:
            i.start()
        for i in p:
            i.join()
        print("JoinFinished")
        diff=round(time.time()-past,2)*1000
        print(f'LoopCost{diff}MS')
        past=time.time()
        ts = round((time.time() - past) * 1000, 2)
    print('ProgramRunToTheEnd')
    #diff = round(time.time() - past, 2) * 1000

