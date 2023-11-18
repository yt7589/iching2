#
import argparse
from typing import Dict
from datetime import datetime
import queue
import threading
#
from apps.lmax.csv_data_source import CsvDataSource

class ForexData(object):
    bars = {}
    datastream = queue.Queue()

    def __init__(self):
        self.name = 'apps.lmax.forex_data.ForexData'
        self.series = {}

    def add(self, sample):
        ts = datetime.strptime(sample["timestamp"], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.series[ts] = sample

    def get(self, ts, key):
        return self.series[ts][key]

    def tick_to_bar(self, tick_file:str) -> Dict:
        bars = {}
        bar = {}
        resolution = 60
        with open(tick_file, 'r', encoding='utf-8') as f:
            f.readline()
            values = f.readline().rstrip("\n").split(",")
            timestamp_string = values[0] + " " + values[1]
            last_sample_ts = datetime.strptime(timestamp_string, "%m/%d/%Y %H:%M:%S.%f")
            for line in f:
                values = line.rstrip("\n").split(",")
                timestamp_string = values[0] + " " + values[1]
                ts = datetime.strptime(timestamp_string, "%m/%d/%Y %H:%M:%S.%f")
                delta = ts - last_sample_ts
                if delta.seconds >= resolution:
                    bars[ts] = dict(bar)
                    bar["open"] = float(values[2])
                    bar["high"] = float(values[2])
                    bar["low"] = float(values[2])
                    last_sample_ts = ts
                else:
                    try:
                        bar["high"] = max([bar["high"], float(values[2])])
                        bar["low"] = min([bar["low"], float(values[2])])
                        bar["close"] = float(values[2])
                    except:
                        print('first bar forming...')
        return bars
    
    def generate_bars(self):
        bar = {}
        while True:
            print(f'generate_bars...')
            tick = ForexData.datastream.get()
            current_time = datetime.now()
            if current_time.second == 0:
                ForexData.bars[current_time] = dict(bar)
                bar["open"] = list(tick.values())[0]
                bar["high"] = list(tick.values())[0]
                bar["low"] = list(tick.values())[0]
                print(ForexData.bars)
            else:
                try:
                    bar["high"] = max([bar["high"], list(tick.values())[0]])
                    bar["low"] = min([bar["low"], list(tick.values())[0]])
                    bar["close"] = list(tick.values())[0]
                except:
                    print(str(current_time), ' bar forming...')
    

def main(args:argparse.Namespace = {}) -> None:
    # tick_data_demo()
    # order_book_demo()
    # tick_to_bar_demo()
    geneate_bars_demo()

def tick_data_demo():
    sample = {
        "type": "TICKER",
        "instrument_id": "eur-usd",
        "timestamp": "2022-07-29T11:10:54.755Z",
        "best_bid": "1.180970",
        "best_ask": "1.181010",
        "trade_id": "0B5WMAAAAAAAAAAS",
        "last_quantity": "1000.0000",
        "last_price": "1.180970",
        "session_open": "1.181070",
        "session_low": "1.180590",
        "session_high": "1.181390"
    }
    series = ForexData()
    series.add(sample)
    timestamp = datetime.strptime(sample["timestamp"], '%Y-%m-%dT%H:%M:%S.%fZ')
    print(series.get(timestamp, "trade_id"))

def order_book_demo():
    sample = {
        "type": "ORDER_BOOK",
        "instrument_id": "eur-usd",
        "timestamp": "2022-07-29T11:10:54.755Z",
        "status": "OPEN",
        "bids":[
            {
                "price": "1.181060",
                "quantity": "500000.0000"
            },
            {
                "price": "1.181050",
                "quantity": "200000.0000"
            }
        ],
        "asks": [
            {
                "price": "1.181100",
                "quantity": "250000.0000"
            },
            {
                "price": "1.181110",
                "quantity": "350000.0000"
            }
        ]
    }
    series = ForexData()
    series.add(sample)
    timestamp = datetime.strptime(sample["timestamp"], '%Y-%m-%dT%H:%M:%S.%fZ')
    print(series.get(timestamp, "bids")[0]['price'])

def tick_to_bar_demo():
    tick_file = 'work/forex_data/chp05/eurusd_1_tick.csv'
    data = ForexData()
    bars = data.tick_to_bar(tick_file=tick_file)
    print(list(bars.items())[-4:])

def geneate_bars_demo():
    data = ForexData()
    tick_file = 'work/forex_data/chp05/eurusd_1_tick.csv'
    kwArgs = {
        'datastream': ForexData.datastream,
        'tick_file': tick_file
    }
    data_source_thread = threading.Thread(target=CsvDataSource.emulate_tick_stream, kwargs=kwArgs)
    # data_receiver_thread = threading.Thread(target = trading_algo)
    data_receiver_thread = threading.Thread(target=data.generate_bars)
    data_source_thread.start()
    data_receiver_thread.start()




















def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_mode', action='store', type=int, default=1, dest='run_mode', help='run mode')
    return parser.parse_args()

if '__main__' == __name__:
    args = parse_args()
    main(args=args)    