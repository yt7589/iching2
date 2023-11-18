#
from datetime import datetime
from apps.forex.forex_repository import ForexRepository

class TickBarAggregater(object):
    def __init__(self):
        self.name = 'apps.forex.tick_bar_aggregater.TickBarAggregater'

    @staticmethod
    def generate_bar_from_tick(resolution):
        '''
        由Tick指定间隔生成Bar
        '''
        last_sample_ts = datetime.now()
        bar = {'Open': 0, 'High': 0, 'Low': 0, 'Close': 0}
        while True:
            tick = ForexRepository.ticks_for_bar.get(block=True)
            if 'instrument_id' in tick.keys():
                ts = datetime.strptime(tick['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
                bid = float(tick['bids'][0]['price'])
                delta = ts - last_sample_ts
                bar['High'] = max([bar['High'], bid])
                bar['Low'] = min([bar['Low'], bid])
                bar['Close'] = bid # Note that we update price BEFORE checking the condition to start a new bar!
                if delta.seconds >= resolution - 1:
                    if bar['Open'] != 0:
                        ForexRepository.bars_queue.put(bar)
                    last_sample_ts = ts
                    bar = {'Open': bid, 'High': bid, 'Low': bid, 'Close': bid} # 生成新对象用于下一次插入
            ForexRepository.ticks_for_trade.put(tick)