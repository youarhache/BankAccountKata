from bankaccount.entities.account import Account

def test_account_entity_init():
    code = '1111111111V'
    account = Account(code, account_balance=100.00)

    assert account.code == code
    assert account.balance == 100.00

def test_account_from_dict():
    code = '2222222222M'
    dict = {
        'code' : code,
        'balance' : 321.10
    }
    account = Account.from_dict(dict)

    assert account.code == code
    assert account.balance == 321.10

def test_account_to_dict():
    dict = {
        'code' : '1234522222F',
        'balance' : 1200.00
    }

    account = Account.from_dict(dict)

    assert dict == account.to_dict()

def test_account_comparison():
    dict = {
        'code' : '1234522222F',
        'balance' : 1200.00
    }
    account1 = Account.from_dict(dict)
    account2 = Account.from_dict(dict)

    assert account1 == account2