# 用于保存信息的类，主要是各类消息队列
import queue
import threading

class ForexRepository(object):
    ticks_for_bar = queue.Queue() # 用于生成Bar
    ticks_for_trade = queue.Queue() # 用于交易策略
    ticks_for_order = queue.Queue() # 用于触发订单
    bars_queue = queue.Queue() # 用于策略模块生成订单
    next_bars_queue = queue.Queue() # 用于订单执行时取出价格
    orders_queue = queue.Queue()
    # 用于控制线程间同步
    data_event = threading.Event()
    trade_event = threading.Event()
    order_event = threading.Event()