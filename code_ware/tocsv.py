import pandas as pd
import multiprocessing as mp
import pymssql as pm
import MysqlDbc as mdbc
import os,re

a = {
    'a': ['Feb 23 2018', 'Feb-23-2018', '2011/01/01', '2011-01-01', '12-03-2018'],
    'b': ['a', 'a', 'b', 'b', 'a']
}

b = pd.DataFrame(a)
b['a'] = pd.to_datetime(b['a'])
b = pd.concat([b for i in range(10)])


def compre(**k):
    if 'obj' in k:
        obj = k['obj']
    else:
        raise KeyError
    folder = r'zip/'
    if not os.path.exists(folder):
        os.mkdir(folder)
    file = f'{folder}to_csv_{mode}.{mode}'
    obj.to_csv(file, index=False, encoding='utf8', compression='bz2',mode='a')


if __name__ == '__main__':

    sql = "select * from test"
    table=re.findall(r'(?<=from ).+?(?=tabel)',sql)
    print(table)
    exit()
    cnn = mdbc.ConnectSqlserver(host='192.168.16.128', port=1433, user='sa', pwd='123', database='db')
    cnn.cursor.execute(sql)
    row = cnn.cursor.fetchmany(10)
    while row:
        print(row)
        row = cnn.cursor.fetchmany(10)
    cnn.Close()
    # print(rs)
    # p = []
    # type = ['gzip', 'bz2', 'zip', 'xz', 'txt']
    # for i in type:
    #     k = {
    #         'type': i,
    #         'obj': b
    #     }
    #     p.append(mp.Process(target=compre, kwargs=k), )
    #
    # for i in p:
    #     i.start()
    # for i in p:
    #     i.join()
    # print('Finished')
