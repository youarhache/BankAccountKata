import datetime
from bankaccount.entities.transfer import Transfer
from bankaccount.repositories.db_repo_account import DbRepoAccounts

class DbRepoTrs:
    def __init__(self, db_session):
        self._session = db_session

    def add_transfer(self, trs=None):
        if trs:
            self._session.add(trs)
        else : 
            raise AttributeError("Transfer to add can't be None")
 
    def list(self, filters=None):
        if not filters:
            result = self._session.query(Transfer).all()
        else:
            result = None
            _q = self._session.query(Transfer)
            for key, value in filters.items():
                _acc_repo = DbRepoAccounts(self._session)
                if key == 'trs_from':
                    acc = _acc_repo.find_account(value)
                    _q = _q.filter_by(trs_from=acc) 
                elif key == 'trs_to':
                    acc = _acc_repo.find_account(value)
                    _q = _q.filter_by(trs_to=value) 
                else:
                    raise AttributeError(f'Attribure {key} not recognized')
            result = _q.all()
        return result

    