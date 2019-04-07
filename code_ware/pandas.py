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
	pd.to_csv([filename],encoding='utf8',Index=False)
	#将数据写入CSV文件
	pd.read_csv([filename],encoding='utf8')
	#将数据从CSV文件中读取
	
    except :
        s=sys.exc_info()
        print(f'error {s[1]}:at line {s[2].tb_lineno}')
############################
	convert	pandas._libs.tslibs.timestamps.Timestamp into use date:
		t = pd.tslib.Timestamp('2016-03-03 00:00:00')
		t.date()

	convert str into date
		datetime.strptime(x, '%m/%d/%Y')
	convert datetime to date
		t.date()
############################
	convert dataframe string to datetime64
		port_data['PORTFOLIO_UPDATE_DATE'] = pd.to_datetime(port_data['PORTFOLIO_UPDATE_DATE'])
############################
	print title or column name
		if 'SECURITY_CLIENT_ID' in analysis_data.columns.values: print('发现目标_1')
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
