import pytest
from unittest import mock
import datetime
import uuid
from .fake_uow import FakeUnitOfWork
from bankaccount.entities.transfer import Transfer
from bankaccount.entities.account import Account
from bankaccount.usecases import (transfer_usecases as uc_trs, 
                                request_objects as rq,
                                response_objects as rs)


@pytest.fixture
def transfer_domain_entities():
    test_trs1 = Transfer(
                        trs_id=uuid.uuid4(),
                        trs_timestamp="2019-01-22 09:00:00",
                        trs_from=Account("1234567890F",1000),
                        trs_to=Account("3333333333A",1000),
                        trs_amount=321.00
    )
    test_trs2 = Transfer(
                        trs_id=uuid.uuid4(),
                        trs_timestamp="2019-01-22 09:10:20",
                        trs_from=Account("4444444444C",2000),
                        trs_to=Account("7765432255B",1000),
                        trs_amount=1234.50
    )
    test_trs3 = Transfer(
                        trs_id=uuid.uuid4(),
                        trs_timestamp="2019-01-23 15:05:04",
                        trs_from=Account("5555555555E",1000),
                        trs_to=Account("6666666666V",1000),
                        trs_amount=400.00
    )
    test_trs4 = Transfer(
                        trs_id=uuid.uuid4(),
                        trs_timestamp="2019-01-24 14:00:59",
                        trs_from=Account("7777777777A",1000),
                        trs_to=Account("1111188888B",1000),
                        trs_amount=492.50
    )

    return [test_trs1, test_trs2, test_trs3, test_trs4]

@pytest.fixture
def unit_of_work():
    uow = FakeUnitOfWork()
    uow.accounts.add_account(Account.from_dict({'code':'1234567890F','balance':1000.00}))
    uow.accounts.add_account(Account.from_dict({'code':'7765432255B','balance':10000.00}))
    return uow

#transfert operation
def test_trs_op_no_param(unit_of_work):
    uowm =unit_of_work

    trs_op = uc_trs.TransferAmountUseCase(uowm)
    req = rq.TransferAmountRequest.from_dict({})
    resp = trs_op.execute(req)

    assert bool(resp) is False
    assert unit_of_work._committed is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'transfer : parameter is required'}


def test_trs_op_success(unit_of_work):
    uowm =unit_of_work
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _trs = {'id':uuid.uuid4(),'timestamp':timestamp, 'from':'1234567890F', 'to':'7765432255B', 'amount':100.00}

    trs_repo = uowm.transfers
    trs_op = uc_trs.TransferAmountUseCase(uowm)
    req = rq.TransferAmountRequest.from_dict({'transfer': _trs})
    resp = trs_op.execute(req)

    assert bool(resp) is True
    assert unit_of_work._committed


def test_trs_op_wrong_param(unit_of_work):
    uowm = unit_of_work

    trs_op = uc_trs.TransferAmountUseCase(uowm)
    req = rq.TransferAmountRequest(trs=0)
    resp = trs_op.execute(req)

    assert bool(resp) is False
    assert unit_of_work._committed is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'transfer : parameter not in the correct format'}


def test_trs_op_payer_is_payee(unit_of_work):
    uowm = unit_of_work
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _trs = {'id':uuid.uuid4(),'timestamp':timestamp, 'from':'1234567890F', 'to':'1234567890F', 'amount':100.00}


    trs_op = uc_trs.TransferAmountUseCase(uowm)
    req = rq.TransferAmountRequest.from_dict({'transfer': _trs})
    resp = trs_op.execute(req)
    
    assert bool(resp) is False
    assert unit_of_work._committed is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': 'payer account must be different than the payee'}


def test_trs_op_account_not_found(unit_of_work):
    uowm = unit_of_work
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _trs = {'id':uuid.uuid4(),'timestamp':timestamp, 'from':'0000000000F', 'to':'7765432255B', 'amount':100.00}

    trs_op = uc_trs.TransferAmountUseCase(uowm)
    req = rq.TransferAmountRequest.from_dict({'transfer': _trs})
    resp = trs_op.execute(req)

    assert bool(resp) is False
    assert unit_of_work._committed is False
    assert resp.value == {'type': rs.ResponseFailure.PARAMETERS_ERROR,
                        'message': "account doesn't exist"}


def test_trs_op_payer_not_debited(unit_of_work):
    with mock.patch.object(unit_of_work.accounts,'account_withdraw', side_effect=Exception('error message')):
        uowm = unit_of_work

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _trs = {'id':uuid.uuid4(),'timestamp':timestamp, 'from':'1234567890F', 'to':'7765432255B', 'amount':100.00}

        trs_op = uc_trs.TransferAmountUseCase(uowm)
        req = rq.TransferAmountRequest.from_dict({'transfer': _trs})
        resp = trs_op.execute(req)

        assert bool(resp) is False
        assert unit_of_work._committed is False
        assert unit_of_work._rolledback
        assert resp.value == {'type': rs.ResponseFailure.SYSTEM_ERROR,
                            'message': 'Exception : error message'}


def test_trs_op_payer_debited_payee_not_credited(unit_of_work):
    with mock.patch.object(unit_of_work._accounts,'account_deposit', side_effect=Exception('error message')): 
        uowm = unit_of_work
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _trs = {'id':uuid.uuid4(),'timestamp':timestamp, 'from':'1234567890F', 'to':'7765432255B', 'amount':100.00}

        trs_op = uc_trs.TransferAmountUseCase(uowm)
        req = rq.TransferAmountRequest.from_dict({'transfer': _trs})
        resp = trs_op.execute(req)

        assert bool(resp) is False
        assert unit_of_work._committed is False
        assert unit_of_work._rolledback
        assert resp.value == {'type': rs.ResponseFailure.SYSTEM_ERROR,
                            'message': 'Exception : error message'}


def test_trs_op_generic_error(unit_of_work):
    with mock.patch.object(unit_of_work._transfers,'add_transfer', side_effect=Exception('error message')):
        uowm = unit_of_work
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _trs = {'id':uuid.uuid4(),'timestamp':timestamp, 'from':'1234567890F', 'to':'7765432255B', 'amount':100.00}

        trs_op = uc_trs.TransferAmountUseCase(uowm)
        req = rq.TransferAmountRequest.from_dict({'transfer': _trs})
        resp = trs_op.execute(req)

        assert bool(resp) is False
        assert unit_of_work._committed is False
        assert unit_of_work._rolledback
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