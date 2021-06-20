import pytest

from src.repository import memrepo
from src.shared.domain_model_abc import DomainModel


@pytest.fixture
def user_dicts():
    return [
        {
            "user_id": "305a6c67-8bea-4994-81ed-b6511c4b181f",
            "login": "user1",
        },
        {
            "user_id": "f30dcc11-6f48-4bfb-a17e-f90b9d566c03",
            "login": "user2",
        },
        {
            "user_id": "de9538b3-98f7-4469-b111-2ac64170c84f",
            "login": "user3",
        },
    ]


def _check_results(domain_models_list, data_list):
    assert len(domain_models_list) == len(data_list)
    assert all([isinstance(dm, DomainModel) for dm in domain_models_list])
    assert set([dm.login for dm in domain_models_list]) == set(
        [d["login"] for d in data_list]
    )


class TestMemrepoList:
    def test_without_parameters(self, user_dicts):
        repo = memrepo.MemRepo(user_dicts)
        _check_results(repo.list(), user_dicts)

    def test_with_filters_unknown_key(self, user_dicts):
        repo = memrepo.MemRepo(user_dicts)

        with pytest.raises(KeyError):
            repo.list(filters={"/": "unexpected param"})

    def test_with_filters_unknown_operator(self, user_dicts):
        repo = memrepo.MemRepo(user_dicts)

        with pytest.raises(ValueError):
            repo.list(filters={"login__in": [20, 30]})

    def test_with_filters_login(self, user_dicts):
        repo = memrepo.MemRepo(user_dicts)

        _check_results(repo.list(filters={"login": "user3"}), [user_dicts[2]])

    def test_with_filters_login_eq(self, user_dicts):
        repo = memrepo.MemRepo(user_dicts)

        _check_results(repo.list(filters={"login": "user3"}), [user_dicts[2]])

    def test_with_filters_user_id(self, user_dicts):
        repo = memrepo.MemRepo(user_dicts)

        _check_results(
            repo.list(filters={"user_id": "de9538b3-98f7-4469-b111-2ac64170c84f"}),
            [user_dicts[2]],
        )
