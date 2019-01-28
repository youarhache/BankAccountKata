import datetime
from bankaccount.entities.transfer import Transfer

class MemRepoTrs:
    def __init__(self, entries=None):
        self._entries = []
        if entries:
            self._entries.extend(entries)
    
    
    def _apply_filter(self, elem, key, value):
        return elem[key] == value
    

    def add_transfer(self, trs=None):
        _timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _id = len(self._entries)+1
        if trs:
            _new_trs = {'trs_id':_id, 
                        'trs_timestamp': _timestamp,
                        'trs_from': trs['from'],
                        'trs_to':trs['to'],
                        'trs_amount':trs['amount']}
            self._entries.append(_new_trs)
            return Transfer.from_dict(_new_trs)
        return None

 
    def list(self, filters=None):
        if not filters:
            result = self._entries
        else:
            result = []
            result.extend(self._entries)

            for key, value in filters.items():
                result = [e for e in result if self._apply_filter(e, key, value)]

        return [Transfer.from_dict(r) for r in result]

    