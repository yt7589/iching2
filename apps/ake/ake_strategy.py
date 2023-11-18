from datetime import datetime

import akshare as ak
import backtrader as bt
import pandas as pd

class AkeStrategy(bt.Strategy):
    """
    主策略程序
    """
    params = (("maperiod", 20),
              ('printlog', False),)  # 全局设定交易策略的参数, maperiod是 MA 均值的长度

    def __init__(self):
        """
        初始化函数
        """
        self.data_close = self.datas[0].close  # 指定价格序列
        self.dt = self.datas[0].datetime
        self.max_dt = self.datas[0].datetime[-1]
        print(f'### datas: {type(self.datas[0])}; {self.datas[0]}; {self.datas[0].datetime[-1]}')
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buy_price = None
        self.buy_comm = None
        # 添加移动均线指标
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod
        )

    def next(self):
        """
        主逻辑
        """
        delta = 0.005
        span = 10
        if self.dt[0] + span + 1 > self.max_dt:
            return
        # self.log(f'收盘价, {data_close[0]}')  # 记录收盘价
        if self.order:  # 检查是否有指令等待执行,
            return
        # 检查是否持仓
        if self.broker.get_cash() >= 0:
            base_price = self.data_close[0] * (1 + delta)
            buy_sign = False
            for idx in range(span):
                if self.data_close[idx] > base_price:
                    buy_sign = True
                    break
            if buy_sign:
                self.order = self.buy()
                dt = self.datas[0].datetime.date(0)
                # print('%s, %s' % (dt.isoformat(), txt))
                print(f'{dt.isoformat()} 买入 初始现金：{self.broker.get_cash()}；初始仓位：{self.position};')
        else:
            base_price = self.data_close[0] * (1 - delta)
            sell_sign = False
            for idx in range(span):
                if self.data_close[idx] < base_price:
                    sell_sign = True
                    break
            if sell_sign:
                self.order = self.sell()
                dt = self.datas[0].datetime.date(0)
                print(f'{dt.isoformat()} 卖出 初始现金：{self.broker.get_cash()}；初始仓位：{self.position};')
        # if not self.position:  # 没有持仓
        #     # 执行买入条件判断：收盘价格上涨突破15日均线
        #     if self.data_close[0] > self.sma[0]:
        #         self.log("BUY CREATE, %.2f" % self.data_close[0])
        #         # 执行买入
        #         self.order = self.buy()
        # else:
        #     # 执行卖出条件判断：收盘价格跌破15日均线
        #     if self.data_close[0] < self.sma[0]:
        #         self.log("SELL CREATE, %.2f" % self.data_close[0])
        #         # 执行卖出
        #         self.order = self.sell()

    def log(self, txt, dt=None, do_print=False):
        """
        Logging function fot this strategy
        """
        if self.params.printlog or do_print:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        """
        记录交易执行情况
        """
        # 如果 order 为 submitted/accepted,返回空
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 如果order为buy/sell executed,报告价格结果
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f"买入:\n价格:{order.executed.price},\
                成本:{order.executed.value},\
                手续费:{order.executed.comm}"
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(
                    f"卖出:\n价格：{order.executed.price},\
                成本: {order.executed.value},\
                手续费{order.executed.comm}"
                )
            self.bar_executed = len(self)

            # 如果指令取消/交易失败, 报告结果
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("交易失败")
        self.order = None

    def notify_trade(self, trade):
        """
        记录交易收益情况
        """
        if not trade.isclosed:
            return
        self.log(f"策略收益：\n毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}")

    def stop(self):
        """
        回测结束后输出结果
        """
        self.log("(MA均线： %2d日) 期末总资金 %.2f" % (self.params.maperiod, self.broker.getvalue()), do_print=True)
