from matplotlib import pyplot as plt
from data_import import read_data as rd
import datetime,time
import numpy as np

# 计算两个日期相差天数，自定义函数名，和两个日期的变量名。
def Caltime(date1, date2):
    # %Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
    date1 = time.strptime(date1, "%Y%m%d")
    date2 = time.strptime(date2, "%Y%m%d")
    # 根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    # 返回两个变量相差的值，就是相差天数
    return date2-date1
if __name__=='__main__':
    a=r'flight_detail.txt'  #文件路径
    x=[]                    #初始化坐标
    data=rd(a)#np.array(rd(a))
    ori_x=data[0]
    y=data[1]
    base=ori_x[0]
    for i in ori_x:
        add=str(Caltime(base,i)).split(',')[0].split(' ')[0]
        if add.isdigit():
            x.append(int(add)+1)
        else:
            x.append(1)
    plt.plot(x,y)
    avg=round((y[-1]-y[0])/x[-1],2)
    print(f'{avg}Kilometer Per Day')
    plt.show()