#
from typing import Dict

class BaseBroker(object):
    def __init__(self):
        self.name = 'apps.forex.brokers.base_broker.BaseBroker'

    def execute_order(self, tick: Dict, order:Dict) -> int:
        order.status = 'Executed'
        return 0