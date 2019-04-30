import time
from multiprocessing import  cpu_count, Queue, Process
from queue import Empty
import traceback


def add(q, index, Q,waste):
    r,b = 0,0
    while 1:
        try:
            args = q.get(block=False)
            if args[0] == 1:
                Q.put(r)
                break
            else:
                r += 1
        except Empty:
            b+=1
            time.sleep(0.001)
            continue
        except:
            print('Unknown Error:')
            traceback.print_exc()
            exit(1)
        #time.sleep(0.00001)
    waste.put(b)



if __name__ == '__main__':
    multipy = 2
    past, cpus = time.time(), cpu_count() * multipy
    Q,waste = Queue(),Queue()
    for j in range(1):
        T, p = Queue(), []
        # Data
        for i in range(500000):
            T.put((0, i, i + 1))
        # Control Signal
        for i in range(cpus):
            T.put((1, i, i + 1))
        for i in range(cpus):
            p.append(Process(target=add, args=(T, i, Q,waste)))
        for i in p:
            i.start()
        for i in p:
            i.join()
        print("JoinFinished")
        tt = []
        while not Q.empty():
            tt.append(Q.get())
        for i, j in enumerate(tt):
            print(f'Process_{i} Return {j}')
        print(f'Total Return {sum(tt)}')
        w=0
        while not waste.empty():
            w+=waste.get()
    print(f'ProgramRunToTheEnd Costs {round(time.time()*1000-past*1000,2)}MS,WasteOfLoop {w} Cycles')
