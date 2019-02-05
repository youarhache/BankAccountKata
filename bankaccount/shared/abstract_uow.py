import abc


class UnitOfWorkManager(abc.ABC):
    @abc.abstractmethod
    def start(self):
        pass


class UnitOfWork(abc.ABC):
    @abc.abstractmethod
    def __enter__(self):
        pass

    @abc.abstractmethod
    def __exit__(self, type, value, traceback):
        pass

    @abc.abstractmethod
    def commit(self):
        pass

    @abc.abstractmethod
    def rollback(self):
        pass

    @property
    def accounts(self):
        pass

    @property
    def transfers(self):
        pass