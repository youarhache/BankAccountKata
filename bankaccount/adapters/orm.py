import uuid
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, FLOAT, CHAR, ForeignKey
from sqlalchemy.orm import mapper, scoped_session, sessionmaker, relationship, backref, clear_mappers
import sqlalchemy.exc
import sqlalchemy.orm.exc
from sqlalchemy_utils.functions import create_database, drop_database
from sqlalchemy_utils.types.uuid import UUIDType

from bankaccount.repositories.db_uow import DbUnitOfWorkManager
from bankaccount.repositories.db_repo_account import DbRepoAccounts
from bankaccount.repositories.db_repo_transfer import DbRepoTrs
from bankaccount.entities.account import Account
from bankaccount.entities.transfer import Transfer


class SqlAlchemy:

    def __init__(self, uri):
        self.engine = create_engine(uri)
        self._session_maker = scoped_session(sessionmaker(self.engine))

    @property
    def unit_of_work_manager(self):
        return DbUnitOfWorkManager(self._session_maker)

    def recreate_schema(self):
        drop_database(self.engine.url)
        self.create_schema()

    def create_schema(self):
        create_database(self.engine.url)
        self.metadata.create_all()

    def get_session(self):
        return self._session_maker()

    def configure_mappings(self):
        clear_mappers()
        self.metadata = MetaData(self.engine)

        accounts = Table('accounts', self.metadata,
                       Column('pk', Integer, primary_key=True),
                       Column('account_code', String(11)),
                       Column('account_balance', FLOAT))

        transfers = Table('transfers', self.metadata,
                       Column('pk', Integer, primary_key=True),
                       Column('id', CHAR(32)),
                       Column('timestamp', String(17)),
                       Column('account_from_id', Integer, ForeignKey('accounts.pk')),
                       Column('account_to_id', Integer, ForeignKey('accounts.pk')),
                       Column('amount', FLOAT)
                       )

        mapper(
            Account,
            accounts,
            properties={
                '__pk': accounts.c.pk,
                'code': accounts.c.account_code,
                'balance': accounts.c.account_balance
            },
        )
        mapper(
        Transfer,
            transfers,
            properties={
                '__pk': transfers.c.pk,
                'trs_id': transfers.c.id,
                'trs_timestamp': transfers.c.timestamp,
                'trs_amount': transfers.c.amount,
                'trs_from': relationship(Account, foreign_keys=[transfers.c.account_from_id], backref=backref("account_from", uselist=False)),
                'trs_to': relationship(Account, foreign_keys=[transfers.c.account_to_id], backref=backref("account_to", uselist=False))
            },
        )