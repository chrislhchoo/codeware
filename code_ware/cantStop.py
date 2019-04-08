
def add(q, index):
    r = 0
    while not q.empty():
        args = q.get()
        # print(f'q.qsize()={q.qsize()}')
        r = args[0] * args[1]
    print(f'{index}_QueueIsEmpty')
    # return r


if __name__ == '__main__':
    past = time.time()
    cpus = 2  # cpu_count()
    for j in range(16):
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
        logger.info(f'\tprocessing:\t\t time={ts}MS')
    print('Program_Stoped')
