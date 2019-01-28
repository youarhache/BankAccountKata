from bankaccount.entities.transfer import Transfer

def test_transfer_entity_init():
    trs = Transfer( 
                    trs_id = 52,
                    trs_timestamp = '2019-01-21 00:00:00',
                    trs_from = '11111 111111V',
                    trs_to =  '22222 222222M',
                    trs_amount=45.30)

    assert trs.trs_id == 52
    assert trs.trs_timestamp == '2019-01-21 00:00:00'
    assert trs.trs_from == '11111 111111V'
    assert trs.trs_to == '22222 222222M'
    assert trs.trs_amount == 45.30

def test_transfer_from_dict(): 
    dict = {
            'trs_id': 33,
            'trs_timestamp': '2019-01-21 09:00:00',
            'trs_from': '22222 222222M',
            'trs_to': '11111 111111V',
            'trs_amount': 100.00
        }
    trs = Transfer.from_dict(dict)

    assert trs.trs_id == 33
    assert trs.trs_timestamp == '2019-01-21 09:00:00'
    assert trs.trs_from == '22222 222222M'
    assert trs.trs_to == '11111 111111V'
    assert trs.trs_amount == 100.00

def test_transfer_to_dict():
    dict = {
            'trs_id': 33,
            'trs_timestamp': '2019-01-21 09:00:00',
            'trs_from': '22222 222222M',
            'trs_to': '11111 111111V',
            'trs_amount': 100.00
        }

    trs = Transfer.from_dict(dict)

    assert dict == trs.to_dict()

def test_transfer_comparison():
    dict = {
            'trs_id': 33,
            'trs_timestamp': '2019-01-21 09:00:00',
            'trs_from': '22222 222222M',
            'trs_to': '11111 111111V',
            'trs_amount': 100.00
        }
    trs1 = Transfer.from_dict(dict)
    trs2 = Transfer.from_dict(dict)

    assert trs1 == trs2