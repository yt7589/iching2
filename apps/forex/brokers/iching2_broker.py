# 虚拟的代理服务机构
from typing import Dict
from apps.forex.brokers.base_broker import BaseBroker

class Iching2Broker(BaseBroker):
    commission_ratio = 0.0

    def __init__(self):
        self.name = 'apps.forex.brokers.iching2_broker.Iching2Broker'

    def execute_order(self, tick:Dict, order:Dict) -> int:
        print(f'### 模拟执行订单... 添加commission')
        if order['Type'] == 'Market':
            if order['Side'] == 'Buy':
                current_liquidity = float(tick['asks'][0]['quantity'])
                price = float(tick['asks'][0]['price'])
                if order['Size'] <= current_liquidity:
                    order['Executed Price'] = price
                    order['commission'] = price * order['Size'] * Iching2Broker.commission_ratio
                    order['RealPay'] = price * order['Size'] * (1 + Iching2Broker.commission_ratio)
                    order['Status'] = 'Executed'
                else:
                    order['Status'] = 'Rejected'
            if order['Side'] == 'Sell':
                current_liquidity = float(tick['bids'][0]['quantity'])
                price = float(tick['bids'][0]['price'])
                if order['Size'] <= current_liquidity:
                    order['Executed Price'] = price
                    order['commission'] = price * order['Size'] * Iching2Broker.commission_ratio
                    order['RealPay'] = price * order['Size'] * (1 + Iching2Broker.commission_ratio)
                    order['Status'] = 'Executed'
                else:
                    order['Status'] = 'Rejected'
        return 0