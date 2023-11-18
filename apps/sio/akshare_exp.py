#
import argparse
import time
import pandas as pd
import akshare as ak

def main(args:argparse.Namespace = {}) -> None:
    print(f'### Akshare lib experiment v0.0.1')
    # get_stock_zh_index_daily_df() # 获取上证50股指日行情
    # #  获取上证50到期列表
    # get_option_cffex_sz50_list_sina_df()
    # # 列出指定到期日的所有合约
    # get_option_finance_board_df()
    # 指定某个具体合约查看日K数据
    get_option_cffex_sz50_daily_sina_df()
    # # 获取所有金融期货合约
    # get_match_main_contract()
    # # 获取上证50指数期货日K行情
    # get_futures_main_sina_hist()

def get_futures_main_sina_hist():
    '''
    获取上证50指数日K行情，如下所示：
             日期     开盘价     最高价     最低价     收盘价    成交量    持仓量  动态结算价
0    2020-01-02  3093.0  3116.8  3084.0  3097.2  27268  30691    0.0
1    2020-01-03  3107.0  3107.0  3079.0  3080.4  20460  27359    0.0
2    2020-01-06  3071.8  3096.8  3039.2  3058.4  29104  30249    0.0
3    2020-01-07  3069.0  3086.8  3062.2  3073.4  23925  26221    0.0
4    2020-01-08  3054.8  3065.6  3034.0  3046.6  24585  26519    0.0
..          ...     ...     ...     ...     ...    ...    ...    ...
481  2021-12-27  3298.0  3310.6  3282.4  3304.0  32292  54290    0.0
482  2021-12-28  3309.0  3328.0  3298.6  3320.8  38257  55803    0.0
483  2021-12-29  3328.0  3328.0  3249.6  3250.2  41054  56754    0.0
484  2021-12-30  3255.0  3293.0  3248.0  3278.2  32804  51714    0.0
485  2021-12-31  3286.2  3298.8  3275.0  3279.4  28997  50789    0.0    
    '''
    print(f'')
    futures_main_sina_hist = ak.futures_main_sina(symbol="IH0", start_date="20200101", end_date="20221231")
    print(futures_main_sina_hist)

def get_match_main_contract():
    '''
    获取所有金融期货合约
    64	IH0	cffex	上证50指数期货连续
    如下所示：
           symbol      time      open      high       low  current_price     hold  volume        amount
0   沪深300指数期货2311  15:00:00  3600.200  3603.600  3577.400       3587.800  71770.0   48298  1.732845e+08
1     5年期国债期货2312  15:15:00   102.030   102.105   101.980        102.055  98122.0   39848  4.066123e+06
2    上证50指数期货2311  15:00:00  2430.800  2433.600  2411.400       2416.600  40232.0   26470  6.402990e+07
3   中证500指数期货2311  15:00:00  5566.000  5577.000  5537.000       5561.200  62285.0   31596  1.755593e+08
4     2年期国债期货2312  15:15:00   101.004   101.034   100.974        101.008  55551.0   35698  3.605509e+06
5  中证1000指数期货2311  15:00:00  6050.400  6079.400  6025.200       6066.000  48280.0   35815  2.167454e+08    
    '''
    cffex_text = ak.match_main_contract(symbol="cffex")
    while True:
        time.sleep(3)
        futures_zh_spot_df = ak.futures_zh_spot(symbol=cffex_text, market="FF", adjust='0')
        print(futures_zh_spot_df)    


def get_stock_zh_index_daily_df():
    '''
    获取上证50股指日行情，其股票代码为：sh000016，返回结果为：
                date      open      high       low     close      volume
            0     2004-01-02   996.996  1021.568   993.892  1011.347     8064653
            1     2004-01-05  1008.279  1060.898  1008.279  1060.801  1446818000
    '''
    df = ak.stock_zh_index_daily(symbol="sh000016")
    print(df)
    df['date'] = pd.to_datetime(df['date']) # date转为时间格式
    df = df.set_index('date')
    print(f'refined df:\n{df};')

def get_option_cffex_sz50_list_sina_df():
    '''
    获取上证50到期列表，结果为：
    {'上证50指数': ['ho2312', 'ho2311', 'ho2403', 'ho2406', 'ho2409', 'ho2401']}
    '''
    df = ak.option_cffex_sz50_list_sina()
    opn_dates = df['上证50指数'] # 字符串列表
    for od in opn_dates:
        print(f'{od};')

def get_option_finance_board_df():
    '''
    列出指定到期日的所有合约
    '''
    df = ak.option_finance_board(symbol="上证50股指期权", end_month="2312")
    print(f'df: {df};')
    print(f'df[0]: {type(df.loc[1, :])}; {df.loc[1, :]};') # 取出第2行
    rec = df.loc[1, :].to_dict()
    print(f'rec: {rec};')
    for row in df.iterrows():
        rec = row[1].to_dict()
        print(f'### {type(row)}; {rec};')

def get_option_cffex_sz50_daily_sina_df():
    '''
    指定某个具体合约查看日K数据
    '''
    df = ak.option_cffex_sz50_daily_sina(symbol="ho2312P3200")
    print(f'df: {df};')
    df['date'] = pd.to_datetime(df['date']) # date转为时间格式
    df = df.set_index('date')
    print(f'new df: \n{df};')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_mode', action='store', type=int, default=1, dest='run_mode', help='run mode')
    return parser.parse_args()

if '__main__' == __name__:
    args = parse_args()
    main(args=args)