from bankaccount.usecases import request_objects as ro

def test_transfer_amount_request_no_params():
    req = ro.TransferAmountRequest()

    assert req.has_errors()
    assert bool(req) is False
    assert req.errors[0]['parameter'] == 'transfer'
    assert req.errors[0]['message'] == 'parameter is required'


def test_transfer_amount_request_from_empty_dict():
    req = ro.TransferAmountRequest.from_dict({})

    assert req.has_errors()
    assert bool(req) is False
    assert req.errors[0]['parameter'] == 'transfer'
    assert req.errors[0]['message'] == 'parameter is required'


def test_transfer_amount_request_empty_params():
    req = ro.TransferAmountRequest(trs={})

    assert req.has_errors()
    assert bool(req) is False
    assert req.errors[0]['parameter'] == 'transfer'
    assert req.errors[0]['message'] == 'a required attribute is missing'


def test_transfer_amount_request_from_dict_empty_params():
    req = ro.TransferAmountRequest.from_dict({'transfer': {}})

    assert req.has_errors()
    assert bool(req) is False
    assert req.errors[0]['parameter'] == 'transfer'
    assert req.errors[0]['message'] == 'a required attribute is missing'


def test_transfer_amount_request_wrong_format():
    req = ro.TransferAmountRequest(trs='')

    assert req.has_errors()
    assert bool(req) is False
    assert req.errors[0]['parameter'] == 'transfer'
    assert req.errors[0]['message'] == 'parameter not in the correct format'


def test_transfer_amount_request_with_correct_params():
    _trs = {'id': '0e101bfe-724f-4e1c-9ac3-6e4f67608c74', 'timestamp': '2018-01-29 10:34:55',
            'from': '1111111111V','to': '2222222222D',  'amount': 100.00}
    req = ro.TransferAmountRequest(trs=_trs)

    assert req.transfer == _trs
    assert bool(req) is True


def test_transfer_amount_request_from_dict_with_params():
    _trs = {'id': '0e101bfe-724f-4e1c-9ac3-6e4f67608c74', 'timestamp': '2018-01-29 10:34:55',
            'from': '1111111111V','to': '2222222222D',  'amount': 100.00}
    req = ro.TransferAmountRequest.from_dict({'transfer':_trs})

    assert req.transfer == _trs
    assert bool(req) is True


def test_transfer_amount_request_wrong_account_code():
    _trs = {'id': '0e101bfe-724f-4e1c-9ac3-6e4f67608c74', 'timestamp': '2018-01-29 10:34:55',
            'from': '1111111111V','to': '',  'amount': 100.00}
    req = ro.TransferAmountRequest(trs=_trs)

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'transfer'
    assert req.errors[0]['message'] == "account codes can't be empty"
    assert bool(req) is False


def test_transfer_amount_request_wrong_id():
    _trs = {'id': '', 'timestamp': '2018-01-29 10:34:55',
            'from': '1111111111V','to': '2222222222D',  'amount': 100.00}
    req = ro.TransferAmountRequest(trs=_trs)

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'transfer'
    assert req.errors[0]['message'] == "ID can't be empty"
    assert bool(req) is False


def test_transfer_amount_request_wrong_account_amount():
    _trs = {'id': '0e101bfe-724f-4e1c-9ac3-6e4f67608c74', 'timestamp': '2018-01-29 10:34:55',
            'from': '1111111111V','to': '2222222222D',  'amount': '100.00 EUR'}
    req = ro.TransferAmountRequest(trs=_trs)

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'transfer'
    assert req.errors[0]['message'] == "amount must be a positive number"
    assert bool(req) is False


def test_account_request_negative_account_amount():
    _trs = {'id': '0e101bfe-724f-4e1c-9ac3-6e4f67608c74', 'timestamp': '2018-01-29 10:34:55',
            'from': '1111111111V','to': '2222222222D',  'amount': -300.00}
    req = ro.TransferAmountRequest(trs=_trs)

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'transfer'
    assert req.errors[0]['message'] == "amount must be a positive number"
    assert bool(req) is False