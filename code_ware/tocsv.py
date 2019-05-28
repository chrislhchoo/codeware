"""
本程序依托py版本3.6或者以上
需安装库
    1 pymssql
    2 numpy
    3 sqlalchemy
    4 pandas
"""
import os
import pandas as pd,time
from sqlalchemy import create_engine
from datetime import datetime as dtm

if __name__ == '__main__':
    # 这里填写数据库信息
    #########################################################
    user = 'sa'  # 用户名
    pwd = 'Chris@1984'  # 密码
    ip = '192.168.16.131'  # ip
    port = 1433  # 端口
    database = 'AdventureWorks2014'  # 库名
    engine = create_engine(f'mssql+pymssql://{user}:{pwd}@{ip}:{port}/{database}')
    #########################################################
    tablename = 'Production.TransactionHistoryArchive'
    sql = f"select * from {tablename}"
    df = pd.read_sql(sql, engine)
    type = ['zip', 'bz2', 'gzip', 'xz', None]
    filename = rf'{tablename}'  # 导出的文件名
    path = r'd:\compress'  # 导出的文件路径
    past=time.time()
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
    for i in type:
        df.to_pickle(rf'{path}\{filename}.{i if i !=None else "pkl"}', compression=i)
        print(f'Compress {i if i !=None else "pkl"} cost {round((time.time()-past)*1000,2)}MS')
        past = time.time()
    # df = pd.read_pickle(rf'{path}\{filename}', compression='zip')
    # df.to_sql('test_test', con=engine, if_exists='append', index=False)
