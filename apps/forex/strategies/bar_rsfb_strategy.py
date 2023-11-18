#
from typing import Dict
from apps.forex.account import Account
from apps.forex.forex_repository import ForexRepository
from apps.forex.strategies.base_strategy import BaseStrategy

class BarRsfbStrategy(BaseStrategy):
    '''
    根据一个Bar形态，上涨时卖出，下跌时买入
    '''
    def __init__(self):
        self.name = 'apps.forex.bar_rsfb_strategy.BarRsfbStrategy'

    def execute(self, account:Account, bar: Dict) -> int:
        ####################################
        #     trade logic starts here      #
        ####################################
        print(f'交易策略看到的行情：{bar}; ?????')
        open = bar['Open']
        close = bar['Close']
        rst = 0
        print(f'    交易策略看到的行情：1 position: {account.market_position}; capital: {account.capital};')
        if close > open:
            print(f'    交易策略看到的行情：2')
            if account.market_position <= 0:
                return -1
            order = {}
            order['Type'] = 'Market'
            order['Price'] = close
            order['Side'] = 'Sell'
            order['Size'] = account.market_position # 将所有持仓全部卖出
            print(f'    交易策略看到的行情：3')
            ForexRepository.orders_queue.put(order)
            print(f'    交易策略看到的行情：4')
            print(f'订单：{order};')
            print(f'    交易策略看到的行情：5')
            rst = 1
        elif close < open:
            print(f'    交易策略看到的行情：6')
            if account.capital <= 0:
                return -2
            order = {}
            order['Type'] = 'Market'
            order['Price'] = close
            order['Side'] = 'Buy'
            print(f'    交易策略看到的行情：7')
            # if account.market_position == 0:
            #     order['Size'] = 10000
            # else:
            #     order['Size'] = 20000
            print(f'    交易策略看到的行情：8')
            order['Size'] = int(account.capital / close * 0.9)
            ForexRepository.orders_queue.put(order)
            print(f'    交易策略看到的行情：9')
            print(f'订单：{order};')
            rst = 2
        else:
            rst = -3
        ####################################
        #       trade logic ends here      #
        ####################################
        return rst
        