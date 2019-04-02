import time,timeit,pandas as pd,re
from datetime import datetime as dtm
class converter:
    # def __init__(self):
    #     pass
    #convert string format to date
    def str2date(self,dtstr):
        isalphabeta=re.findall(r'[a-zA-Z]+',dtstr)
        if len(isalphabeta)==0:
            partition=re.findall(r'\d+',dtstr)
            print(partition)
            if len(partition)>=2:#not pure number'2019-3-3'
                list=dtstr.split(' ')
                if len(list)>=1:
                    delimit=re.findall('[^0-9]',list[0])[0]
                if isinstance(dtstr,str):
                    if dtstr.replace(' ','')==dtstr:
                        ret = dtm.strptime(dtstr, f"%Y{delimit}%m{delimit}%d")
                    elif dtstr.replace(' ','')!=dtstr:
                        if len(partition)==6:
                            ret = dtm.strptime(dtstr, f"%Y{delimit}%m{delimit}%d %H:%M:%S")
                        elif len(partition)==5:
                            ret = dtm.strptime(dtstr, f"%Y{delimit}%m{delimit}%d %H:%M")
            elif len(partition)==1:#pure number['20190303','20190909232323','201901010101']
                if len(dtstr)==8:
                    yy=int(dtstr[:4])
                    mm=int(dtstr[4:6])
                    dd = int(dtstr[6:8])
                    #print(yy,mm,dd)
                    ret= dtm(yy,mm,dd)
                elif len(dtstr)==14:
                    yy=int(dtstr[:4])
                    mm=int(dtstr[4:6])
                    dd = int(dtstr[6:8])
                    h=int(dtstr[8:10])
                    M=int(dtstr[10:12])
                    s=int(dtstr[12:])
                    #print(yy, mm, dd,h,M,s)
                    ret=dtm(yy, mm, dd,h,M,s)
                elif len(dtstr)==12:
                    yy=int(dtstr[:4])
                    mm=int(dtstr[4:6])
                    dd = int(dtstr[6:8])
                    h=int(dtstr[8:10])
                    M=int(dtstr[10:12])
                    s=0
                    #print(yy, mm, dd,h,M,s)
                    ret=dtm(yy, mm, dd,h,M,s)
        elif len(isalphabeta)>=1:
            pass
        return ret
    # convert timestamp to datetime
    def tsp2tm(self,timestamp):
        ret=dtm.fromtimestamp(timestamp)
        #print(ret)
        return ret
    #convert timestamp to date
    def tsp2dt(self, timestamp):
        ret=self.tsp2tm(timestamp)
        ret=self.str2date(str(ret).split(' ')[0])
        return ret
    def obj2pdtsp(self,dt):
        if isinstance(dt,str):
            dt=self.str2date(dt)
        ret=pd.Timestamp(dt)
        return ret
if __name__=="__main__":
    a=converter()
    b=a.tsp2dt(1545730074)
    x='2019-1-1 3:3'
    c=a.obj2pdtsp(x)
    print(type(c))
    # print(type(x))
    print(c)
    count=100000
    t0 = 1000*timeit.timeit('start_date = datetime.datetime.strptime(a, "%Y-%m-%d")',
                            "import datetime\na='2019-9-9'", number=count)
    t0=round(t0,2)
    #print(f'{t0}')