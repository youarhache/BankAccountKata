import pytest
from bankaccount.usecases import response_objects as ro
from bankaccount.usecases import request_objects as rq

@pytest.fixture
def response_value():
    return {'key': ['value1', 'value2']}


@pytest.fixture
def response_type():
    return 'ResponseError'


@pytest.fixture
def response_msg():
    return 'a response error message'


def test_response_success():
    assert bool(ro.ResponseSuccess) is True


def test_response_success_is_true(response_value):
    assert bool(ro.ResponseSuccess(response_value)) is True


def test_response_failure_is_false(response_type, response_msg):
    assert bool(ro.ResponseFailure(response_type, response_msg)) is False


def test_response_success_value(response_value):
    resp = ro.ResponseSuccess(response_value)
    assert resp.value == response_value


def test_response_failure_value(response_type, response_msg):
    resp = ro.ResponseFailure(response_type, response_msg)
    assert resp.value == {'type':response_type, 'message': response_msg}


def test_response_failure_attributes(response_type, response_msg):
    resp = ro.ResponseFailure(response_type, response_msg)
    
    assert resp.message == response_msg
    assert resp.type == response_type


def test_response_failure_from_exception(response_type):
    resp = ro.ResponseFailure(response_type, Exception("exception message"))

    assert resp.type == response_type
    assert resp.message == 'Exception : exception message'
    assert bool(resp) is False


def test_response_failure_from_invalide_request():
    req = rq.TransferHistoRequest()
    req.add_error('param1', 'error in param1 message')
    req.add_error('param2', 'error in param2 message')
    resp = ro.ResponseFailure.from_invalid_request(req)

    assert bool(resp) is False
    assert resp.type == ro.ResponseFailure.PARAMETERS_ERROR
    assert resp.message == 'param1 : error in param1 message\nparam2 : error in param2 message'


def test_build_response_failure_parameters_error():
    resp  = ro.ResponseFailure.build_parameters_error('parameters error message')

    assert bool(resp) is False
    assert resp.type == ro.ResponseFailure.PARAMETERS_ERROR
    assert resp.message == 'parameters error message'


def test_build_response_failure_resource_error():
    resp  = ro.ResponseFailure.build_resource_error('resource error message')

    assert bool(resp) is False
    assert resp.type == ro.ResponseFailure.RESOURCE_ERROR
    assert resp.message == 'resource error message'


def test_build_response_failure_system_error():
    resp  = ro.ResponseFailure.build_system_error('system error message')

    assert bool(resp) is False
    assert resp.type == ro.ResponseFailure.SYSTEM_ERROR
    assert resp.message == 'system error message'