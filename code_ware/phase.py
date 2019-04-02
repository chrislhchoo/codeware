# -*- coding: utf-8 -*-
"""
Analytics
*
* Author: 
* Date:   2017-10-10
*
"""


import numpy as np

from optparse import OptionParser  # For command line inputs.
import pandas as pd

from sqlalchemy import create_engine
import esgx_get_data_Chris as gd

from datetime import datetime as dtm, date, timedelta
from pandas.tseries.offsets import BDay
import timeit,platform,subprocess,cx_Oracle,sys,os,time,Utils,pd_to_db,re
from multiprocessing import Pool, cpu_count
from functools import partial
from multiprocessing import Queue,Process,Manager
from sys import version_info
if version_info < (3,0):
    from urllib import quote_plus
else:
    from urllib.parse import quote_plus


esgx_db_params = ""
debug_code = False
save_to_db = True
concurrent_periods = 2

def set_db_connect():
    node = platform.node()
    if node == "":
		pass
    elif node == '' or node == '':
		pass
    else:
		pass

    db_conn = cx_Oracle.connect(
        db_user + "/" + db_password + "@" + db_host + ".statestr.com:" + db_port + "/" + db_service_name)
    db_conn.autocommit = True
    return db_conn

def date_in_range(items, searchitem):
    """
    :param items: list of dates
    :param searchitem: search date
    :return: check where search date falls in range, and returns beginning date of that range
    """
    # if isinstance(searchitem, str):
    #     searchitem =  dtm.strptime(searchitem,'%Y-%m-%d')
    searchitem=pd.DataFrame([searchitem])
    searchitem=pd.to_datetime(searchitem[0])
    if isinstance(items[0],dtm):
        items=np.array([i.date() for i in items])
    # print('#########################')
    # print(type(searchitem[0]),type(items),type(items[0]))
    # print('#########################')
    if len(items) > 1:
        # Check if searchitem is within range
        idx = [s <= searchitem[0].date() < t for s, t in zip(items, items[1:])]
        return items[np.ix_(idx)]
    else:
        return np.empty((0,0))


def find_portfolio_date_to_use(analysis_date, port_dates):
    """
    :param analysis_date: date for which Analytics being calculated
    :param port_dates: list of portfolio update date
    :return: returns portfolio date to use for analysis date
    """
    port_date_to_use = date_in_range(port_dates, analysis_date)
    """ if analysis date is out of range for portfolio dates, assign first or last date accordingly """
    if port_date_to_use.size == 0:
        #print(f'analysis_date={analysis_date}\t{type(analysis_date)}\tport_dates[0]={port_dates[0]}\t{type(port_dates[0])}')
        # if type(port_dates[0]) is dtm:
        #     analysis_date=dtm.strptime(analysis_date.strftime('%Y%m%d'), '%Y%m%d')
        # print(
        #     f'analysis_date={analysis_date}\t{type(analysis_date)}\tport_dates[0]={port_dates[0]}\t{type(port_dates[0])}')
        #print(type(port_dates))
        if type(port_dates[0]) is dtm:
            port_dates=np.array([i.date() for i in port_dates])
        if analysis_date < port_dates[0]:
            port_date_to_use = port_dates[0]
        elif port_dates[-1] <= analysis_date:
            port_date_to_use = port_dates[-1]
    else:
        port_date_to_use = port_date_to_use[0]

    return port_date_to_use


def build_portfolio_analysis_data(analysis_date, next_day, port_date_subset, port_cfg, sec_data_wide, port_data, ccy_data):
    """
    :param analysis_date: date for which valuation of security is being done
    :param next_day: next business day of analysis date
    :param port_date_subset: list of portfolio dates within selected period
    :param port_cfg: portfolio configuration details
    :param sec_data_wide: security data for selected period
    :param port_data: portfolio data for selected period
    :param ccy_data: currency data for selected period
    :return: value and return of securities in portfolio on analysis date
    """

    """ find which portfolio update date to use for analysis date """
    #print(type(port_date_subset[0]))
    #port_date_subset=port_date_subset.values.astype('datetime64[s]').tolist()
    ts = [(i - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's') for i in port_date_subset]
    ts=[dtm.utcfromtimestamp(i) for i in ts]
    #print(type(ts[1]))
    port_date_subset=np.array(ts)

    port_date_to_use = find_portfolio_date_to_use(analysis_date, port_date_subset)
    #print('analysis_date & port_date_to_use', analysis_date, port_date_to_use)

    """ get portfolio details on selected portfolio date """
    portfolio_data = port_data[port_data['PORTFOLIO_UPDATE_DATE'] == port_date_to_use].dropna(axis=0, subset=['POSITION'], how='all')
    portfolio_data = portfolio_data.reset_index().set_index('SECURITY_CLIENT_ID')
    if isinstance(sec_data_wide['EFFECTIVE_DATE'] [0],str):
        analysis_date_str=str(analysis_date)
    analysis_data = sec_data_wide[sec_data_wide['EFFECTIVE_DATE'] == analysis_date_str]
    analysis_data = analysis_data.reset_index().set_index('SECURITY_CLIENT_ID')
    """ find index for which portfolio ids, price data is available """
    idx = analysis_data.index.isin(portfolio_data.index)
    # Drop rows if all columns are Nan
    analysis_data = analysis_data[idx].dropna(axis=0, how='all')

    portfolio_data = portfolio_data[portfolio_data.index.isin(analysis_data.index)].dropna(axis=0, how='all')
    #print("Portfoilio shape", portfolio_data.shape)

    """ Return calculation will be based of previous day's portfolio. So we will calculate next business day return on
    today's portfolio and save in table. For metric calculation we have to use data on analysis day
    as well as previous business day"""
    next_day_return = sec_data_wide[sec_data_wide['EFFECTIVE_DATE'] == next_day]

    next_day_return = next_day_return[['TOTAL_RETURN_USD_LOG', 'SECURITY_CLIENT_ID']].reset_index().set_index('SECURITY_CLIENT_ID') #'return_fx_log'
    idx = next_day_return.index.isin(analysis_data.index)
    next_day_return = next_day_return[idx].dropna(axis=0, how='all')

    """ Portfolio value and return calculation """

    analysis_data['USD_VALUE_ON_PORT_DATE'] = portfolio_data['POSITION'] * portfolio_data['CLOSING_PRICE_USD']
    if analysis_date-port_date_to_use == timedelta(days=0):
        analysis_data['BASE_VALUE_ON_ANALYSIS_DATE'] = analysis_data['USD_VALUE_ON_PORT_DATE']
    else:
        analysis_data['BASE_VALUE_ON_ANALYSIS_DATE'] = analysis_data['USD_VALUE_ON_PORT_DATE'] * np.exp(analysis_data['TOTAL_RETURN_USD_LOG_CUMUL'] - portfolio_data['TOTAL_RETURN_USD_LOG_CUMUL'])

    """ As we are using previous day for return calculation, first day of portfolio period is start_date-1"""
    if analysis_date == port_cfg['PORT_BEGIN_DATE']:
        analysis_data['BASE_CURRENCY_TR_NEXT_DAY'] = np.zeros((analysis_data.shape[0],1))
    else:
        analysis_data['BASE_CURRENCY_TR_NEXT_DAY'] = np.exp(next_day_return['TOTAL_RETURN_USD_LOG'])-1

    if port_cfg['BASE_CURRENCY_ID'] != 0:   #USD
        currency_x_rate = ccy_data[ccy_data['EFFECTIVE_DATE'] == analysis_date]['EXCHANGE_RATE'].values # * analysis_data.shape[0]
        currency_return = ccy_data[ccy_data['EFFECTIVE_DATE'] == next_day]['TOTAL_RETURN_LOG'].values # * next_day_return.shape[0]
        currency_usd_return_log_cumsum_ana = ccy_data[ccy_data['EFFECTIVE_DATE'] == analysis_date]['TOTAL_RETURN_CUMULATIVE'].values
        currency_usd_return_log_cumsum_port = ccy_data[ccy_data['EFFECTIVE_DATE'] == port_date_to_use]['TOTAL_RETURN_CUMULATIVE'].values
        print("Currency data ", analysis_date.strftime('%Y-%m-%d'), currency_x_rate, currency_return, currency_usd_return_log_cumsum_port)

        analysis_data['BASE_VALUE_ON_ANALYSIS_DATE'] = analysis_data['USD_VALUE_ON_PORT_DATE'] * currency_x_rate \
                                                       * np.exp(analysis_data['TOTAL_RETURN_USD_LOG_CUMUL'] - portfolio_data['TOTAL_RETURN_USD_LOG_CUMUL']
                                                                + currency_usd_return_log_cumsum_ana - currency_usd_return_log_cumsum_port)
        analysis_data['BASE_CURRENCY_TR_NEXT_DAY'] = np.exp(next_day_return['TOTAL_RETURN_USD_LOG'] + currency_return)-1

    analysis_data['SECURITY_WEIGHT'] = (analysis_data['BASE_VALUE_ON_ANALYSIS_DATE']/analysis_data['BASE_VALUE_ON_ANALYSIS_DATE'].abs().sum()).as_matrix()
    return analysis_data


def calculate_daily_port_values(port_date_index, run_dates, port_cfg, dt_index):
    """
    :param port_date_index: list of portfolio update dates
    :param run_dates: list of selected frequency dates within portfolio run period
    :param port_cfg: portfolio configuration information
    :param dt_index: index of one of the periods to run from run_dates
    :return: total number of days calculated
    """
    return_total_days = 0
    """ finalize period to run and get related data for that period """
    portfolio_id = port_cfg['PORTFOLIO_ID']
    portfolio_table = port_cfg['PORTFOLIO_TABLE']
    base_currency_id = port_cfg['BASE_CURRENCY_ID']

    start_date = port_cfg['START_DATE'] if dt_index == 0 else run_dates[dt_index-concurrent_periods].date()
    end_date = port_cfg['END_DATE'] if dt_index+concurrent_periods >= run_dates.size else run_dates[dt_index].date()-timedelta(days=1)
    print("Portfolio-", portfolio_id)
    print("Running analysis for period ", dt_index, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    daily_dates = pd.bdate_range(start_date, end_date, freq='B')
    start_date = (start_date - BDay(1)).date()
    end_date = (end_date + BDay(1)).date()
    port_start_date = find_portfolio_date_to_use(start_date, port_date_index)
    port_end_date = find_portfolio_date_to_use(end_date, port_date_index)
    ccy_start_dt = start_date
    ccy_end_date = end_date
    if port_start_date < start_date:
        ccy_start_dt = port_start_date
    elif port_end_date > end_date:
        ccy_end_date = port_end_date

    dbengine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % quote_plus(esgx_db_params))
    db_connect = set_db_connect()
    #port_data contains portfolio data input portfolio in given range
    filename = f'Chris_get_portfolio_holdings_data_{portfolio_id}_{port_start_date}_{port_end_date}_{portfolio_table}.csv'
    if os.path.isfile(filename):
        #print(f'{filename} exists file')
        port_data = pd.read_csv(filename, encoding='utf8')
    else:
        #print(f'no such file {filename}')
        gd_time_port, port_data = gd.get_portfolio_data(db_connect, portfolio_id, portfolio_table, port_start_date,
                                                        port_end_date,filename)


    #security_data_wide contains data from the security table mapped to the input portfolio
    filename = f'Chris_get_security_data_daily_{portfolio_id}_{port_start_date}_{port_end_date}_{portfolio_table}.csv'

    if os.path.isfile(filename):
        #print(f'{filename} exists file')
        security_data_wide = pd.read_csv(filename, encoding='utf8')
    else:
        #print(f'no such file {filename}')
        gd_time_sec, security_data_wide = gd.get_security_data_daily(db_connect, portfolio_id, portfolio_table,
                                                                     start_date,end_date,port_start_date,port_end_date,filename)

    #ccy_data contains base currency data
    filename = f"Chris_get_currency_data_{ccy_start_dt.strftime('%Y-%m-%d')}_{ccy_end_date.strftime('%Y-%m-%d')}_{base_currency_id}.csv"
    if os.path.isfile(filename):
        #print(f'{filename} exists file')
        ccy_data = pd.read_csv(filename, encoding='utf8')
    else:
        #print(f'no such file {filename}')
        gd_time_ccy, ccy_data = gd.get_currency_data(db_connect, ccy_start_dt.strftime('%Y-%m-%d'),
                                                     ccy_end_date.strftime('%Y-%m-%d'),
                                                     base_currency_id,filename)

    port_data['PORTFOLIO_UPDATE_DATE'] = pd.to_datetime(port_data['PORTFOLIO_UPDATE_DATE'])

    port_date_subset = np.sort(port_data['PORTFOLIO_UPDATE_DATE'].unique())

    #print("Time to get portfolio and security data", gd_time_port, gd_time_sec)
    print("Memory size(GB) of security and portfolio data",
        (security_data_wide.values.nbytes + security_data_wide.index.nbytes + security_data_wide.columns.nbytes)/1000000000.0,
           (port_data.values.nbytes + port_data.index.nbytes + port_data.columns.nbytes)/1000000000.0)
    port_data = port_data.sort_values(['PORTFOLIO_UPDATE_DATE', 'SECURITY_CLIENT_ID'], axis=0)
    security_data_wide = security_data_wide.sort_values(['EFFECTIVE_DATE','SECURITY_ID'], axis=0)

    """ Loop through each analysis date in period and generate security value data """
    pqueue,log_queue,ret_queue= Queue(),Queue(),Queue()
    mgr = Manager()
    ns= mgr.list()
    for dt_current_index in range(daily_dates.size):
        pqueue.put(daily_dates[dt_current_index].date())
        # if pqueue.qsize()>=10:
        #     break
    cpus=8
    p,portDT, Shape0, Shape1 = [], [], [],[]
    past=time.time()
    print('---------------------------------Start to Parallel')
    for i in range(cpus):
        p.append(Process(target=paralleled,args=(i,port_date_subset,port_cfg,portfolio_id,pqueue,log_queue,security_data_wide,port_data,ccy_data,ret_queue)))
    #p.append(Process(target=data_write_in,args=(pqueue,ret_queue)))
    print(f'多进程数量为{len(p)}')
    for i in p:
        i.start()
    for i in p:
        i.join()
    print('Join_Finished')
    data_write_in(pqueue,ret_queue)
    while not log_queue.empty():
        log=log_queue.get(block=True, timeout=0.1)
        portDT.append(log[0])
        Shape0.append(log[1])
        Shape1.append(log[2])
    dic={
        'portDT':portDT,
        'Shape0':Shape0,
        'Shape1':Shape1
    }
    print('Dict_Ready')
    df = pd.DataFrame(dic)
    print('Dataframe_Ready')
    df.to_csv('ResultLogResearch.csv', mode='a', encoding='utf8')
    print(f'paralleled_run_for {round(time.time()-past,2)}S')

def data_write_in(pqueue,ret_queue):
    c = Utils.ora_connector(pool=0)
    a = pd_to_db.df_to_db(c)
    temp = []
    while not pqueue.empty():
        while not ret_queue.empty():
            temp.append(ret_queue.get())
        try:
            result = pd.concat(temp)
        except Exception as e:
            print('合并集合错误')
            print(len(result))
            print(e)
            sys.exit()
        a.insert_many('ESGX_SECURITY_VALUE_RESEARCH',result)
    print('上一批写入结束')
    while not ret_queue.empty():
        temp.append(ret_queue.get())
    print('加载最后队列成功')
    result = pd.concat(temp)
    print(f'合并队列成功，队列长度{result.shape[0]}')
    a.insert_many('ESGX_SECURITY_VALUE_RESEARCH',result)
    print('最终批写入结束')
    print(f'进程2_2结束')


def paralleled(num,port_date_subset, port_cfg, portfolio_id, pqueue,log_queue,security_data_wide,port_data,ccy_data,ret_queue):
    while not pqueue.empty():
        print(f'进程{num}提取数据')
        analysis_date = pqueue.get(block=True, timeout=0.01)
        next_day = (analysis_date + BDay(1)).date()
        #try:
        tic = timeit.default_timer()
        """ Build portfolio data needed for analysis date to run """
        #print(dtm.now().strftime('%Y-%m-%d.%H.%M.%S.%f') + ': Processing date -', analysis_date)
        # security_data_wide=data.security_data_wide
        # port_data = data.port_data
        # ccy_data = data.ccy_data
        analysis_data = build_portfolio_analysis_data(analysis_date, next_day, port_date_subset, port_cfg, security_data_wide, port_data, ccy_data)
        print(f'进程{num}生成中间结果')
        """ Dataframe to save security_level data """
        security_value_df = analysis_data.copy()
        #save the simple return
        #security_value_df['BASE_CURRENCY_TR_NEXT_DAY'] = np.log(security_value_df['BASE_CURRENCY_TR_NEXT_DAY']+1)
        security_value_df['PORTFOLIO_ID'] = [portfolio_id] * security_value_df.shape[0]
        security_value_df['CLIENT_ID'] = [port_cfg['CLIENT_ID']] * security_value_df.shape[0]
        security_value_df['EFFECTIVE_DATE'] = [analysis_date] * security_value_df.shape[0]
        security_value_df['CREATE_DATE'] = [dtm.now()] * security_value_df.shape[0]
        security_value_df.reset_index(inplace=True)
        security_value_df.drop('SECURITY_CLIENT_ID',1, inplace=True)
        # except:
        #     print('Failed to drop column "SECURITY_CLIENT_ID"')
        security_value_df.drop(['index', 'USD_VALUE_ON_PORT_DATE', 'CLOSING_PRICE_USD',
                                'TOTAL_RETURN_USD_LOG', 'TOTAL_RETURN_USD_LOG_CUMUL'], 1, inplace=True)
        security_value_df.rename(columns={'BASE_VALUE_ON_ANALYSIS_DATE': 'BASE_CURRENCY_VALUE'},
                                 inplace=True)

        """ Save data to database """
        if save_to_db:
            #print('Appending_Data_To_CSV')
            try:
                    #security_value_df.to_sql('ESGX_SECURITY_VALUE_RESEARCH', db_connect, if_exists='append', index=False) #, schema=port_cfg['client_schema'])
                #c = Utils.ora_connector(pool=0)
                #a = pd_to_db.df_to_db(c)
                if security_value_df.shape[0]>=1:
                    #a.insert_many('ESGX_SECURITY_VALUE_RESEARCH',security_value_df)
                    log_queue.put([str(analysis_date), security_value_df.shape[0], security_value_df.shape[1]],timeout=0.01)
                    ret_queue.put(security_value_df,timeout=0.01)
                    #security_value_df.to_csv('Result_ESGX_SECURITY_VALUE.csv', mode='a',encoding='utf8')  # , schema=port_cfg['client_schema'])
            except:
                raise
        toc = timeit.default_timer()
        done_msg = dtm.now().strftime('%Y-%m-%d.%H.%M.%S.%f') + ": " + analysis_date.strftime('%Y-%m-%d') + \
                   " Completed in " + str(round(toc-tic,1)) + " s" + '\n'
        print(f'进程{num}结束')
        #print(f'队列长度为{pqueue.qsize()}')
        #return_total_days += 1
        #print(done_msg)
        # except Exception as e:
        #     print('tslib')
        #     if isinstance(analysis_date, pd.tslib.Timestamp) or isinstance(analysis_date, date):
        #         analysis_date = analysis_date.strftime('%Y-%m-%d')
        #     print("Exception-", analysis_date, e)
    #return return_total_days
    print("Queue_is_empty")

def calculate_security_value(client_id, portfolio_id, start_date, end_date, daily_update):
    results = []
    calc_time = 0
    esg_db = create_engine("mssql+pyodbc:///?odbc_connect=%s" % esgx_db_params)
    params={}
    if portfolio_id == -1:#not applicable
        if client_id == -1:#not applicable
            # no portfolio is assigned, so get all of the portfolios for that client
            stmt = ""
        else:
            params['client_id']=client_id
            stmt = ""
    else:#applicable
        # find just the portfolio that the user selected in the command line
        params['portfolio_id'] = portfolio_id
        stmt = "SELECT * FROM ESGX_PORTFOLIO WHERE PORTFOLIO_ID =:portfolio_id "
    db_connect = set_db_connect()
    cur=db_connect.cursor()
    ports = pd.read_sql(stmt, db_connect, params=params)
    #ports = esg_db.execute(stmt)
    for i,port_cfg in ports.iterrows():
        # try:
        """ get data for selected portfolio """
        port_config = dict(port_cfg)
        portfolio_id = port_config['PORTFOLIO_ID']
        port_config['PORTFOLIO_TABLE'] = 'ESGX_PORTFOLIO_HOLDINGS'
        port_config['PORT_BEGIN_DATE'] = port_config['START_DATE']
        #port_config['client_schema'] = client_cfg['client_schema']
        if start_date != '':
            #port_config['START_DATE'] =port_config['START_DATE'].date()
            #original Chris on 20190328
            if re.findall(r'[a-zA-Z]',start_date)[0]:
                port_config['START_DATE'] = dtm.strptime(start_date, '%d-%b-%Y').date()
            else:
                port_config['START_DATE'] = dtm.strptime(start_date, '%Y-%m-%d %H:%M:%S').date()
            if re.findall(r'[a-zA-Z]',end_date)[0]:
                port_config['END_DATE'] = dtm.strptime(end_date, '%d-%b-%Y').date()
            else:
                port_config['END_DATE'] = dtm.strptime(end_date, '%Y-%m-%d %H:%M:%S').date()
        if daily_update:
            params={'portfolio_id':portfolio_id}
            sql="SELECT max(EFFECTIVE_DATE) LAST_DATE FROM ESGX_SECURITY_VALUE WHERE PORTFOLIO_ID = :portfolio_id"
            #convert last_date_run to date Chris on  20190328
            last_date_run = pd.read_sql(sql, db_connect,params=params)['LAST_DATE'][0].date()
            sql="SELECT max(EFFECTIVE_DATE) LAST_DATE FROM ESGX_SECURITY"
            last_date_sec = pd.read_sql(sql, db_connect)['LAST_DATE'][0].date()
            if start_date == '' or port_config['START_DATE'] >= last_date_run:
                port_config['START_DATE'] = last_date_run
            if end_date == '' or port_config['END_DATE'] >= last_date_sec:
                port_config['END_DATE'] = last_date_sec
            if save_to_db:
                #print(port_config)
                tablename="ESGX_SECURITY_VALUE_research"
                params={
                    'portfolio_id':portfolio_id,
                    'START_DATE':port_config['START_DATE'],
                    'END_DATE':port_config['END_DATE']
                }
                sql=f"DELETE FROM {tablename} WHERE PORTFOLIO_ID = :portfolio_id AND EFFECTIVE_DATE between :START_DATE and :END_DATE"
                result = cur.execute(sql,params)
        print("Portfolio-", port_config['PORTFOLIO_NAME'], port_config['BASE_CURRENCY_ID'])
        #port_update_dates has portfolio update dates
        filename=f'Chris_get_portfolio_dates_{portfolio_id}.csv'
        if os.path.isfile(filename):
            #print(f'{filename} exists file')
            port_update_dates = pd.read_csv(filename, encoding='utf8')
        else:
            #print(f'no such file {filename}')
            gd_time_port, port_update_dates = gd.get_portfolio_dates(db_connect, portfolio_id,
                                                                     'ESGX_PORTFOLIO_HOLDINGS', filename)

        # get a list of all portfolio update dates for the portfolio, in order
        port_date_index = pd.DatetimeIndex(np.sort(port_update_dates['PORTFOLIO_UPDATE_DATE'].unique())).date
        # list of date chunks for parallelization (currently lists every month within portfolio range)
        if daily_update:
            run_dates = pd.DatetimeIndex([port_config['END_DATE']])
        else:
            run_dates = pd.bdate_range(port_config['START_DATE'], port_config['END_DATE'], freq='M')
            if run_dates.size <= 0:
                run_dates = pd.DatetimeIndex([port_config['END_DATE']])

        # func defines the function that will run to calculate daily portfolio values
        func = partial(calculate_daily_port_values, port_date_index, run_dates, port_config)
        if debug_code:
            func(0)
        else:
            # number of required processes is the same as the number of date chunks we're using
            required_processes = run_dates.size

            # workers = minimum of (number of cpus available, number of date chunks we're using)
            # pool = the pool of processers used
            """ No of workers/processes to set """
            try:
                print("cpu_count", cpu_count())
                workers = int(round(cpu_count()*0.80)) or 1
            except NotImplementedError:
                workers = 1

            workers = min(workers, required_processes)
            print('Processes - ', workers)
            pool = Pool(processes=workers)
            """ Launch available processes and pass index to calculate_daily_port_values """
            """ concurrent_periods is set to 2 which will allow us to run 2 months at a time """
            for i in range(0, run_dates.size, concurrent_periods):
                tic = timeit.default_timer()
                calculate_daily_port_values(port_date_index, run_dates, port_config, i)
                toc = timeit.default_timer()
                calc_time = toc - tic
                print('Calculation for ' + str(sum(results)) + ' days completed in -', calc_time)
            # try:
            #     tic = timeit.default_timer()
            #     calculate_daily_port_values(port_date_index, run_dates, port_config,0)
            #     results = pool.map(func, range(0, run_dates.size, concurrent_periods))
            #     toc = timeit.default_timer()
            #     calc_time = toc-tic
            #     print('Calculation for ' + str(sum(results)) + ' days completed in -', calc_time)
            # except WindowsError:
            #     pass
    # except Exception as e:
    #     print("Exception-", e)
    #     print("Error at line number {0} in function calculate_security_value".format(e.__traceback__.tb_lineno))
    esg_db.dispose()
    print("Finished")
    return sum(results), calc_time

if __name__ == '__main__':
    past=time.time()
    """ Create the command line input options: """
    parser = OptionParser()
    parser.add_option("-s", "--start_date", dest="start_date", help="Start date for analysis.", metavar="STARTDT", default='')
    parser.add_option("-e", "--end_date", dest="end_date", help="End date for analysis.", metavar="ENDDT", default='')
    parser.add_option("-c", "--client_id", dest="client_id", help="Client Id", metavar="CLIENTID", default=-1)
    parser.add_option("-p", "--portfolio_id", dest="portfolio_id", help="Portfolio id", metavar="PORT", default=-1)
    parser.add_option("-d", "--daily_update", dest="daily_update", help="Run Daily Update", metavar="DU", default=1)

    (options, args) = parser.parse_args()  # Capture the command line input.
    #20190328 Chris
    #options.portfolio_id = 1000050#1000100
    options.start_date = "25-FEB-2019"
    options.end_date = "27-MAR-2019"
    options.client_id = 100000
    #####################
    calculate_security_value(options.client_id, options.portfolio_id, options.start_date, options.end_date, int(options.daily_update))
    print(f'总时间为{round(time.time()-past,2)}S')
