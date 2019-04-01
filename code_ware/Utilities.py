import time,timeit
from datetime import datetime as dtm
class converter:
    def __init__(self):
        pass
    def str2date(self,dtstr):
        ret = dtm.strptime(dtstr, "%Y-%m-%d")
        return ret
    def tsp2tm(self,timestamp):
        ret=dtm.fromtimestamp(timestamp)
        print(ret)
        return ret
    def tsp2dt(self, timestamp):
        ret=self.tsp2tm(timestamp)
        ret=self.str2date(str(ret).split(' ')[0])
        return ret
if __name__=="__main__":
    a=converter()
    print(a.tsp2dt(1545730074))
    count=100000
    t0 = 1000*timeit.timeit('start_date = datetime.datetime.strptime(a, "%Y-%m-%d")',
                            "import datetime\na='2019-9-9'", number=count)
    t0=round(t0,2)
    print(f'{t0}')

    #a+=1