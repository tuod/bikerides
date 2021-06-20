import uuid
from unittest import mock

import pytest

from src.domain.user import User
from src.use_cases import request_objects as req
from src.use_cases import user_use_cases as uc


@pytest.fixture
def domain_user_list():
    user_1 = User(
        login="user1",
        user_id=uuid.uuid4(),
    )
    user_2 = User(
        login="user1",
        user_id=uuid.uuid4(),
    )
    return [user_1, user_2]


class TestUserListUseCase:
    def test_without_params(self, domain_user_list):
        repo = mock.Mock()
        repo.list.return_value = domain_user_list

        user_list_use_case = uc.UserListUseCase(repo)
        request_object = req.UserListRequestObject.from_dict({})
        response_object = user_list_use_case.execute(request_object)

        assert bool(response_object) is True
        repo.list.assert_called_with(filters=None)

        assert response_object.value == domain_user_list
