import datetime
import json
import uuid

import pytest

from src.domain.user import User
from src.serializers import user_serializer as srs


class TestSerializeDomainModelUser:
    def test_serialize(self):
        code = uuid.uuid4()

        user = User(user_id=code, login="user1")

        expected_json = """
            {{
                "user_id": "{}",
                "login": "user1"
            }}
        """.format(
            code
        )

        json_user = json.dumps(user, cls=srs.UserModelEncoder)
        assert json.loads(json_user) == json.loads(expected_json)

    def test_wrong_type(self):
        with pytest.raises(TypeError):
            json.dumps(datetime.datetime.now(), cls=srs.UserModelEncoder)
