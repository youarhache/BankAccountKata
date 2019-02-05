import pytest
import json
from bankaccount.adapters.orm import SqlAlchemy
from bankaccount.entities.transfer import Transfer
from bankaccount.entities.account import Account


test_acc_req1 = {
        'code': '1234567890F',
        'amount': 10000.00
    }
test_acc_req2 = {
        'code': '0101010101A',
        'amount': 10000.00
    }
test_acc_req3 = {
        'code': '3216540987V',
        'amount': 10000.00
    }

test_acc1 = Account(account_code='1234567890F',account_balance=10000.00)
test_acc2 = Account(account_code='0101010101A',account_balance=10000.00)

test_trs_req1 = {
        'from': '1234567890F',
        'to': '0101010101A',
        'amount': 100.00
    }

test_trs_req2 = {
        'from': '0101010101A',
        'to': '1234567890F',
        'amount': 500.00
    }

mimetype = 'application/json'

headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }


@pytest.fixture(scope='module')
def db():
    db = SqlAlchemy('sqlite:///bankaccount.db')
    db.configure_mappings()
    db.recreate_schema()
    return db


@pytest.fixture
def prepare_accounts(client):
    client.post('/account', data=json.dumps(test_acc_req1), headers=headers)
    client.post('/account', data=json.dumps(test_acc_req2), headers=headers)


@pytest.fixture
def prepare_transfer(client):
    client.post('/transfer', data=json.dumps(test_trs_req1), headers=headers)


def test_int_account_creation(db, client):
    http_response = client.post('/account', data=json.dumps(test_acc_req3), headers=headers)
    with db.unit_of_work_manager.start() as uow:
        inserted_acc = uow.accounts.find_account(test_acc_req3['code'])

    assert http_response.status_code == 200
    assert inserted_acc.balance == test_acc_req3['amount']
    assert inserted_acc.code == test_acc_req3['code']


def test_int_account_deposit(db, client, prepare_accounts):
    http_response =client.put('/account-deposit', data=json.dumps(test_acc_req1), headers=headers)
    with db.unit_of_work_manager.start() as uow:
        changed_acc = uow.accounts.find_account(test_acc_req1['code'])

    assert http_response.status_code == 200
    assert changed_acc.balance == test_acc1.balance + test_acc_req1['amount']
    assert changed_acc.code == test_acc_req1['code']


def test_int_account_withdraw(db, client):
    http_response =client.put('/account-withdraw', data=json.dumps(test_acc_req2), headers=headers)
    with db.unit_of_work_manager.start() as uow:
        changed_acc = uow.accounts.find_account(test_acc_req2['code'])

    assert http_response.status_code == 200
    assert changed_acc.balance == test_acc2.balance -test_acc_req2['amount']
    assert changed_acc.code == test_acc_req2['code']


def test_int_transfer_create(db, client):
    http_response =client.post('/transfer', data=json.dumps(test_trs_req1), headers=headers)
    with db.unit_of_work_manager.start() as uow:
        payer_acc = uow.accounts.find_account(test_trs_req1['from'])
        payee_acc = uow.accounts.find_account(test_trs_req1['to'])

    assert http_response.status_code == 200
    assert payer_acc.balance == test_acc2.balance + test_acc_req1['amount'] -test_trs_req1['amount']
    assert payee_acc.balance == test_acc1.balance - test_acc_req1['amount'] +test_trs_req1['amount']


def test_int_transfer_lookup_by_payer(db, client, prepare_transfer):
    http_response =client.get('/transfers?filter_trs_from=1234567890F')
    
    assert http_response.status_code == 200
    assert len(http_response.data) > 0