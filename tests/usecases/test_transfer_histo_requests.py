from bankaccount.usecases import request_objects as ro

def test_transfer_list_request_no_params():
    req = ro.TransferHistoRequest()

    assert req.filters is None
    assert bool(req) is True


def test_transfer_list_request_from_empty_dict():
    req = ro.TransferHistoRequest.from_dict({})

    assert req.filters is None
    assert bool(req) is True


def test_transfer_list_request_empty_filters():
    req = ro.TransferHistoRequest(filters={})

    assert req.filters == {}
    assert bool(req) is True


def test_transfer_list_request_from_dict_empty_filters():
    req = ro.TransferHistoRequest.from_dict({'filters': {}})

    assert req.filters == {}
    assert bool(req) is True


def test_transfer_list_request_with_filters():
    req = ro.TransferHistoRequest(filters={'trs_from': '1111111111V', 'trs_to': '2222222222F'})

    assert req.filters == {'trs_from': '1111111111V', 'trs_to': '2222222222F'}
    assert bool(req) is True


def test_transfer_list_request_from_dict_with_filters():
    req = ro.TransferHistoRequest.from_dict({'filters':{'trs_from': '1111111111V', 'trs_to': '2222222222F'}})

    assert req.filters == {'trs_from': '1111111111V', 'trs_to': '2222222222F'}
    assert bool(req) is True


def test_transfer_list_request_wrong_filters():
    req = ro.TransferHistoRequest(filters='')

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'filters'
    assert bool(req) is False
