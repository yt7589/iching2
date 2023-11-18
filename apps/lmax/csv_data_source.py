#
from datetime import datetime
import time
import queue

class CsvDataSource(object):
    def __init__(self):
        self.name = 'apps.lmax.csv_data_source.CsvDataSource'

    @staticmethod
    def get_tick(tick_file:str) -> None:
        with open(tick_file, 'r', encoding='utf-8') as f:
            f.readline()
            tick = {}
            values = f.readline().rstrip("\n").split(",")
            timestamp_string = values[0] + " " + values[1]
            ts = datetime.strptime(timestamp_string, "%m/%d/%Y %H:%M:%S.%f")
            tick[ts] = float(values[2])
        return tick
    
    @staticmethod
    def emulate_tick_stream(datastream: queue.Queue, tick_file:str) -> None:
        while True:
            time.sleep(1)
            temp = CsvDataSource.get_tick(tick_file=tick_file)
            datastream.put(temp)