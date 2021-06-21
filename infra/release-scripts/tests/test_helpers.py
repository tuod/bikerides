from pathlib import Path

from src import helpers


def test_remove_path_prefix():
    absolute1 = Path("/home/test1")
    prefix1 = Path("/home")
    result = helpers.remove_path_prefix(full_path=absolute1, prefix=prefix1)
    assert str(result) == "./test1"
