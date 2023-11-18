#
import time
import csv
from apps.forex.forex_repository import ForexRepository
import queue

class LmaxBarRepo(object):
    def __init__(self):
        self.name = 'apps.forex.exchs.lmax_bar_repo.LmaxBarRepo'

    @staticmethod
    def connect():
        start_time = time.perf_counter()
        with open("apps/forex/datasets/lmax_eru_usd_1_m_v001.txt", 'r', encoding='utf-8') as f:
            csvFile = csv.DictReader(f)
            all_data = list(csvFile)
            end_time = time.perf_counter()
            print(f'Data read in {round(end_time - start_time, 0)} second(s).')
        counter = 0
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
        # for bar in all_data:
        #     bar['Open'] = float(bar['Open'])
        #     bar['High'] = float(bar['High'])
        #     bar['Low'] = float(bar['Low'])
        #     bar['Close'] = float(bar['Close'])
        #     if counter == 0:
        #         print(f'### LmaxBarRepo 1')
        #         ForexRepository.bars_queue.put(bar)
        #         prev_bar = bar
        #     else:
        #         print(f'### LmaxBarRepo 2')
        #         curr_bar = ForexRepository.next_bars_queue.get(block=False)
        #         ForexRepository.bars_queue.put(curr_bar)
        #         ForexRepository.next_bars_queue.put(bar)
        #     print(f'@@@ {counter}: {bar};')
            counter += 1
            if counter == 10: # 用于测试时提前终止
                break
            ForexRepository.data_event.clear()
            ForexRepository.trade_event.set()
            ForexRepository.data_event.wait()
        print('Finished reading data')