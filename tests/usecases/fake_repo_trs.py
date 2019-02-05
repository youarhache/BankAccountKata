import datetime
from bankaccount.entities.transfer import Transfer

class MemRepoTrs:
    def __init__(self, db_session=None, entries=None):
        self._entries = []
        if entries:
            self._entries.extend(entries)
    
    
    def _apply_filter(self, elem, key, value):
        return elem[key] == value
    

    def add_transfer(self, trs=None):
        if trs:
            self._entries.append(trs.to_dict())

 
    def list(self, filters=None):
        if not filters:
            result = self._entries
        else:
            result = []
            result.extend(self._entries)

            for key, value in filters.items():
                result = [e for e in result if self._apply_filter(e, key, value)]

        return [Transfer.from_dict(r) for r in result]

    