import pytest
from unittest import mock
from .fake_uow import FakeUnitOfWork
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

@pytest.fixture
def unit_of_work():
    return FakeUnitOfWork()

@pytest.fixture
def params():
    return {'code':'1234567890F','amount':3200.00}
     


#Account creation
def test_account_creation_with_correct_params(params, unit_of_work):
    uowm = unit_of_work

    account_creation = uc_account.AccountCreationUseCase(uowm)
    req = rq.AccountOperationRequest.from_dict({'account':params})
    resp = account_creation.execute(req)
    
    assert bool(resp) is True
    assert unit_of_work._committed


def test_account_creation_no_params(unit_of_work):
    uowm = unit_of_work

    account_creation = uc_account.AccountCreationUseCase(uowm)
    req = rq.AccountOperationRequest()
    resp = account_creation.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'account : parameter is required'}
    assert unit_of_work._committed  is False


def test_account_creation_wrong_params_format(unit_of_work):
    uowm = unit_of_work

    account_creation = uc_account.AccountCreationUseCase(uowm)
    req = rq.AccountOperationRequest(account=0)
    resp = account_creation.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'account : parameter not in the correct format'}
    assert unit_of_work._committed  is False


def test_account_creation_existing_account(account_domain_entity, params, unit_of_work):
    uowm = unit_of_work
    unit_of_work.accounts.add_account(account_domain_entity)

    account_creation = uc_account.AccountCreationUseCase(uowm)
    
    req = rq.AccountOperationRequest(account=params)
    resp = account_creation.execute(req)
    
    assert bool(resp) is False
    assert unit_of_work._committed  is False
    assert resp.value == {'type': rs.ResponseFailure.RESOURCE_ERROR,
                        'message': 'account already exists'}


def test_account_creation_error(params, unit_of_work):
    with mock.patch.object(unit_of_work.accounts,'add_account', side_effect=Exception('error message')):
        uowm = unit_of_work

        account_creation = uc_account.AccountCreationUseCase(uowm)
        req = rq.AccountOperationRequest(account=params)
        resp = account_creation.execute(req)
        
        assert bool(resp) is False
        assert unit_of_work._committed  is False
        assert resp.value == {'type': rs.ResponseFailure.SYSTEM_ERROR,
                            'message': 'Exception : error message'}
        assert unit_of_work._rolledback

#Account deposit
def test_account_deposit_with_correct_params(account_domain_entity, params, unit_of_work):
    uowm = unit_of_work
    unit_of_work.accounts.add_account(account_domain_entity)
    
    account_deposit = uc_account.AccountDepositUseCase(uowm)
    req = rq.AccountOperationRequest.from_dict({'account':params})
    resp = account_deposit.execute(req)
    
    assert bool(resp) is True
    assert unit_of_work._committed


def test_account_deposit_no_params(unit_of_work):
    uowm = unit_of_work

    account_deposit = uc_account.AccountDepositUseCase(uowm)
    req = rq.AccountOperationRequest()
    resp = account_deposit.execute(req)
    
    assert bool(resp) is False
    assert unit_of_work._committed  is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'account : parameter is required'}


def test_account_deposit_wrong_params_format(unit_of_work):
    uowm = unit_of_work

    account_deposit = uc_account.AccountDepositUseCase(uowm)
    req = rq.AccountOperationRequest(account=0)
    resp = account_deposit.execute(req)
    
    assert bool(resp) is False
    assert unit_of_work._committed  is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'account : parameter not in the correct format'}


def test_account_deposit_nonexistent_account(params, unit_of_work):
    uowm = unit_of_work

    account_deposit = uc_account.AccountDepositUseCase(uowm)
    req = rq.AccountOperationRequest(account=params)
    resp = account_deposit.execute(req)
    
    assert bool(resp) is False
    assert unit_of_work._committed  is False
    assert resp.value == {'type': rs.ResponseFailure.RESOURCE_ERROR,
                        'message': 'account not found'}


def test_account_deposit_error(account_domain_entity, params, unit_of_work):
    with mock.patch.object(unit_of_work.accounts,'account_deposit', side_effect=Exception('error message')):
        uowm = unit_of_work
        uowm.accounts.add_account(account_domain_entity)

        account_deposit = uc_account.AccountDepositUseCase(uowm)
        req = rq.AccountOperationRequest(account=params)
        resp = account_deposit.execute(req)
        
        assert bool(resp) is False
        assert unit_of_work._committed  is False
        assert unit_of_work._rolledback
        assert resp.value == {'type': rs.ResponseFailure.SYSTEM_ERROR,
                            'message': 'Exception : error message'}


#Account withdraw
def test_account_withdraw_with_correct_params(account_domain_entity, params, unit_of_work):
    uowm = unit_of_work
    unit_of_work.accounts.add_account(account_domain_entity)

    account_withdraw = uc_account.AccountWithdrawUseCase(uowm)
    req = rq.AccountOperationRequest.from_dict({'account':params})
    resp = account_withdraw.execute(req)
    
    assert bool(resp) is True
    assert unit_of_work._committed


def test_account_withdraw_wrong_amount(account_domain_entity, params, unit_of_work):
    uowm = unit_of_work
    unit_of_work.accounts.add_account(account_domain_entity)

    account_withdraw = uc_account.AccountWithdrawUseCase(uowm)
    wrong_params = {'code':'1234567890F','amount':5000.00}
    req = rq.AccountOperationRequest.from_dict({'account':wrong_params})
    resp = account_withdraw.execute(req)
    
    assert bool(resp) is False
    assert unit_of_work._committed  is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'incorrect withdraw amount'}


def test_account_withdraw_no_params(unit_of_work):
    uowm = unit_of_work

    account_withdraw = uc_account.AccountWithdrawUseCase(uowm)
    req = rq.AccountOperationRequest()
    resp = account_withdraw.execute(req)
    
    assert bool(resp) is False
    assert unit_of_work._committed  is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'account : parameter is required'}


def test_account_withdraw_wrong_params_format(unit_of_work):
    uowm = unit_of_work

    account_withdraw = uc_account.AccountWithdrawUseCase(uowm)
    req = rq.AccountOperationRequest(account=0)
    resp = account_withdraw.execute(req)
    
    assert bool(resp) is False
    assert unit_of_work._committed  is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'account : parameter not in the correct format'}


def test_account_withdraw_nonexistent_account(params, unit_of_work):
    uowm = unit_of_work

    account_withdraw = uc_account.AccountWithdrawUseCase(uowm)
    req = rq.AccountOperationRequest(account=params)
    resp = account_withdraw.execute(req)
    
    assert bool(resp) is False
    assert unit_of_work._committed  is False
    assert resp.value == {'type': rs.ResponseFailure.RESOURCE_ERROR,
                        'message': 'account not found'}


def test_account_withdraw_error(account_domain_entity, params, unit_of_work):
    with mock.patch.object(unit_of_work.accounts,'account_withdraw', side_effect=Exception('error message')):
        uowm = unit_of_work
        uowm.accounts.add_account(account_domain_entity)

        account_withdraw = uc_account.AccountWithdrawUseCase(uowm)
        req = rq.AccountOperationRequest(account=params)
        resp = account_withdraw.execute(req)
        
        assert bool(resp) is False
        assert unit_of_work._committed  is False
        assert unit_of_work._rolledback
        assert resp.value == {'type': rs.ResponseFailure.SYSTEM_ERROR,
                            'message': 'Exception : error message'}