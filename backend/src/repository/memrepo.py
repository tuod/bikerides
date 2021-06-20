from src.domain import user as model


class MemRepo:
    def __init__(self, entries=None):
        self._entries = []
        if entries:
            self._entries.extend(entries)

    @staticmethod
    def _check(element, key, value):
        if "__" not in key:
            key = key + "__eq"

        key, operator = key.split("__")

        if operator not in ["eq"]:
            raise ValueError("Operator {} is not supported".format(operator))

        operator = "__{}__".format(operator)

        # if key in ['size', 'price']:
        #     return getattr(element[key], operator)(int(value))
        # elif key in ['latitude', 'longitude']:
        #     return getattr(element[key], operator)(float(value))

        return getattr(element[key], operator)(value)

    def list(self, filters=None):
        if not filters:
            result = self._entries
        else:
            result = []
            result.extend(self._entries)

            for key, value in filters.items():
                result = [e for e in result if self._check(e, key, value)]

        return [model.User.from_dict(r) for r in result]
