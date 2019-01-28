import pytest
from unittest import mock
from bankaccount.entities.account import Account
from bankaccount.usecases import (account_usecases as uc_account, 
                                request_objects as rq,
                                response_objects as rs)


@pytest.fixture
def account_domain_entity():
    return Account(
        account_code="1234567890F",
        account_balance=3200.00
    )


#Account creation
def test_account_creation_with_correct_params():
    repo = mock.Mock()
    repo.find_account.return_value = None
    repo.add_account.return_value = account_domain_entity

    account_creation = uc_account.AccountCreationUseCase(repo)
    params = {'code':'1234567890F','amount':3200.00}
    req = rq.AccountOperationRequest.from_dict({'account':params})
    resp = account_creation.execute(req)
    
    assert bool(resp) is True
    assert resp.value == account_domain_entity
    repo.add_account.assert_called_with(account=params)


def test_account_creation_no_params():
    repo = mock.Mock()
    repo.find_account.return_value = None
    repo.add_account.return_value = account_domain_entity

    account_creation = uc_account.AccountCreationUseCase(repo)
    req = rq.AccountOperationRequest()
    resp = account_creation.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'account : parameter is required'}


def test_account_creation_wrong_params_format():
    repo = mock.Mock()
    repo.find_account.return_value = None
    repo.add_account.return_value = account_domain_entity

    account_creation = uc_account.AccountCreationUseCase(repo)
    req = rq.AccountOperationRequest(account=0)
    resp = account_creation.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'account : parameter not in the correct format'}


def test_account_creation_existing_account():
    repo = mock.Mock()
    repo.add_account.return_value = account_domain_entity
    repo.find_account.return_value = account_domain_entity

    account_creation = uc_account.AccountCreationUseCase(repo)
    params = {'code':'1234567890F','amount':3200.00}
    req = rq.AccountOperationRequest(account=params)
    resp = account_creation.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.RESOURCE_ERROR,
                        'message': 'account already exists'}


def test_account_creation_error():
    repo = mock.Mock()
    repo.find_account.return_value = None
    repo.add_account.side_effect = Exception('error message')

    account_creation = uc_account.AccountCreationUseCase(repo)
    params = {'code':'1234567890F','amount':3200.00}
    req = rq.AccountOperationRequest(account=params)
    resp = account_creation.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.SYSTEM_ERROR,
                        'message': 'Exception : error message'}

#Account deposit
def test_account_deposit_with_correct_params(account_domain_entity):
    repo = mock.Mock()
    repo.find_account.return_value = account_domain_entity
    with_deposit = Account.from_dict({'code':'1234567890F','balance':3400.30})
    repo.account_deposit.return_value = with_deposit

    account_deposit = uc_account.AccountDepositUseCase(repo)
    params = {'code':'1234567890F','amount':200.30}
    req = rq.AccountOperationRequest.from_dict({'account':params})
    resp = account_deposit.execute(req)
    
    assert bool(resp) is True
    assert resp.value == with_deposit
    repo.account_deposit.assert_called_with(account=params)


def test_account_deposit_no_params():
    repo = mock.Mock()
    repo.find_account.return_value = None
    repo.account_deposit.return_value = account_domain_entity

    account_deposit = uc_account.AccountDepositUseCase(repo)
    req = rq.AccountOperationRequest()
    resp = account_deposit.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'account : parameter is required'}


def test_account_deposit_wrong_params_format():
    repo = mock.Mock()
    repo.find_account.return_value = None
    repo.account_deposit.return_value = account_domain_entity

    account_deposit = uc_account.AccountDepositUseCase(repo)
    req = rq.AccountOperationRequest(account=0)
    resp = account_deposit.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'account : parameter not in the correct format'}


def test_account_deposit_nonexistent_account():
    repo = mock.Mock()
    repo.account_deposit.return_value = None
    repo.find_account.return_value = None

    account_deposit = uc_account.AccountDepositUseCase(repo)
    params = {'code':'0000000000F','amount':200.30}
    req = rq.AccountOperationRequest(account=params)
    resp = account_deposit.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.RESOURCE_ERROR,
                        'message': 'account not found'}


def test_account_deposit_error(account_domain_entity):
    repo = mock.Mock()
    repo.find_account.return_value = account_domain_entity
    repo.account_deposit.side_effect = Exception('error message')

    account_deposit = uc_account.AccountDepositUseCase(repo)
    params = {'code':'1234567890F','amount':200.30}
    req = rq.AccountOperationRequest(account=params)
    resp = account_deposit.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.SYSTEM_ERROR,
                        'message': 'Exception : error message'}

#Account withdraw

def test_account_withdraw_with_correct_params(account_domain_entity):
    repo = mock.Mock()
    repo.find_account.return_value = account_domain_entity
    after_withdraw = Account.from_dict({'code':'1234567890F', 'balance':2200.00})
    repo.account_withdraw.return_value = after_withdraw

    account_withdraw = uc_account.AccountWithdrawUseCase(repo)
    params = {'code':'1234567890F','amount':1000.00}
    req = rq.AccountOperationRequest.from_dict({'account':params})
    resp = account_withdraw.execute(req)
    
    assert bool(resp) is True
    assert resp.value == after_withdraw
    repo.account_withdraw.assert_called_with(account=params)


def test_account_withdraw_wrong_amount(account_domain_entity):
    repo = mock.Mock()
    repo.find_account.return_value = account_domain_entity
    repo.account_withdraw.return_value = account_domain_entity

    account_withdraw = uc_account.AccountWithdrawUseCase(repo)
    params = {'code':'1234567890F','amount':5000.00}
    req = rq.AccountOperationRequest.from_dict({'account':params})
    resp = account_withdraw.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'incorrect withdraw amount'}


def test_account_withdraw_no_params():
    repo = mock.Mock()
    repo.find_account.return_value = None
    repo.account_withdraw.return_value = account_domain_entity

    account_withdraw = uc_account.AccountWithdrawUseCase(repo)
    req = rq.AccountOperationRequest()
    resp = account_withdraw.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'account : parameter is required'}


def test_account_withdraw_wrong_params_format():
    repo = mock.Mock()
    repo.find_account.return_value = None
    repo.account_withdraw.return_value = account_domain_entity

    account_withdraw = uc_account.AccountWithdrawUseCase(repo)
    req = rq.AccountOperationRequest(account=0)
    resp = account_withdraw.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'account : parameter not in the correct format'}


def test_account_withdraw_nonexistent_account():
    repo = mock.Mock()
    repo.account_withdraw.return_value = None
    repo.find_account.return_value = None

    account_withdraw = uc_account.AccountWithdrawUseCase(repo)
    params = {'code':'0000000000F','amount':1000.00}
    req = rq.AccountOperationRequest(account=params)
    resp = account_withdraw.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.RESOURCE_ERROR,
                        'message': 'account not found'}


def test_account_withdraw_error(account_domain_entity):
    repo = mock.Mock()
    repo.find_account.return_value = account_domain_entity
    repo.account_withdraw.side_effect = Exception('error message')

    account_withdraw = uc_account.AccountWithdrawUseCase(repo)
    params = {'code':'1234567890F','amount':3200.00}
    req = rq.AccountOperationRequest(account=params)
    resp = account_withdraw.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.SYSTEM_ERROR,
                        'message': 'Exception : error message'}