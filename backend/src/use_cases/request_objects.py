import collections.abc

from src.shared import request_object as req


class UserListRequestObject(req.ValidRequestObject):
    def __init__(self, filters=None):
        self.filters = filters

    @classmethod
    def from_dict(cls, input_dict):
        invalid_req = req.InvalidRequestObject()

        if "filters" in input_dict and not isinstance(
            input_dict["filters"], collections.abc.Mapping
        ):
            invalid_req.add_error("filters", "Is not iterable")

        if invalid_req.has_errors():
            return invalid_req

        return UserListRequestObject(filters=input_dict.get("filters", None))
