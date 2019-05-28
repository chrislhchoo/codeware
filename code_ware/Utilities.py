import time, timeit, pandas as pd, re
from datetime import datetime as dtm
import random, math
import heapq
import numpy as np


class timeformatconverter:
    def str2date(self, dtstr):
        abc = re.findall(r'[a-zA-Z]+', dtstr)
        if len(abc) == 0:
            partition = re.findall(r'\d+', dtstr)
            if len(partition) >= 2:  # not pure number'2019-3-3'
                list = dtstr.split(' ')
                if len(list) >= 1:
                    delimit = re.findall('[^0-9]', list[0])[0]
                if isinstance(dtstr, str):
                    if dtstr.replace(' ', '') == dtstr:
                        ret = dtm.strptime(dtstr, f"%Y{delimit}%m{delimit}%d")
                    elif dtstr.replace(' ', '') != dtstr:
                        if len(partition) == 6:
                            ret = dtm.strptime(dtstr, f"%Y{delimit}%m{delimit}%d %H:%M:%S")
                        elif len(partition) == 5:
                            ret = dtm.strptime(dtstr, f"%Y{delimit}%m{delimit}%d %H:%M")
            elif len(partition) == 1:  # pure number['20190303','20190909232323','201901010101']
                if len(dtstr) == 8:
                    yy = int(dtstr[:4])
                    mm = int(dtstr[4:6])
                    dd = int(dtstr[6:8])
                    # print(yy,mm,dd)
                    ret = dtm(yy, mm, dd)
                elif len(dtstr) == 14:
                    yy = int(dtstr[:4])
                    mm = int(dtstr[4:6])
                    dd = int(dtstr[6:8])
                    h = int(dtstr[8:10])
                    M = int(dtstr[10:12])
                    s = int(dtstr[12:])
                    # print(yy, mm, dd,h,M,s)
                    ret = dtm(yy, mm, dd, h, M, s)
                elif len(dtstr) == 12:
                    yy = int(dtstr[:4])
                    mm = int(dtstr[4:6])
                    dd = int(dtstr[6:8])
                    h = int(dtstr[8:10])
                    M = int(dtstr[10:12])
                    s = 0
                    # print(yy, mm, dd,h,M,s)
                    ret = dtm(yy, mm, dd, h, M, s)
        elif len(abc) == 1:
            partition = re.findall(r'\d+', dtstr)
            temp = []
            for i, j in enumerate(abc):
                if len(j) == 3:
                    month = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
                    for m, n in enumerate(month):
                        if n == j.upper():
                            j = m + 1
                            mm = j
                            break
            for ptt in partition:
                if len(ptt) == 4:
                    yy = int(i)
                elif len(ptt) == 2:
                    dd = int(ptt)
        ret = dtm(yy, mm, dd)
        return ret

    # convert timestamp to datetime
    def tsp2tm(self, timestamp):
        ret = dtm.fromtimestamp(timestamp)
        # print(ret)
        return ret

    # convert timestamp to date
    def tsp2dt(self, timestamp):
        ret = self.tsp2tm(timestamp)
        ret = self.str2date(str(ret).split(' ')[0])
        return ret

    def obj2pdtsp(self, dt):
        if isinstance(dt, str):
            dt = self.str2date(dt)
        ret = pd.Timestamp(dt)
        return ret


def Equilateral_triangle(x, y, r):
    '''
    x,y是等边三角形重心坐标
    r是三角形重心到点的距离
    theta随机生成
    '''
    theta = random.random()
    ret = []
    for i in range(3):
        x_append = r * math.cos(theta + 2 * i * math.pi / 3) - x
        y_append = r * math.sin(theta + 2 * i * math.pi / 3) - y
        ret.append([x_append, y_append])
    return ret


def listDerivation(inputList):
    '''
    Derivate the list
    :param inputList:
    :return: a derivated list
    '''
    derivation = []
    for index, value in enumerate(inputList):
        if index == 0:
            lastvalue = value
        else:
            derivation.append(value - lastvalue)
            lastvalue = value
    return derivation


def listlargestK(k, inputList):
    '''
    return the most largest K value's index
    :param k:
    :param inputList:
    :return:
    '''
    maxlist = []
    for maxtime in range(k):
        tempindex = inputList.index(max(inputList))
        maxlist.append(tempindex)
        inputList[tempindex] = -1
    return maxlist


def oneDimensionKmeans(inputList, **kwargs):
    # the function must pass cluster parameter,it should be an integer and bigger than 2
    if 'cluster' in kwargs:
        if isinstance(kwargs['cluster'], int):
            k = kwargs['cluster']
            if k <= 1:
                print('cluster must bigger than 2')
                raise ValueError
            elif k >= len(inputList) + 1:
                print('cluster must smaller than length of the list')
                raise ValueError
        else:
            print('parameter cluster must an integer and bigger than 2')
            raise TypeError
    else:
        raise KeyError
    if not isinstance(inputList, list):
        try:
            inputList = list(inputList)
        except Exception as e:
            print(e)
            raise TypeError

    input = list(set(inputList))  # distinct the input list
    input.sort()  # sort the input list
    derivation = listDerivation(input)  # Deriving this one dimension list
    dividpoint = k - 1  # define the divide point

    index_list = listlargestK(dividpoint, derivation)  # take the largest k-1 derivation
    index_list.sort()
    ret_list = []
    for i in range(0, index_list.__len__())[::-1]:
        ret_list.append(input[index_list[i] + 1:])
        input = input[:index_list[i] + 1]
    ret_list.append(input)
    return ret_list


def standardDeviation(inputlist):
    arr_std = np.std(inputlist, ddof=1)
    return arr_std


if __name__ == "__main__":
    a = (0.1, 0.2, 0.3, 4, 5, 6, 7, 8, 16, 19, 21, 33, 37, 32, 55, 60, 61, 91, 99, 101, 103, 105)
    a = list(a)
    clust=20
    for cls in range (clust):
        if cls>=2:
            print('#####################################')
            print(f'clust={cls}')
            print(f'standardDeviation(a)={round(standardDeviation(a),3)}')
            groups=oneDimensionKmeans(a, cluster=cls)
            print(groups)
            sd=0
            for i,j in enumerate(groups):
                std=np.nan_to_num(round(standardDeviation(j),3))
                print(f'standardDeviation({i})={std}')
                sd+=std
            print(f'Total std={sd}')
            print('#####################################')
