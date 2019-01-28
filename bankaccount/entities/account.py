from bankaccount.shared.abstract_entity import AbstractEntity

class Account:
    def __init__(self, account_code, account_balance):
        self.code = account_code
        self.balance = account_balance

    @classmethod
    def from_dict(cls, dict):
        account = cls(account_code = dict['code'],
                    account_balance = dict['balance'])
        return account

    def to_dict(self):
        dict = {
            'code': self.code,
            'balance': self.balance
        }
        return dict

    def __eq__(self, other):
        return self.to_dict()==other.to_dict()

AbstractEntity.register(Account)