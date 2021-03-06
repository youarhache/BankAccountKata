import json
import pytest
import uuid

from bankaccount.serializers.account_serializer import AccountEncoder
from bankaccount.serializers.transfer_serializer import TransferEncoder
from bankaccount.entities.account import Account
from bankaccount.entities.transfer import Transfer

def test_account_serielizer():
    test_account = Account(account_code = "1234556789V", account_balance = 12340.00)
    expected = '{"code" : "1234556789V", "balance" : 12340.00}'

    json_account = json.dumps(test_account, cls=AccountEncoder)
    assert json.loads(json_account) == json.loads(expected)

def test_transfer_serielizer():
    _id = str(uuid.uuid4())
    test_trs = Transfer(
                        trs_id=_id,
                        trs_timestamp="2019-01-22 09:00:00",
                        trs_from=Account.from_dict({"code":"222222222M", "balance":1000}),
                        trs_to=Account.from_dict({"code":"1111111111V", "balance":1000}),
                        trs_amount=321.45
    )
    expected = '''
            {
                "trs_id":"'''+_id+'''",
                "trs_timestamp":"2019-01-22 09:00:00",
                "trs_from":{"code":"222222222M", "balance":1000},
                "trs_to":{"code":"1111111111V", "balance":1000},
                "trs_amount":321.45
            }'''

    json_trs = json.dumps(test_trs, cls=TransferEncoder)
    assert json.loads(json_trs) == json.loads(expected)