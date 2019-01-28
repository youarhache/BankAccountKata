from bankaccount.usecases import request_objects as ro

def test_account_create_request_no_params():
    req = ro.AccountOperationRequest()

    assert req.has_errors()
    assert bool(req) is False
    assert req.errors[0]['parameter'] == 'account'
    assert req.errors[0]['message'] == 'parameter is required'


def test_account_create_request_from_empty_dict():
    req = ro.AccountOperationRequest.from_dict({})

    assert req.has_errors()
    assert bool(req) is False
    assert req.errors[0]['parameter'] == 'account'
    assert req.errors[0]['message'] == 'parameter is required'


def test_account_create_request_empty_params():
    req = ro.AccountOperationRequest(account={})

    assert req.has_errors()
    assert bool(req) is False
    assert req.errors[0]['parameter'] == 'account'
    assert req.errors[0]['message'] == 'account code and amount are required'


def test_account_create_request_from_dict_empty_params():
    req = ro.AccountOperationRequest.from_dict({'account': {}})

    assert req.has_errors()
    assert bool(req) is False
    assert req.errors[0]['parameter'] == 'account'
    assert req.errors[0]['message'] == 'account code and amount are required'


def test_account_create_request_wrong_format():
    req = ro.AccountOperationRequest(account='')

    assert req.has_errors()
    assert bool(req) is False
    assert req.errors[0]['parameter'] == 'account'
    assert req.errors[0]['message'] == 'parameter not in the correct format'


def test_account_create_request_with_correct_params():
    req = ro.AccountOperationRequest(account={'code': '1111111111V', 'amount': 100.00})

    assert req.account == {'code': '1111111111V', 'amount': 100.00}
    assert bool(req) is True


def test_account_create_request_from_dict_with_params():
    req = ro.AccountOperationRequest.from_dict({'account':{'code': '2222222222F', 'amount': 50.00}})

    assert req.account == {'code': '2222222222F', 'amount': 50.00}
    assert bool(req) is True


def test_account_create_request_wrong_account_code():
    req = ro.AccountOperationRequest(account={'code': '', 'amount': 100.00})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'account'
    assert req.errors[0]['message'] == "account code can't be empty"
    assert bool(req) is False

def test_account_create_request_wrong_account_amount():
    req = ro.AccountOperationRequest(account={'code': '1111111111V', 'amount': '100.00 EUR'})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'account'
    assert req.errors[0]['message'] == "amount must be a positive number"
    assert bool(req) is False

def test_account_request_negative_account_amount():
    req = ro.AccountOperationRequest(account={'code': '1111111111V', 'amount': -300.00})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'account'
    assert req.errors[0]['message'] == "amount must be a positive number"
    assert bool(req) is False