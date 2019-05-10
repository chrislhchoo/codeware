# -*- coding: utf-8 -*-

import time
import traceback
from multiprocessing import cpu_count, Queue, Process
from queue import Empty

def handleProcess(inQue, outQue, args):
    a=0
    print('start processFun whit', inQue, outQue, args)
    while 1:
        time.sleep(0.0001)
        try:
            inData = inQue.get(block=False)
        except Empty:
            a+=1
            #print(f'进程 {args} 获取输入队列为空')
            time.sleep(0.0001)
            continue
        except:
            print('未知异常:')
            traceback.print_exc()
            continue


        if inData[0] == 'exit':
            #print(f'进程 {args} 获取退出指令，退出')
            try:
                outQue.put_nowait(['exit',0])
            except:
                traceback.print_exc()
            break
        #print(f'进程 {args} 正正处理{inData}')

        time.sleep(0.0001)

inQue,outQue = Queue(),Queue()
handler = []
cpus = cpu_count()

def writeDataProcess(inQue, handlerCount):
    start,end = 0,5000
    print('writeDataProcess', inQue)
    while 1:
        if start == end:
            for index in range(handlerCount):
                try:
                    inQue.put_nowait(['exit', 0, 0])
                except:
                    traceback.print_exc()
            break
        if inQue.qsize() > cpus * 2:
            time.sleep(0.0001)
            continue
        else:
            try:
                # print('writer data',['ops', start, start+1])
                inQue.put_nowait(['ops', start, start+1])
            except:
                traceback.print_exc()
            start += 1

def readDataProcess(outQue, handlerCount):
    # global outQue, handler
    exitCount = 0
    print('readDataProcess len(handler)',len(handler))
    while 1:
        time.sleep(0.1)
        if exitCount == handlerCount:
            print('all hander end')
            break
        try:
            outData = outQue.get(block=False)
        except Empty:
            #print(f'进程 readDataProcess 获取输入队列为空')
            time.sleep(0.0001)
            continue
        except:
            print('未知异常:')
            traceback.print_exc()
            continue
        if outData[0] == 'exit':
            print('readDataProcess outDate:', outData)
            exitCount += 1
        else:
            print(f'接收到数据：{outData}')

def initResouce():
    inQue, outQue, handler = Queue(), Queue(), []
    writer = Process(target=writeDataProcess, args=(inQue,cpus))
    writer.start()
    time.sleep(0.0001)

    for index in range(cpus):
        handler.append(Process(target=handleProcess, args=(inQue, outQue, index)))
    for handp in handler:
        handp.start()

    reader = Process(target=readDataProcess, args=(outQue, len(handler)))
    reader.start()
    time.sleep(0.0001)

    return writer,reader

def waitForEnd(writer,reader):
    while 1:
        if writer.is_alive():
            time.sleep(0.0001)
            continue
        #print('writer exit')
        if reader.is_alive():
            time.sleep(0.0001)
            continue
        #print('reader exit')
        print('all exit')
        return

def main():
    writer, reader = initResouce()
    waitForEnd(writer,reader)

if __name__ == '__main__':
    past=time.time()
    main()
    print(f'Cost {round(time.time()-past,2)}S')