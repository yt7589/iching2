#
import numpy as np
import matplotlib.pylab as plt
import unittest
from apps.forex.strategies.trend_following_strategy import TrendFollowingStrategy

class TTrendFollowingStrategy(unittest.TestCase):
    # python -m unittest utc.apps.forex.strategies.t_trend_following_strategy.TTrendFollowingStrategy.test_display_data
    def test_display_data(self):
        '''
        显示图像，大致找到交易时间节点
        '''
        data_fn = 'apps/forex/datasets/trend_following/audusd_daily.csv'
        first_run = True
        dts = []
        close_prices = []
        ma5 = []
        ma20 = []
        with open(data_fn, 'r', encoding='utf-8') as fd:
            for row in fd:
                row = row.strip()
                if first_run:
                    first_run = False
                    continue
                arrs0 = row.split(',')
                dt = arrs0[0]
                dts.append(dt)
                close_price = float(arrs0[5])
                close_prices.append(close_price)
                close_prices_len = len(close_prices)
                start_idx5 = close_prices_len - 5
                if start_idx5 < 0:
                    start_idx5 = 0
                ma5_data = close_prices[start_idx5:]
                ma5.append(sum(ma5_data)/len(ma5_data))
                start_idx20 = close_prices_len - 20
                if start_idx20 < 0:
                    start_idx20 = 0
                ma20_data = close_prices[start_idx20:]
                ma20.append(sum(ma20_data)/len(ma20_data))
                print(f'##### {dt}, {close_price}')
        print(f'### {len(close_prices)}; {len(ma5)}; {len(ma20)}; ????????????')
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.set_xticks(np.arange(0, len(dts) + 1, 60))
        plt.xticks(rotation=45)
        plt.plot(dts[0:100], close_prices[0:100], color='b', label='price')
        plt.plot(dts[0:100], ma5[0:100], color='c', label='ma5')
        plt.plot(dts[0:100], ma20[0:100], color='g', label='ma20')
        plt.legend()
        plt.title('Trend Following Strategy Graph')
        plt.xlabel('time')
        plt.ylabel('close price')
        plt.show()