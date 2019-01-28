import pytest

from bankaccount.shared.abstract_entity import AbstractEntity
from bankaccount.entities.transfer import Transfer
from bankaccount.repository import mem_repo_trs

@pytest.fixture
def transfers_dicos():
    return [
    {
        'trs_id':1,
        'trs_timestamp':"2019-01-22 09:00:00",
        'trs_from':"1234567890F",
        'trs_to':"3333333333A",
        'trs_amount':321.00
    },
    {
        'trs_id':2,
        'trs_timestamp':"2019-01-22 09:10:20",
        'trs_from':"4444444444C",
        'trs_to':"7765432255B",
        'trs_amount':1234.50
    },
    {
        'trs_id':3,
        'trs_timestamp':"2019-01-23 15:05:04",
        'trs_from':"5555555555E",
        'trs_to':"7765432255B",
        'trs_amount':400.00
    },
    {
        'trs_id':4,
        'trs_timestamp':"2019-01-24 14:00:59",
        'trs_from':"7777777777A",
        'trs_to':"1111188888B",
        'trs_amount':492.50
    }]

def _check_results(domain_entities_list, data_list):
    """
        Helper function to compare the lenght of the two lists, 
        check that the elements are domaine entities using isinstance
        and finally that the same entities are present in both lists by comparing ids

        Parameters:
            domain_entities_list: a list of entities returned by the repository
            data_list: expected list

    """
    assert len(domain_entities_list) == len(data_list)
    assert all([isinstance(entity, AbstractEntity) for entity in domain_entities_list])
    assert set([entity.trs_id for entity in domain_entities_list]) == set([d['trs_id'] for d in data_list])


def test_repository_list_no_params(transfers_dicos):
    repo = mem_repo_trs.MemRepoTrs(transfers_dicos)
    _check_results(repo.list(), transfers_dicos)


def test_repository_list_with_filters_unknown_key(transfers_dicos):
    repo = mem_repo_trs.MemRepoTrs(transfers_dicos)

    with pytest.raises(KeyError):
        repo.list(filters={'toto': 'test'})


def test_transfer_repo_list_with_filters_from(transfers_dicos):
    repo = mem_repo_trs.MemRepoTrs(transfers_dicos)
    trs_list = repo.list(filters={'trs_from':'1234567890F'})

    _check_results(trs_list, [transfers_dicos[0]])


def test_transfer_repo_list_with_filters_to(transfers_dicos):
    repo = mem_repo_trs.MemRepoTrs(transfers_dicos)
    trs_list = repo.list(filters={'trs_to':'7765432255B'})

    _check_results(trs_list, [transfers_dicos[1], transfers_dicos[2]])


#add trasfer
def test_repo_add_transfert_success(transfers_dicos):
    repo = mem_repo_trs.MemRepoTrs(transfers_dicos)
    l = len(repo._entries)
    result = repo.add_transfer({'from':'1234567890F', 'to':'7765432255B', 'amount':190.00})

    assert len(repo._entries) == l+1
    assert isinstance(result, AbstractEntity)
    assert result.trs_from == '1234567890F'
    assert result.trs_to == '7765432255B'
    assert result.trs_amount == 190.00



def test_repo_add_transfert_no_params(transfers_dicos):
    repo = mem_repo_trs.MemRepoTrs(transfers_dicos)
    l = len(repo._entries)
    result = repo.add_transfer()

    assert result is None
    assert len(repo._entries) == l


def test_repo_add_transfert_wrong_params(transfers_dicos):
    repo = mem_repo_trs.MemRepoTrs(transfers_dicos)
    l = len(repo._entries)
    result = repo.add_transfer(trs=0)

    assert result is None
    assert len(repo._entries) == l