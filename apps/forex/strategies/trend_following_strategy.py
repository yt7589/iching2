# 趋势跟踪策略
import csv
from typing import Dict
from datetime import datetime
from apps.forex.strategies.base_strategy import BaseStrategy
from apps.forex.sliding_window import SlidingWindow
from apps.forex.account import Account
from apps.forex.forex_repository import ForexRepository

class TrendFollowingStrategy(BaseStrategy):
    data_window_small = SlidingWindow(5)
    data_window_large = SlidingWindow(20)

    def __init__(self):
        self.name = 'apps.forex.strategies.trend_following_strategy.TrendFollowingStrategy'

    def execute(self, account:Account, bar: Dict) -> int:
        ####################################
        #     trade logic starts here      #
        ####################################
        open = bar['Open']
        close = bar['Close']
        TrendFollowingStrategy.data_window_small.add(close)
        TrendFollowingStrategy.data_window_large.add(close)
        ma_small = TrendFollowingStrategy.moving_average(TrendFollowingStrategy.data_window_small.data)
        ma_large = TrendFollowingStrategy.moving_average(TrendFollowingStrategy.data_window_large.data)
        if close < ma_small and ma_small < ma_large and account.market_position >= 0:
            order = {}
            order['Type'] = 'Market'
            order['Price'] = close
            order['Side'] = 'Sell'
            if account.market_position == 0:
                order['Size'] = 10000
            else:
                order['Size'] = 20000
            # orders_stream.put(order)
            ForexRepository.orders_queue.put(order)

        if close > ma_small and ma_small > ma_large and account.market_position <= 0:
            order = {}
            order['Type'] = 'Market'
            order['Price'] = close
            order['Side'] = 'Buy'
            if account.market_position == 0:
                order['Size'] = 10000
            else:
                order['Size'] = 20000
            # orders_stream.put(order)
            ForexRepository.orders_queue.put(order)

    @staticmethod
    def moving_average(data):
	    return sum(data) / len(data)







    @staticmethod
    def prepare_data():
        '''
        准备澳大利元与美元（audusd）货币对日K数据
        '''
        with open('apps/forex/datasets/trend_following/audusd_daily.csv', 'w', encoding='utf-8') as dest_fd:
            with open('apps/forex/datasets/trend_following/lmax_aud_usd_1m.txt', 'r', encoding='utf-8') as src_fd:
                TrendFollowingStrategy._prepare_data(src_fd=src_fd, dest_fd=dest_fd)
    def _prepare_data(dest_fd, src_fd):
        csvFile = csv.DictReader(src_fd)
        all_data = list(csvFile)
        dest_fd.write(('Date,Time,Open,High,Low,Close\n'))
        timestamp = SlidingWindow(2)
        bar = {'Open': 0, 'High': 0, 'Low': 0, 'Close': 0}

        for sample in all_data:
            open = float(sample[' <Open>'])
            high = float(sample[' <High>'])
            low = float(sample[' <Low>'])
            close = float(sample[' <Close>'])
            ts = datetime.strptime(sample['<Date>'] + 'T' + sample[' <Time>'] + 'Z', "%m/%d/%YT%H:%M:%SZ")
            timestamp.add(ts)

            if timestamp.previous() != 0:
                if (timestamp.last().date() != timestamp.previous().date() and str(timestamp.last().time()) != '00:00:00') or (str(timestamp.previous().time()) == '00:00:00'):
                    if bar['Open'] != 0:
                        dest_fd.write(','.join(map(str,[*bar.values()])) + "\n")
                    bar = {'Date': timestamp.last().date(), 'Time': timestamp.last().time(), 'Open': open, 'High': high, 'Low': low, 'Close': close}

            bar['High'] = max([bar['High'], high])
            bar['Low'] = min([bar['Low'], low])
            bar['Close'] = close
            bar['Time'] = timestamp.last().time()


if '__main__' == __name__:
    TrendFollowingStrategy.prepare_data()