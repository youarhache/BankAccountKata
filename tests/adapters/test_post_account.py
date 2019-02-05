import json
from unittest import mock

from bankaccount.usecases import response_objects as resp
from bankaccount.entities.account import Account


test_account = Account(
        account_code="1234567890F",
        account_balance=10000.00
    )

mimetype = 'application/json'

headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
data = {
        'code': '1234567890F',
        'amount': 10000.00
    }

@mock.patch('bankaccount.usecases.account_usecases.AccountCreationUseCase')
def test_post_account_success(mock_usecase, client):
    mock_usecase().execute.return_value = resp.ResponseSuccess(test_account)
    http_response = client.post('/account', data=json.dumps(data), headers=headers)

    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('bankaccount.usecases.account_usecases.AccountCreationUseCase')
def test_post_account_failure(mock_usecase, client):
    mock_usecase().execute.return_value = resp.ResponseFailure.build_system_error('test error message')
    http_response = client.post('/account', data=json.dumps(data), headers=headers)

    assert json.loads(http_response.data.decode('UTF-8')) == {'type': resp.ResponseFailure.SYSTEM_ERROR, 
                                                            'message': 'test error message'}
    assert http_response.status_code == 500
    assert http_response.mimetype == 'application/json'