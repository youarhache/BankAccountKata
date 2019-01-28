from bankaccount.shared.abstract_entity import AbstractEntity

class Transfer:
    def __init__(self, trs_id, trs_timestamp, trs_from, trs_to, trs_amount):
        self.trs_id = trs_id
        self.trs_timestamp = trs_timestamp
        self.trs_from = trs_from
        self.trs_to = trs_to
        self.trs_amount = trs_amount

    @classmethod
    def from_dict(cls, dict):
        trs = cls(
                    trs_id = dict['trs_id'],
                    trs_timestamp = dict['trs_timestamp'],
                    trs_from = dict['trs_from'],
                    trs_to = dict['trs_to'],
                    trs_amount = dict['trs_amount']
                )
        return trs

    def to_dict(self):
        dict = {
            'trs_id': self.trs_id,
            'trs_timestamp': self.trs_timestamp,
            'trs_from': self.trs_from,
            'trs_to': self.trs_to,
            'trs_amount': self.trs_amount
        }
        return dict

    def __eq__(self, other):
        return self.to_dict()==other.to_dict()

AbstractEntity.register(Transfer)