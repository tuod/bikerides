from src.shared.domain_model_abc import DomainModel


class User(DomainModel):
    def __init__(self, login, user_id):
        self.login = login
        self.user_id = user_id

    @classmethod
    def from_dict(cls, input_dict):
        return User(
            login=input_dict["login"],
            user_id=input_dict["user_id"],
        )

    def to_dict(self):
        return {
            "login": self.login,
            "user_id": self.user_id,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
