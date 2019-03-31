import os,pymysql

def read_data(file_path):
    x=[]
    y=[]
    f = open(file_path,'r')                             #以读方式打开文件
    for line in f.readlines():                          #依次读取每行
        line = line.strip()                             #去掉每行头尾空白
        if not len(line) or line.startswith('#'):       #判断是否是空行或注释行
            continue                                    #是的话，跳过不处理
        temp=line.split('\t')
        x.append(temp[0])
        y.append(float(temp[1]))
    f.close()                                           #关闭文件
    return x,y
class a:
    def __init__(self):
        self.x=0
if __name__=='__main__':
    #a=r'D:\flight.txt'
    #print(read_data(a))
    pass
    x=a()
    print(a.x)