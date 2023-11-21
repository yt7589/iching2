# 
from apps.forex.account import Account
from apps.forex.forex_repository import ForexRepository
from apps.forex.strategies.base_strategy import BaseStrategy
from apps.forex.strategies.bar_rsfb_strategy import BarRsfbStrategy
from apps.forex.strategies.trend_following_strategy import TrendFollowingStrategy

class TradeEngine(object):
    RM_PAPER_TRADING = 1
    RM_BACK_TESTING = 2
    def __init__(self):
        self.name = 'apps.forex.trade_engine.TradeEngine'

    @staticmethod
    def execute(account:Account, run_mode:int, strategy:BaseStrategy = BarRsfbStrategy()) -> None:
        # strategy = BarRsfbStrategy()
        # strategy = TrendFollowingStrategy()
        print(f'### 启动TradeEngine...')
        ForexRepository.trade_event.clear()
        ForexRepository.trade_event.wait()
        while True:
            try:
                if TradeEngine.RM_PAPER_TRADING == run_mode:
                    tick = ForexRepository.ticks_for_trade.get()
                    bar = ForexRepository.bars_queue.get(block=False)
                else:
                    bar = ForexRepository.bars_queue.get(block=False, timeout=1)
                rst = strategy.execute(account=account, bar=bar)
                print(f'### 策略执行结果：{rst}; {type(strategy)};')
                if rst == -1:
                    print(f'！！！ 因为没有开仓不能卖产！！！！！！！！！！\n*****************************\n\n')
                elif rst == -2:
                    print(f'！！！ 因为没有资金不能买！！！！！！！！！！！！\n********************************\n\n')
                if rst == 0:
                    account.equity_timeseries.append(account.equity)
                    account.net_capital = account.capital + account.market_position * bar['Close']
                    account.net_capitals.append(account.net_capital)
                if TradeEngine.RM_BACK_TESTING == run_mode:
                    # ForexRepository.bars_queue.put(bar)
                    ForexRepository.trade_event.clear()
                    ForexRepository.order_event.set()
                    ForexRepository.trade_event.wait()
                else:
                    print(f'### 模拟实盘模式')
                    ForexRepository.ticks_for_order.put(tick)
            except:
                print(f'### TradeEngine.execute Exception!')