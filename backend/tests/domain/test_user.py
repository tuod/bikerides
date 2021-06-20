import pytest

from src.domain.user import User


@pytest.fixture
def user_dict():
    return {"login": "login", "user_id": "user_id"}


class TestUserModel:
    def test_init(self):
        user = User(
            login="login",
            user_id="user_id",
        )
        assert user.login == "login"
        assert user.user_id == "user_id"

    def test_from_dict(self, user_dict):
        user = User.from_dict(user_dict)
        assert user.login == "login"
        assert user.user_id == "user_id"

    def test_to_dict(self, user_dict):
        user = User.from_dict(user_dict)
        assert user.to_dict() == user_dict

    def test_comparison(self, user_dict):
        user1 = User.from_dict(user_dict)
        user2 = User.from_dict(user_dict)
        assert user1 == user2
