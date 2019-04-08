import time
from multiprocessing import Queue,Process,cpu_count
from queue import Empty

def add(q, index,Q):
    r = 0
    while not q.empty():
        try:
            args = q.get(block=False)
            #Q.put(args[0])
        except Empty:
            print(f'{index}_Empty')
            pass
        except:
            print('else')
    print(f'{index}_QueueIsEmpty')

if __name__ == '__main__':
    past ,cpus= time.time(),cpu_count()*4
    Q= Queue()
    for j in range(1):
        q, p = Queue(), []
        for i in range(2000000):
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
    print('ProgramStoped')
    rs=[]
    # while not Q.empty():
    #     rs.append(Q.get())
    diff = round(time.time() - past, 2) * 1000
    print(f'AppendCost{diff}MS')
    past = time.time()
    rs.sort()
    diff = round(time.time() - past, 2) * 1000
    print(f'SortCost{diff}MS')
    past = time.time()
    print(len(rs))
