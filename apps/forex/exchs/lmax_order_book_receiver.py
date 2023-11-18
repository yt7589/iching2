# 接收LMAX的OrderBook数据
import json
import websocket
from apps.forex.forex_repository import ForexRepository

class LmaxOrderBookReceiver(object):
    def __init__(self):
        self.name = 'apps.forex.lmax_order_book_receiver.LmaxOrderBookReceiver'

    @staticmethod
    def connect(url:str, subscription_msg:str):
        ws = websocket.create_connection(url)
        ws.send(subscription_msg)
        ws.recv() # 忽略第一个响应消息
        while True:
            msg = ws.recv()
            try:
                tick = json.loads(msg)
                if 'instrument_id' in tick.keys():
                    bid = float(tick['bids'][0]['price'])
                    ask = float(tick['asks'][0]['price'])
                    if ask - bid < 0.001:
                        ForexRepository.ticks_for_bar.put(tick)
            except:
                print(f'!!!!! Exception Msg: {msg};')