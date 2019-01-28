import json
from unittest import mock

from bankaccount.usecases import response_objects as resp
from bankaccount.entities.transfer import Transfer


test_trs = Transfer(
        trs_id=1,
        trs_timestamp="2019-01-22 09=00=00",
        trs_from="1234567890F",
        trs_to="3333333333A",
        trs_amount=321.00
    )

mimetype = 'application/json'
headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
data = {
        'from': '1234567890F',
        'to': '3333333333A',
        'amount': 321.00
    }

@mock.patch('bankaccount.usecases.transfer_usecases.TransferAmountUseCase')
def test_post_transfer(mock_usecase, client):
    mock_usecase().execute.return_value = resp.ResponseSuccess(test_trs)
    http_response = client.post('/transfer', data=json.dumps(data), headers=headers)

    assert json.loads(http_response.data.decode('UTF-8')) == test_trs.to_dict()
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('bankaccount.usecases.transfer_usecases.TransferAmountUseCase')
def test_post_transfer_failure(mock_usecase, client):
    mock_usecase().execute.return_value = resp.ResponseFailure.build_system_error('test error message')
    http_response = client.post('/transfer', data=json.dumps(data), headers=headers)

    assert json.loads(http_response.data.decode('UTF-8')) == {'type': resp.ResponseFailure.SYSTEM_ERROR, 
                                                            'message': 'test error message'}
    assert http_response.status_code == 500
    assert http_response.mimetype == 'application/json'
