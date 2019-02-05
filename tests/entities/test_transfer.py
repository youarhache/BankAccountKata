import uuid
from bankaccount.entities.account import Account
from bankaccount.entities.transfer import Transfer


acc1 = Account('1111111111V', 1500.00)
acc2 = Account('2222222222M', 3200.00)

def test_transfer_entity_init():
    id = uuid.uuid4()
    trs = Transfer( 
                    trs_id = id,
                    trs_timestamp = '2019-01-21 00:00:00',
                    trs_from = acc1,
                    trs_to =  acc2,
                    trs_amount=45.30)

    assert trs.trs_id == id
    assert trs.trs_timestamp == '2019-01-21 00:00:00'
    assert trs.trs_from == acc1
    assert trs.trs_to == acc2
    assert trs.trs_amount == 45.30

def test_transfer_from_dict(): 
    id = uuid.uuid4()
    dict = {
            'trs_id': id,
            'trs_timestamp': '2019-01-21 09:00:00',
            'trs_from': acc1.to_dict(),
            'trs_to': acc2.to_dict(),
            'trs_amount': 100.00
        }
    trs = Transfer.from_dict(dict)

    assert trs.trs_id == id
    assert trs.trs_timestamp == '2019-01-21 09:00:00'
    assert trs.trs_from == acc1
    assert trs.trs_to == acc2
    assert trs.trs_amount == 100.00

def test_transfer_to_dict():
    dict = {
            'trs_id': uuid.uuid4(),
            'trs_timestamp': '2019-01-21 09:00:00',
            'trs_from':  acc1.to_dict(),
            'trs_to':  acc2.to_dict(),
            'trs_amount': 100.00
        }

    trs = Transfer.from_dict(dict)

    assert dict == trs.to_dict()

def test_transfer_comparison():
    dict = {
            'trs_id': uuid.uuid4(),
            'trs_timestamp': '2019-01-21 09:00:00',
            'trs_from':  acc1.to_dict(),
            'trs_to':  acc2.to_dict(),
            'trs_amount': 100.00
        }
    trs1 = Transfer.from_dict(dict)
    trs2 = Transfer.from_dict(dict)

    assert trs1 == trs2