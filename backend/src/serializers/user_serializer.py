import json


class UserModelEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "user_id": str(o.user_id),
                "login": o.login,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
