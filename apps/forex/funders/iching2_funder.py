# 缺省配资平台类，主要用于回测和模拟实盘
from typing import Dict
from datetime import datetime
from apps.forex.funders.base_funder import BaseFunder
from apps.forex.account import Account

class Iching2Funder(BaseFunder):
    IOT_DEPOSIT = 1
    IOT_WITHDRAW = 2
    IOT_LOAN = 3
    IOT_REPAY = 4
    initial_capital = 1000000000
    capital = initial_capital
    leverage = 30 # 杠杆率
    ratio = 0.0006 # 日利率
    loans = {} # loan_id: {account, amount, loan_date, due_date, leverage, ratio}
    finished_loans = {}
    capital_io = [
        {'io_type': 1, 'io_amount': initial_capital, 'amount': initial_capital, 'loan_id': 0}
    ] # {io_type, io_amount, amount, loan_id}，其中io_type：1-注资；2-提现；3-贷款；4-还款；如果是贷款和还款时，才会有loan_id
    seq = 1
    # 后台进程会算每个账户借款产生的利息，如果资不抵债自动平仓，需要有一定余量

    def __init__(self):
        self.name = 'apps.forex.funders.iching2_funder.Iching2Funder'
    
    def loan_special(self, account:Account, amount:float, loan_date: datetime, due_date: datetime, leverage:float, ratio:float) -> int:
        '''
        按指定的利率贷款
        '''
        loan_id = Iching2Funder.seq
        Iching2Funder.seq += 1
        Iching2Funder.loans[loan_id] = {
            'loan_id': loan_id,
            'account': account,
            'amount': amount,
            'loan_date': loan_date, #datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            'due_date': due_date,
            'leverage': leverage,
            'ratio': ratio
        }
        Iching2Funder.capital_io.append([{
            'io_type': Iching2Funder.IOT_LOAN,
            'io_amount': amount,
            'amount': Iching2Funder.capital_io[-1]['amount'] - amount,
            'loan_id': loan_id
        }])
        Iching2Funder.capital = Iching2Funder.capital_io[-1]['amount']

    def loan(self, account:Account, amount:float, loan_date: datetime, due_date: datetime) -> int:
        '''
        贷款，返回loan_id
        '''
        self.loan_special(account=account, amount=amount, loan_date=loan_date, due_date=due_date, leverage=Iching2Funder.leverage, ratio=Iching2Funder.ratio)

    def repay(self, account:Account, loan_id:int, amount:float) -> bool:
        '''
        给指定贷款记录还款
        '''
        Iching2Funder.finished_loans[loan_id] = dict(Iching2Funder.loans[loan_id])
        del Iching2Funder.loans[loan_id]
        Iching2Funder.capital_io.append([{
            'io_type': Iching2Funder.IOT_REPAY,
            'io_amount': amount,
            'amount': Iching2Funder.capital[-1][amount] + amount,
            'loan_id': loan_id
        }])
        Iching2Funder.capital = Iching2Funder.capital_io[-1]['amount']

    def get_due_amount(self, account:Account, loan_id:int) -> Dict:
        loan_rec = Iching2Funder.loans[loan_id]
        loan_date = loan_rec['loan_date']
        loan_days = datetime.now() - loan_date + 1
        interest = loan_days * loan_rec['ratio']
        return {'amount': loan_rec['amount'], 'interest': interest, 'due_amount': loan_rec['amount'] + interest}