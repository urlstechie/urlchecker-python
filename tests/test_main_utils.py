import os
import pytest
from urlchecker.main.utils import get_tmpdir


def test_get_tmpdir(tmp_path):
    """
    test getting a temporary directory (and creating or not)
    """
    print(tmp_path)

    # Directory should not be created
    not_created = get_tmpdir(create=False)
    if os.path.exists(not_created):
        raise AssertionError

    # Directory should be created at tmp_path
    base_dir = str(tmp_path)
    created = get_tmpdir(base_dir)
    if not os.path.exists(created):
        raise AssertionError

    # Name should have prefix
    named = get_tmpdir(prefix="tacos", create=False)
    if not (os.path.basename(named).startswith("tacos")):
        raise AssertionError
