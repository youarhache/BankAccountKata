from sqlalchemy.orm import mapper, scoped_session, sessionmaker, composite
from bankaccount.repositories.db_repo_transfer import DbRepoTrs
from bankaccount.repositories.db_repo_account import DbRepoAccounts
from bankaccount.shared.abstract_uow import UnitOfWork, UnitOfWorkManager

class DbUnitOfWorkManager(UnitOfWorkManager):
    def __init__(self, session_mkr):
        self._session_maker = session_mkr

    def start(self):
        return DbUnitOfWork(self._session_maker)


class DbUnitOfWork(UnitOfWork):
    def __init__(self, sessionfactory):
        self._sessionfactory = sessionfactory

    def __enter__(self):
        self.session = self._sessionfactory()
        return self

    def __exit__(self, type, value, traceback):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    @property
    def accounts(self):
        return DbRepoAccounts(self.session)

    @property
    def transfers(self):
        return DbRepoTrs(self.session)