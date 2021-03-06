Shell
    ############################
    Get current Date,Time
        Date
            date +"%Y-%m-%d"
        Time
            date +"%Y-%m-%d %T"
    ############################
    Read certain line or lines from a file
        pwd=`sed -n '1,3p' hfr.txt`
    ############################
    Validation if directory is exists:
        if [ -d "${SQLPLUS_SPOOL_DIR}" ]
    Validation if  variable is exists:
        if [ -z "$1" ]
    ############################
    Make a directory:
        mkdir "${SQLPLUS_SPOOL_DIR}"
    ############################
    Execute script,if right write to file 1,if not write to file 2
        exec 1> $STDOUT_FILE 2> $STDERR_FILE
    ############################
    Resign a variable named MMDD,equals to right/left 4 charector
        typeset -R4 MMDD=$YYYYMMDD
        typeset -L4 MMDD=$YYYYMMDD
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################
    ############################

Python
    ############################
    pd.fillna(Num)
    Replace all NaN elements with Nums.
    #将空值填充为某数字
    ############################
    pd.bdate_range#
    #从开始日期到结束日期，列出工作日
    ############################
    pd.bdate_range.size
    #日期长度
    ############################
    pd.shape
    #第一位是行数，第二位是列
    ############################
    pd.dataframe.iloc[i]
    #将dataframe第i行转换成类似于字典类型
    mydict = [{'a': 1, 'b': 2, 'c': 3, 'd': 4},
            {'a': 100, 'b': 200, 'c': 300, 'd': 400},
            {'a': 1000, 'b': 2000, 'c': 3000, 'd': 4000 }]
    df = pd.DataFrame(mydict)
    df.iloc[0]
    a    1
    b    2
    c    3
    d    4
    ############################
    pd.to_csv([filename],encoding='utf8',index=False)
    #将数据写入CSV文件
    pd.read_csv([filename],encoding='utf8')
    #将数据从CSV文件中读取

    except :
        s=sys.exc_info()
        print(f'error {s[1]}:at line {s[2].tb_lineno}')
    ############################
    convert	pandas._libs.tslibs.timestamps.Timestamp into use date:
    #将TimeStamp转换成Date
        t = pd.tslib.Timestamp('2016-03-03 00:00:00')
        t.date()
    #将TimeStamp转换成Datetime
        a=dtm.now()
        p=pd.Timestamp(a)
        print(p,type(p))
        p=pd.Timestamp.to_pydatetime(p)
        print(p, type(p))
    convert str into date
        datetime.strptime(x, '%m/%d/%Y')
    convert datetime to date
        t.date()
    ############################
    convert dataframe string to datetime64
    #将String转换成DATE
        port_data['PORTFOLIO_UPDATE_DATE'] = pd.to_datetime(port_data['PORTFOLIO_UPDATE_DATE'])
    ############################
    #打印字段名
    print title or column name
        if 'SECURITY_CLIENT_ID' in analysis_data.columns.values:
        print(analysis_data.columns.values)
    ############################

    multiprocessing share object
        from multiprocessing import Manager
        mgr = Manager()
        ns = mgr.Namespace()
        ns.df = my_dataframe
    ############################
    convert datetime64 to datetime and back
        import pandas as pd,numpy as np
        from datetime import datetime
        a='2019-01-01'
        b=pd.Timestamp(a)
        c=np.datetime64(a)
        d = np.datetime64(b)
        f=c.astype(datetime)
    ############################
    week of the year
        from datetime import datetime
        dt=datetime.now()#.date()
        print(dt.isocalendar())
        returns (2019, 17, 1)
    ############################
    PD Equal SQL:
        ---------------
        SELECT total_bill, tip, smoker, time FROM tips LIMIT 5;

        tips[['total_bill', 'tip', 'smoker', 'time']].head(5)
        ---------------
        SELECT * FROM tips WHERE time = 'Dinner'
        LIMIT 5;

        tips[tips['time'] == 'Dinner'].head(5)
        ---------------
        SELECT * FROM tips WHERE time = 'Dinner' AND tip > 5.00;

        tips[(tips['time'] == 'Dinner') & (tips['tip'] > 5.00)]
        ---------------
        SELECT * FROM tips WHERE size >= 5 OR total_bill > 45;

        tips[(tips['size'] >= 5) | (tips['total_bill'] > 45)]
        ---------------
        SELECT sex, count(*) FROM tips GROUP BY sex;

        tips.groupby('sex').size()
        ---------------
        SELECT day, AVG(tip), COUNT(*) FROM tips GROUP BY day;

        tips.groupby('day').agg({'tip': np.mean, 'day': np.size})
        ---------------
        SELECT smoker, day, COUNT(*), AVG(tip) FROM tips GROUP BY smoker, day;

        tips.groupby(['smoker', 'day']).agg({'tip': [np.size, np.mean]})
        ---------------
        SELECT * FROM df1 INNER JOIN df2 ON df1.key = df2.key;

        pd.merge(df1, df2, on='key')
        ---------------
        SELECT * FROM df1 LEFT OUTER JOIN df2 ON df1.key = df2.key;

        pd.merge(df1, df2, on='key', how='left')
        ---------------
        SELECT * FROM df1 RIGHT OUTER JOIN df2 ON df1.key = df2.key;

        pd.merge(df1, df2, on='key', how='right')
        ---------------
        UPDATE tips	SET tip = tip*2 WHERE tip < 2;

        tips.loc[tips['tip'] < 2, 'tip'] *= 2
        b['a'] = b['a']+'1'
        ---------------
        DELETE FROM tips WHERE tip > 9;

        tips = tips.loc[tips['tip'] <= 9]
    ############################
    Change one column of dataframe to datetime
    #修改dataframe一个列的值
        b['a'] = pd.to_datetime(b['a'])
    ############################
    #timeit timing module
        x=timeit.timeit('a=dtm(2019,1,1)\npd.Timestamp("20190101")',
                        'import pandas as pd\nfrom datetime import datetime as dtm',
                        number=100000)
        print(x)
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
Oracle
    Procedure return a result set
        Define(See script as)
            C:\Chris\SentToHuyi\HFR_DATA_VALIDATION\PA_RESEARCH.SSGS_HFX_validation_V1.2
        Execute
            variable rc refcursor;
            exec PA_RESEARCH.SSGS_HFX_VALIDATION.PROC_HFX_DATA_VALIDATE(:rc);
            print rc
        Bash(See script as)
            C:\Chris\SentToHuyi\HFR_DATA_VALIDATION\ssa_hfr_data_validation_v1.3
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
