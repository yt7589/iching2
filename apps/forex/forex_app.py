# 外汇交易系统
import argparse
import time
import threading
import matplotlib.pyplot as plt
from apps.forex.forex_config import ForexConfig
from apps.forex.exchs.lmax_order_book_receiver import LmaxOrderBookReceiver
from apps.forex.tick_bar_aggregater import TickBarAggregater
# from apps.forex.strategies.bar_rsfb_strategy import BarRsfbStrategy
from apps.forex.trade_engine import TradeEngine
from apps.forex.account_manager import AccountManager
from apps.forex.order_engine import OrderEngine
from apps.forex.brokers.iching2_broker import Iching2Broker
from apps.forex.exchs.lmax_bar_repo import LmaxBarRepo
from apps.forex.sliding_window import SlidingWindow

def main(args:argparse.Namespace = {}) -> None:
    print(f'外汇交易系统 v0.0.2 001')
    # paper_trading(args=args)
    back_testing(args=args)
    # business_logic(args=args)

def trend_following_back_testing(args:argparse.Namespace = {}) -> None:
    '''
    趋势跟踪策略回测
    '''
    data_window_small = SlidingWindow(5)
    data_window_large = SlidingWindow(20)

def back_testing(args:argparse.Namespace = {}) -> None:
    '''
    基于历史数据的回测平台
    '''
    start_time = time.perf_counter()
    incoming_price_thread = threading.Thread(target = LmaxBarRepo.connect)
    account = AccountManager.get_account_by_id('a001')
    trading_thread = threading.Thread(target = TradeEngine.execute, args=(account, TradeEngine.RM_BACK_TESTING))
    broker = Iching2Broker()
    ordering_thread = threading.Thread(target = OrderEngine.processOrdersBackTesting, args=(account, broker))
    incoming_price_thread.start()
    trading_thread.start()
    ordering_thread.start()
    while True:
        if incoming_price_thread.is_alive():
            time.sleep(1)
        else:
            end_time = time.perf_counter()
            print(f'Backtest complete in {round(end_time - start_time, 0)} second(s).')
            plt.plot(account.equity_timeseries)
            plt.show()
            break

def paper_trading(args:argparse.Namespace = {}) -> None:
    '''
    基于真实行情数据的模拟实盘测试
    '''
    print(f'模拟实盘测试')
    url = 'wss://public-data-api.london-demo.lmax.com/v1/web-socket'
    subscription_msg = '{"type": "SUBSCRIBE","channels": [{"name": "ORDER_BOOK","instruments": ["eur-usd"]}]}'
    data_receiver_thread = threading.Thread(target = LmaxOrderBookReceiver.connect, args = (url, subscription_msg))
    incoming_price_thread = threading.Thread(target = TickBarAggregater.generate_bar_from_tick, args = (ForexConfig.bar_resolution,))
    account = AccountManager.get_account_by_id('a001')
    trading_thread = threading.Thread(target = TradeEngine.execute, args=(account, TradeEngine.RM_PAPER_TRADING))
    broker = Iching2Broker()
    ordering_thread = threading.Thread(target = OrderEngine.processOrders, args=(account, broker))
    data_receiver_thread.start()
    incoming_price_thread.start()
    trading_thread.start()
    ordering_thread.start()




def business_logic(args:argparse.Namespace = {}) -> None:
    from typing import List
    from datetime import datetime
    bars_rfn = 'apps/forex/datasets/lmax_eru_usd_1_m.txt'
    is_first = True
    recs = []
    CNT = 10
    num = 0
    with open(bars_rfn, 'r', encoding='utf-8') as fd:
        for row in fd:
            if is_first:
                is_first = False
                continue # 忽略第一行
            row = row.strip()
            ### ['1/27/2015', '13:29:00', '1.12942', '1.12950', '1.12942', '1.12949', '200', '150', '639', '3', '2', '8'];
            arrs0 = row.split(',')
            dt = datetime.strptime(f'{arrs0[0]} {arrs0[1]}', "%m/%d/%Y %H:%M:%S")
            rec = {
                'Datetime': datetime.strftime(dt, '%Y-%m-%d %H:%M:%S'),	
                'Open': float(arrs0[2]), 'High': float(arrs0[3]), 'Low': float(arrs0[4]), 'Close': float(arrs0[5]),
                'Direction': 0,
                'Quantity': 0,
                'Position': 0,
                'Capital': 0.0,
                'Borrow': 0.0,
                'Pay': 0.0,
                'Interest': 0.0,
                'Profit': 0.0,
                'PnL': 0.0,
                'Net': 0.0,
                'Red_line': 0.0
            }
            recs.append(rec)
            num += 1
            if num >= CNT:
                break
    for rec in recs:
        print(rec)
    recs[0]['Capital'] = 100000.0
    if recs[0]['Close'] > recs[0]['Open']:
        recs[0]['Direction'] = -1
    elif recs[0]['Close'] > recs[0]['Open']:
        recs[0]['Direction'] = 1
    do_stepi(recs=recs, step=1)
    print(f'### 1. {recs[1]};\n*****************')
    do_stepi(recs=recs, step=2)
    print(f'### 2 {recs[2]};')
    

def do_stepi(recs, step:int) -> None:
    leverage = 30
    fund_ratio = 0.0006
    # 处理上一个时间节点的交易
    #
    if recs[step]['Close'] > recs[step]['Open']:
        recs[step]['Direction'] = -1
    elif recs[step]['Close'] < recs[step]['Open']:
        recs[step]['Direction'] = 1
    # 当前金额乘以90%除以当前收盘价得到可购买数量
    if 1 == recs[step - 1]['Direction']: # 买：涉及借款问题
        print(f'借款买')
        quantity = min(int((recs[step-1]['Capital']*0.9)/recs[step-1]['Close']), 10000)
        if quantity <= 0:
            print(f'    余额不足，无法执行买入操作')
            recs[step]['Quantity'] = 0
            recs[step]['Position'] = recs[step-1]['Position']
            recs[step]['Capital'] = recs[step-1]['Capital']
            recs[step]['Borrow'] = recs[step-1]['Borrow']
            recs[step]['Pay'] = recs[step-1]['Pay']
            recs[step]['Interest'] = recs[step-1]['Interest']
            recs[step]['Profit'] = 0.0
            recs[step]['Net'] = recs[step-1]['Net']
            recs[step]['Red_line'] = recs[step-1]['Red_line']
            recs[step]['PnL'] = recs[step-1]['PnL'] + recs[step]['Profit']
            return
        recs[step-1]['Quantity'] = quantity
        total_amount = quantity * (recs[step - 1]['Close']+0.00001*10)
        a_part = total_amount / (leverage + 1)
        recs[step]['Position'] = recs[step-1]['Position'] + recs[step-1]['Direction']*recs[step-1]['Quantity']
        recs[step]['Pay'] = a_part
        recs[step]['Borrow'] = total_amount - a_part
        recs[step]['Interest'] = recs[step]['Borrow'] * fund_ratio
        recs[step]['Capital'] = recs[step-1]['Capital'] - recs[step]['Pay'] - recs[step]['Interest']
        recs[step]['Profit'] = (recs[step]['Close'] - recs[step-1]['Close'])*recs[step-1]['Direction']*recs[step-1]['Quantity']
        recs[step]['Red_line'] = recs[step-1]['Quantity'] * recs[step]['Close'] * 1.05
        recs[step]['Net'] = recs[step]['Capital'] + recs[step]['Position']*recs[step]['Close'] - recs[step]['Borrow']
        recs[step]['PnL'] = recs[step-1]['PnL'] + recs[step]['Profit']
    elif -1 == recs[step - 1]['Direction']:
        print(f'卖出')
        if recs[step-1]['Position'] <= 0:
            print(f'    没有仓位，不能进行卖出操作')
            recs[step]['Quantity'] = 0
            recs[step]['Position'] = recs[step-1]['Position']
            recs[step]['Capital'] = recs[step-1]['Capital']
            recs[step]['Borrow'] = recs[step-1]['Borrow']
            recs[step]['Pay'] = recs[step-1]['Pay']
            recs[step]['Interest'] = recs[step-1]['Interest']
            recs[step]['Profit'] = 0.0
            recs[step]['Net'] = recs[step-1]['Net']
            recs[step]['Red_line'] = recs[step-1]['Red_line']
            recs[step]['PnL'] = recs[step-1]['PnL'] + recs[step]['Profit']
            return
    return

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_mode', action='store', type=int, default=1, dest='run_mode', help='run mode')
    return parser.parse_args()

if '__main__' == __name__:
    args = parse_args()
    main(args=args)