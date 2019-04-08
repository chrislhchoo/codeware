import time
from multiprocessing import Queue,Process,cpu_count
from queue import Empty

def add(q, index):
    r = 0
    while not q.empty():
        try:
            args = q.get(block=False)
            r = args[0] * args[1]
        except Empty:
            print(f'{index}_Break')
            pass
    print(f'{index}_QueueIsEmpty')

if __name__ == '__main__':
    past ,cpus= time.time(),cpu_count()
    for j in range(1):
        qq, q, p = Queue(), Queue(), []
        for i in range(1000):
            q.put((i, i + 1))
        for i in range(cpus):
            p.append(Process(target=add, args=(q, i)))
        for i in p:
            i.start()
        for i in p:
            i.join()
        print("JoinFinished")
        ts = round((time.time() - past) * 1000, 2)
    print('ProgramStoped')
