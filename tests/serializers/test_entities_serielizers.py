import json
import pytest

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
    test_trs = Transfer(
                        trs_id=1,
                        trs_timestamp="2019-01-22 09:00:00",
                        trs_from="2222222222M",
                        trs_to="1111111111V",
                        trs_amount=321.45
    )
    expected = """
            {
                "trs_id":1,
                "trs_timestamp":"2019-01-22 09:00:00",
                "trs_from":"2222222222M",
                "trs_to":"1111111111V",
                "trs_amount":321.45
            }"""

    json_trs = json.dumps(test_trs, cls=TransferEncoder)
    assert json.loads(json_trs) == json.loads(expected)