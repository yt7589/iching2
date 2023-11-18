#
import argparse
from datetime import datetime

import akshare as ak
import backtrader as bt
import matplotlib.pyplot as plt
import pandas as pd
from apps.ake.bt01_strategy import Bt01Strategy

class AkeApp(object):
    def __init__(self):
        self.name = 'apps.ake.ake_app.AkeApp'
        plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置画图时的中文显示
        plt.rcParams["axes.unicode_minus"] = False  # 设置画图时的负号显示

    def startup(self, args:argparse.Namespace = {}) -> None:
        print(f'Akshare交易环境启动')
        start_cash=1000000
        stake=5000
        start_date = datetime(2009, 4, 3)  # 回测开始时间
        end_date = datetime(2023, 10, 26)  # 回测结束时间
        # 利用 AKShare 获取股票的后复权数据，这里只获取前 6 列
        stock_hfq_df = ak.stock_zh_a_hist(symbol="600001", adjust="hfq").iloc[:, :6]
        # 处理字段命名，以符合 Backtrader 的要求
        stock_hfq_df.columns = [
            'date',
            'open',
            'close',
            'high',
            'low',
            'volume',
        ]
        # 把 date 作为日期索引，以符合 Backtrader 的要求
        stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])
        cerebro = bt.Cerebro()  # 初始化回测系统
        data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date)  # 加载数据
        cerebro.adddata(data)  # 将数据传入回测系统
        cerebro.addstrategy(Bt01Strategy)  # 将交易策略加载到回测系统中
        # cerebro.addsizer(bt.sizers.FixedSize, stake=stake)  # 设置买入数量
        cerebro.broker.setcash(start_cash)  # 设置初始资本为 100000
        cerebro.broker.setcommission(commission=0.002)  # 设置交易手续费为 0.2%
        cerebro.run()  # 运行回测系统
        port_value = cerebro.broker.getvalue()  # 获取回测结束后的总资金
        pnl = port_value - start_cash  # 盈亏统计
        print(f"初始资金: {start_cash}\n回测期间：{start_date.strftime('%Y%m%d')}:{end_date.strftime('%Y%m%d')}")
        print(f"总资金: {round(port_value, 2)}")
        print(f"净收益: {round(pnl, 2)}")






































    def run_backtest(self):
        # 利用 AKShare 获取股票的后复权数据，这里只获取前 6 列
        stock_hfq_df = ak.stock_zh_a_hist(symbol="600001", adjust="hfq").iloc[:, :6]
        # 处理字段命名，以符合 Backtrader 的要求
        stock_hfq_df.columns = [
            'date',
            'open',
            'close',
            'high',
            'low',
            'volume',
        ]
        # 把 date 作为日期索引，以符合 Backtrader 的要求
        stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])
        start_cash=1000000
        stake=5000
        cerebro = bt.Cerebro()  # 初始化回测系统
        start_date = datetime(2009, 4, 3)  # 回测开始时间
        end_date = datetime(2023, 10, 26)  # 回测结束时间
        data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date)  # 加载数据
        cerebro.adddata(data)  # 将数据传入回测系统
        cerebro.addstrategy(AkeStrategy)  # 将交易策略加载到回测系统中
        start_cash = 1000000
        cerebro.addsizer(bt.sizers.FixedSize, stake=stake)  # 设置买入数量
        cerebro.broker.setcash(start_cash)  # 设置初始资本为 100000
        cerebro.broker.setcommission(commission=0.002)  # 设置交易手续费为 0.2%
        cerebro.run()  # 运行回测系统

        port_value = cerebro.broker.getvalue()  # 获取回测结束后的总资金
        pnl = port_value - start_cash  # 盈亏统计

        print(f"初始资金: {start_cash}\n回测期间：{start_date.strftime('%Y%m%d')}:{end_date.strftime('%Y%m%d')}")
        print(f"总资金: {round(port_value, 2)}")
        print(f"净收益: {round(pnl, 2)}")

        cerebro.plot(style='candlestick')  # 画图


    def finetune(self):
        code="600001"
        start_cash=1000000
        stake=100
        commission_fee=0.002
        start_date = datetime(2009, 4, 3)  # 回测开始时间
        end_date = datetime(2023, 10, 26)  # 回测结束时间
        cerebro = bt.Cerebro()  # 创建主控制器
        cerebro.optstrategy(AkeStrategy, maperiod=range(3, 31))  # 导入策略参数寻优
        # 利用 AKShare 获取股票的后复权数据，这里只获取前 6 列
        stock_hfq_df = ak.stock_zh_a_hist(symbol=code, adjust="hfq").iloc[:, :6]
        # 处理字段命名，以符合 Backtrader 的要求
        stock_hfq_df.columns = [
            'date',
            'open',
            'close',
            'high',
            'low',
            'volume',
        ]
        # 把 date 作为日期索引，以符合 Backtrader 的要求
        stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])
        data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date)  # 规范化数据格式
        cerebro.adddata(data)  # 将数据加载至回测系统
        cerebro.broker.setcash(start_cash)  # broker设置资金
        cerebro.broker.setcommission(commission=commission_fee)  # broker手续费
        cerebro.addsizer(bt.sizers.FixedSize, stake=stake)  # 设置买入数量
        print("期初总资金: %.2f" % cerebro.broker.getvalue())
        cerebro.run(maxcpus=1)  # 用单核 CPU 做优化
        print("期末总资金: %.2f" % cerebro.broker.getvalue())

    