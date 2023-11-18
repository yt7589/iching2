# 账户管理类
# 注：当前公考虑一个账户进行一个外汇对的交易
from apps.forex.account import Account

class AccountManager(object):
    accounts = {
        'a001': Account(account_id='a001')
    }

    def __init__(self):
        self.name = 'apps.forex.account_manager.AccountManager'

    def get_account_by_id(account_id:str) -> Account:
        return AccountManager.accounts[account_id]