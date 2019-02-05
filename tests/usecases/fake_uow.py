from .fake_repo_trs import MemRepoTrs
from .fake_repo_account import MemRepoAccounts
from bankaccount.shared.abstract_uow import UnitOfWork, UnitOfWorkManager


class FakeUnitOfWork(UnitOfWork, UnitOfWorkManager):
    def __init__(self, session_mkr=None):
        self._accounts = MemRepoAccounts()
        self._transfers = MemRepoTrs()

    def start(self):
        self._committed = False
        self._rolledback = False
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.exn_type = type
        self.exn = value
        self.traceback = traceback

    def commit(self):
        self._committed = True

    def rollback(self):
        self._rolledback = True

    @property
    def accounts(self):
        return self._accounts

    @property
    def transfers(self):
        return self._transfers