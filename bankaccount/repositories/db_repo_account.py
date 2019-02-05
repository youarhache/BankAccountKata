from bankaccount.entities.account import Account

class DbRepoAccounts:
    def __init__(self, db_session):
        self._session = db_session

    def find_account(self, account_code= None):
        _elem = self._session.query(Account).filter_by(code=account_code).first()
        return _elem

    def add_account(self, account=None):
        if account:
            self._session.add(account)

    def account_deposit(self, account, amount):
        if account and amount:
            account.balance += amount

    def account_withdraw(self, account, amount):
        if account and amount:
            account.balance -= amount