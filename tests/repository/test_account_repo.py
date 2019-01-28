import pytest

from bankaccount.shared.abstract_entity import AbstractEntity
from bankaccount.entities.account import Account
from bankaccount.repository import mem_repo_account


@pytest.fixture
def account_dicos():
    return [
    {
        'code':"7765432255E",
        'balance':4000.00
    },
    {
        'code':"1111188888B",
        'balance':8492.10
    }]


def test_repo_find_account_no_param_return_none(account_dicos):
    repo = mem_repo_account.MemRepoAccounts(account_dicos)
    result = repo.find_account()

    assert result is None


def test_repo_find_account_correct_param(account_dicos):
    repo = mem_repo_account.MemRepoAccounts(account_dicos)
    result = repo.find_account(account_code= "1111188888B")
    
    assert isinstance(result, AbstractEntity)
    assert result == Account.from_dict(account_dicos[1])


def test_repo_find_account_not_found(account_dicos):
    repo = mem_repo_account.MemRepoAccounts(account_dicos)
    result = repo.find_account(account_code= "1234567890A")

    assert result is None


#create account tests
def test_repo_add_account_correct(account_dicos):
    new_account = {'code':'1234567890F', 'balance':3090.00}
    repo = mem_repo_account.MemRepoAccounts(account_dicos)
    l = len(repo._entries)
    result = repo.add_account({'code':'1234567890F', 'amount':3090.00})

    assert len(repo._entries) == l+1
    assert new_account in repo._entries
    assert isinstance(result, AbstractEntity)
    assert result == Account.from_dict(new_account)


def test_repo_add_account_no_params(account_dicos):
    repo = mem_repo_account.MemRepoAccounts(account_dicos)
    l = len(repo._entries)
    result = repo.add_account()

    assert result is None
    assert len(repo._entries) == l


def test_repo_add_account_wrong_params(account_dicos):
    repo = mem_repo_account.MemRepoAccounts(account_dicos)
    l = len(repo._entries)
    result = repo.add_account(account=0)

    assert result is None
    assert len(repo._entries) == l


#Account deposit
def test_repo_account_deposit_correct(account_dicos):
    repo = mem_repo_account.MemRepoAccounts(account_dicos)
    new_account = {'code':repo._entries[0]['code'], 'balance':repo._entries[0]['balance'] + 590.50}
    result = repo.account_deposit({'code':repo._entries[0]['code'], 'amount':590.50})

    assert new_account == repo._entries[0]
    assert isinstance(result, AbstractEntity)
    assert result == Account.from_dict(new_account)


def test_repo_account_deposit_no_params(account_dicos):
    repo = mem_repo_account.MemRepoAccounts(account_dicos)
    result = repo.account_deposit()

    assert result is None


def test_repo_account_deposit_wrong_params(account_dicos):
    repo = mem_repo_account.MemRepoAccounts(account_dicos)
    result = repo.account_deposit(account=0)

    assert result is None


#Account withdraw
def test_repo_account_withdraw_correct(account_dicos):
    repo = mem_repo_account.MemRepoAccounts(account_dicos)
    new_account = {'code':repo._entries[1]['code'], 'balance':(repo._entries[1]['balance'] - 1000.00)}
    result = repo.account_withdraw({'code':repo._entries[1]['code'], 'amount':1000.00})

    assert account_dicos[0] == repo._entries[0]
    assert new_account == repo._entries[1]
    assert isinstance(result, AbstractEntity)
    assert result == Account.from_dict(new_account)


def test_repo_account_withdraw_no_params(account_dicos):
    repo = mem_repo_account.MemRepoAccounts(account_dicos)
    result = repo.account_withdraw()

    assert result is None


def test_repo_account_withdraw_wrong_params(account_dicos):
    repo = mem_repo_account.MemRepoAccounts(account_dicos)
    result = repo.account_withdraw(account=0)

    assert result is None