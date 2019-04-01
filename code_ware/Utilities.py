import time,datetime,timeit
class converter:
    def __init__(self):
        import time,datetime
    def str2date(self,dtstr):
        ret = datetime.datetime.strptime(dtstr, "%Y-%m-%d")
        return ret
    def tsp2tm(self,timestamp):
        ret=datetime.datetime.fromtimestamp(timestamp)
        print(ret)
        return ret
    def tsp2dt(self, timestamp):
        ret=self.tsp2tm(timestamp)
        ret=self.str2date(str(ret).split(' ')[0])
        return ret
if __name__=="__main__":
    a=converter()
    print(a.tsp2dt(1545730073))
    count=100000
    t0 = 1000*timeit.timeit('start_date = datetime.datetime.strptime(a, "%Y-%m-%d")',
                            "import datetime\na='2019-9-9'", number=count)
    t1 = 1000*timeit.timeit("math.exp(3)",'import math',number=count)
    t2= 1000*timeit.timeit("pow(math.e,3)",'import math',number=count)
    t0,t1,t2=round(t0,2),round(t1,2),round(t2,2)
    print(f'{t0}\t{t1}\t{t2}')

    #a+=1