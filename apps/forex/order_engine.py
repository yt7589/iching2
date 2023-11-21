#
from typing import Dict, Any
from apps.forex.account import Account
from apps.forex.forex_repository import ForexRepository
from apps.forex.brokers.base_broker import BaseBroker

class OrderEngine(object):
    ask_delta = 0.00005
    bid_delta = 0.00005

    def __init__(self):
        self.name = 'apps.forex.order_engine.OrderEngine'

    @staticmethod
    def processOrders(account: Account, broker: BaseBroker): # In production this should be called with every new tick, separate feed
        while True:
            tick = ForexRepository.ticks_for_order.get(block = True)
            current_price = float(tick['bids'][0]['price'])
            OrderEngine.processOrdersBase(account, broker, tick, current_price)


    @staticmethod
    def processOrdersBase(account: Account, broker: BaseBroker, tick:Dict, current_price:float) -> None:
        account.last_price = current_price
        # print(tick['timestamp'], "Price:", current_price, "Equity:", account.equity)

        while True:
            try:
                order = ForexRepository.orders_queue.get(block=False)
                # available_funds = (account.initial_capital + account.equity) * account.leverage - account.market_position / account.leverage
                # if order['Size'] < available_funds:
                #     # emulateBrokerExecution(tick, order)
                broker.execute_order(tick, order)
                if order['Status'] == 'Executed':
                    account.last_price = order['Executed Price']
                    print('Executed at ', str(account.last_price), 'current price = ', str(current_price), 'order price = ', str(order['Executed Price']))
                    if order['Side'] == 'Buy':
                        account.market_position = account.market_position + order['Size']
                        account.capital -= order['RealPay']
                        account.equity += (current_price - order['Price']) * order['Size']
                        account.list_of_orders.append(order)
                    if order['Side'] == 'Sell':
                        account.market_position = account.market_position - order['Size']
                        account.capital += order['RealPay']
                        account.equity -= (current_price - order['Price']) * order['Size']
                        account.list_of_orders.append(order)
                    account.equity_timeseries.append(account.equity)
                    account.net_capital = account.capital + account.market_position * account.last_price
                    account.net_capitals.append(account.net_capital)
                    print(f'### 账户信息：captial: {account.capital}; position: {account.market_position}; equity: {account.equity}; net_capital: {account.net_capital}; ??????')
                    print(f'\n***************************************\n\n')
                elif order['Status'] == 'Rejected':
                    ForexRepository.orders_queue.put(order)
            except:
                order = 'No order'
                break

    @staticmethod
    def processOrdersBackTesting(account: Account, broker: BaseBroker): # In production this should be called with every new tick, separate feed
        ForexRepository.order_event.clear()
        ForexRepository.order_event.wait()
        while True:
            try:
                bar = ForexRepository.next_bars_queue.get(block = True, timeout = 1)
            except:
                break
            current_price = bar['Close']
            print(f'### OrderEngine.processOrdersBackTesting bar: {bar};')
            tick = {
                'timestamp': '?????',
                'Date': 'var_date',
                'Time': 'var_time',
                'bids': [
                    {'price': bar['Close'], 'quantity': 1000000000} # 每次均能成交 - bid_delta
                ],
                'asks': [
                    {'price': bar['Close'], 'quantity': 1000000000} # + ask_delta
                ]
            } # 根据Bar生成虚拟的tick
            OrderEngine.processOrdersBase(account, broker, tick, current_price)
            ForexRepository.order_event.clear()
            ForexRepository.data_event.set()
            ForexRepository.order_event.wait()