import re, datetime, time
from multiprocessing import Pool, cpu_count, Queue, Process, Lock
import random, sys
from queue import Empty
import traceback


def add(q, index, Q, waste, lost_stack):
    r, b = 0, 0
    while 1:
        try:
            args = q.get(block=False)
            time.sleep(1)
            lost_stack.put([args])
            if args[0] == 1:
                Q.put(r)
                lost_stack.get()
                break
            else:
                r += 1
                sum = 0
                time.sleep(15)
                for x in range(args[1]):
                    sum += x
                lost_stack.get()
        except Empty:
            b += 1
            time.sleep(0.00000001)
            continue
        except:
            print('Unknown Error:')
            traceback.print_exc()
            exit(1)
    waste.put(b)


if __name__ == '__main__':
    multipy = 1
    past, cpus = time.time(), 4  # cpu_count() * multipy
    Q, waste = Queue(), Queue()
    processes = {}
    task_stack = []
    for i in range(cpus):
        x = Queue()
        task_stack.append(x)
    n = 0
    for j in range(1):
        T, p = Queue(), []
        # Data
        for i in range(599990, 600000):
            T.put((0, i))
        # Control Signal
        for i in range(cpus):
            T.put((1, i))
        for i in range(cpus):
            p = Process(target=add, args=(T, i, Q, waste, task_stack[i]))
            processes[n] = p
            n += 1
        for i in range(n):
            processes[i].start()
        print(processes)

        #################################
        while len(processes) >= 1:
            time.sleep(1)
            for n in processes.copy().keys():
                p = processes[n]
                if p.exitcode is None:
                    if not p.is_alive():  # Not finished and not running
                        # Do your error handling and restarting here assigning the new process to processes[n]
                        print('is gone as if never born!')
                elif p.exitcode >= 1 and not p.is_alive():
                    print(f'Process {n} Ended with an error or a terminate',p.exitcode)
                    del processes[n]
                    p.join()
                    # Handle this either by restarting or delete the entry so it is removed from list as for else
                else:
                    print(f'Process {n} finished',p.exitcode)
                    del processes[n]  # Removed finished items from the dictionary
                    p.join()  # Allow tidyup
                    # When none are left then loop will end
        #################################
        print("JoinFinished")
        tt = []
        while not Q.empty():
            tt.append(Q.get())
        for i, j in enumerate(tt):
            print(f'Process_{i} Return {j}')
        print(f'Total Return {sum(tt)}')
        w = 0
        while not waste.empty():
            w += waste.get()
    task_lost = []
    for i in task_stack:
        while not i.empty():
            task_lost.append(i.get())
    print('Who is Lost')
    print(task_lost)
    print(f'ProgramRunToTheEnd Costs {round(time.time()*1000-past*1000,2)}MS,\nwaste of loop {round(w/1000,2)}k cycles')
    sys.exit()
