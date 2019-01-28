import pytest
from unittest import mock
import datetime
from bankaccount.entities.transfer import Transfer
from bankaccount.entities.account import Account
from bankaccount.usecases import (transfer_usecases as uc_trs, 
                                request_objects as rq,
                                response_objects as rs)


@pytest.fixture
def transfer_domain_entities():
    test_trs1 = Transfer(
                        trs_id=1,
                        trs_timestamp="2019-01-22 09:00:00",
                        trs_from="1234567890F",
                        trs_to="3333333333A",
                        trs_amount=321.00
    )
    test_trs2 = Transfer(
                        trs_id=2,
                        trs_timestamp="2019-01-22 09:10:20",
                        trs_from="4444444444C",
                        trs_to="7765432255B",
                        trs_amount=1234.50
    )
    test_trs3 = Transfer(
                        trs_id=3,
                        trs_timestamp="2019-01-23 15:05:04",
                        trs_from="5555555555E",
                        trs_to="6666666666V",
                        trs_amount=400.00
    )
    test_trs4 = Transfer(
                        trs_id=4,
                        trs_timestamp="2019-01-24 14:00:59",
                        trs_from="7777777777A",
                        trs_to="1111188888B",
                        trs_amount=492.50
    )

    return [test_trs1, test_trs2, test_trs3, test_trs4]



#transfert operation
def test_trs_op_no_param():
    trs_repo = mock.Mock()
    account_repo = mock.Mock()

    trs_op = uc_trs.TransferAmountUseCase(trs_repo, account_repo)
    req = rq.TransferAmountRequest.from_dict({})
    resp = trs_op.execute(req)

    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'transfer : parameter is required'}


def test_trs_op_success(transfer_domain_entities):
    trs_repo = mock.Mock()
    account_repo = mock.Mock()
    account_repo.find_account.return_value = Account("1234567890F", 1000.00)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _trs = Transfer(5,timestamp, "1234567890F", "7765432255B", 100.00)
    trs_repo.add_transfer.return_value = _trs
    account_repo.account_withdraw.return_value = Account("1234567890F", 900.00)
    account_repo.account_deposit.return_value = Account("7765432255B", 1100.00)

    trs_op = uc_trs.TransferAmountUseCase(trs_repo, account_repo)
    req = rq.TransferAmountRequest.from_dict({'transfer': {'from':'1234567890F', 'to':'7765432255B', 'amount':100.00}})
    resp = trs_op.execute(req)

    assert bool(resp) is True
    assert resp.value == Transfer(5,timestamp, "1234567890F", "7765432255B", 100.00)


def test_trs_op_wrong_param():
    trs_repo = mock.Mock()
    account_repo = mock.Mock()

    trs_op = uc_trs.TransferAmountUseCase(trs_repo, account_repo)
    req = rq.TransferAmountRequest(trs=0)
    resp = trs_op.execute(req)

    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'transfer : parameter not in the correct format'}


def test_trs_op_payer_is_payee():
    trs_repo = mock.Mock()
    account_repo = mock.Mock()

    trs_op = uc_trs.TransferAmountUseCase(trs_repo, account_repo)
    req = rq.TransferAmountRequest.from_dict({'transfer': {'from':'1234567890F', 'to':'1234567890F', 'amount':100.00}})
    resp = trs_op.execute(req)
    
    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'payer account must be different than the payee'}


def test_trs_op_account_not_found():
    trs_repo = mock.Mock()
    account_repo = mock.Mock()
    account_repo.find_account.return_value = None

    trs_op = uc_trs.TransferAmountUseCase(trs_repo, account_repo)
    req = rq.TransferAmountRequest.from_dict({'transfer': {'from':'1234567890F', 'to':'7765432255B', 'amount':100.00}})
    resp = trs_op.execute(req)

    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': "account doesn't exist"}


def test_trs_op_payer_not_debited():
    trs_repo = mock.Mock()
    account_repo = mock.Mock()
    account_repo.account_withdraw.return_value = None

    trs_op = uc_trs.TransferAmountUseCase(trs_repo, account_repo)
    req = rq.TransferAmountRequest.from_dict({'transfer': {'from':'1234567890F', 'to':'7765432255B', 'amount':100.00}})
    resp = trs_op.execute(req)

    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.RESOURCE_ERROR,
                        'message': "payer account could't be debited"}


def test_trs_op_payer_debited_payee_not_credited():
    trs_repo = mock.Mock()
    account_repo = mock.Mock()
    account_repo.account_withdraw.return_value = Account("1234567890F", 900.00)
    account_repo.account_deposit.return_value = None

    trs_op = uc_trs.TransferAmountUseCase(trs_repo, account_repo)
    req = rq.TransferAmountRequest.from_dict({'transfer': {'from':'1234567890F', 'to':'7765432255B', 'amount':100.00}})
    resp = trs_op.execute(req)

    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.RESOURCE_ERROR,
                        'message': "payee account could't be credited"}
    #assert rollback
    account_repo.account_deposit.assert_called_with(account={'code':'1234567890F', 'amount':100.00})

def test_trs_op_generic_error():
    account_repo = mock.Mock()
    trs_repo = mock.Mock()
    trs_repo.add_transfer.side_effect = Exception('error message')

    trs_op = uc_trs.TransferAmountUseCase(trs_repo, account_repo)
    req = rq.TransferAmountRequest.from_dict({'transfer': {'from':'1234567890F', 'to':'7765432255B', 'amount':100.00}})
    resp = trs_op.execute(req)

    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.SYSTEM_ERROR,
                        'message': 'Exception : error message'}


#Transfer history list
def test_transfer_history_no_filters():
    repo = mock.Mock()
    repo.list.return_value = transfer_domain_entities

    trs_history = uc_trs.TransferHistoryUseCase(repo)
    req = rq.TransferHistoRequest.from_dict({})
    resp = trs_history.execute(req)

    repo.list.assert_called_with(filters= None)
    assert bool(resp) is True
    assert resp.value == transfer_domain_entities


def test_transfer_history_with_filters():
    repo = mock.Mock()
    repo.list.return_value = transfer_domain_entities

    trs_history_filtered = uc_trs.TransferHistoryUseCase(repo)
    from_filter = {'trs_from':'1234567890A'}
    req = rq.TransferHistoRequest.from_dict({'filters': from_filter})
    resp = trs_history_filtered.execute(req)

    assert bool(resp) is True
    repo.list.assert_called_with(filters= from_filter)


def test_transfer_history_wrong_request():
    repo = mock.Mock()
    repo.list.return_value = transfer_domain_entities

    trs_history_filtered = uc_trs.TransferHistoryUseCase(repo)
    req = rq.TransferHistoRequest.from_dict({'filters': 0})
    resp = trs_history_filtered.execute(req)

    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'filters : parameter not in the correct format'}


def test_transfer_history_error():
    repo = mock.Mock()
    repo.list.side_effect = Exception('error message')

    trs_history_filtered = uc_trs.TransferHistoryUseCase(repo)
    req = rq.TransferHistoRequest.from_dict({})
    resp = trs_history_filtered.execute(req)

    assert bool(resp) is False
    assert resp.value == {'type': rs.ResponseFailure.SYSTEM_ERROR,
                        'message': 'Exception : error message'}