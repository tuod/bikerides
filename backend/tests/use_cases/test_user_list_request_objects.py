from src.use_cases import request_objects as ro


class TestBuildUserListRequestObject:
    def test_without_parameters(self):
        req = ro.UserListRequestObject()

        assert req.filters is None
        assert bool(req) is True

    def test_from_empty_dict(self):
        req = ro.UserListRequestObject.from_dict({})

        assert req.filters is None
        assert bool(req) is True

    def test_with_empty_filters(self):
        req = ro.UserListRequestObject(filters={})

        assert req.filters == {}
        assert bool(req) is True

    def test_from_dict_with_empty_filters(self):
        req = ro.UserListRequestObject.from_dict({"filters": {}})

        assert req.filters == {}
        assert bool(req) is True

    def test_with_filters(self):
        req = ro.UserListRequestObject(filters={"a": 1, "b": 2})

        assert req.filters == {"a": 1, "b": 2}
        assert bool(req) is True

    def test_from_dict_with_filters(self):
        req = ro.UserListRequestObject.from_dict({"filters": {"a": 1, "b": 2}})

        assert req.filters == {"a": 1, "b": 2}
        assert bool(req) is True

    def test_from_dict_with_invalid_filters(self):
        req = ro.UserListRequestObject.from_dict({"filters": 5})

        assert req.has_errors()
        assert req.errors[0]["parameter"] == "filters"
        assert bool(req) is False
