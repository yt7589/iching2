# 账户详细信息

class Account(object):
    def __init__(self, account_id:str):
        self.name = 'apps.forex.account.Account'
        self.account_id = account_id
        self.initial_capital = 50000.0 # 初始资金
        self.capital = self.initial_capital # 当前资金
        self.leverage = 30 # 杠杆率
        self.market_position = 50000 # 仓位
        self.equity = 0 # 资产净值
        self.last_price = 0 # 最后一次交易价格
        self.equity_timeseries = [] # 资产净值时间序列
        self.net_capital = self.initial_capital
        self.list_of_orders = []