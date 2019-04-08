import time,timeit,pandas as pd,re
from datetime import datetime as dtm
class timeformatconverter:
    def str2date(self,dtstr):
        abc=re.findall(r'[a-zA-Z]+',dtstr)
        if len(abc)==0:
            partition=re.findall(r'\d+',dtstr)
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
        elif len(abc)==1:
            partition = re.findall(r'\d+', dtstr)
            temp=[]
            for i,j in enumerate(abc):
                if len(j)==3:
                    month = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
                    for m,n in enumerate(month):
                        if n==j.upper():
                            j=m+1
                            mm = j
                            break
            for i in partition:
                if len(i)==4:
                    yy = int(i)
                elif len(i)==2:
                    dd=int(i)
        ret=dtm(yy,mm,dd)
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
    #print(f'{t0}')