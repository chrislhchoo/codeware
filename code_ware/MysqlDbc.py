'''
Create by Chris on 20180426
v 1.0
使用范围和方法:
    1 Dql方法用于执行sql查询语句以及执行存储过程,但返回结果不包含字段名
    2 ColumnNameDql方法和Dql方法一样,但包含字段名
    3 Dml用于执行update和insert语句
v 1.1 by Chris on 20180427
    1 添加Postgresql驱动
v 1.2 by Chris on 20190428
    1 添加定义关闭连接,类继承后不需要再重写查询方法
    2 添加MSSQL驱动
    3 拆出close方法,调用后需要手动关闭连接,避免频繁连接和关闭数据库连接
v 1.3 by Chris on 20180510
    1 mysql类修复bug,没有断开连接重复查询得到的都是重复结果
v 1.4 by Chris on 20181817
    1 添加sqlite驱动
调用方法:
    db_cur = ConnectMysql(host='192.168.0.104', user='sa', pwd='123', database='db',port=3306)
    sql='select * from Test'
    for i in db_cur.ColumnNameDql(sql):
        print(i)
'''
try:
    import pymysql
except:
    print('导入Mysql驱动失败')
try:
    import psycopg2
    import psycopg2.extras
except:
    print('导入Postgresql驱动失败')
try:
    import pymssql
except:
    print('导入Mssql驱动失败')
try:
    import sqlite3
except:
    print('导入sqLite驱动失败')
import re


class ConnectMysql():  # Mysql驱动类
    def __init__(self, **mps):  # host,user,pwd,database):
        self.host = mps['host']  # '192.168.199.192'
        self.user = mps['user']  # 'sa'
        self.pwd = mps['password']  # '123'
        self.database = mps['database']  # 'db'
        self.port = mps['port']  # 'db'
        self.db = ''
        self.cursor = self.Connector(self.host, self.user, self.pwd, self.database, self.port)

    def Connector(self, host, user, pwd, database, port):
        self.db = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=pwd,
            db=database,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        return self.db.cursor()

    def Close(self):
        try:
            self.db.close()
        except:
            print('关闭数据库连接失败')

    def Dql(self, sql):  # 执行sql查询语句以及执行存储过程
        print(f'被执行的SQL语句：{sql}')
        cursor = self.cursor
        head = sql.split(' ')[0]
        if head == 'call':
            head = '调用存储过程'
        elif head == 'select':
            head = '查询'
        elif head == 'set':
            head = '设置'
        else:
            return 1
        try:
            cursor.execute(sql)
            results_temp = cursor.fetchall()
            return results_temp
        except:
            print(head + '语句执行错误')
            return {'': ''}

    def ColumnNameDql(self, sql):
        cursor = self.cursor
        head = sql.split(' ')[0]
        if head == 'call':
            head = '调用存储过程'
        elif head == 'select':
            head = '查询'
        else:
            return 1
        try:
            self.db.commit()
            cursor.execute(sql)
            results_temp = cursor.fetchall()
            return results_temp
        except Exception as e:
            print(head + '语句执行错误')
            print('-------------------')
            print(f'Exception:{e}')
            print('-------------------')

    def Dml(self, sql):
        cursor = self.cursor
        head = sql.split(' ')[0]
        if head == 'update':
            head = '更新'
        elif head == 'insert':
            head = '插入'
        elif head == 'delete':
            head = '删除'
        elif head == 'truncate':
            head = '清空'
        elif head == 'create':
            head = '创建'
        elif head == 'select':
            head = '锁表更新'
        else:
            return 1
        try:
            cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(head + '语句执行错误')
            print(e)
            return 1
        return 0

    def RollBack(self):
        self.db.rollback()


class ConnectPostgresql(ConnectMysql):  # Postgresql驱动类
    def Connector(self, host, user, pwd, database, port):
        print('连接方法')
        self.db = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=pwd,
            database=database,
            cursor_factory=psycopg2.extras.RealDictCursor  # DictCursor
        )
        cursors = self.db.cursor()
        return cursors

    def Close(self):
        try:
            self.cursor.close()
        except:
            print('关闭数据库连接失败')


class ConnectSqlserver(ConnectMysql):  # Mssql驱动类
    def __init__(self, host, user, pwd, database, port):
        self.cursor=self.Connector(host, user, pwd, database, port)
    def Connector(self, host, user, pwd, database, port):
        self.db = pymssql.connect(
            host=host,
            port=port,
            user=user,
            password=pwd,
            database=database,
            as_dict=True
        )
        cursors = self.db.cursor()
        return cursors

    def Close(self):
        try:
            self.cursor.close()
        except:
            print('关闭数据库连接失败')

    def ColumnNameDql(self, sql):
        cursor = self.cursor
        head = sql.split(' ')[0]
        if head == 'call':
            head = '调用存储过程'
        elif head == 'select':
            head = '查询'
        try:
            cursor.execute(sql)
            row = cursor.fetchall()
            temp = {}
            rs = []
            for i in row:
                for k, v in i.items():
                    temp[k] = str(v).encode('latin-1').decode('gbk')
                rs.append(temp)
                temp = {}
            return rs
        except Exception as e:
            print(head + '语句执行错误')
            print('-------------------')
            print(f'Exception:{e}')
            print('-------------------')
            self.Close()


class ConnectSqlite(ConnectMysql):  # Sqlite驱动类
    def __init__(self, dbPath):
        self.db = sqlite3.connect(dbPath)

    # def Connector(self, dbPath):

    def Close(self):
        try:
            self.db.close()
        except:
            print('关闭数据库连接失败')

    def Dql(self, sql):  # 执行sql查询语句以及执行存储过程
        curson = self.db.execute(sql)
        head = sql.split(' ')[0]
        if head == 'call':
            head = '调用存储过程'
        elif head == 'select':
            head = '查询'
        else:
            return 1
        try:
            self.db.commit()
            results_temp = curson.fetchall()
            return results_temp
        except:
            print(head + '语句执行错误')
            return {'': ''}

    def Dml(self, sql):
        curson = self.db.execute(sql)
        head = sql.split(' ')[0]
        if head == 'update':
            head = '更新'
        elif head == 'insert':
            head = '插入'
        elif head == 'delete':
            head = '删除'
        elif head == 'create':
            head = '创建'
        elif head == 'truncate':
            head = '清空'
        else:
            return 1
        try:
            self.db.commit()
        except:
            print(head + '语句执行错误')
            return 1
        return 0

    def ColumnNameDql(self, sql):
        cursor = self.cursor
        head = sql.split(' ')[0]
        if head == 'call':
            head = '调用存储过程'
        elif head == 'select':
            head = '查询'
        else:
            return 1
        try:
            cursor.execute(sql)
            row = cursor.fetchall()
            temp = {}
            rs = []
            for i in row:
                for k, v in i.items():
                    temp[k] = str(v).encode('latin-1').decode('gbk')
                rs.append(temp)
                temp = {}
            return rs
        except Exception as e:
            print(head + '语句执行错误')
            print('-------------------')
            print(f'Exception:{e}')
            print('-------------------')
            self.Close()


if __name__ == '__main__':
    cnn = ConnectMysql(host='localhost', port=3306, user='root', password='123', database='parkdb')
    sql = "select * from log limit 100"
    rs = cnn.Dql(sql)
    print(rs[10]['date'])
    # print(rs)
