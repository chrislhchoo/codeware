import time
from multiprocessing import Queue,Process,cpu_count
from queue import Empty

def add(q, index,Q):
    r = 0
    while not q.empty():
        try:
            args = q.get(block=False)
            Q.put(args[0])
        except Empty:
            #print(f'{index}_Break')
            pass
    print(f'{index}_QueueIsEmpty')

if __name__ == '__main__':
    past ,cpus= time.time(),cpu_count()
    Q= Queue()
    for j in range(1):
        q, p = Queue(), []
        for i in range(1000):
            q.put((i, i + 1))
        for i in range(cpus):
            p.append(Process(target=add, args=(q, i,Q)))
        for i in p:
            i.start()
        for i in p:
            i.join()
        print("JoinFinished")
        ts = round((time.time() - past) * 1000, 2)
    print('ProgramStoped')
    rs=[]
    while not Q.empty():
        rs.append(Q.get())
    rs.sort()
    print(len(rs))
