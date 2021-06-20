class InvalidRequestObject(object):
    def __init__(self):
        self.errors = []

    def add_error(self, parameter, message):
        self.errors.append({"parameter": parameter, "message": message})

    def has_errors(self):
        return len(self.errors) > 0

    def __bool__(self):
        return False


class ValidRequestObject(object):
    @classmethod
    def from_dict(cls, input_dict):
        raise NotImplementedError

    def __bool__(self):
        return True
