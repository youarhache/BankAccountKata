import json
from unittest import mock

from bankaccount.usecases import response_objects as resp
from bankaccount.entities.transfer import Transfer

transfer_dict1 = {
        'trs_id':1,
        'trs_timestamp':"2019-01-22 09:00:00",
        'trs_from':"1234567890F",
        'trs_to':"3333333333A",
        'trs_amount':321.00
    }
transfer_dict2 = {
        'trs_id':2,
        'trs_timestamp':"2019-01-22 09:10:20",
        'trs_from':"4444444444C",
        'trs_to':"7765432255B",
        'trs_amount':1234.50
    }
transfer_dict3 = {
        'trs_id':3,
        'trs_timestamp':"2019-01-23 15:05:04",
        'trs_from':"5555555555E",
        'trs_to':"7765432255B",
        'trs_amount':400.00
    }
transfer_dict4 = {
        'trs_id':4,
        'trs_timestamp':"2019-01-24 14:00:59",
        'trs_from':"7777777777A",
        'trs_to':"1111188888B",
        'trs_amount':492.50
    }
trs1 = Transfer.from_dict(transfer_dict1)
trs2 = Transfer.from_dict(transfer_dict2)
trs3 = Transfer.from_dict(transfer_dict3)
trs4 = Transfer.from_dict(transfer_dict4)

test_transfers = [trs1, trs2, trs3, trs4]


@mock.patch('bankaccount.usecases.transfer_usecases.TransferHistoryUseCase')
def test_get_transfers(mock_usecase, client):
    mock_usecase().execute.return_value = resp.ResponseSuccess(test_transfers)
    http_response = client.get('/transfers')

    assert json.loads(http_response.data.decode('UTF-8')) == [transfer_dict1, transfer_dict2, 
                                                            transfer_dict3, transfer_dict4]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('bankaccount.usecases.transfer_usecases.TransferHistoryUseCase')
def test_get_transfers_failure(mock_usecase, client):
    mock_usecase().execute.return_value = resp.ResponseFailure.build_system_error('test error message')
    http_response = client.get('/transfers')

    assert json.loads(http_response.data.decode('UTF-8')) == {'type': resp.ResponseFailure.SYSTEM_ERROR, 
                                                            'message': 'test error message'}
    assert http_response.status_code == 500
    assert http_response.mimetype == 'application/json'


@mock.patch('bankaccount.usecases.transfer_usecases.TransferHistoryUseCase')
def test_get_transfers_with_filters(mock_usecase,client):
    mock_usecase().execute.return_value = resp.ResponseSuccess({})
    request_to_use = mock.Mock()
    with(mock.patch('bankaccount.usecases.request_objects.TransferHistoRequest')) as mock_request:
        mock_request.from_dict.return_value = request_to_use
        http_response = client.get('/transfers?filter_param1=value1&filter_param2=value2')

    mock_request.from_dict.assert_called_with({'filters':{'param1':'value1', 'param2':'value2'}})
    mock_usecase.execute.asset_called_with(request_to_use)
    assert http_response.status_code == 200