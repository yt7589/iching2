#
from typing import Dict
from datetime import datetime

class BaseFunder(object):
    def __init__(self):
        self.name = 'apps.forex.funders.base_funder.BaseFunder'

    def loan(self, amount:float, load_date: datetime, due_date: datetime, leverage:float, ratio:float) -> str:
        pass

    def repay(self, amount:float) -> bool:
        pass

    def get_due_amount(self, load_id:str) -> Dict:
        pass