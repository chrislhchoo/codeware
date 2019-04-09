# -*- coding: utf-8 -*-
"""
auth by:Chris
"""
import re, datetime, time
from multiprocessing import Pool, cpu_count, Queue, Process
from _queue import Empty
import traceback

def add(q, index,Q):
    r = 0
    while 1:
        try:
            args = q.get(block=False)
        except Empty:
            print(f'进程 {index} 获取输入队列为空')
        except:
            print('未知异常:')
            traceback.print_exc()

        if args[0] == 'exit':
            print(f'进程 {index} 获取退出指令，退出')
            break
        print(f'进程 {index} 正正处理{args}')

        time.sleep(0.01)
    # print(f'{index}_QueueIsEmpty')


if __name__ == '__main__':
    multipy=1
    past ,cpus= time.time(),cpu_count()*multipy
    Q= Queue()
    for j in range(1):
        q, p = Queue(), []
        # 数据项
        for i in range(20000):
            q.put(('ops',i, i + 1))
        # 控制退出项
        for i in range(cpus):
            q.put(('exit',i, i + 1))
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

