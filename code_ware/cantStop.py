# -*- coding: utf-8 -*-
"""
auth by:Chris
"""
import re
import time as ti
from multiprocessing import Pool, cpu_count, Queue, Process
from queue import Empty
import traceback


def add(leakqueue, index):
    r = 0
    while 1:
        try:
            args = leakqueue.get(block=False)
            if args[0] == 'exit':
                # print(f'进程 {index} 获取退出指令，退出')
                break
                # print(f'进程 {index} 正正处理{args}')
        except Empty:
            continue
            # print(f'进程 {index} 获取输入队列为空')
        except:
            # print('未知异常:')
            traceback.print_exc()

        ti.sleep(0.01)
        # print(f'{index}_QueueIsEmpty')


if __name__ == '__main__':
    multipy = 8
    past, cpus = ti.time(), cpu_count() * multipy
    Q = Queue()
    for j in range(1):
        q, p = Queue(), []
        # 数据项
        for i in range(20000):
            q.put(('ops', i, i + 1))
        # 控制退出项
        for i in range(cpus):
            q.put(('exit', i, i + 1))
        diff = round(ti.time() - past, 2) * 1000
        print(f'PutCost{diff}MS')
        past = ti.time()
        for i in range(cpus):
            p.append(Process(target=add, args=(q, i)))
        for i in p:
            i.start()
        for i in p:
            i.join()
        print("JoinFinished")
        diff = round(ti.time() - past, 2) * 1000
        print(f'LoopCost_{diff}MS')
        past = ti.time()
        ts = round((ti.time() - past) * 1000, 2)
    print('ProgramRunToTheEnd')
