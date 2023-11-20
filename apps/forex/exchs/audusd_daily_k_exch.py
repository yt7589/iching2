#
import csv
from apps.forex.exchs.base_exch import BaseExch
from apps.forex.forex_repository import ForexRepository

class AudusdDailyKExch(BaseExch):
    def __init__(self):
        self.name = 'apps.forex.exchs.audusd_daily_k_exch.AudusdDailyKExch'

    @staticmethod
    def connect():
        # 读入AUDUSD日K线行情数据
        with open('apps/forex/datasets/trend_following/audusd_daily.csv', 'r', encoding='utf-8') as fd:
            csvFile = csv.DictReader(fd)
            all_data = list(csvFile)
        # counter = 0 # 用于测试临时终止
        for idx in range(len(all_data) - 1):
            bar = {
                'Open': float(all_data[idx]['Open']),
                'High': float(all_data[idx]['High']),
                'Low': float(all_data[idx]['Low']),
                'Close': float(all_data[idx]['Close'])
            }
            ForexRepository.bars_queue.put(bar)
            print(f'当前行情：{bar};')
            next_bar = {
                'Open': float(all_data[idx+1]['Open']),
                'High': float(all_data[idx+1]['High']),
                'Low': float(all_data[idx+1]['Low']),
                'Close': float(all_data[idx+1]['Close'])
            }
            ForexRepository.next_bars_queue.put(next_bar)
            # counter += 1 # 用于测试临时终止
            # if counter == 10: # 用于测试时提前终止
            #     break
            ForexRepository.data_event.clear()
            ForexRepository.trade_event.set()
            ForexRepository.data_event.wait()
        print('Finished reading data')






        # counter = 0
        # for bar in all_data:
        #     bar['Open'] = float(bar['Open'])
        #     bar['High'] = float(bar['High'])
        #     bar['Low'] = float(bar['Low'])
        #     bar['Close'] = float(bar['Close'])
        #     bar_feed.put(bar)
        #     counter += 1
        #     if counter == 100000:
        #         break
        #     if int(counter / 100000) == counter / 100000:
        #         print('Processed', counter, 'bars')
        #     System.F1.clear()
        #     System.F2.set()
        #     System.F1.wait()
        # print('Finished reading data')