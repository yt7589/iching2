# 策略基类
from apps.forex.account import Account

class BaseStrategy(object):
    def __init__(self):
        self.name = 'apps.forex.strategies.base_strategy.BaseStrategy'

    def execute(self, account:Account):
        pass