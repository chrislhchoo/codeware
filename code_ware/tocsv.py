"""
本程序依托py版本3.6或者以上
需安装库
    1 pymssql
    2 numpy
    3 sqlalchemy
    4 pandas
"""
import os
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime as dtm

if __name__ == '__main__':
    # 这里填写数据库信息
    #########################################################
    user = 'sa'  # 用户名
    pwd = '123123'  # 密码
    ip = '192.168.16.131'  # ip
    port = 1433  # 端口
    database = 'db'  # 库名
    engine = create_engine(f'mssql+pymssql://{user}:{pwd}@{ip}:{port}/{database}')
    #########################################################
    tablename = 'test'
    sql = f"select * from {tablename}"
    df = pd.read_sql(sql, engine)
    filename = rf'{tablename}.zip'  # 导出的文件名
    path = r'd:\compress'  # 导出的文件路径
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
    df.to_pickle(rf'{path}\{filename}', compression='zip')
    df = pd.read_pickle(rf'{path}\{filename}', compression='zip')
    df={'a':[188],'b':['明天'],'c':[dtm.now()]}
    df=pd.DataFrame(df)
    print(df)
    df.to_sql('test_test', con=engine, if_exists='append', index=False)
